#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class StringNode:
    def __init__(self, tok):
        self.tok = tok.value
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BoolNode:
    def __init__(self, tok):
        self.tok = tok.value
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class ExitNode:
    def __init__(self, tok):
        self.tok = tok.type
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class CommentNode:
    def __init__(self, tok):
        self.tok = tok.value
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class PrintedNoteNode:
    BRIGHT_BLUE = '\033[94m'
    RESET = '\033[0m'

    def __init__(self, tok):
        self.tok = self.BRIGHT_BLUE + tok.value + self.RESET
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


class CallFuncNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        if self.node_to_call:
            self.pos_start = self.node_to_call.pos_start
        else:
            self.pos_start = 0

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        elif self.node_to_call:
            self.pos_end = self.node_to_call.pos_end
        else:
            self.pos_end = 0


class LambdaNode:
    def __init__(self, arg_name_toks, lambda_expr, args_value_toks):
        self.arg_name_toks = arg_name_toks
        self.lambda_expr = lambda_expr
        self.args_value_toks = args_value_toks

        self.pos_start = self.arg_name_toks[0].pos_start

        if len(self.args_value_toks) > 0:
            self.pos_end = self.args_value_toks[len(self.args_value_toks) - 1].pos_end
        else:
            self.pos_end = self.args_value_toks.pos_end


class NestedFuncNode:
    def __init__(self, arg_values):
        self.arg_values = arg_values

        if self.arg_values:
            self.pos_start = self.arg_values[0].pos_start
        else:
            self.pos_start = 0

        if len(self.arg_values) > 0:
            self.pos_end = self.arg_values[len(self.arg_values) - 1].pos_end
        elif self.arg_values:
            self.pos_end = self.arg_values.pos_end
        else:
            self.pos_end = 0
