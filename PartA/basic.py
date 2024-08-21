from PartA.Lexer import Lexer
from PartA.Parser import Parser
from PartA.interpreter import Interpreter, Number
from PartA.interpreter import Context
from PartA.Token import SymbolTable

global_symbol_table = SymbolTable()
# global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("False", Number(0))
global_symbol_table.set("True", Number(1))

#######################################
# RUN
#######################################

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error #TODO: change

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
