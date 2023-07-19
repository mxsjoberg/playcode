/*

*/

/*

program         ::= statement+
statement       ::= PRINT expression
expression      ::= term ((PLUS | MINUS) term)*
term            ::= factor ((MUL | DIV) factor)*
factor          ::= PLUS factor | MINUS factor | INTEGER | LPAR expression RPAR

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

#include <iostream>
#include <regex>
#include <string>
#include <vector>

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
    TokenType type;
    std::string lexeme;
    size_t line = 0;
    size_t charIndex = 0;
    int value = 0;
    std::string variableName;
};

#define print(x) std::cout << x << std::endl;

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

// std::string ASTtoString(const AST& ast, size_t indent = 0) {
//     std::string output = "";
//     for (size_t i = 0; i < indent; i++) {
//         output += " ";
//     }

//     output += tokenToString(ast.token);

//     if (ast.children.size() > 0) {
//         output += "[\n";
//         for (size_t i = 0; i < ast.children.size(); i++) {
//             output += ASTtoString(ast.children[i], indent + 1);
//             if (i < ast.children.size() - 1) {
//                 output += ",\n";
//             }
//         }
//         output += "\n";
//         for (size_t i = 0; i < indent; i++) {
//             output += " ";
//         }
//         output += "]";
//     }
//     return output;
// }

void printTree(const AST& node, int level = 0) {
    std::cout << std::string(level * 2, ' ') << tokenToString(node.token) << std::endl;
    for (const AST& child : node.children) {
        printTree(child, level + 1);
    }
}

AST parse_expression(const std::vector<Token>& tokens, size_t& currentTokenIndex);
AST parse_statement(const std::vector<Token>& tokens, size_t& currentTokenIndex);
AST parse_term(const std::vector<Token>& tokens, size_t& currentTokenIndex);
AST parse_factor(const std::vector<Token>& tokens, size_t& currentTokenIndex);

// parse : program ::= statement+
AST parse(const std::vector<Token>& tokens) {
    size_t currentTokenIndex = 0;
    AST program;
    program.token = Token{TokenType::BOF};
    // statement+
    while (currentTokenIndex < tokens.size()) {
        program.children.push_back(parse_statement(tokens, currentTokenIndex));
    }
    return program;
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
    // term
    AST expression = parse_term(tokens, currentTokenIndex);
    // ((PLUS | MINUS) term)*
    while (tokens[currentTokenIndex].type == TokenType::PLUS || tokens[currentTokenIndex].type == TokenType::MINUS) {
        // (PLUS | MINUS)
        Token token = tokens[currentTokenIndex];
        currentTokenIndex++;
        // term
        auto children = {expression, parse_term(tokens, currentTokenIndex)};
        expression = AST{token, children};
    }
    return expression;
}

// parse : term ::= factor ((MUL | DIV) factor)*
AST parse_term(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    // factor
    AST term = parse_factor(tokens, currentTokenIndex);
    // ((MUL | DIV) factor)*
    while (tokens[currentTokenIndex].type == TokenType::MUL || tokens[currentTokenIndex].type == TokenType::DIV) {
        // (MUL | DIV)
        Token token = tokens[currentTokenIndex];
        currentTokenIndex++;
        // factor
        auto children = {term, parse_factor(tokens, currentTokenIndex)};
        term = AST{token, children};
    }
    return term;
}

// parse : factor ::= PLUS factor | MINUS factor | INTEGER | LPAR expression RPAR
AST parse_factor(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    AST expression;
    AST factor;
    // PLUS factor | MINUS factor | INTEGER | LPAR expression RPAR
    Token token = tokens[currentTokenIndex];
    switch (token.type) {
        // PLUS factor
        case TokenType::PLUS:
            // PLUS
            factor.token = token;
            currentTokenIndex++;
            // factor
            factor.children.push_back(parse_factor(tokens, currentTokenIndex));
            return factor;
        // MINUS factor
        case TokenType::MINUS:
            // MINUS
            factor.token = token;
            currentTokenIndex++;
            // factor
            factor.children.push_back(parse_factor(tokens, currentTokenIndex));
            return factor;
        // INTEGER
        case TokenType::INTEGER:
            // INTEGER
            currentTokenIndex++;
            return AST{token};
        // LPAR expression RPAR
        case TokenType::LPAR:
            // LPAR
            currentTokenIndex++;
            // expression
            expression = parse_expression(tokens, currentTokenIndex);
            // RPAR
            if (tokens[currentTokenIndex].type != TokenType::RPAR) {
                throw std::runtime_error("Expected ')'");
            }
            currentTokenIndex++;
            return expression;
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
    for (AST node : tree.children) {
        // PRINT
        if (node.token.type == TokenType::PRINT) {
            auto result = evaluate(node.children[0]);
            std::cout << "> " << result << std::endl;
        } else {
            throw std::runtime_error("Unexpected token");
        }
    }
}

///
//
// Main
//
///

int main() {
    // std::string source = "print 1 + (2 * 4) - (6 / 2)";
    std::string input = R"(
        print 42
        print 1 + (2 * 4) - (6 / 2)
    )";
    std::regex pattern(R"(^\s+)", std::regex::multiline);
    std::string source = std::regex_replace(input, pattern, "");
    // tokenize
    std::vector<Token> tokens = tokenize(source);
    // for (Token token : tokens) {
    //     // std::cout << token.lexeme << " @ " << token.line << ":" << token.charIndex << std::endl;
    //     std::cout << token.lexeme << std::endl;
    // }
    // parse
    AST statements = parse(tokens);
    // print(ASTtoString(statements));
    // PROGRAM[
    //  PRINT[
    //   "-"[
    //    "+"[
    //     INTEGER(1),
    //     "*"[
    //      INTEGER(2),
    //      INTEGER(4)
    //     ]
    //    ],
    //    "/"[
    //     INTEGER(6),
    //     INTEGER(2)
    //    ]
    //   ]
    //  ]
    // ]
    printTree(statements);
    // interpret
    interpret(statements);
    // > 6
}
