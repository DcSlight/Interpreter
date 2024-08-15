from Position import Position
from Token import *
from Error import *
from FunctionalProgramming.function import Function
import string

#######################################
# CONSTANTS
#######################################

# TODO: move to the BNF

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_string(self):
        tok_type = TT_STRING
        word = ""
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS:
            word += self.current_char
            self.advance()

        # Check for Built-ins
        if word in BOOLEANS:
            tok_type = TT_BOOL
        elif word == TT_EXIT:
            tok_type = TT_EXIT
            return Token(tok_type, pos_start=pos_start)

        return Token(tok_type, word, pos_start=pos_start)

    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_EE
        elif self.current_char == ">":
            self.advance()
            tok_type = TT_FUNC_SIGN

        return Token(tok_type, pos_start=pos_start)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start)

    def make_less_then(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start)

    def make_not_equal(self):
        tok_type = TT_NOT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_NE

        return Token(tok_type, pos_start=pos_start)

    def make_and(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "&":
            self.advance()
            tok_type = TT_AND
            return Token(tok_type, pos_start=pos_start)

        return [], IllegalCharError(pos_start, self.pos, "'" + self.current_char + "'")

    def make_or(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "|":
            self.advance()
            tok_type = TT_OR
            return Token(tok_type, pos_start=pos_start)

        return [], IllegalCharError(pos_start, self.pos, "'" + self.current_char + "'")

    def make_comment(self):
        tok_type = TT_COMMENT
        comment = ""
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "#":
            self.advance()
            tok_type = TT_PRINTED_NOTE

        while self.current_char != None:
            comment += self.current_char
            self.advance()
        self.advance()

        return Token(tok_type, comment, pos_start=pos_start)

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char == TT_FUNC:
                tokens.append(Token(TT_FUNC, pos_start=self.pos))
                self.advance()
            elif self.current_char in ' \t':
                self.advance()
            elif self.current_char in LETTERS:
                tokens.append(self.make_string())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '<':
                tokens.append(self.make_less_then())
            elif self.current_char == '!':
                tokens.append(self.make_not_equal())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MODULO, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == '@':
                tokens.append(Token(TT_CALL_FUNC, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_FUNC_LBRACKET, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_FUNC_RBRACKET, pos_start=self.pos))
                self.advance()
            elif self.current_char == '&':
                tokens.append(self.make_and())
            elif self.current_char == '|':
                tokens.append(self.make_or())
            elif self.current_char == '#':
                tokens.append(self.make_comment())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
