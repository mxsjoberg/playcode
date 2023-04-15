/*

program         ::= statement+
statement       ::= "print" expression
condition       ::=
expression      ::= integer
integer         ::= [0-9]+

*/

/*

PRINT -> "print"
INTEGER -> [0-9]+

*/

/*

print 42

*/

#import <iostream>
#import <string>
#import <vector>

enum class TokenType {
    PRINT,
    INTEGER,
};

struct Token {
    TokenType type;
    std::string lexeme;
};

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

// tokenize the source code
std::vector<Token> tokenize(const std::string& source) {
    std::vector<Token> tokens;
    size_t currentCharIndex = 0;
    while (currentCharIndex < source.size()) {
        char ch = source[currentCharIndex];
        switch (ch) {
            case ' ':
            case '\t':
            case '\r':
            case '\n':
                currentCharIndex++;
                break;
            default:
                if (isdigit(ch)) {
                    size_t start = currentCharIndex;
                    while (isdigit(source[currentCharIndex]) && currentCharIndex < source.size()) {
                        currentCharIndex++;
                    }
                    std::string lexeme = source.substr(start, currentCharIndex - start);
                    tokens.push_back({TokenType::INTEGER, lexeme});
                } else if (isalpha(ch)) {
                    size_t start = currentCharIndex;
                    while (isalnum(source[currentCharIndex]) && currentCharIndex < source.size()) {
                        currentCharIndex++;
                    }
                    std::string lexeme = source.substr(start, currentCharIndex - start);
                    if (lexeme == "print" || lexeme == "PRINT") {
                        tokens.push_back({TokenType::PRINT, upper(lexeme)});
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

Token parse_expression(const std::vector<Token>& tokens, size_t& currentTokenIndex);
std::vector<Token> parse_statement(const std::vector<Token>& tokens, size_t& currentTokenIndex);

// parse : program
std::vector<std::vector<Token>> parse(const std::vector<Token>& tokens) {
    std::vector<std::vector<Token>> tree;
    size_t currentTokenIndex = 0;
    while (currentTokenIndex < tokens.size()) {
        std::vector<Token> statement = parse_statement(tokens, currentTokenIndex);
        tree.push_back(statement);
    }
    return tree;
}

// parse : statement
std::vector<Token> parse_statement(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    std::vector<Token> statement;
    Token token = tokens[currentTokenIndex];
    switch (token.type) {
        case TokenType::PRINT:
            statement.push_back(token);
            currentTokenIndex++;
            statement.push_back(parse_expression(tokens, currentTokenIndex));
            break;
        default:
            throw std::runtime_error("Unexpected token");
    }
    return statement;
}

// parse : expression
Token parse_expression(const std::vector<Token>& tokens, size_t& currentTokenIndex) {
    Token token = tokens[currentTokenIndex];
    switch (token.type) {
        case TokenType::INTEGER:
            currentTokenIndex++;
            return token;
        default:
            throw std::runtime_error("Unexpected token");
    }
}

///
//
// Main
//
///

int main() {
    std::string source = "print 42";
    std::vector<Token> tokens = tokenize(source);
    // for (Token token : tokens) {
    //  std::cout << token.lexeme << std::endl;
    // }
    std::vector<std::vector<Token>> statements = parse(tokens);
    for (std::vector<Token> statement : statements) {
        for (Token token : statement) {
            std::cout << token.lexeme << std::endl;
        }
    }
}


