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

    def define_func_name(self):
        name = ""
        flag = False
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char != TT_FUNC and self.current_char in LETTERS:
            name = self.read_word()
            #self.advance()
        if self.current_char == TT_FUNC:  #last $ exist
            flag = True
            self.advance()
        else:
            pos_start = self.pos.copy()
            if self.current_char:  #check if character exist
                char = self.current_char
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
            if not flag:  #missing $ at the end
                return [], InvalidSyntaxError(pos_start, self.pos)
        return Token(TT_FUNC_NAME, name, pos_start, self.pos)

    def define_func_args(self):
        args = []
        pos_start = self.pos.copy()
        arg_name = ""
        if self.current_char in ' \t':  #white space
            self.advance()
        if self.current_char != "(":
            return [], InvalidSyntaxError(pos_start, self.pos)
        self.advance()
        while self.current_char and self.current_char != ")":
            if self.current_char in ' \t':  # white space
                self.advance()
            elif self.current_char in LETTERS:
                arg_name = self.read_word()
                #self.advance()
            elif self.current_char == ",":
                args.append(arg_name)
                arg_name = ""
                self.advance()
            else:
                pos_start = self.pos.copy()
                if self.current_char:
                    return [], IllegalCharError(pos_start, self.pos, "'" + self.current_char + "'")
                else:
                    return [], InvalidSyntaxError(pos_start, self.pos)
        if arg_name:
            args.append(arg_name)
        else:
            if args:
                return [], InvalidSyntaxError(pos_start, self.pos)
        self.advance()
        return Token(TT_FUNC_ARGS, args, pos_start, self.pos)

    def read_word(self):
        word = ""

        while self.current_char != None and self.current_char in LETTERS:
            word += self.current_char
            self.advance()

        return word

    def define_func_context(self):
        context = ""
        pos_start = self.pos.copy()
        if self.current_char in ' \t':  #white space
            self.advance()
        if self.current_char != "=":
            return [], InvalidSyntaxError(pos_start, self.pos)
        self.advance()
        if self.current_char != ">":
            return [], InvalidSyntaxError(pos_start, self.pos)
        self.advance()
        if self.current_char in ' \t':  # white space
            self.advance()
        if self.current_char != "{":
            return [], InvalidSyntaxError(pos_start, self.pos)
        self.advance()
        while self.current_char and self.current_char != "}":
            context += self.current_char
            self.advance()
        if self.current_char != "}":
            return [], InvalidSyntaxError(pos_start, self.pos)
        self.advance()
        return Token(TT_FUNC_CONTEXT, context, pos_start, self.pos)

    def call_func(self):
        pos_start = self.pos.copy()
        word = self.read_word()
        print(word)




    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char == TT_FUNC and self.pos.idx == 0:
                self.advance()
                tokens.append(self.define_func_name())
                tokens.append(self.define_func_args())
                tokens.append(self.define_func_context())
                if type(tokens[2]) is tuple:
                    return tokens[2]
                f = Function(tokens[0].value, tokens[1].value, tokens[2].value)
                f.context_to_tokens()
            elif self.current_char in ' \t':
                self.advance()
            elif self.current_char in LETTERS:
                self.call_func()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
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
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
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
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
