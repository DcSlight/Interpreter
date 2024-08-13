class Function:
    def __init__(self, name, args , context):
        self.name = name
        self.args = args
        self.context = context

    def context_to_tokens(self):
        self.check_scope()

