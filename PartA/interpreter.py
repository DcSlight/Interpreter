from PartA.Token import *
from PartA.Error import *
from abc import abstractmethod
from PartA.Nodes import NestedFuncNode


#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


#######################################
# VALUES
#######################################

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )

    @abstractmethod
    def anded_by(self, other):
        pass

    @abstractmethod
    def ored_by(self, other):
        pass


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(int(self.value / other.value)).set_context(self.context), None

    def modulo(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value % other.value).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(True if self.value == 0 else False).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


class Bool(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(int(self.value / other.value)).set_context(self.context), None

    def modulo(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Number(self.value % other.value).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Bool) or isinstance(other, Bool):
            return Bool((self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number) or isinstance(other, Bool):
            return Bool((self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Bool) or isinstance(other, Number):
            # TODO: check for (1 > 3) && (1 < 2)
            return Bool((self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Bool) or isinstance(other, Number):
            # TODO: check for (1 > 3) && (1 < 2)
            return Bool((self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        error, result = None, None
        left = res.register(self.visit(node.left_node, context))
        if node.op_tok.type == TT_OR and left.value:
            return res.success(left.set_pos(node.pos_start, node.pos_end))

        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MODULO:
            result, error = left.modulo(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_AND:
            result, error = left.anded_by(right)
        elif node.op_tok.type == TT_OR:
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.type == TT_NOT:
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        from PartA.function import Function
        func_value = Function(func_name, arg_names, body_node).set_context(context).set_pos(node.pos_start,
                                                                                            node.pos_end)

        if context.symbol_table.get(func_name):
            return res.failure(FunctionNameDefinedError(
                func_value.pos_start, func_value.pos_end,
                f"{func_name} already defined"
            ))

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallFuncNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        return_value = None
        flag = False
        for arg_node in node.arg_nodes:
            if isinstance(arg_node, NestedFuncNode):

                new_args = res.register(self.visit(arg_node, context))
                if not flag:
                    return_value = res.register(value_to_call.execute(args))
                else:
                    return_value = res.register(value_to_call.execute(new_args))
                # TODO: return value is not function raise error
                flag = True

                from PartA.function import Function
                if isinstance(return_value, Function):
                    return_value = res.register(return_value.execute(new_args))
                    value_to_call = return_value
                    args = new_args
            else:
                args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        if not flag:
            return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)

    def visit_LambdaNode(self, node, context):
        res = RTResult()

        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        lambda_expr = node.lambda_expr
        # arg_values = [arg_value for arg_value in node.args_value_toks]
        from PartA.function import Lambda
        func_value = Lambda(arg_names, lambda_expr).set_context(context).set_pos(node.pos_start,
                                                                                 node.pos_end)

        arg_values = []

        return_value = None
        flag = False
        for arg_value in node.args_value_toks:
            if isinstance(arg_value, NestedFuncNode):

                new_args = res.register(self.visit(arg_value, context))
                if not flag:
                    return_value = res.register(func_value.execute(arg_values))
                else:
                    return_value = res.register(return_value.execute(new_args))
                # TODO: return value is not function raise error
                flag = True

                from PartA.function import Function
                if isinstance(return_value, Function):
                    return_value = res.register(return_value.execute(new_args))
                    arg_values = new_args
            else:
                arg_values.append(res.register(self.visit(arg_value, context)))
            if res.error: return res

        if not flag:
            return_value = res.register(func_value.execute(arg_values))
        if res.error: return res
        return res.success(return_value)

    def visit_StringNode(self, node, context):
        res = RTResult()
        var_name = node.tok
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_BoolNode(self, node, context):
        res = RTResult()
        var_name = node.tok
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_CommentNode(self, node, context):
        res = RTResult()
        return res.success("")

    def visit_PrintedNoteNode(self, node, context):
        res = RTResult()
        return res.success(node.tok)

    def visit_ExitNode(self, node, context):
        res = RTResult()
        return res.success(node.tok)

    def visit_NestedFuncNode(self, node, context):
        res = RTResult()
        args = []
        for arg_node in node.arg_values:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return res.success(args)

