# playcode: a playful programming language

## TODO

- [ ] delete `pc.cpp` -> rename `fpc.cpp` to `pc.cpp`

## grammar

    program                 ::= (TAG)? statement+

    statement               ::= if_statement | assignment_statement | swap_statement | goto_statement | print_statement

        if_statement            ::= IF condition COLON statement+ (ELSE statement_list)? END

        assignment_statement    ::= ID INCREMENT | ID DECREMENT | ID ASSIGN expression

        swap_statement          ::= SWAP ID ID

        goto_statement          ::= GOTO TAG

        print_statement         ::= PRINT expression

    condition               ::= (TRUE | FALSE) | expression ((LT | GT | LE | GE | EQ | NEQ) expression)?

    expression              ::= term ((PLUS | MINUS) term)*

    term                    ::= factor ((MUL | DIV) factor)*

    factor                  ::= PLUS factor | MINUS factor | INTEGER | STRING | ID | LPAR expression RPAR

## tokens
    
    IF          -> "if"
    ELSE        -> "else"
    END         -> "end"
    SWAP        -> "swap"
    GOTO        -> "goto"
    PRINT       -> "print"
    INCREMENT   -> "++"
    DECREMENT   -> "--"
    ASSIGN      -> "="
    COLON       -> ":"
    PLUS        -> "+"
    MINUS       -> "-"
    MUL         -> "*"
    DIV         -> "/"
    LPAR        -> "("
    RPAR        -> ")"
    LT          -> "<"
    GT          -> ">"
    LE          -> "<="
    GE          -> ">="
    EQ          -> "=="
    NEQ         -> "!="

    TAG         -> @[a-zA-Z_][a-zA-Z0-9_]*
    ID          -> [a-zA-Z_][a-zA-Z0-9_]*
    INTEGER     -> [0-9]+
    TRUE        -> "true"
    FALSE       -> "false"
    STRING      -> ".*"

Swap keyword swaps the values of two variables.

A tag, such as `@my_tag` is used to mark a statement with a tag (similar to functions). Tags can be used to jump to a statement.

### example valid programs

```
print 42
```

```
x = 42
# comment
if x < 0:
    print false
else
    print "positive"
end
```

```
# swap
x = 2
y = 3
swap x y
print y == 2 # true
```

```
# repeat
x = 0
@inc x++
goto @inc
print x # 2
```

## issues

- [ ] `goto` jumps to the first statement with the given tag, how to deal with multiple same tags (make unique?)
- [ ] `goto` jumps repeat only statement after tag, or everything after tag in program? (if everything, perhaps add keyword `once` to avoid endless repetition)

