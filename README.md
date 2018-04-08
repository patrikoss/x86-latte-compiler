# x86 latte compiler
This is an implementation of a compiler for 'Latte' programming language
The compiler's frontend and backend both have been written in Python.

Before running the program you have to make sure that you have valid
32-bit libraries necessary in the linking step of assembly code.
You can easily install those by typing:

```$ sudo apt-get install gcc-multilib```

In order to run the program, follow the commands:
```
$ make
$ ./latc_x86 path_to_file.lat
```
The program should be run from the root directory.

If for some reason makefile fails to correctly set up virtual environment for
python, one can type:
```
$ cd lib/
$ virtualenv -p python3 x86compilervenv
$ x86compilervenv/bin/activate
$ pip install antlr4-python3-runtime
$ cd ..
$ ./latc_x86 path_to_file.lat
```

The code has been tested and should work with python version 3.5.2
(and possibly higher)

### Tools used ###
*  Antlr4 - parser generator, using LL(*) for parsing. The .jar file has been attached in the lib/ directory and is necessary to generate the files
at src/autogen/

Antlr4 doesn't produce the AST itself, but instead implement a Visitor
(or Listener) pattern for tree traversal.

In order to work with antlr4 in python 3, runtime has to be installed, by
typing ```$ pip install antlr4-python3-runtime```


### Files Contents ###
* x86-latte-compiler

  * README.txt - contains description of the project
  * latc_x86 - bash script generating .s file and executable file for a given .lat file
  * Latte.g4 - Grammar for Latte, compatible with Antlr4
  * requirements.txt - additional libraries for python 3
  * Makefile - set up a python virtual environment, and allows to generate
                visitors of the parse tree for the grammar specified in .g4 file
  * CompilerTester.py - automatic tester of the solution.
        Usage:
        python CompilerTester.py latc_x86 good path_to_good_test_dir
        or
        python CompilerTester.py latc_x86 bad path_to_bad_test_dir
  - lib/
    * antlr-4.7-complete.jar - antlr4 parser generator
    * runtime.c - library written in c for some common functions, e.g: printInt, printString, error, readInt, readString, concat
    * runtime.s - library for some common functions compiled into assembly
  
  - src/
    * CompileLatte.py - main file, which manages the flow of the program
    * AssemblyCode.py - file containing wrappers for x86 instructions
    * TypeChecker.py - file containing most of the logic connected with validating the input program in terms of its' type correctness
    * FuncionNodesDecorator.py - decorates the function nodes in the parse tree with additional information specific to the functions
    * ReturnReachableValidator.py - performs checks whether a given return statement is always reachable within any declared function. If no, then it throws error
    * Common.py - file containing some common constants definition
    * TypeCheckerErrors.py - contains errors that are thrown during type-checking(front-end) phase, before the actual assembly code is generated
    *  LexerParserErrorHandler.py - defines strategy to use when a parser or lexer encounter an error(to possibly solve the problem)
    * LexerParserErrorListener.py - defines the action to take whenever a lexer or parser encounter an error

