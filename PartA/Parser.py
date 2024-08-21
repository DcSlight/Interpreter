from PartA.Error import *
from PartA.Token import *
from PartA.Nodes import *


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
        # Check if there is a definition of function
        if self.current_tok.matches(TT_FUNC):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        # Check for a function call
        if self.current_tok.matches(TT_CALL_FUNC):
            call_func = res.register(self.call_func())
            if res.error: return res
            return res.success(call_func)

        # Check for comment of just new line command
        if self.current_tok.matches(TT_COMMENT, self.current_tok.value) or self.current_tok.matches(TT_EOF):
            comment = CommentNode(self.current_tok)
            res.register_advancement()
            self.advance()
            return res.success(comment)

        # Check for printed notes
        if self.current_tok.matches(TT_PRINTED_NOTE, self.current_tok.value):
            printed_note = PrintedNoteNode(self.current_tok)
            res.register_advancement()
            self.advance()
            return res.success(printed_note)

        # Check if exit interpreter
        if self.current_tok.matches(TT_EXIT):
            exit_node = ExitNode(self.current_tok)
            res.register_advancement()
            self.advance()
            return res.success(exit_node)

        # Check for lambda
        if self.current_tok.matches(TT_LLAMBDA):
            lambda_func = res.register(self.lambda_func())
            if res.error: return res
            return res.success(lambda_func)

        return self.bin_op(self.comp_expression, (TT_AND, TT_OR))

    def comp_expression(self):
        # Check if there is no operation
        res = ParseResult()
        if self.current_tok.matches(TT_NOT):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expression())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        return self.bin_op(self.second_expression, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE))

    def lambda_func(self):
        res = ParseResult()
        res.register_advancement()
        self.advance()
        arg_name_toks = []

        # Lambda has no arguments
        if self.current_tok.matches(TT_LAMBDA_SIGN):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected arg name"
            ))

        # Check if lambda has arguments
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

            if self.current_tok.type != TT_LAMBDA_SIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ':'"
                ))
        res.register_advancement()
        res.register(self.advance())
        lambda_expr = res.register(self.command())
        if res.error: return res
        if self.current_tok.type == TT_RLAMBDA:
            res.register(self.advance())
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ']'"
            ))

        args_value_toks = []
        arg_value_temp = []

        counter = 0
        while self.current_tok.matches(TT_LPAREN):
            counter += 1
            # Check if for ( to get arg values
            if not self.current_tok.matches(TT_LPAREN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ("
                ))
            res.register_advancement()
            self.advance()

            arg_value_temp.append(res.register(self.command()))
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
                arg_value_temp.append(res.register(res.register(self.atom())))
                if res.error: return res

            if not self.current_tok.matches(TT_RPAREN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected " + ')'
                ))
            res.register_advancement()
            self.advance()
            if (counter == 1):
                args_value_toks.extend(arg_value_temp)
            else:
                args_value_toks.append(NestedFuncNode(arg_value_temp))
            arg_value_temp = []

        return res.success(LambdaNode(
            arg_name_toks,
            lambda_expr,
            args_value_toks
        ))

    def func_def(self):
        res = ParseResult()

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

        node_to_return = res.register(self.command())

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, string, '+', '-', '(' or '!'"
            ))

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))

    def call_func(self):
        res = ParseResult()
        res.register_advancement()
        self.advance()

        if not self.current_tok.matches(TT_STRING, self.current_tok.value):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected function name"
            ))
        name_to_call = res.register(self.second_expression())
        arg_nodes = []
        arg_nodes_temp = []

        counter = 0
        while self.current_tok.matches(TT_FUNC_LBRACKET):
            counter += 1
            if not self.current_tok.matches(TT_FUNC_LBRACKET):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected " + '{'
                ))
            res.register_advancement()
            self.advance()
            if not self.current_tok.matches(TT_FUNC_RBRACKET):
                # Check if function has argument
                arg_nodes_temp.append(res.register(self.second_expression()))
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
                    arg_nodes_temp.append(res.register(res.register(self.second_expression())))
                    if res.error: return res

                if not self.current_tok.matches(TT_FUNC_RBRACKET):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected " + '}'
                    ))
            res.register_advancement()
            self.advance()
            if (counter == 1):
                arg_nodes.extend(arg_nodes_temp)
            else:
                arg_nodes.append(NestedFuncNode(arg_nodes_temp))
            arg_nodes_temp = []

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
        elif tok.type == TT_BOOL:
            res.register(self.advance())
            return res.success(BoolNode(tok))
        elif tok.type == TT_STRING:
            res.register(self.advance())
            return res.success(StringNode(tok))
        elif tok.type == TT_CALL_FUNC:
            call_func = res.register(self.call_func())
            if res.error: return res
            return res.success(call_func)
        elif tok.type == TT_LLAMBDA:
            call_func = res.register(self.lambda_func())
            if res.error: return res
            return res.success(call_func)

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.comp_expression())
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
            "Expected int or float or boolean or string"
        ))

    def first_expression(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MODULO))

    def second_expression(self):
        return self.bin_op(self.first_expression, (TT_PLUS, TT_MINUS))

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in TT_INT:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        if tok.type == TT_BOOL:
            res.register_advancement()
            self.advance()
            return res.success(BoolNode(BOOLEANS[tok.value]))
        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int"
        ))
