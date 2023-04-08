# playcode: a playful programming language

## grammar

    program                 ::= statement_list

    statement_list          ::= [TAG] statement | [TAG] statement statement_list

    statement               ::= if_statement | assignment_statement | print_statement | swap_statement | goto_statement

    if_statement            ::= IF expression NEWLINE statement_list [ ELSE statement_list ] END

    assignment_statement    ::= ID INCREMENT | ID DECREMENT | ID ASSIGN expression

    print_statement         ::= PRINT expression

    swap_statement          ::= SWAP ID ID

    goto_statement          ::= GOTO TAG

    expression              ::= comparison

    comparison              ::= addition [( == | != | <= | >= | < | > ) addition ]*

    addition                ::= multiplication [( + | - ) multiplication ]*

    multiplication          ::= unary [( * | / ) unary ]*

    unary                   ::= ( - | ! ) unary | primary

    primary                 ::= NUMBER | STRING | TRUE | FALSE | expression | ID

## keywords and symbols

    IF          -> "if"
    ELSE        -> "else"
    END         -> "end"
    SWAP        -> "swap"
    TAG         -> "@"
    PRINT       -> "print"
    TRUE        -> "true"
    FALSE       -> "false"
    INCREMENT   -> "++"
    DECREMENT   -> "--"
    ASSIGN      -> "="
    NEWLINE     -> "\n"

Swap keyword swaps the values of two variables.

Tag keyword is used to mark a statement with a tag. Tags can be used to jump to a statement.

### example valid programs

```
print 42
```

```
x = 42
# comment
if x < 0
    print false
else
    # another comment
    print "positive"
end
# comment
y = 5
while y > 0
    print y--
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
