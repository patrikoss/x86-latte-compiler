import sys
import os
from termcolor import cprint
import subprocess
import io

EXIT_FAIL_TESTER = -1

EXIT_FAIL = -1
EXIT_OK = 0
GEN_CODE_FILE_SUF = '.s'
INPUT_CODE_FILE_SUF = '.lat'
CORRECT_OUTPUT_SUF = '.output'
INPUT_TEST_SUF = '.input'
LATTE_OUTPUT_SUF = '.out'
TIMEOUT = 3

GOOD_MSG = b"OK\n"
BAD_MSG = b"ERROR\n"
DEF_ENCODING = 'UTF-8'
TMPFILE = 'latte.tmp'

def printGrey(string):
    cprint(string, 'grey', attrs=['bold'])

def printRed(string):
    cprint(string, 'red', attrs=['bold'])

def printGreen(string):
    cprint(string, 'green', attrs=['bold'])

def printWhite(string):
    cprint(string, 'white', attrs=['bold'])

def printMagenta(string):
    cprint(string, 'magenta', attrs=['bold'])

class GoodTestError(Exception):
    def __init__(self):
        pass

class Test():
    def __init__(self, latteExe, latteFilepath):
        self.latteExe = latteExe
        self.latteFilepath = latteFilepath
        self.folderpath = os.path.dirname(self.latteFilepath)
        self.latteBaseFileExt = os.path.basename(self.latteFilepath)
        self.latteBaseFile, _ = os.path.splitext(self.latteBaseFileExt)

    def run(self):
        self.testAcceptFile()
        self.testCompilatorStdErr()

    def testAcceptFile(self):
        proccess = subprocess.Popen(args=[self.latteExe, self.latteFilepath],
            stderr=subprocess.PIPE)
        _, self.compilatorStderr = proccess.communicate()
        self.returnCode = proccess.returncode

    def testCompilatorStdErr(self):
        # dump self.compilatorStderr to temporary file to verify that it has correct message
        with open(TMPFILE, 'wb') as fp:
            fp.write(self.compilatorStderr)
        with open(TMPFILE, 'rb') as fp:
            self.firstLineStderr = fp.readline()
            self.restStdErr = fp.read()
        if os.path.exists(TMPFILE) and os.path.isfile(TMPFILE):
            os.remove(TMPFILE)

    def printRestStdErr(self):
        printGrey("Rest of stderr:")
        printGrey(self.restStdErr)

    def printReport(self):
        printWhite("Summary {file}".format(file=self.latteBaseFile))
        self.printReturnCodeReport()
        self.printComilatorStderrReport()
        self.printRestStdErr()


class BadTest(Test):
    def __init__(self, latteExe, latteFilepath):
        super().__init__(latteExe, latteFilepath)

    def run(self):
        super().run()

    def printReturnCodeReport(self):
        printReturn = printGreen if self.returnCode != EXIT_OK else printRed
        printReturn("Return code: {ret}. Expected: !={retNotExp}".format(
            ret=self.returnCode, retNotExp=EXIT_OK))

    def printComilatorStderrReport(self):
        printStdErr = printGreen if self.firstLineStderr == BAD_MSG else printRed
        printStdErr("1st line of stderr: {line}, expected: {expLine}".format(
            line=self.firstLineStderr, expLine=BAD_MSG))

    def printReport(self):
        super().printReport()


