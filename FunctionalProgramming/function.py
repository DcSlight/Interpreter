import re

class Function:
    def __init__(self, name, args, context):
        self.name = name
        self.args = args
        self.context = context

    def check_scope(self):
        # Extract all possible tokens from the context
        tokens = re.findall(r'\b\w+\b', self.context)
        print(tokens)
        # Iterate over each token
        for token in tokens:
            # Check if the token is not an argument and is not a valid keyword
            if token not in self.args and not self.is_keyword(token) and token != self.name:
                # If the token is not a function call, raise an error
                raise ValueError(f"Variable '{token}' in context is not a valid argument or function.")

    def is_keyword(self, token):
        # This checks for Python keywords and common operators
        return token in [
            "+", "-", "*", "/", "and", "or", "not", "if", "else",
            "for", "while", "in", "return", "=", "==", "<", ">", "<=", ">=", "(", ")", ","
        ]

    def context_to_tokens(self):
        self.check_scope()
        # You can further tokenize or process the context here

# Example usage
#function = Function(name="something", args=["a", "b"], context="a * something(a-1)")
#function.context_to_tokens()  # Should pass without issues

#function_with_error = Function(name="something_else", args=["a", "b"], context="a * c")
#function_with_error.context_to_tokens()  # Should raise ValueError: Variable 'c' in context is not a valid argument or function.
