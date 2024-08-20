#######################################
# TOKENS
#######################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MODULO = 'MODULO'

TT_EQ = 'EQ'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'

#######################################
# FUNCTIONS TOKENS
#######################################
TT_FUNC = '$'
TT_FUNC_NAME = 'FUNC_NAME'
TT_FUNC_ARGS = 'FUNC_ARGS'
TT_FUNC_SIGN = '=>'
TT_FUNC_BODY = 'FUNC_BODY'
TT_LLAMBDA = '['
TT_RLAMBDA = ']'
TT_LAMBDA_SIGN = ':'
TT_CALL_FUNC = '@'
TT_FUNC_LBRACKET = '{'
TT_FUNC_RBRACKET = '}'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_AND = '&&'
TT_OR = '||'
TT_STRING = 'STRING'
TT_BOOL = 'BOOL'
TT_COMMA = 'COMMA'
TT_NOT = '!'
TT_COMMENT = '#'
TT_PRINTED_NOTE = '##'
TT_EOF = 'EOF'
TT_EXIT = 'EXIT'

KEYWORDS = [
    "+", "-", "*", "/", "%", "==", "<", ">", "<=", ">=", "(", ")", ","
]

BOOLEANS = ["True", "False"]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value=None):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if not value and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
