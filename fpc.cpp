/*

program         ::= statement+
statement       ::= PRINT expression
expression      ::= term ((PLUS | MINUS) term)*
term            ::= factor ((MUL | DIV) factor)*
factor          ::= INTEGER | LPAR expression RPAR

*/

/*

PRINT -> "print"
PLUS -> "+"
MINUS -> "-"
MUL -> "*"
DIV -> "/"
LPAR -> "("
RPAR -> ")"
INTEGER -> [0-9]+

*/

/*

print 4 + 2

*/

#import <iostream>
#import <string>
#import <vector>

enum class TokenType {
    BOF,
    PRINT,
    PLUS,
    MINUS,
    MUL,
    DIV,
    LPAR,
    RPAR,
    INTEGER,
};

struct Token {
    // base values
    TokenType type;
    std::string lexeme;
    // other values
    size_t line = 0;
    size_t charIndex = 0;
    std::string variableName;
};

#define log(x) std::cout << x << std::endl;

///
//
// Lexer
//
///

// convert string to lowercase
std::string lower(std::string& str) {
    std::transform(str.begin(), str.end(), str.begin(),
    [](unsigned char c){ return std::tolower(c); });
    return str;
}

// convert string to uppercase
std::string upper(std::string& str) {
    std::transform(str.begin(), str.end(), str.begin(),
    [](unsigned char c){ return std::toupper(c); });
    return str;
}

// token representation
std::string tokenToString(const Token& token) {
    switch (token.type) {
        case TokenType::BOF: return "PROGRAM";
        case TokenType::PRINT: return "PRINT";
        case TokenType::PLUS: return "\"+\"";
        case TokenType::MINUS: return "\"-\"";
        case TokenType::MUL: return "\"*\"";
        case TokenType::DIV: return "\"/\"";
        case TokenType::LPAR: return "EXPR";
        // case TokenType::RPAR: return "\")\"";
        case TokenType::INTEGER: return "INTEGER(" + token.lexeme + ")";
        default: return "?";
    }
}

// tokenize the source code
std::vector<Token> tokenize(const std::string& source) {
    std::vector<Token> tokens;
    size_t currentLine = 1;
    size_t currentCharIndex = 0;
    while (currentCharIndex < source.size()) {
        char ch = source[currentCharIndex];
        switch (ch) {
            case ' ':
            case '\t':
            case '\r':
                currentCharIndex++;
                break;
            case '\n':
                currentLine++;
                currentCharIndex++;
                break;
            case '+':
                tokens.push_back({TokenType::PLUS, "+", currentLine, currentCharIndex - 1});
                currentCharIndex++;
                break;
            case '-':
                tokens.push_back({TokenType::MINUS, "-", currentLine, currentCharIndex - 1});
                currentCharIndex++;
                break;
            case '*':
                tokens.push_back({TokenType::MUL, "*", currentLine, currentCharIndex - 1});
                currentCharIndex++;
                break;
            case '/':
                tokens.push_back({TokenType::DIV, "/", currentLine, currentCharIndex - 1});
                currentCharIndex++;
                break;
            case '(':
                tokens.push_back({TokenType::LPAR, "(", currentLine, currentCharIndex - 1});
                currentCharIndex++;
                break;
            case ')':
                tokens.push_back({TokenType::RPAR, ")", currentLine, currentCharIndex - 1});
                currentCharIndex++;
                break;
            default:
                if (isdigit(ch)) {
                    size_t start = currentCharIndex;
                    while (isdigit(source[currentCharIndex]) && currentCharIndex < source.size()) {
                        currentCharIndex++;
                    }
                    std::string lexeme = source.substr(start, currentCharIndex - start);
                    tokens.push_back({TokenType::INTEGER, lexeme, currentLine, currentCharIndex - lexeme.size()});
                } else if (isalpha(ch)) {
                    size_t start = currentCharIndex;
                    while (isalnum(source[currentCharIndex]) && currentCharIndex < source.size()) {
                        currentCharIndex++;
                    }
                    std::string lexeme = source.substr(start, currentCharIndex - start);
                    if (lexeme == "print" || lexeme == "PRINT") {
                        tokens.push_back({TokenType::PRINT, upper(lexeme), currentLine, currentCharIndex - lexeme.size()});
                    } else {
                        throw std::runtime_error("Unexpected identifier");
                    }
                }
        }
    }

    return tokens;
}

///
//
// Parser
//
///

struct AST {
    Token token;
    std::vector<AST> children;
};

std::string ASTtoString(const AST& ast, size_t indent = 0) {
    std::string output = "";
    // for (size_t i = 0; i < indent; i++) {
    //     output += "  ";
    // }

    output += tokenToString(ast.token);

    if (ast.children.size() > 0) {
        output += " [";
        for (size_t i = 0; i < ast.children.size(); i++) {
            output += ASTtoString(ast.children[i], indent + 1);
            if (i < ast.children.size() - 1) {
                output += ", ";
            }
        }
        output += "] ";
    }
    return output;
}

