from antlr4 import *
if __name__ is not None and "." in __name__:
    from .autogen.LatteParser import LatteParser
else:
    from autogen.LatteParser import LatteParser

import math
from copy import deepcopy
from AssemblyCode import *
from Common import *

DEBUG = False

# This class defines a complete generic visitor for a parse tree produced by LatteParser.

class CodeGenerator(ParseTreeVisitor):

    def __init__(self):
        # list of instructions
        self.instructions = []


    def generateCode(self):
        code = ''
        for instr in self.instructions:
            if isinstance(instr, Instruction):
                code += TAB
            code += str(instr) + '\n'
        return code


    def emitInstr(self, instr):
        self.instructions.append(instr)


    # Visit a parse tree produced by LatteParser#program.
    def visitProgram(self, ctx:LatteParser.ProgramContext):
        # initialize the global dictionary mapping strings to labels
        self.stringLabel = ctx._stringLabel
        # generate empty string as default value for string declaration
        self.emitInstr(StringLabel("", 0))
        self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#TopFunDef.
    def visitTopFunDef(self, ctx:LatteParser.TopFunDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ClsDef.
    def visitClsDef(self, ctx:LatteParser.ClsDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ClsExtDef.
    def visitClsExtDef(self, ctx:LatteParser.ClsExtDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#clsattr.
    def visitClsattr(self, ctx:LatteParser.ClsattrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#clsfun.
    def visitClsfun(self, ctx:LatteParser.ClsfunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#fundef.
    def visitFundef(self, ctx:LatteParser.FundefContext):
        # generate labels for strings that appear in the given function
        # for the first time
        for string in ctx._funStrings:
            self.emitInstr(StringLabel(string, self.stringLabel[string]))

        # function label
        funName = ctx.ID().getText()
        if funName == MAIN:
            self.emitInstr(Globl(funName))

        self.emitInstr(FunctionLabel(funName=funName))

        # function prolog
        self.emitInstr(Push(bp))
        self.emitInstr(Move(sp,bp))

        # calculate how much memory we have to reserve for local variables
        bytesAllocated = 0
        for varId in ctx.localVars:
            bytesAllocated += len(ctx.localVars[varId]) * stackElementSize

        # align SP position so that its address is divisible by standard
        # stack-pointer alignment(usually 16)
        bytesAllocated = math.ceil(bytesAllocated/alignSP) * alignSP
        if bytesAllocated != 0:
            self.emitInstr(SubSp(bytesAllocated))

        # dictionary mapping variable ids with their types and memory offset
        # wrt base pointer(bp)
        self.vars = dict()
        # offset wrt bp pointing to the first location below bp, that is
        # free - no local variables have been assigned this address
        self.newLocalVarOffset = -stackElementSize
        # new code label for return statement. Whenever the return statement
        # is spotted inside the function, jump to the returnLabel is performed
        self.returnLabel = CodeLabel()

        # save 2*addrSize bytes for control-link and return address
        bpParamOffset = 2 * stackElementSize
        # add the parameters as local variables visible inside the function
        for i, (varType, varId) in enumerate(ctx.params):
            self.vars[varId] = (varType, bpParamOffset)
            bpParamOffset += stackElementSize

        # generate code for the function body
        self.visit(ctx.block())

        # cleanup - no need for info about parameters(offset wrt bp and type)
        # after we leave the function
        del self.vars
        del self.newLocalVarOffset
        self.emitInstr(self.returnLabel)
        del self.returnLabel

        # function epilog
        if bytesAllocated != 0:
            self.emitInstr(AddSp(bytesAllocated))
        self.emitInstr(Pop(bp))
        self.emitInstr(Return())


    # Visit a parse tree produced by LatteParser#arg.
    def visitArg(self, ctx:LatteParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#block.
    def visitBlock(self, ctx:LatteParser.BlockContext):
        # take copy of all the local variables visible before the block
        snapshotVars = deepcopy(self.vars)

        # generate code for the statements within the block
        self.visitChildren(ctx)

        # restore the old variables from before the block, after generating
        # the code for the block
        self.vars = snapshotVars


    # Visit a parse tree produced by LatteParser#Empty.
    def visitEmpty(self, ctx:LatteParser.EmptyContext):
        return []


    # Visit a parse tree produced by LatteParser#BlockStmt.
    def visitBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Decl.
    def visitDecl(self, ctx:LatteParser.DeclContext):
        self.declType = ctx.type_().getText()
        self.visitChildren(ctx)
        del self.declType


    def _visitAss(self, ctx, operator):
        lhs = ctx.expr(0) if operator == '=' else ctx.expr()
        if isinstance(lhs, LatteParser.EIdContext):
            ident = lhs.ID().getText()
            _, offsetId = self.vars[ident]
            if operator == '=':
                # assignment, assume result is in ax
                self.emitInstr(Move(ax, Memory(bp, offsetId)))
            elif operator in {'++', '--'}:
                # increment(++) or decrement(--)
                Operation = Add if operator == '++' else Sub
                self.emitInstr(Move(Memory(bp, offsetId), ax))
                self.emitInstr(Operation(ax, ConstantInt(1)))
                self.emitInstr(Move(ax, Memory(bp,offsetId)))
        else:
            pass
            # TODO lhs = class attribute


    # Visit a parse tree produced by LatteParser#Ass.
    def visitAss(self, ctx:LatteParser.AssContext):
        # rhs result in ax
        self.visit(ctx.expr(1))
        self._visitAss(ctx, '=')


    # Visit a parse tree produced by LatteParser#Incr.
    def visitIncr(self, ctx:LatteParser.IncrContext):
        self._visitAss(ctx, '++')


    # Visit a parse tree produced by LatteParser#Decr.
    def visitDecr(self, ctx:LatteParser.DecrContext):
        return self._visitAss(ctx, '--')


    # Visit a parse tree produced by LatteParser#Ret.
    def visitRet(self, ctx:LatteParser.RetContext):
        self.visit(ctx.expr())
        self.emitInstr(Jump(self.returnLabel))


    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx:LatteParser.VRetContext):
        self.emitInstr(Jump(self.returnLabel))


    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx:LatteParser.CondContext):
        #evaulate the condition - result in ax
        self.visit(ctx.expr())
        jumpLabelRest = CodeLabel()
        # check if condition is false. If yes jump to rest of the code
        self.emitInstr(Cmpl(ax, ConstantInt(0)))
        self.emitInstr(Jump(jumpLabelRest, '=='))

        # if the condition was true, we generate instructions inside if
        self.visit(ctx.stmt())

        # rest of the code
        self.emitInstr(jumpLabelRest)


    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx:LatteParser.CondElseContext):
        # evaluate the conditon - result in ax
        self.visit(ctx.expr())

        # generate 2 new labels
        jumpLabelFalse = CodeLabel()
        jumpLabelRest = CodeLabel()

        # check if condition is false. If so, jump to labelFalse
        self.emitInstr(Cmpl(ax, ConstantInt(0)))
        self.emitInstr(Jump(jumpLabelFalse, '=='))

        # if the condition was true, execute code for instructions in if - stmt
        self.visit(ctx.stmt(0))
        # and then jump to rest of the code, skipping the else-statements
        self.emitInstr(Jump(jumpLabelRest))

        # statements for else
        self.emitInstr(jumpLabelFalse)
        self.visit(ctx.stmt(1))

        # rest of the code
        self.emitInstr(jumpLabelRest)


    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx:LatteParser.WhileContext):
        # we will generate the code for checking the condtion after
        # the code for the inside of loop.
        whileBody = CodeLabel()
        condition = CodeLabel()
        self.emitInstr(Jump(condition))
        self.emitInstr(whileBody)
        self.visit(ctx.stmt())
        self.emitInstr(condition)
        self.visit(ctx.expr())
        self.emitInstr(Cmpl(ax, ConstantInt(1)))
        self.emitInstr(Jump(whileBody, '=='))


    # Visit a parse tree produced by LatteParser#SExp.
    def visitSExp(self, ctx:LatteParser.SExpContext):
        # generate code for expression, result in ax but we do not care
        self.visit(ctx.expr())


    # Visit a parse tree produced by LatteParser#Int.
    def visitInt(self, ctx:LatteParser.IntContext):
        return TINT


    # Visit a parse tree produced by LatteParser#Str.
    def visitStr(self, ctx:LatteParser.StrContext):
        return TSTRING


    # Visit a parse tree produced by LatteParser#Bool.
    def visitBool(self, ctx:LatteParser.BoolContext):
        return TBOOLEAN


    # Visit a parse tree produced by LatteParser#Void.
    def visitVoid(self, ctx:LatteParser.VoidContext):
        return TVOID


    # Visit a parse tree produced by LatteParser#Class.
    def visitClass(self, ctx:LatteParser.ClassContext):
        return ctx.ID().getText()


    # Visit a parse tree produced by LatteParser#ItemDecl.
    def visitItemDecl(self, ctx:LatteParser.ItemDeclContext):
        ident = ctx.ID().getText()
        offset = self.newLocalVarOffset
        self.newLocalVarOffset -= stackElementSize
        self.vars[ident] = (self.declType, offset)
        if self.declType == TBOOLEAN:
            #defaultValue = False
            self.emitInstr(Move(ConstantInt(0), Memory(bp, offset)))
        elif self.declType == TINT:
            #defaultValue == 0
            self.emitInstr(Move(ConstantInt(0), Memory(bp, offset)))
        elif self.declType == TSTRING:
            #defaultValue = ""
            # get label for empty string
            emptyStrLabel = StringLabel("", self.stringLabel[""]).getAsText()
            self.emitInstr(Move(ConstantStrLabel(emptyStrLabel), Memory(bp, offset)))
        else:
            # TODO class
            pass


    # Visit a parse tree produced by LatteParser#ItemDef.
    def visitItemDef(self, ctx:LatteParser.ItemDefContext):
        # first calculate the right hand-side value
        self.visit(ctx.expr())

        # add, possibly overwriting an existing identifier
        ident = ctx.ID().getText()
        offset = self.newLocalVarOffset
        self.newLocalVarOffset -= stackElementSize
        self.vars[ident] = (self.declType, offset)

        if self.declType in  {TBOOLEAN, TINT, TSTRING}:
            # store the calculated rhs value into identifier's address
            self.emitInstr(Move(ax, Memory(bp, offset)))
        else:
            # TODO: item def for classes
            pass


    # Visit a parse tree produced by LatteParser#EId.
    def visitEId(self, ctx:LatteParser.EIdContext):
        ident = ctx.ID().getText()
        # look for ident within local variables
        if ident in self.vars:
            idType, idOffset = self.vars[ident]

            if idType in {TINT, TBOOLEAN, TSTRING}:
                mem = Memory(bp, idOffset)
                self.emitInstr(Move(mem, ax))
            else:
                # TODO evaluation of classess attributes
                pass


    def calculateSPalignment(self, argumentsBytes):
        """
        The function calculates the value needed to be subtracted from sp,
        so that when the arguments are pushed,
        the address of SP is divisible by alignSP(default = 16)
        """
        global spAddress
        currSp = spAddress[0]
        targetSp = currSp - argumentsBytes
        targetAlignedSp = math.floor(targetSp/alignSP) * alignSP
        return abs(targetAlignedSp - targetSp)


    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx:LatteParser.EFunCallContext):
        global spAddress
        if DEBUG:
            print("Fun call: ", ctx.ID().getText(), "spAddress:", spAddress[0])

        funName = ctx.ID().getText()
        funArgs = [c for c in ctx.expr()]
        # arguments on stack
        argumentsBytes = len(funArgs) * stackElementSize

        subBytesSP = self.calculateSPalignment(argumentsBytes)
        # decrease the stack pointer
        if subBytesSP != 0:
            self.emitInstr(SubSp(subBytesSP))

        # push the arguments on the stack in reverse order
        for arg in funArgs[::-1]:
            self.visit(arg)
            self.emitInstr(Push(ax))

        # when calling the function update spAddress(decrease 2*stackElementSize)
        # to store dynamic link and return address
        spAddress[0] -= 2*stackElementSize

        # call the function
        self.emitInstr(Call(funName))

        # restore spAddress
        spAddress[0] += 2*stackElementSize

        # pop the arguments from the stack, a.k.a increase the stack pointer
        if subBytesSP+argumentsBytes != 0:
            self.emitInstr(AddSp(subBytesSP+argumentsBytes))

        if DEBUG:
            print("Fun exit: ", ctx.ID().getText(), "spAddress:", spAddress[0])


    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx:LatteParser.ERelOpContext):
        operator = self.visit(ctx.relOp())
        self.visit(ctx.expr(0))
        self.emitInstr(Push(ax))
        self.visit(ctx.expr(1))
        self.emitInstr(Pop(cx))

        self.emitInstr(Cmpl(cx, ax))
        # move zero - the register
        self.emitInstr(Set(operator, reg=al))
        self.emitInstr(Cbw())
        self.emitInstr(Cwde())


    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx:LatteParser.ETrueContext):
        self.emitInstr(Move(ConstantInt(1), ax))


    # Visit a parse tree produced by LatteParser#ECastNull.
    def visitECastNull(self, ctx:LatteParser.ECastNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx:LatteParser.EOrContext):
        # generate 3 new labels
        jmpLabelTrue = CodeLabel()
        jmpLabelFalse = CodeLabel()
        jmpLabelRest = CodeLabel()

        # check if the left operand evaluates to true. If yes, then skip
        # evaluation of the right operand and save 1 to ax
        self.visit(ctx.expr(0))
        self.emitInstr(Cmpl(ax, ConstantInt(1)))
        self.emitInstr(Jump(jmpLabelTrue, '=='))

        # evaluate right operand and check if it evaluates to true. If
        # yes, move 1 to ax, else move 0
        self.visit(ctx.expr(1))
        self.emitInstr(Cmpl(ax, ConstantInt(0)))
        self.emitInstr(Jump(jmpLabelFalse, "=="))

        # OR evaluates to True
        self.emitInstr(jmpLabelTrue)
        self.emitInstr(Move(ConstantInt(1), ax))
        self.emitInstr(Jump(jmpLabelRest))

        # OR evalueates to false
        self.emitInstr(jmpLabelFalse)
        self.emitInstr(Move(ConstantInt(0),ax))

        # rest of the code
        self.emitInstr(jmpLabelRest)


    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx:LatteParser.EIntContext):
        val = int(ctx.INT().getText())
        self.emitInstr(Move(ConstantInt(val), dest=ax))


    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx:LatteParser.EUnOpContext):
        op = self.visit(ctx.unOp())
        self.visit(ctx.expr())
        if op == '-':
            self.emitInstr(NegateInt(ax, dest=ax))
        elif op == '!':
            self.emitInstr(NegateBool(ax, dest=ax))


    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx:LatteParser.EStrContext):
        string = ctx.STR().getText()
        strLabel = StringLabel(string, self.stringLabel[string]).getAsText()
        self.emitInstr(Move(ConstantStrLabel(strLabel), dest=ax))


    # Visit a parse tree produced by LatteParser#EFieldAcs.
    def visitEFieldAcs(self, ctx:LatteParser.EFieldAcsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ENewObj.
    def visitENewObj(self, ctx:LatteParser.ENewObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx:LatteParser.EMulOpContext):
        self.visit(ctx.expr(0))
        self.emitInstr(Push(ax))
        self.visit(ctx.expr(1))
        self.emitInstr(Move(ax, cx))
        self.emitInstr(Pop(ax))
        operation = ctx.mulOp().getText()
        if operation == '*':
            self.emitInstr(Mul(ax,cx))
        elif operation == '/':
            self.emitInstr(Div(ax,cx))
        elif operation == '%':
            self.emitInstr(Mod(ax,cx))
            self.emitInstr(Move(dx,ax))


    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx:LatteParser.EAndContext):
        # generate 3 new labels
        jmpLabelFalse = CodeLabel()
        jmpLabelTrue = CodeLabel()
        jmpLabelRest = CodeLabel()

        # check if the left operand evaluates to false. If yes, then skip
        # evaluation of the right operand, and move 0 to ax
        self.visit(ctx.expr(0))
        self.emitInstr(Cmpl(ax, ConstantInt(0)))
        self.emitInstr(Jump(jmpLabelFalse, '=='))

        # evaluate right operand and
        # check if the right operand evaluates to true. If yes then move 1
        # to ax, else move 0
        self.visit(ctx.expr(1))
        self.emitInstr(Cmpl(ax, ConstantInt(1)))
        self.emitInstr(Jump(jmpLabelTrue, '=='))

        # AND evaluates to false
        self.emitInstr(jmpLabelFalse)
        self.emitInstr(Move(ConstantInt(0), ax))
        self.emitInstr(Jump(jmpLabelRest))

        # AND evaluates to true
        self.emitInstr(jmpLabelTrue)
        self.emitInstr(Move(ConstantInt(1), ax))

        # rest of the code
        self.emitInstr(jmpLabelRest)


    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx:LatteParser.EParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx:LatteParser.EFalseContext):
        return self.emitInstr(Move(ConstantInt(0), ax))


    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx:LatteParser.EAddOpContext):

        self.visit(ctx.expr(0))
        self.emitInstr(Push(ax))
        self.visit(ctx.expr(1))
        self.emitInstr(Pop(cx))
        operation = self.visit(ctx.addOp())
        if ctx._exprType == TINT:
            if operation == '+':
                self.emitInstr(Add(cx, ax))
            elif operation == '-':
                self.emitInstr(Sub(cx, ax))
            self.emitInstr(Move(cx,ax))
        elif ctx._exprType == TSTRING and operation=='+':
            # debug
            global spAddress
            if DEBUG:
                print("Fun start: ", "concat", "spAddress:", spAddress[0])

            argumentsBytes = 2* stackElementSize
            subBytesSp = self.calculateSPalignment(argumentsBytes)
            if subBytesSp != 0:
                self.emitInstr(SubSp(subBytesSp))
            self.emitInstr(Push(ax))
            self.emitInstr(Push(cx))

            # update spAddress to store dynamic link and return address
            spAddress[0] -= 2*stackElementSize
            self.emitInstr(Call(concat))
            # restore spAddress
            spAddress[0] += 2*stackElementSize
            self.emitInstr(AddSp(subBytesSp+argumentsBytes))

            if DEBUG:
                print("Fun exit: ", "concat", "spAddress:", spAddress[0])


    # Visit a parse tree produced by LatteParser#NegInt.
    def visitNegInt(self, ctx:LatteParser.NegIntContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#NegBool.
    def visitNegBool(self, ctx:LatteParser.NegBoolContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Add.
    def visitAdd(self, ctx:LatteParser.AddContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Sub.
    def visitSub(self, ctx:LatteParser.SubContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Mul.
    def visitMul(self, ctx:LatteParser.MulContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Div.
    def visitDiv(self, ctx:LatteParser.DivContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Mod.
    def visitMod(self, ctx:LatteParser.ModContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Lt.
    def visitLt(self, ctx:LatteParser.LtContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx:LatteParser.LeContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx:LatteParser.GtContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx:LatteParser.GeContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx:LatteParser.EqContext):
        return ctx.getText()


    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx:LatteParser.NeqContext):
        return ctx.getText()
