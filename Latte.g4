grammar Latte;

program
    : topDef+ EOF
    ;

topDef
    : fundef                                            # TopFunDef
    | 'class' ID '{' clsattr* clsfun* '}'               # ClsDef
    | 'class' ID 'extends' ID '{' clsattr* clsfun* '}'  # ClsExtDef
    ;

clsattr
    : type_ ID (',' ID)* ';'
    ;

clsfun
    : fundef
    ;

fundef
    : type_ ID '(' arg? ')' block
    ;

arg
    : type_ ID ( ',' type_ ID )*
    ;

block
    : '{' stmt* '}'
    ;

stmt
    : ';'                                # Empty
    | block                              # BlockStmt
    | type_ item ( ',' item )* ';'       # Decl
    | expr '=' expr ';'                   # Ass
    | expr '++' ';'                       # Incr
    | expr '--' ';'                       # Decr
    | 'return' expr ';'                  # Ret
    | 'return' ';'                       # VRet
    | 'if' '(' expr ')' stmt             # Cond
    | 'if' '(' expr ')' stmt 'else' stmt # CondElse
    | 'while' '(' expr ')' stmt          # While
    | expr ';'                           # SExp
    ;

type_
    : 'int'     # Int
    | 'string'  # Str
    | 'boolean' # Bool
    | 'void'    # Void
    | ID        # Class
    ;

item
    : ID                                # ItemDecl
    | ID '=' expr                       # ItemDef
    ;

expr
    : unOp expr                           # EUnOp
    | expr mulOp expr                     # EMulOp
    | expr addOp expr                     # EAddOp
    | expr relOp expr                     # ERelOp
    | <assoc=right> expr '&&' expr        # EAnd
    | <assoc=right> expr '||' expr        # EOr
    | ID                                  # EId
    | INT                                 # EInt
    | 'true'                              # ETrue
    | 'false'                             # EFalse
    | ID '(' ( expr ( ',' expr )* )? ')'  # EFunCall
    | STR                                 # EStr
    | '(' expr ')'                        # EParen
    | 'new' ID                            # ENewObj
    | expr '.' expr                       # EFieldAcs
    | '(' type_ ')' 'null'                # ECastNull
    ;

unOp
    : '-'                   # NegInt
    | '!'                   # NegBool
    ;

addOp
    : '+'                   # Add
    | '-'                   # Sub
    ;

mulOp
    : '*'                   # Mul
    | '/'                   # Div
    | '%'                   # Mod
    ;

relOp
    : '<'                   # Lt
    | '<='                  # Le
    | '>'                   # Gt
    | '>='                  # Ge
    | '=='                  # Eq
    | '!='                  # Neq
    ;

COMMENT : ('#' ~[\r\n]* | '//' ~[\r\n]*) -> channel(HIDDEN);
MULTICOMMENT : '/*' .*? '*/' -> channel(HIDDEN);

fragment Letter  : Capital | Small ;
fragment Capital : [A-Z\u00C0-\u00D6\u00D8-\u00DE] ;
fragment Small   : [a-z\u00DF-\u00F6\u00F8-\u00FF] ;
fragment Digit : [0-9] ;

INT : Digit+ ;
fragment ID_First : Letter | '_';
ID : ID_First (ID_First | Digit)* ;

WS : (' ' | '\r' | '\t' | '\n')+ ->  skip;

STR
    :   '"' StringCharacters? '"'
    ;
fragment StringCharacters
    :   StringCharacter+
    ;
fragment
StringCharacter
    :   ~["\\]
    |   '\\' [tnr"\\]
    ;