AST parse_expression(const std::vector<Token>& tokens, size_t& currentTokenIndex);
AST parse_statement(const std::vector<Token>& tokens, size_t& currentTokenIndex);
AST parse_term(const std::vector<Token>& tokens, size_t& currentTokenIndex);
AST parse_factor(const std::vector<Token>& tokens, size_t& currentTokenIndex);

// parse : program ::= statement+
AST parse(const std::vector<Token>& tokens) {
    AST tree;
    size_t currentTokenIndex = 0;
    // statement+
    while (currentTokenIndex < tokens.size()) {
        tree.children.push_back(parse_statement(tokens, currentTokenIndex));
    }
    return tree;
}

// parse : statement ::= PRINT expression
AST parse_statement(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    AST statement;
    // PRINT
    statement.token = tokens[currentTokenIndex];
    currentTokenIndex++;
    // expression
    statement.children.push_back(parse_expression(tokens, currentTokenIndex));
    return statement;
}

// parse : expression ::= term ((PLUS | MINUS) term)*
AST parse_expression(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    AST expression;
    // term
    AST term = parse_term(tokens, currentTokenIndex);
    expression = term;
    // ((PLUS | MINUS) term)*
    while (currentTokenIndex < tokens.size()) {
        Token token = tokens[currentTokenIndex];
        // PLUS | MINUS
        if (token.type == TokenType::PLUS || token.type == TokenType::MINUS) {
            expression.token = token;
            expression.children.push_back(term);
            currentTokenIndex++;
            // term
            expression.children.push_back(parse_term(tokens, currentTokenIndex));
        } else {
            break;
        }
    }
    return expression;
}

// parse : term ::= factor ((MUL | DIV) factor)*
AST parse_term(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    AST term;
    // factor
    AST factor = parse_factor(tokens, currentTokenIndex);
    term = factor;
    // ((MUL | DIV) factor)*
    while (currentTokenIndex < tokens.size()) {
        Token token = tokens[currentTokenIndex];
        // MUL | DIV
        if (token.type == TokenType::MUL || token.type == TokenType::DIV) {
            term.token = token;
            term.children.push_back(factor);
            currentTokenIndex++;
            // factor
            term.children.push_back(parse_factor(tokens, currentTokenIndex));
        } else {
            break;
        }
    }
    return term;
}

// parse : factor ::= INTEGER | LPAR expression RPAR
AST parse_factor(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    AST factor;
    AST expression;
    Token token = tokens[currentTokenIndex];
    // INTEGER | LPAR expression RPAR
    switch (token.type) {
        // INTEGER
        case TokenType::INTEGER:
            currentTokenIndex++;
            return AST{token};
        // LPAR expression RPAR
        case TokenType::LPAR:
            currentTokenIndex++;
            // expression
            expression = parse_expression(tokens, currentTokenIndex);
            if (tokens[currentTokenIndex].type != TokenType::RPAR) {
                throw std::runtime_error("Expected ')'");
            }
            currentTokenIndex++;
            return AST{expression};
        default:
            throw std::runtime_error("Unexpected token");
    }
}

///
//
// Interpreter
//
///

int evaluate(AST expression) {
    log("evaluate: " << expression.token.lexeme);
    if (expression.token.type == TokenType::INTEGER) {
        return std::stoi(expression.token.lexeme);
    } else if (expression.token.type == TokenType::PLUS) {
        return evaluate(expression.children[0]) + evaluate(expression.children[1]);
    } else if (expression.token.type == TokenType::MINUS) {
        return evaluate(expression.children[0]) - evaluate(expression.children[1]);
    } else if (expression.token.type == TokenType::MUL) {
        return evaluate(expression.children[0]) * evaluate(expression.children[1]);
    } else if (expression.token.type == TokenType::DIV) {
        return evaluate(expression.children[0]) / evaluate(expression.children[1]);
    } else {
        throw std::runtime_error("Unexpected token");
    }
}

void interpret(AST tree) {
    AST node = tree.children[0];
    if (node.token.type == TokenType::PRINT) {
        AST expression = node.children[0];
        int result = evaluate(expression);
        std::cout << "=> " << result << std::endl;
    } else {
        throw std::runtime_error("Unexpected token");
    }

}

///
//
// Main
//
///

int main() {
    std::string source = "print 4 + (2 / 2)";
    std::vector<Token> tokens = tokenize(source);
    // for (Token token : tokens) {
    //     // std::cout << token.lexeme << " @ " << token.line << ":" << token.charIndex << std::endl;
    //     std::cout << token.lexeme << std::endl;
    // }
    AST statements = parse(tokens);
    log(ASTtoString(statements));
    // interpret(statements);
}


