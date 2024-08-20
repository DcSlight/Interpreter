import basic
import sys
from Token import *

INTERACTIVE_MODE = True

# Reading from file, if there is a valid filename that exists.
if len(sys.argv) == 2:
    INTERACTIVE_MODE = False
    try:
        if not sys.argv[1].endswith('.lambda'):
            raise Exception(f'File Name Error: file {sys.argv[1]} not ends with .lambda')
        with open(sys.argv[1]) as file:
            text_file = file.read().splitlines()

        for line in text_file:
            text = line
            result, error = basic.run(file, text)

            if error:
                print(error.as_string())
            else:
                print(result)

    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(e.__repr__())

# Interactive interpreter mode.
while INTERACTIVE_MODE:
    text = input('----> ')
    result, error = basic.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result == TT_EXIT:
        break
    elif result: print(result)
