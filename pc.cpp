// pc.cpp

/*

program           ::= statement+
statement         ::= print_statement
print_statement   ::= "print" expression
expression        ::= integer
integer           ::= [0-9]+

*/

/*

PRINT -> "print"
INTEGER -> [0-9]+

*/

/*

print 42

*/

#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <map>

// #define log(str);
#define log(str) std::cout << str << std::endl;

// Token types : for lexer
enum class TokenType {
  // IF,
  // ELSE,
  // WHILE,
  // NEWLINE,
  // END_BLOCK,
  PRINT,
  INTEGER,
  // NUMBER,
  // STRING,
  // BOOLEAN,
  // INCREMENT,
  // DECREMENT,
  // ASSIGN,
  // COMMA,
  // IDENTIFIER,
  // EQUAL,
  // NOTEQUAL,
  // LESS,
  // LESSEQUAL,
  // GREATER,
  // GREATEREQUAL,
  // PLUS,
  // MINUS,
  // ASTERISK,
  // SLASH,
  // NOT,
  ERROR,
  END_OF_FILE
};

// Token type to string : for debugging
std::string tokenTypeToString(TokenType type) {
  switch (type) {
    case TokenType::PRINT:
      return "PRINT";
    case TokenType::INTEGER:
      return "INTEGER";
    case TokenType::ERROR:
      return "ERROR";
    case TokenType::END_OF_FILE:
      return "END_OF_FILE";;
    default:
      return "UNKNOWN";
  }
}
// Token struct : stores token type, lexeme, and line number
struct Token {
  TokenType type;
  std::string lexeme;
  // track line number
  size_t line;
};

///
// 
// Lexer
//
///

// Lexer class : tokenizes source code
class Lexer {
  public:
    Lexer(const std::string& source);
    Token getNextToken();
    // helper functions
    char peek();
    char advance();
    bool isAtEnd();
    bool isAlpha(char c);
    bool isAlphaNumeric(char c);
    bool isDigit(char c);
    bool isWhitespace(char c);
    void addToken(TokenType type, std::string lexeme);
    // Token identifier();
    Token number();
    // Token string();
    // Token boolean();
  private:
    std::string m_source;
    std::vector<Token> m_tokens;
    size_t m_currentTokenIndex;
    size_t m_currentCharIndex;
    size_t m_currentLine;
};
char Lexer::peek() {
  return m_source[m_currentCharIndex];
}
char Lexer::advance() {
  m_currentCharIndex++;
  return m_source[m_currentCharIndex - 1];
}
bool Lexer::isAtEnd() {
  return m_currentCharIndex >= m_source.length();
}
bool Lexer::isAlpha(char c) {
  return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}
bool Lexer::isDigit(char c) {
  return c >= '0' && c <= '9';
}
bool Lexer::isAlphaNumeric(char c) {
  return isAlpha(c) || isDigit(c);
}
bool Lexer::isWhitespace(char c) {
  return c == ' ' || c == '\t' || c == '\r';
}
// helper to add token to vector
void Lexer::addToken(TokenType type, std::string lexeme) {
  m_tokens.push_back({ type, lexeme, m_currentLine });
}

Lexer::Lexer(const std::string& source) : m_source(source), m_currentTokenIndex(0), m_currentCharIndex(0), m_currentLine(1) {}

