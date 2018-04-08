import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from autogen.LatteLexer import LatteLexer

from autogen.LatteParser import LatteParser
from LexerParserErrorHandler import BailErrorStrategy
from LexerParserErrorListener import LexerParserErrorListener

from TypeChecker import TypeCheckVisitor
from CodeGenerator import CodeGenerator
from FunctionNodesDecorator import FunctionNodeDecorator
from ReturnReachableValidator import ReturnReachableValidator
from TypeCheckerErrors import *

from Common import EXIT_OK, EXIT_FAIL

import os
import subprocess


def generateExerciseFiles(code, runtimeFilepath, filepath):
    def getFolderpath(filepath):
        """
        Returns the absolute path to folder in which given file denoted
        by its path exists
        :rtype: string
        """
        return os.path.dirname(os.path.abspath(filepath))

    def dumpAssembly(code, targetFilename, targetFolderpath):
        """
        Dumps assembly code into file
        :type code: string
        :type targetFilename: string
        :type targetFolderpath: string
        :return: path to the created assembly file
        :rtype: str
        """
        targetFilepath = os.path.join(targetFolderpath, targetFilename)
        with open(targetFilepath, 'w') as fp:
            fp.write(code)
        return targetFilepath

    def dumpExecutable(codeFilepath, runtimeLibpath, targetFilename, targetFolderpath):
        """
        Dumps executable created by compiling code from codeFilepath file(.s)
        and code from runtimeLibpath file(.s) into file targetFilename inside
        folder targetFoldername
        :type codeFilepath: string
        :type runtimeLibpath: string
        :type targetFilename: string
        :type targetFolderpath: string
        :return: path to the created executable file
        :rtype: str
        """
        targetFilepath = os.path.join(targetFolderpath, targetFilename)
        cmd = ['gcc', '-m32', '-o', targetFilepath, runtimeLibpath, codeFilepath]
        completedProcess = subprocess.run(args=cmd, stderr=subprocess.DEVNULL)
        if completedProcess.returncode != EXIT_OK:
            print("During executable generation an error occurred.", end='', file=sys.stderr)
            exit(EXIT_FAIL)
        return targetFilepath


    targetFolderpath = getFolderpath(filepath=filepath)
    basenameExt = os.path.basename(filepath)
    basename, extension = os.path.splitext(basenameExt)
    basenameExec, basenameAssembly = basename, basename+'.s'
    assFilepath = dumpAssembly(code, basenameAssembly, targetFolderpath)
    dumpExecutable(assFilepath, runtimeFilepath, basenameExec, targetFolderpath)

def main(filepath, RUNTIME_LIB_FILE):
    with open(filepath, 'r') as fp:
        input = FileStream(filepath)
    #input = InputStream(sys.stdin.read())
    lexer = LatteLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LatteParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(LexerParserErrorListener())

    parser._errHandler = BailErrorStrategy()
    tree = parser.program()

    try:
        TypeCheckVisitor().visit(tree)
        ReturnReachableValidator().visit(tree)

        # if we got here, we accept the program
        print("OK", file=sys.stderr)
        FunctionNodeDecorator().visit(tree)
        gen = CodeGenerator()
        gen.visit(tree)

        # dump the files as specified in the exercise
        generateExerciseFiles(gen.generateCode(), RUNTIME_LIB_FILE, filepath)

        exit(EXIT_OK)
    except TypeCheckerError as e:
        print("ERROR", file=sys.stderr)
        print(e, file=sys.stderr)
        exit(EXIT_FAIL)
    except Exception as e:
        print("ERROR", file=sys.stderr)
        print(e, file=sys.stderr)
        exit(EXIT_FAIL)


def existFile(filepath):
    """
    Verifies that the file exist and indeed it is a file.
    :rtype: boolean
    """
    filenameExt = os.path.basename(filepath)
    filename, extension = os.path.splitext(filenameExt)

    return len(filename) > 0 and os.path.isfile(filepath)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Pass the path to the Latte program file and runtime library.\n")
        exit(EXIT_FAIL)

    filepath = sys.argv[1]
    filepath = os.path.abspath(filepath)
    RUNTIME_LIB_FILE=sys.argv[2]
    RUNTIME_LIB_FILE=os.path.abspath(RUNTIME_LIB_FILE)
    if not existFile(filepath):
        print("Invalid filepath. Please provide a path to a valid file.")
        exit(EXIT_FAIL)
    main(filepath, RUNTIME_LIB_FILE)
