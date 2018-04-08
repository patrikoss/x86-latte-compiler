class TypeCheckerError(Exception):
    # Every type checker error should have at least 2 attributes:
    # self.line
    # self.col

    def __init__(self, ctx):
        self.ctx, self.line, self.col = ctx, ctx.start.line, ctx.start.column

    def __str__(self):
        errMsg = "Type checker error:\n"
        errMsg += "Encountered error: {} at line: {}, col: {}: {}\n".format( \
            type(self).__name__,self.line, self.col, self.ctx.getText())
        return errMsg

class FunctionRedeclaration(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.funName = ctx.ID().getText()

class UndeclaredClass(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class ClassRedeclaration(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class CyclicInheritance(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class VariableRedeclaration(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class UndeclaredType(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class TypeMismatch(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class UnsupportedOperand(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class UndeclaredVariable(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class UndeclaredFunction(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidArguments(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidAttributeAccess(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidLhs(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidVariableDeclaration(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class NoMainFunction(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidMainFunction(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class InvalidReturn(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class ReturnPossiblyUnreachable(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)

class DivisionByZero(TypeCheckerError):
    def __init__(self, ctx):
        super().__init__(ctx)
