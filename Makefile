Project = .
antlr4jar = $(Project)/lib/antlr-4.7-complete.jar
antlr4autogen = $(Project)/src/autogen/
grammarFile = $(Project)/Latte.g4
compilervenv = $(Project)/lib/x86compilervenv


all: createVirtualEnv activateVirtualEnv

antlrgenVisitor:
	mkdir -p $(antlr4autogen)
	java -jar $(antlr4jar) -Dlanguage=Python3 -visitor -no-listener -o $(antlr4autogen) $(grammarFile)


createVirtualEnv:
	( \
		virtualenv -p python3 $(compilervenv); \
		. $(compilervenv)/bin/activate; \
		pip install antlr4-python3-runtime; \
		pip install termcolor; \
	)


activateVirtualEnv:
	/bin/bash -c "source $(compilervenv)/bin/activate; exec /bin/bash -i"

clean:
	rm -rf $(compilervenv)
