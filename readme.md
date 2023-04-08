# playcode: a playful programming language

This is a work-in-progress.

## grammar

    program -> statement_list

    statement_list -> statement | statement statement_list

    statement -> if_statement | while_statement | assignment_statement | print_statement

    if_statement -> IF expression NEWLINE statement_list [ ELSE statement_list ] END

    while_statement -> WHILE expression NEWLINE statement_list END

    assignment_statement -> IDENTIFIER INCREMENT | IDENTIFIER DECREMENT | IDENTIFIER ASSIGN expression

    print_statement -> PRINT expression

    expression -> comparison

    comparison -> addition ( ( == | != | <= | >= | < | > ) addition )*

    addition -> multiplication ( ( + | - ) multiplication )*

    multiplication -> unary ( ( * | / ) unary )*

    unary -> ( - | ! ) unary | primary

    primary -> NUMBER | STRING | TRUE | FALSE | expression | IDENTIFIER

    IF          -> "if"
    ELSE        -> "else"
    WHILE       -> "while"
    END         -> "end"
    PRINT       -> "print"
    TRUE        -> "true"
    FALSE       -> "false"
    INCREMENT   -> "++"
    DECREMENT   -> "--"
    ASSIGN      -> "="
    NEWLINE     -> "\n"

### example program

x = 42
y = 5
# comment
if x < 0
    print false
else
    print "positive"
end
# comment
while y > 0
    print y--
end

