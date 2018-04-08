from antlr4.error.ErrorListener import ErrorListener
import sys
from Common import EXIT_FAIL

class LexerParserErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("ERROR",file=sys.stderr)
        print("Parse error.\nEncountered error while parsing.", file=sys.stderr)
        print("Line: {line}, column {col}\n{msg}".format(line=line,col=column,msg=msg),
            file=sys.stderr)
        exit(EXIT_FAIL)
