from PartA.interpreter import Interpreter


class Function:
    def __init__(self, name, args, body):
        self.name = name or "<anonymous>"
        self.args = args
        self.body = body
        # TODO: maybe move to Value class
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def execute(self, args):
        from PartA.interpreter import RTResult, Context, SymbolTable, RTError
        res = RTResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.args):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.args)} too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(self.args):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(self.args) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))

        for i in range(len(args)):
            arg_name = self.args[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.body, new_context))
        if res.error: return res
        return res.success(value)

    # def check_scope(self):
    #     print(self.name, self.args, self.body)
    #     # Extract all possible tokens from the context
    #     tokens = re.findall(r'\b\w+\b', self.body)
    #     print(tokens)
    #     # Iterate over each token
    #     for token in tokens:
    #         # Check if the token is not an argument and is not a valid keyword
    #         if token not in self.args and token not in KEYWORDS and token != self.name:
    #             # If the token is not a function call, raise an error
    #             raise ValueError(f"Variable '{token}' in context is not a valid argument or function.")

    def copy(self):
        copy = Function(self.name, self.args, self.body)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"


# Example usage
# function = Function(name="something", args=["a", "b"], context="a * something(a-1)")
# function.context_to_tokens()  # Should pass without issues

# function_with_error = Function(name="something_else", args=["a", "b"], context="a * c")
# function_with_error.context_to_tokens()  # Should raise ValueError: Variable 'c' in context is not a valid argument or function.


class Lambda:
    def __init__(self, args, expr):
        self.args = args
        self.expr = expr
        # self.values = values
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def execute(self, args):
        from PartA.interpreter import RTResult, Context, SymbolTable, RTError
        res = RTResult()
        interpreter = Interpreter()
        new_context = Context(self.__repr__(), self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.args):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.args)} too many args passed into '{self.__repr__()}'",
                self.context
            ))

        if len(args) < len(self.args):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(self.args) - len(args)} too few args passed into '{self.__repr__()}'",
                self.context
            ))

        for i in range(len(args)):
            arg_name = self.args[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.expr, new_context))
        if res.error: return res
        return res.success(value)

    def copy(self):
        copy = Lambda(self.args, self.expr)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<lambda>"
