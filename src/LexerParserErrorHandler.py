from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.Errors import InputMismatchException
from antlr4 import Parser, RecognitionException

import sys

class BailErrorStrategy(DefaultErrorStrategy):
    def recover(self, recognizer: Parser, e: RecognitionException):
        raise(InputMismatchException(recognizer))


    def recoverInline(self, recognizer:Parser):
        raise(InputMismatchException(recognizer))


    def sync(self, recognizer:Parser):
        pass
