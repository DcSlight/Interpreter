from Error import *
from Token import *
from Nodes import *


#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.command()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res

    ###################################

    def command(self):
        res = ParseResult()
        if self.current_tok.matches(TT_FUNC):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        if self.current_tok.matches(TT_STRING, self.current_tok.value):
            call_func = res.register(self.call_func())
            if res.error: return res
            return res.success(call_func)

        return self.second_expression()

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_FUNC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_start,
                f"Expected $"
            ))
        res.register_advancement()
        self.advance()

        # Check if function name defined
        if not self.current_tok.matches(TT_STRING, self.current_tok.value):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_start,
                f"Expected Function name"
            ))
        var_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if not self.current_tok.matches(TT_FUNC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected $"
            ))
        res.register_advancement()
        self.advance()

        # Check if for ()
        if not self.current_tok.matches(TT_LPAREN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected ("
            ))
        res.register_advancement()
        self.advance()

        if not self.current_tok.matches(TT_STRING, self.current_tok.value) and not self.current_tok.matches(TT_RPAREN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected )"
            ))

        arg_name_toks = []
        # Check if function has argument
        if self.current_tok.matches(TT_STRING, self.current_tok.value):
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            # Check if function has more arguments
            while self.current_tok.matches(TT_COMMA):
                res.register_advancement()
                self.advance()

                if not self.current_tok.matches(TT_STRING, self.current_tok.value):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected arg name"
                    ))
                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        res.register_advancement()
        self.advance()

        # Check for function sign
        if not self.current_tok.matches(TT_FUNC_SIGN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected =>"
            ))
        res.register_advancement()
        self.advance()

        # # Check for {}
        # if not self.current_tok.matches(TT_FUNC_LBRACKET):
        #     return res.failure(InvalidSyntaxError(
        #         self.current_tok.pos_start, self.current_tok.pos_end,
        #         f"Expected " + '{'
        #     ))
        # res.register_advancement()
        # self.advance()

        if self.current_tok.matches(TT_FUNC_RBRACKET):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected command"
            ))

        # Check for commands in function
        # function_commands = []
        # while not self.current_tok.matches(TT_EOF) and not self.current_tok.matches(TT_FUNC_RBRACKET):
        #     function_commands.append(self.current_tok)
        #     res.register_advancement()
        #     self.advance()


        node_to_return = res.register(self.second_expression())

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))

    def call_func(self):
        res = ParseResult()
        name_to_call = res.register(self.atom())
        arg_nodes = []


        if not self.current_tok.matches(TT_FUNC_LBRACKET):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected " + '{'
            ))
        res.register_advancement()
        self.advance()

        # Check if function has argument
        arg_nodes.append(res.register(self.atom()))
        if res.error: return res

        # Check if function has more arguments
        while self.current_tok.matches(TT_COMMA):
            res.register_advancement()
            self.advance()

            if self.current_tok.matches(TT_FUNC_RBRACKET):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected arg"
                ))
            res.register_advancement()
            arg_nodes.append(res.register(res.register(self.atom())))
            if res.error: return res

        if not self.current_tok.matches(TT_FUNC_RBRACKET):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected " + '}'
            ))
        res.register_advancement()
        self.advance()

        return res.success(CallFuncNode(
            name_to_call,
            arg_nodes
        ))






    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.second_expression())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float"
        ))

    def first_expression(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    # expr - second expression TODO: delete
    # term - first expression TODO: delete
    def second_expression(self):
        return self.bin_op(self.first_expression, (TT_PLUS, TT_MINUS))

    ###################################

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int"
        ))
