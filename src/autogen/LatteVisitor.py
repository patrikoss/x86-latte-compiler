# Generated from /home/patryk/studia/magisterka/mrjp/zadanie2/x86LatteCompiler/Latte.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LatteParser import LatteParser
else:
    from LatteParser import LatteParser

# This class defines a complete generic visitor for a parse tree produced by LatteParser.

class LatteVisitor(ParseTreeVisitor):

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
        return self.visitChildren(ctx)


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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#VRet.
    def visitVRet(self, ctx:LatteParser.VRetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Cond.
    def visitCond(self, ctx:LatteParser.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#CondElse.
    def visitCondElse(self, ctx:LatteParser.CondElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#While.
    def visitWhile(self, ctx:LatteParser.WhileContext):
        return self.visitChildren(ctx)


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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EFunCall.
    def visitEFunCall(self, ctx:LatteParser.EFunCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ERelOp.
    def visitERelOp(self, ctx:LatteParser.ERelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ETrue.
    def visitETrue(self, ctx:LatteParser.ETrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ECastNull.
    def visitECastNull(self, ctx:LatteParser.ECastNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EOr.
    def visitEOr(self, ctx:LatteParser.EOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EInt.
    def visitEInt(self, ctx:LatteParser.EIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EUnOp.
    def visitEUnOp(self, ctx:LatteParser.EUnOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EStr.
    def visitEStr(self, ctx:LatteParser.EStrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EFieldAcs.
    def visitEFieldAcs(self, ctx:LatteParser.EFieldAcsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#ENewObj.
    def visitENewObj(self, ctx:LatteParser.ENewObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EMulOp.
    def visitEMulOp(self, ctx:LatteParser.EMulOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EAnd.
    def visitEAnd(self, ctx:LatteParser.EAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EParen.
    def visitEParen(self, ctx:LatteParser.EParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EFalse.
    def visitEFalse(self, ctx:LatteParser.EFalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#EAddOp.
    def visitEAddOp(self, ctx:LatteParser.EAddOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#NegInt.
    def visitNegInt(self, ctx:LatteParser.NegIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#NegBool.
    def visitNegBool(self, ctx:LatteParser.NegBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Add.
    def visitAdd(self, ctx:LatteParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Sub.
    def visitSub(self, ctx:LatteParser.SubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Mul.
    def visitMul(self, ctx:LatteParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Div.
    def visitDiv(self, ctx:LatteParser.DivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Mod.
    def visitMod(self, ctx:LatteParser.ModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Lt.
    def visitLt(self, ctx:LatteParser.LtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Le.
    def visitLe(self, ctx:LatteParser.LeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Gt.
    def visitGt(self, ctx:LatteParser.GtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Ge.
    def visitGe(self, ctx:LatteParser.GeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Eq.
    def visitEq(self, ctx:LatteParser.EqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LatteParser#Neq.
    def visitNeq(self, ctx:LatteParser.NeqContext):
        return self.visitChildren(ctx)



del LatteParser