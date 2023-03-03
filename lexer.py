# CONSTANTS
digits = '0123456789'

# TOKENS
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


# Errors ==================================
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fName}, line {self.pos_start.ln + 1}'
        return result
        
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

# Position ==================================
class Position:
    def __init__(self, idx, ln, col, fName, fText):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fName = fName
        self.fText = fText

    def advance(self, curr_char):
        self.idx += 1
        self.col += 1

        if curr_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fName, self.fText)


# LEXER ==================================
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    def __init__(self, fName, text):
        self.fName = fName
        self.text = text
        self.pos = Position(-1,0,-1, fName, text)
        self.curr_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.curr_char)
        self.curr_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.curr_char != None:
            if self.curr_char in ' \t':
                self.advance()
            elif self.curr_char in digits:
                tokens.append(self.make_number())    
            elif self.curr_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.curr_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.curr_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.curr_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.curr_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else: # ERROR
                pos_start = self.pos.copy()
                char = self.curr_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos,"'" + char + "'")
        
        return tokens, None

    def make_number(self):
        num_str = ''
        dot = 0

        while self.curr_char != None and self.curr_char in digits + '.':
            if self.curr_char == '.':
                if dot == 1:
                    break

                dot += 1
                num_str += '.'
            else:
                num_str += self.curr_char

            self.advance()

        if dot == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


# RUN

def run(fName, text):
    lexer = Lexer(fName,text)
    tokens, error = lexer.tokenize()

    return tokens,error