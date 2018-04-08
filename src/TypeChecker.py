# Generated from ./Latte.g4 by ANTLR 4.7

if __name__ is not None and "." in __name__:
    from .autogen.LatteParser import LatteParser
else:
    from autogen.LatteParser import LatteParser

from TypeCheckerErrors import *
from Common import *
from copy import deepcopy
from antlr4 import *


def takeParserRules(node):
    """
    Logical predicate saying to only consider nodes that inherits from
    ParserRuleContext
    :param node: node in Antlr4 AST
    :type node: Node in antlr4 tree

    :return: True if node is of type ParserRuleContext
    :rtype: bool

    """
    return isinstance(node, ParserRuleContext)

# This class defines a complete generic visitor for a parse tree produced by LatteParser.
class TypeCheckVisitor(ParseTreeVisitor):
    """
    Validates the types of the parse tree are correct.
    Throws error if it encounter type error.
    Also, it decorates the expressions nodes with the type of the value returned,
    under the attribute '_exprType'
    """

    def __init__(self):
        # declare global and local envirtonment
        self.globals = dict()
        self.locals = dict()

        # declare classess structures
        self.classes = dict()
        self.clsattrs = dict()
        self.clsfuns = dict()

        # declare basic types
        self.initTypes =  initTypes
        self.basicVarTypes = initTypes[:3]

        # initialize basic values for classess
        self.defaultSuperClass = '#object'
        self.classes[self.defaultSuperClass] = None
        self.clsattrs[self.defaultSuperClass] = dict()
        self.clsfuns[self.defaultSuperClass] = dict()
        self.clsfuns[self.defaultSuperClass]['printInt'] = (TVOID, [TINT])
        self.clsfuns[self.defaultSuperClass]['printString'] = (TVOID, [TSTRING])
        self.clsfuns[self.defaultSuperClass]['error'] = (TVOID, [])
        self.clsfuns[self.defaultSuperClass]['readInt'] = (TINT, [])
        self.clsfuns[self.defaultSuperClass]['readString'] = (TSTRING, [])
        self.currentClass = self.defaultSuperClass


    # Visit a parse tree produced by LatteParser#program.
    def visitProgram(self, ctx:LatteParser.ProgramContext):
        # record the topdef function declarations
        topdefs = ctx.getChildren(predicate=lambda x: isinstance(x, LatteParser.TopFunDefContext))
        topdefs = [topdef for topdef in topdefs]

        # collect method declaration for the defaultSuperClass(#object)
        fundefs = [topdef.fundef() for topdef in topdefs]
        self._collectClsFuns(ctx, fundefs)

        # validate classess definition
        clsdefs = ctx.getChildren(predicate = lambda context: \
            isinstance(context, LatteParser.ClsExtDefContext) or \
            isinstance(context, LatteParser.ClsDefContext))
        for clsdef in clsdefs:
            self.visit(clsdef)

        # validate topdef function definitions
        for topdef in topdefs:
            self.visit(topdef)

            # validate main has no parameters and return type
            if topdef.fundef().ID().getText() == MAIN:
                retType, paramTypes = self.clsfuns[self.defaultSuperClass][MAIN]
                if retType != TINT or paramTypes != []:
                    raise InvalidMainFunction(topdef)

        # validate that main exists
        if MAIN not in self.clsfuns[self.defaultSuperClass]:
            raise NoMainFunction(ctx)


    # Visit a parse tree produced by LatteParser#TopFunDef.
    def visitTopFunDef(self, ctx:LatteParser.TopFunDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ClsDef.
    def visitClsDef(self, ctx:LatteParser.ClsDefContext):
        baseCls = ctx.ID().getText()
        sprCls = self.defaultSuperClass
        return self._visitClsDef(ctx, baseCls, sprCls)


    # Visit a parse tree produced by LatteParser#ClsExtDef.
    def visitClsExtDef(self, ctx:LatteParser.ClsExtDefContext):
        baseCls = ctx.ID(0).getText()
        sprCls = ctx.ID(1).getText()
        if sprCls not in self.classes:
            raise UndeclaredClass(ctx.ID(1))
        return self._visitClsDef(ctx, baseCls, sprCls)


    # Visit a parse tree produced by LatteParser#clsattr.
    def visitClsattr(self, ctx:LatteParser.ClsattrContext):
        type_ = ctx.type_().getText()
        attrIds = [attr.getText() for attr in ctx.ID()]
        if type_ not in self.classes and type_ not in initTypes:
            raise UndeclaredType(ctx)
        if type_ == TVOID:
            raise InvalidVariableDeclaration(ctx)
        for attrId in attrIds:
            if attrId in self.clsattrs[self.currentClass]:
                raise VariableRedeclaration(ctx)
            self.clsattrs[self.currentClass][attrId] = type_


    # Visit a parse tree produced by LatteParser#clsfun.
    def visitClsfun(self, ctx:LatteParser.ClsfunContext):
        self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#fundef.
    def visitFundef(self, ctx:LatteParser.FundefContext):
        # extract function's name, type, arguments
        fType = ctx.type_().getText()
        fName = ctx.ID().getText()
        fArgsTypes = ctx.arg().getChildren(predicate=takeParserRules) \
            if ctx.arg() is not None else []
        fArgsTypes = [t.getText() for t in fArgsTypes]
        fArgsIds = ctx.arg().ID() if ctx.arg() is not None else []
        fArgsIds = [fArg.getText() for fArg in fArgsIds]

        # validate function header
        if fType not in self.classes and fType not in initTypes:
            raise UndeclaredType(ctx.type_())
        for i, argType in enumerate(fArgsTypes):
            if argType not in self.classes and argType not in initTypes:
                raise UndeclaredType(ctx)
            if argType == TVOID:
                raise InvalidVariableDeclaration(ctx)
        for i, argId in enumerate(fArgsIds):
            if argId in self.locals:
                raise VariableRedeclaration(ctx)
            self.locals[argId] = fArgsTypes[i]

        # remember function return type
        self._expectedRetType = fType
        # validate function body
        self.visit(ctx.block())
        # cleanup after validation
        self.locals = dict()
        del self._expectedRetType


    # Visit a parse tree produced by LatteParser#arg.
    def visitArg(self, ctx:LatteParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#block.
    def visitBlock(self, ctx:LatteParser.BlockContext):
        snapshotGlobals, snapshotLocals = deepcopy(self.globals), deepcopy(self.locals)
        self.globals.update(self.locals); self.locals = dict()
        self.visitChildren(ctx)
        self.globals, self.locals = snapshotGlobals, snapshotLocals


    # Visit a parse tree produced by LatteParser#Empty.
    def visitEmpty(self, ctx:LatteParser.EmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#BlockStmt.
    def visitBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Decl.
    def visitDecl(self, ctx:LatteParser.DeclContext):
        # verify that type is valid
        type_ = ctx.type_().getText()
        if type_ not in self.initTypes and type_ not in self.classes:
            raise UndeclaredType(ctx)
        if type_ == TVOID:
            raise InvalidVariableDeclaration(ctx)

        # remember the type for the sequence of variable declaration
        self._itemDeclType = type_
        # validate the sequence of variable declaration
        self.visitChildren(ctx)
        # cleanup after verfication
        del self._itemDeclType


    # Visit a parse tree produced by LatteParser#Ass.
    def visitAss(self, ctx:LatteParser.AssContext):
        # verify that rhs is a subclass of lhs
        rhsType = self.visit(ctx.expr(1))
        lhsType = self.visit(ctx.expr(0))
        if not self._isSubclass(rhsType, lhsType):
            raise TypeMismatch(ctx)
        # verify that left-hand side of the assignment operator is valid
        if not (isinstance(ctx.expr(0), LatteParser.EIdContext) or \
            isinstance(ctx.expr(0), LatteParser.EFieldAcsContext)):

            raise InvalidLhs(ctx)

    # Visit a parse tree produced by LatteParser#Incr.
    def visitIncr(self, ctx:LatteParser.IncrContext):
        exprType = self.visit(ctx.expr())
        if exprType != TINT:
            raise UnsupportedOperand(ctx)

    # Visit a parse tree produced by LatteParser#Decr.
    def visitDecr(self, ctx:LatteParser.DecrContext):
        exprType = self.visit(ctx.expr())
        if exprType != TINT:
            raise UnsupportedOperand(ctx)


    # Visit a parse tree produced by LatteParser#Ret.
    def visitRet(self, ctx:LatteParser.RetContext):
        retType = self.visit(ctx.expr())
        # return g(), where g() returns void, we raise exception
        if retType == TVOID or not self._isSubclass(retType, self._expectedRetType):
            raise InvalidReturn(ctx)


    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx:LatteParser.VRetContext):
        if self._expectedRetType != TVOID:
            raise InvalidReturn(ctx)


    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx:LatteParser.CondContext):
        exprType = self.visit(ctx.expr())
        if exprType != TBOOLEAN:
            raise TypeMismatch(ctx.expr())
        self.visit(ctx.stmt())


    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx:LatteParser.CondElseContext):
        exprType = self.visit(ctx.expr())
        if exprType != TBOOLEAN:
            raise TypeMismatch(ctx.expr())
        self.visit(ctx.stmt(0))
        self.visit(ctx.stmt(1))


    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx:LatteParser.WhileContext):
        exprType = self.visit(ctx.expr())
        if exprType != TBOOLEAN:
            raise TypeMismatch(ctx.expr())
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
        ident = ctx.ID().getText()
        if ident in self.locals:
            raise VariableRedeclaration(ctx)
        self.locals[ident] = self._itemDeclType

    # Visit a parse tree produced by LatteParser#ItemDef.
    def visitItemDef(self, ctx:LatteParser.ItemDefContext):
        ident = ctx.ID().getText()
        if ident in self.locals:
            raise VariableRedeclaration(ctx)
        exprType = self.visit(ctx.expr())
        if not self._isSubclass(exprType, self._itemDeclType):
            raise TypeMismatch(ctx)
        self.locals[ident] = self._itemDeclType

    # Visit a parse tree produced by LatteParser#EId.
    def visitEId(self, ctx:LatteParser.EIdContext):
        ident = ctx.ID().getText()
        varType = self._findVarType(ctx, ident)
        ctx._exprType = varType
        return varType

    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx:LatteParser.EFunCallContext):
        # classess cannot access functions outside their scope
        fName = ctx.ID().getText()
        fArgTypes = [self.visit(exp) for exp in ctx.expr()]

        # validate that the function call arguments types and return type matches
        # the types of function declaration
        fret, fparamTypes = self._findFunType(ctx, fName)
        self._validateFunctionArguments(ctx, fArgTypes, fparamTypes)
        ctx._exprType = fret
        return fret


    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx:LatteParser.ERelOpContext):
        [type1, op, type2] = self._calculateOperands(ctx)
        if type1 == TINT or type(op) in {LatteParser.EqContext, LatteParser.NeqContext}:
            ctx._exprType = TBOOLEAN
            return TBOOLEAN
        raise UnsupportedOperand(op)


    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx:LatteParser.ETrueContext):
        ctx._exprType = TBOOLEAN
        return TBOOLEAN


    # Visit a parse tree produced by LatteParser#ECastNull.
    def visitECastNull(self, ctx:LatteParser.ECastNullContext):
        cls = ctx.type_().getText()
        if cls not in self.classes:
            raise UndeclaredType(ctx)
        ctx._exprType = cls
        return cls


    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx:LatteParser.EOrContext):
        [type1, op, type2] = self._calculateOperands(ctx)
        if type1 != TBOOLEAN:
            raise UnsupportedOperand(op)
        ctx._exprType = TBOOLEAN
        return TBOOLEAN


    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx:LatteParser.EIntContext):
        ctx._exprType = TINT
        return TINT


    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx:LatteParser.EUnOpContext):
        unop, type_ = (self.visit(c) for c in ctx.getChildren())
        if type_ == TINT and type(unop) == LatteParser.NegIntContext:
            ctx._exprType = TINT
            return TINT
        elif type_ == TBOOLEAN and type(unop) == LatteParser.NegBoolContext:
            ctx._exprType = TBOOLEAN
            return TBOOLEAN
        raise UnsupportedOperand(unop)


    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx:LatteParser.EStrContext):
        ctx._exprType = TSTRING
        return TSTRING


    # Visit a parse tree produced by LatteParser#EFieldAcs.
    def visitEFieldAcs(self, ctx:LatteParser.EFieldAcsContext):

        objType = self.visit(ctx.expr(0))
        expr = ctx.expr(1)
        # store the current class to restore it later
        snahpshotClass = self.currentClass

        # check the class of the object on the left side of the .(access) operator
        # if it is one of the primary types - raise exception
        if objType in self.initTypes:
            raise InvalidAttributeAccess(ctx)

        if isinstance(expr, LatteParser.EIdContext):
            # field access of a kind: object.some_variable
            fieldId = expr.ID().getText()
            self.currentClass = objType
            fieldType = self._findAttrType(ctx, fieldId)
        elif isinstance(expr, LatteParser.EFunCallContext):
            # field access of a kind: object.some_function()
            funName = expr.ID().getText()
            funArgs = [self.visit(arg) for arg in expr.expr()]
            self.currentClass = objType
            fieldType, funParamTypes = self._findFunType(expr, funName)
            self._validateFunctionArguments(expr, funArgs, funParamTypes)
        elif isinstance(expr, LatteParser.EFieldAcsContext):
            # field access of a kind: object.some_other_object.(...)
            self.currentClass = objType
            fieldType = self.visit(expr)
        else:
            raise InvalidAttributeAccess(ctx)

        # restore the previous class
        self.currentClass = snahpshotClass
        ctx._exprType = fieldType
        return fieldType


    # Visit a parse tree produced by LatteParser#ENewObj.
    def visitENewObj(self, ctx:LatteParser.ENewObjContext):
        cls = ctx.ID().getText()
        if cls not in self.classes:
            raise UndeclaredType(ctx)
        ctx._exprType = cls
        return cls


    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx:LatteParser.EMulOpContext):
        [type1, op, type2] = self._calculateOperands(ctx)
        if type1 != TINT:
            raise UnsupportedOperand(ctx)
        ctx._exprType = TINT
        return TINT


    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx:LatteParser.EAndContext):
        [type1, op, type2] = self._calculateOperands(ctx)
        if type1 != TBOOLEAN:
            raise UnsupportedOperand(ctx)
        ctx._exprType = TBOOLEAN
        return TBOOLEAN


    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx:LatteParser.EParenContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx:LatteParser.EFalseContext):
        ctx._exprType = TBOOLEAN
        return TBOOLEAN


    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx:LatteParser.EAddOpContext):
        [type1, op, type2] = self._calculateOperands(ctx)
        if type1 == TINT:
            ctx._exprType = TINT
            return TINT
        elif type1 == TSTRING and type(op) == LatteParser.AddContext:
            ctx._exprType = TSTRING
            return TSTRING
        raise UnsupportedOperand(ctx)


    # Visit a parse tree produced by LatteParser#NegInt.
    def visitNegInt(self, ctx:LatteParser.NegIntContext):
        return ctx


    # Visit a parse tree produced by LatteParser#NegBool.
    def visitNegBool(self, ctx:LatteParser.NegBoolContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Add.
    def visitAdd(self, ctx:LatteParser.AddContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Sub.
    def visitSub(self, ctx:LatteParser.SubContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Mul.
    def visitMul(self, ctx:LatteParser.MulContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Div.
    def visitDiv(self, ctx:LatteParser.DivContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Mod.
    def visitMod(self, ctx:LatteParser.ModContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Lt.
    def visitLt(self, ctx:LatteParser.LtContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx:LatteParser.LeContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx:LatteParser.GtContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx:LatteParser.GeContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx:LatteParser.EqContext):
        return ctx


    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx:LatteParser.NeqContext):
        return ctx


    # Helper functions
    def _visitClsDef(self, ctx, baseCls, sprCls):
        """
        Verfies the header of the class, and visits the class'
        attributes and method definition
        :return: None
        :rtype: None
        """
        if baseCls in self.classes:
            raise ClassRedeclaration(ctx)
        self.classes[baseCls] = sprCls

        self.clsfuns[baseCls] = dict()
        self.clsattrs[baseCls] = dict()
        self.clsattrs[baseCls][SELF] = baseCls

        self.currentClass = baseCls
        methods = [meth.fundef() for meth in ctx.clsfun()]
        self._collectClsFuns(ctx, methods)
        self.visitChildren(ctx)
        self.currentClass = self.defaultSuperClass


    def _collectClsFuns(self, ctx, methods):
        """
        Register all the methods declarations of the current class,
        and check if there is no redeclaration of some method within the current class
        :param ctx: context

        :param methods: List of methods from self.currentClass
        :type methods: [FundefContext()]

        :return: None
        :rtype: None
        """
        for method in methods:
            # collect method's name, return type and parameters' types
            mType = method.type_().getText()
            mName = method.ID().getText()
            mArgsTypes = method.arg().getChildren(predicate=takeParserRules) \
                if method.arg() is not None else []
            mArgsTypes = [c.getText() for c in mArgsTypes]

            # check if the function has been already declared
            if mName in self.clsfuns[self.currentClass]:
                raise FunctionRedeclaration(method)
            self.clsfuns[self.currentClass][mName] = (mType, mArgsTypes)


    def _isSubclass(self, type1, type2):
        """
        :return: true if type1 is subclass of type2, false otherwise
        :rtype: bool
        """
        if (type1 in self.initTypes or type2 in self.initTypes):
            return type1 == type2
        cls = type1
        while cls != self.classes[self.defaultSuperClass]:
            if cls == type2:
                return True
            cls = self.classes[cls]
        return False


    def _calculateOperands(self, ctx):
        """
        Performs basic checks that every binary operation has to satisfy:
        - types of the argument have to match
        - arguments have to be of the initial types(with exception to operation ==, !=)
        :return: a list of 3 elements:
        - type of the first operand (str)
        - context of the operator (?Context)
        - type of the second operand (str)
        :rtype: [str, Context, str]
        """
        [type1, op, type2] = [self.visit(c) for c in ctx.getChildren()]
        if not self._isSubclass(type1, type2) and not self._isSubclass(type2, type1):
            raise TypeMismatch(ctx)
        if (type1 not in self.initTypes) and (type(op) not in {LatteParser.EqContext, LatteParser.NeqContext}):
            raise UnsupportedOperand(ctx)
        if type1 == TVOID:
            return UnsupportedOperand(ctx)
        return [type1, op, type2]


    def _findAttrType(self, ctx, attrId):
        """
        :return: type of the attribute attrId, from currentClass
        :rtype: str
        """
        cls = self.currentClass
        while cls != self.classes[self.defaultSuperClass]:
            if attrId in self.clsattrs[cls]:
                return self.clsattrs[cls][attrId]
            cls = self.classes[cls]
        raise UndeclaredVariable(ctx)


    def _findFunType(self, ctx, funName):
        """
        :return: signature of the function funName, from currentClass,
                tuple of two elements: function return type, and parameter types
        :rtype: (str, [str])
        """
        cls = self.currentClass
        while cls != self.classes[self.defaultSuperClass]:
            if funName in self.clsfuns[cls]:
                return self.clsfuns[cls][funName]
            cls = self.classes[cls]
        raise UndeclaredFunction(ctx)


    def _findVarType(self, ctx, varId):
        """
        :return: type of the variable given by an identifier: varId
        :rtype: str
        """
        if varId in self.locals:
            return self.locals[varId]
        elif varId in self.globals:
            return self.globals[varId]
        else:
            return self._findAttrType(ctx, varId)


    def _validateFunctionArguments(self, ctx, fArgTypes, fparamTypes):
        """
        Validates if the arguments' types match the parameter types
        :return: None
        :rtype: None
        """
        if len(fparamTypes) != len(fArgTypes):
            raise InvalidArguments(ctx)
        for i, argType in enumerate(fArgTypes):
            if not self._isSubclass(argType, fparamTypes[i]):
                raise TypeMismatch(ctx.expr(i))