Token Lexer::getNextToken() {
  while (m_currentTokenIndex == m_tokens.size()) {
    if (isAtEnd()) {
      Lexer::addToken(TokenType::END_OF_FILE, "");
    } else {
      char c = advance();
      switch (c) {
        case ',':
          // Lexer::addToken(TokenType::COMMA, ",");
          break;
        case '+':
          // Lexer::addToken(TokenType::PLUS, "+");
          break;
        case '-':
          if (peek() == '-') {
            advance();
            // Lexer::addToken(TokenType::DECREMENT, "--");
          } else {
            // Lexer::addToken(TokenType::MINUS, "-");
          }
          break;
        case '*':
          // Lexer::addToken(TokenType::ASTERISK, "*");
          break;
        case '/':
          // Lexer::addToken(TokenType::SLASH, "/");
          break;
        case '!':
          if (peek() == '=') {
            advance();
            // Lexer::addToken(TokenType::NOTEQUAL, "!=");
          } else {
            // Lexer::addToken(TokenType::NOT, "!");
          }
          break;
        case '=':
          if (peek() == '=') {
            advance();
            // Lexer::addToken(TokenType::EQUAL, "==");
          } else {
            // Lexer::addToken(TokenType::ASSIGN, "=");
          }
          break;
        case '<':
          if (peek() == '=') {
            advance();
            // Lexer::addToken(TokenType::LESSEQUAL, "<=");
          } else {
            // Lexer::addToken(TokenType::LESS, "<");
          }
          break;
        case '>':
          if (peek() == '=') {
            advance();
            // Lexer::addToken(TokenType::GREATEREQUAL, ">=");
          } else {
            // Lexer::addToken(TokenType::GREATER, ">");
          }
          break;
        case '#':
          while (peek() != '\n') {
            advance();
          }
          break;
        case ' ':
        case '\t':
        case '\r':
          break;
        case '\n':
          // Lexer::addToken(TokenType::NEWLINE, "
          m_currentLine++;
          break;
        default:
          // parse numeric literal
          if (isDigit(c)) {
            std::string value = "";
            value += c;
            while (isDigit(peek())) {
              value += advance();
            }
            if (peek() == '.') {
              value += advance();
              while (isDigit(peek())) {
                value += advance();
              }
              double number = std::stod(value);
              // Lexer::addToken(TokenType::NUMBER, std::to_string(number));
            } else {
              int number = std::stoi(value);
              Lexer::addToken(TokenType::INTEGER, std::to_string(number));
            }
          // parse identifier or keyword
          } else if (isAlpha(c) || c == '_') {
            std::string value = "";
            value += c;
            while (isAlphaNumeric(peek()) || peek() == '_') {
              value += advance();
            }
            TokenType type;
            // if (value == "if") {
            //     type = TokenType::IF;
            // } else if (value == "else") {
            //     type = TokenType::ELSE;
            // } else if (value == "while") {
            //     type = TokenType::WHILE;
            // } else if (value == "end") {
            //     type = TokenType::END_BLOCK;
            // } else if (value == "true" || value == "false") {
            //     type = TokenType::BOOLEAN;
            // } else if (value == "print") {
            //     type = TokenType::PRINT;
            // } else {
            //     type = TokenType::IDENTIFIER;
            // }
            if (value == "print") {
              type = TokenType::PRINT;
            }
            Lexer::addToken(type, value);
          }
          // else if (c == '"' || c == '\'') {
          //     // parse string literal
          //     std::string value = "";
          //     char quote = c;
          //     while (peek() != quote && !isAtEnd()) {
          //         if (peek() == '\\') {
          //             advance();
          //             value += quote;
          //         } else {
          //             value += advance();
          //         }
          //     }
          //     if (isAtEnd()) {
          //         m_tokens.push_back({ TokenType::ERROR, "Error: Expected closing quote", m_currentLine });
          //     } else {
          //         // closing quote
          //         advance();
          //         m_tokens.push_back({ TokenType::STRING, value, m_currentLine });
          //     }
          // }
          else {
            Lexer::addToken(TokenType::ERROR, "Error: Unexpected character");
          }
          break;
      }
    }
  }
  // return the tokens
  Token token = m_tokens.at(m_currentTokenIndex);
  // advance the token index
  m_currentTokenIndex++;
  return token;
}

///
//
// AST
//
///

class ASTProgram;
class ASTStatement;
class ASTPrintStatement;
class ASTExpression;
class ASTInteger;

class ASTVisitor {
  public:
    virtual ~ASTVisitor() = default;
    virtual void visit(ASTProgram& node) = 0;
    virtual void visit(ASTStatement& node) = 0;
    virtual void visit(ASTPrintStatement& node) = 0;
    virtual void visit(ASTExpression& node) = 0;
    virtual void visit(ASTInteger& node) = 0;
};

class ASTNode {
  public:
    virtual ~ASTNode() = default;
    // virtual void accept(ASTVisitor& visitor) = 0;
};

class ASTProgram : public ASTNode {
  public:
    ASTProgram(std::vector<std::unique_ptr<ASTStatement>> statements)
      : m_statements(std::move(statements)) {}
    // accept a visitor
    void accept(ASTVisitor& visitor) {
      visitor.visit(*this);
    }
    // getter
    const std::vector<std::unique_ptr<ASTStatement>>& getStatements() const {
      return m_statements;
    }
  private:
    std::vector<std::unique_ptr<ASTStatement>> m_statements;
};

class ASTStatement : public ASTNode {
  public:
    ASTStatement(std::unique_ptr<ASTPrintStatement> printStatement)
      : m_printStatement(std::move(printStatement)) {}
    // add more statements here
    // accept a visitor
    void accept(ASTVisitor& visitor) {
      visitor.visit(*this);
    }
    // getter
    ASTPrintStatement& getPrintStatement() {
      return *m_printStatement;
    }
    // add more getters here
  private:
    std::unique_ptr<ASTPrintStatement> m_printStatement;
};