class GoodTest(Test):
    def __init__(self, latteExe, latteFilepath):
        super().__init__(latteExe, latteFilepath)

    def testCreateCodeFile(self):
        self.codeFile = self.latteBaseFile+GEN_CODE_FILE_SUF
        self.createdCodeFile = self.codeFile in os.listdir(self.folderpath)

    def testCreateExeFile(self):
        self.exeFile = self.latteBaseFile
        self.createdExeFile = self.exeFile in os.listdir(self.folderpath)

    def testExeWorks(self):
        if not self.createdExeFile:
            printRed("Cannot verify output of the file {file}, since it has not been created.".format(file=self.latteBaseFile))
            raise GoodTestError()
        exeFilepath = os.path.join(self.folderpath, self.exeFile)

        # if there is some input use, then use it
        inputFilepath = os.path.join(self.folderpath, self.latteBaseFile + INPUT_TEST_SUF)
        inputStr = ''
        if os.path.exists(inputFilepath) and os.path.isfile(inputFilepath):
            with open(inputFilepath, 'rb') as fp:
                inputStr = fp.read()

        executeProcess = subprocess.Popen(args=[exeFilepath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        self.stdout, self.stderr = executeProcess.communicate(input=inputStr,
            timeout=TIMEOUT)
        if executeProcess.returncode != EXIT_OK:
            printGrey("Potentially dangerous return code from running {exe} exec file".format(exe=self.exeFile))
            printGrey("Stderr:")
            printGrey(self.stderr)

        outFile = os.path.join(self.folderpath, self.latteBaseFile+LATTE_OUTPUT_SUF)
        with open(outFile, 'wb') as fp:
            fp.write(self.stdout)


    def testDiff(self):
        solutionOut = self.latteBaseFile + CORRECT_OUTPUT_SUF
        testOut = self.latteBaseFile + LATTE_OUTPUT_SUF
        if solutionOut in os.listdir(self.folderpath) and \
            testOut in os.listdir(self.folderpath):

            solutionOutpath = os.path.join(self.folderpath, solutionOut)
            testOutpath = os.path.join(self.folderpath, testOut)
            diffProcess = subprocess.Popen(
                args=["diff", testOutpath, solutionOutpath],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            self.diffStdOut, self.diffStdErr = diffProcess.communicate()
            self.diffReturnCode = diffProcess.returncode


    def run(self):
        super().run()
        self.testCreateCodeFile()
        self.testCreateExeFile()
        self.testExeWorks()
        self.testDiff()

    def printReturnCodeReport(self):
        printReturn = printGreen if self.returnCode == EXIT_OK else printRed
        printReturn("Return code: {ret}. Expected: {retExp}".format(
            ret=self.returnCode, retExp=EXIT_OK))

    def printComilatorStderrReport(self):
        printStdErr = printGreen if self.firstLineStderr == GOOD_MSG else printRed
        printStdErr("1st line of stderr: {line}, expected: {expLine}".format(
            line=self.firstLineStderr, expLine=GOOD_MSG))

    def printCreationOfCodeFile(self):
        printCreationOfCodeFile = printGreen if self.createdCodeFile else printRed
        printCreationOfCodeFile("Creation of {gen_code_suf_file} file".format(
            gen_code_suf_file=self.latteBaseFile+GEN_CODE_FILE_SUF))

    def printCreationOfExeFile(self):
        printCreationOfExeFile = printGreen if self.createdExeFile else printRed
        printCreationOfExeFile("Creation of {exeFile} exe file".format(
            exeFile=self.exeFile))

    def printDiff(self):
        printWhite("Diff between {fileTest} and {fileGood}".format( \
            fileTest=self.latteBaseFile+LATTE_OUTPUT_SUF, \
            fileGood=self.latteBaseFile+CORRECT_OUTPUT_SUF))
        printDiff = printGreen if self.diffReturnCode == 0 else printRed
        printDiff(self.diffStdOut)

    def printReport(self):
        super().printReport()
        self.printCreationOfCodeFile()
        self.printCreationOfExeFile()
        self.printDiff()



def verifyTests(latcExe, testFolder, mode):
    """
    Runs the latcExe on .lat files from testFolder and verifies the output,
    stderr, and exit code.
    Assumptions:
    - latcExe is an executable file that generates GEN_CODE_FILE_SUF('.s')
    file and executable file
    - testFolder contains .lat input files, and .output files
    :param latcExe: absolute path to latcExe file
    :type latcExe: str
    :param testFolder: absolute path to folder containing tests (good or bad)
    :type testFolder: str
    :param mode: 'good' or 'bad'
    :type mode: str
    :return: None
    """
    files = os.listdir(testFolder)
    latteFiles = [os.path.join(testFolder, f) for f in files if os.path.splitext(f)[1] == '.lat']
    TestKind = GoodTest if mode == 'good' else BadTest
    latteTests = [TestKind(latcExe, f) for f in latteFiles]
    for test in latteTests:
        try:
            test.run()
            test.printReport()
        except GoodTestError as e:
            printRed(e)
        except subprocess.TimeoutExpired as e:
            printRed(e)
        print()


def verifyMode(mode):
    if mode not in {'good', 'bad'}:
        printRed("Invalid mode: {passedMode}. Mode can be one of: 'good' or 'bad'".format(passedMode=mode))
        exit(EXIT_FAIL_TESTER)

def verifyFolder(folderpath):
    if not os.path.isdir(folderpath):
        printRed("Invalid folderpath: {folderpath}".format(folderpath=folderpath))
        exit(EXIT_FAIL_TESTER)

def verifyLatcx86(latcExe):
    if not os.path.exists(latcExe):
        printRed("File '{file}' doesn't exist".format(file=latcExe))
        exit(EXIT_FAIL_TESTER)
    if not os.path.isfile(latcExe):
        printRed("File '{file}' is not a file".format(file=latcExe))
        exit(EXIT_FAIL_TESTER)
    if not os.access(latcExe, os.X_OK):
        printRed("File '{file}' is not executable".format(file=latcExe))
        exit(EXIT_FAIL_TESTER)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        printMagenta("Usage:")
        printMagenta("python CompilerTester.py arg1 arg2 arg3")
        printMagenta("where:")
        printMagenta("arg1: path to latc_x86 file")
        printMagenta("arg2: 'good' or 'bad'")
        printMagenta("arg3: path to folder with good tests or bad tests")
        exit(-1)
    latcx86 = sys.argv[1]   ; verifyLatcx86(latcx86)
    mode = sys.argv[2]      ; verifyMode(mode)
    testFolder = sys.argv[3]; verifyFolder(testFolder)
    latcx86, testFolder = os.path.abspath(latcx86), os.path.abspath(testFolder)
    verifyTests(latcx86, testFolder, mode)
