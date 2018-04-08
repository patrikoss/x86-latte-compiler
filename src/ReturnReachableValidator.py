from antlr4 import *
if __name__ is not None and "." in __name__:
    from .autogen.LatteParser import LatteParser
else:
    from autogen.LatteParser import LatteParser

from Common import *
from TypeCheckerErrors import DivisionByZero, ReturnPossiblyUnreachable


class Undefined():
    def __init__(self):
        pass

class ReturnReachableValidator(ParseTreeVisitor):
    """
    Validates if the return statement is always reached within any functions
    (except for void)
    """
    def __init__(self):
        pass


    # Visit a parse tree produced by LatteParser#program.
    def visitProgram(self, ctx:LatteParser.ProgramContext):
        return self.visitChildren(ctx)


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
        fType = ctx.type_().getText()
        if fType != TVOID:
            self._reachable = False
            self.visitChildren(ctx)
            if not self._reachable:
                raise ReturnPossiblyUnreachable(ctx)
            del self._reachable


    # Visit a parse tree produced by LatteParser#arg.
    def visitArg(self, ctx:LatteParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#block.
    def visitBlock(self, ctx:LatteParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Empty.
    def visitEmpty(self, ctx:LatteParser.EmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#BlockStmt.
    def visitBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Decl.
    def visitDecl(self, ctx:LatteParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Ass.
    def visitAss(self, ctx:LatteParser.AssContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Incr.
    def visitIncr(self, ctx:LatteParser.IncrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Decr.
    def visitDecr(self, ctx:LatteParser.DecrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Ret.
    def visitRet(self, ctx:LatteParser.RetContext):
        self._reachable = True


    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx:LatteParser.VRetContext):
        self._reachable = True


    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx:LatteParser.CondContext):
        cond = self.visit(ctx.expr())
        if cond == True:
            self.visit(ctx.stmt())


    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx:LatteParser.CondElseContext):
        if self._reachable:
            return
        cond = self.visit(ctx.expr())
        if type(cond)==Undefined:
            # if undefined, return must be reachable in both branches
            self.visit(ctx.stmt(0))
            if not self._reachable:
                return
            self._reachable = False
            self.visit(ctx.stmt(1))
            if not self._reachable:
                return
        elif cond == True:
            self.visit(ctx.stmt(0))
        elif cond == False:
            self.visit(ctx.stmt(1))


    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx:LatteParser.WhileContext):
        cond = self.visit(ctx.expr())
        if cond == True:
            self.visit(ctx.stmt())


    # Visit a parse tree produced by LatteParser#SExp.
    def visitSExp(self, ctx:LatteParser.SExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Int.
    def visitInt(self, ctx:LatteParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Str.
    def visitStr(self, ctx:LatteParser.StrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Bool.
    def visitBool(self, ctx:LatteParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Void.
    def visitVoid(self, ctx:LatteParser.VoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Class.
    def visitClass(self, ctx:LatteParser.ClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ItemDecl.
    def visitItemDecl(self, ctx:LatteParser.ItemDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ItemDef.
    def visitItemDef(self, ctx:LatteParser.ItemDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EId.
    def visitEId(self, ctx:LatteParser.EIdContext):
        return Undefined()


    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx:LatteParser.EFunCallContext):
        return Undefined()


    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx:LatteParser.ERelOpContext):
        val1 = self.visit(ctx.expr(0))
        val2 = self.visit(ctx.expr(1))
        op = self.visit(ctx.relOp())
        if Undefined in {type(val1), type(val2)}:
            return Undefined()
        if op == '<':
            return val1 < val2
        elif op == '<=':
            return val1 <= val2
        elif op == '>':
            return val1 > val2
        elif op == '>=':
            return val1 >= val2
        elif op == '==':
            return val1 == val2
        elif op == '!=':
            return val1 != val2


    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx:LatteParser.ETrueContext):
        return True


    # Visit a parse tree produced by LatteParser#ECastNull.
    def visitECastNull(self, ctx:LatteParser.ECastNullContext):
        return None


    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx:LatteParser.EOrContext):
        val1 = self.visit(ctx.expr(0))
        val2 = self.visit(ctx.expr(1))
        if True in {val1, val2}:
            return True
        if val1 == val2 == False:
            return False
        return Undefined()


    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx:LatteParser.EIntContext):
        return int(ctx.INT().getText())


    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx:LatteParser.EUnOpContext):
        op = self.visit(ctx.unOp())
        val = self.visit(ctx.expr())
        if type(val) == Undefined:
            return Undefined()
        return -val if op == '-' else not val


    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx:LatteParser.EStrContext):
        return ctx.STR().getText()


    # Visit a parse tree produced by LatteParser#EFieldAcs.
    def visitEFieldAcs(self, ctx:LatteParser.EFieldAcsContext):
        return Undefined()


    # Visit a parse tree produced by LatteParser#ENewObj.
    def visitENewObj(self, ctx:LatteParser.ENewObjContext):
        return Undefined()


    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx:LatteParser.EMulOpContext):
        val1 = self.visit(ctx.expr(0))
        val2 = self.visit(ctx.expr(1))
        op = self.visit(ctx.mulOp())
        if val2 == 0:
            raise DivisionByZero(ctx)
        if Undefined in {type(val1), type(val2)}:
            return Undefined()
        if op == '*':
            return val1 * val2
        elif op == '/':
            return val1 / val2;
        elif op == '%':
            return val1 % val2


    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx:LatteParser.EAndContext):
        val1 = self.visit(ctx.expr(0))
        val2 = self.visit(ctx.expr(1))
        if False in {val1, val2}:
            return False
        if val1 == val2 == True:
            return True
        return Undefined()


    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx:LatteParser.EParenContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx:LatteParser.EFalseContext):
        return False


    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx:LatteParser.EAddOpContext):
        op = self.visit(ctx.addOp())
        val1 = self.visit(ctx.expr(0))
        val2 = self.visit(ctx.expr(1))
        if Undefined in {type(val1), type(val2)}:
            return Undefined()
        return val1 + val2 if op == '+' else val1 - val2


    # Visit a parse tree produced by LatteParser#NegInt.
    def visitNegInt(self, ctx:LatteParser.NegIntContext):
        return '-'


    # Visit a parse tree produced by LatteParser#NegBool.
    def visitNegBool(self, ctx:LatteParser.NegBoolContext):
        return '!'


    # Visit a parse tree produced by LatteParser#Add.
    def visitAdd(self, ctx:LatteParser.AddContext):
        return '+'


    # Visit a parse tree produced by LatteParser#Sub.
    def visitSub(self, ctx:LatteParser.SubContext):
        return '-'


    # Visit a parse tree produced by LatteParser#Mul.
    def visitMul(self, ctx:LatteParser.MulContext):
        return '*'


    # Visit a parse tree produced by LatteParser#Div.
    def visitDiv(self, ctx:LatteParser.DivContext):
        return '/'


    # Visit a parse tree produced by LatteParser#Mod.
    def visitMod(self, ctx:LatteParser.ModContext):
        return '%'


    # Visit a parse tree produced by LatteParser#Lt.
    def visitLt(self, ctx:LatteParser.LtContext):
        return '<'


    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx:LatteParser.LeContext):
        return '<='


    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx:LatteParser.GtContext):
        return '>'


    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx:LatteParser.GeContext):
        return '>='


    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx:LatteParser.EqContext):
        return '=='


    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx:LatteParser.NeqContext):
        return '!='