class ASTPrintStatement : public ASTNode {
  public:
    ASTPrintStatement(std::unique_ptr<ASTExpression> expression)
      : m_expression(std::move(expression)) {}
    // accept a visitor
    void accept(ASTVisitor& visitor) {
      visitor.visit(*this);
    }
    // getter
    ASTExpression& getExpression() {
      return *m_expression;
    }
  private:
    std::unique_ptr<ASTExpression> m_expression;
};

class ASTExpression : public ASTNode {
  public:
    ASTExpression(std::unique_ptr<ASTInteger> integer)
      : m_integer(std::move(integer)) {}
    // accept a visitor
    void accept(ASTVisitor& visitor) {
      visitor.visit(*this);
    }
    // generate IR
    // llvm::Value* generateIR() {
    //   return m_integer->generateIR();
    // }
    // getter
    ASTInteger& getInteger() {
      return *m_integer;
    }
  private:
    std::unique_ptr<ASTInteger> m_integer;
};

class ASTInteger : public ASTNode {
  public:
    ASTInteger(int value)
      : m_value(value) {}
    // accept a visitor
    void accept(ASTVisitor& visitor) {
      visitor.visit(*this);
    }
    // generate IR
    // llvm::Value* generateIR() {
    //   return llvm::ConstantInt::get(m_context, llvm::APInt(32, m_value));
    // }
    // getter
    int getValue() const {
      return m_value;
    }
  private:
    int m_value;
};

class ASTInterpreter : public ASTVisitor {
  public:
    ASTInterpreter() {}

    // ASTProgram
    void visit(ASTProgram& node) override {
      // iterate over all statements
      for (const auto& statement : node.getStatements()) {
        statement->accept(*this);
      }
    }
    // ASTStatement
    void visit(ASTStatement& node) override {
      node.getPrintStatement().accept(*this);
    }
    // ASTPrintStatement
    void visit(ASTPrintStatement& node) override {
      log("PRINT");
      node.getExpression().accept(*this);
    }
    // void visit(ASTExpression& node) override {
    //   node.getInteger().accept(*this);
    // }
    // void visit(ASTInteger& node) override {
    //   log("INTEGER(" << node.getValue() << ")");
    // }

    // ASTExpression
    void visit(ASTExpression& node) override {
      node.getInteger().accept(*this);
    }
    // ASTInteger
    void visit(ASTInteger& node) override {
      log("INTEGER(" << node.getValue() << ")");
    }
};

///
//
// Parser
//
///

class Parser {
  public:
    Parser(Lexer& lexer)
      : m_lexer(lexer), m_token(m_lexer.getNextToken()) {}
    
    std::unique_ptr<ASTProgram> parse() {
      std::vector<std::unique_ptr<ASTStatement>> statements;
      while (m_token.type != TokenType::END_OF_FILE) {
        auto statement = parseStatement();
        if (statement != nullptr) {
          statements.push_back(std::move(statement));
        }
        m_token = m_lexer.getNextToken();
      }
      return std::make_unique<ASTProgram>(std::move(statements));
    }
  private:
    Lexer& m_lexer;
    Token m_token;

    // ASTStatement
    std::unique_ptr<ASTStatement> parseStatement() {
      if (m_token.type == TokenType::PRINT) {
        return std::make_unique<ASTStatement>(parsePrintStatement());
      }
      return nullptr;
    }
    // ASTPrintStatement
    std::unique_ptr<ASTPrintStatement> parsePrintStatement() {
      m_token = m_lexer.getNextToken();
      auto expression = parseExpression();
      return std::make_unique<ASTPrintStatement>(std::move(expression));
    }
    // ASTExpression
    std::unique_ptr<ASTExpression> parseExpression() {
      return std::make_unique<ASTExpression>(parseInteger());
    }
    // ASTInteger
    std::unique_ptr<ASTInteger> parseInteger() {
      int value = std::stoi(m_token.lexeme);
      return std::make_unique<ASTInteger>(value);
    }
};

///
//
// Main
//
///

int main() {
  std::string input = R"(
    print 42
    print 8
  )";
  std::regex pattern(R"(^\s+)", std::regex::multiline);
  std::string text = std::regex_replace(input, pattern, "");
  // std::cout << text << std::endl;

  Lexer lexer(text);
  // std::vector<Token> tokens;
  // Token token = lexer.getNextToken();
  // while (token.type != TokenType::END_OF_FILE) {
  //     // std::cout << tokenTypeToString(token.type) << "(\"" << token.lexeme << "\")" << std::endl;
  //     tokens.push_back(token);
  //     token = lexer.getNextToken();
  // }

  // parser
  Parser parser(lexer);
  auto ast = parser.parse();
  // visitor
  ASTInterpreter interpreter;
  ast->accept(interpreter);
}
