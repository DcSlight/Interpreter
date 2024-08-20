import unittest
import basic
from FunctionalProgramming.function import Function


class MyTestCase(unittest.TestCase):
    def test_plus(self):
        self.assertEqual(basic.run('<testing>', "2+4")[0].value, 6)

    def test_minus(self):
        self.assertEqual(basic.run('<testing>', "5-2")[0].value, 3)

    def test_mul(self):
        self.assertEqual(basic.run('<testing>', "6*10")[0].value, 60)

    def test_div(self):
        self.assertEqual(basic.run('<testing>', "8/4")[0].value, 2)
        self.assertEqual(basic.run('<testing>', "8/5")[0].value, 1)

    def test_div_zero(self):
        self.assertEqual(basic.run('<testing>', "8/0")[0], None)  # Checking for None in the value result
        self.assertEqual(basic.run('<testing>', "8/0")[1].details, "Division by zero")  # Checking for error

    def test_modulo(self):
        self.assertEqual(basic.run('<testing>', "8%5")[0].value, 3)

    def test_binOpExpr(self):
        self.assertEqual(basic.run('<testing>', "18-2*3")[0].value, 12)
        self.assertEqual(basic.run('<testing>', "5/2+16-3")[0].value, 15)
        self.assertEqual(basic.run('<testing>', "18-2*5-7")[0].value, 1)
        self.assertEqual(basic.run('<testing>', "16/2/4+9*10")[0].value, 92)

    def test_negatives(self):
        self.assertEqual(basic.run('<testing>', "-1")[0].value, -1)
        self.assertEqual(basic.run('<testing>', "7-10")[0].value, -3)
        self.assertEqual(basic.run('<testing>', "-15/3")[0].value, -5)
        self.assertEqual(basic.run('<testing>', "10--4")[0].value, 14)

    def test_bool(self):
        self.assertEqual(basic.run('<testing>', "True")[0].value, True)
        self.assertEqual(basic.run('<testing>', "False")[0].value, False)

    def test_comparison(self):
        self.assertEqual(basic.run('<testing>', "5<3")[0].value, False)
        self.assertEqual(basic.run('<testing>', "3<=3")[0].value, True)
        self.assertEqual(basic.run('<testing>', "3>3")[0].value, False)
        self.assertEqual(basic.run('<testing>', "5>=3")[0].value, True)
        self.assertEqual(basic.run('<testing>', "5==3")[0].value, False)
        self.assertEqual(basic.run('<testing>', "5!=3")[0].value, True)

    def test_bool_operations(self):
        self.assertEqual(basic.run('<testing>', "5 < 10 && 10 < 20")[0].value, True)
        self.assertEqual(basic.run('<testing>', "5 > 10 || 10 < 20")[0].value, True)
        self.assertEqual(basic.run('<testing>', "!True")[0].value, False)

    def test_func_def(self):
        self.assertEqual(str(basic.run('<testing>', "$boolOperations$ (x,y) => (x > 0) && (y < 10)")[0]),
                         str(Function("boolOperations", None, None)))
        self.assertEqual(str(basic.run('<testing>', "$functionNoArgs$ () => 20+50")[0]),
                         str(Function("functionNoArgs", None, None)))

    def test_call_func(self):
        self.assertEqual(str(basic.run('<testing>', "$factorial$ (n) => (n==0) || (n*@factorial{n-1})")[0]),
                         str(Function("factorial", None, None)))
        self.assertEqual(basic.run('<testing>', "@factorial{5}")[0].value, 120)

    def test_lambda(self):
        self.assertEqual(basic.run('<testing>', "[x:x+5](10)")[0].value, 15)
        self.assertEqual(basic.run('<testing>', "[x:[y:x+y](2)](10)")[0].value, 12)

    def test_comment(self):
        self.assertEqual(basic.run('<testing>', "#comment")[0], "")

    def test_printed_note(self):
        self.assertEqual(basic.run('<testing>', "##printed note")[0], "[94mprinted note[0m")  # colorful note

    def test_errors(self):
        self.assertEqual(basic.run('<testing>', "2+")[1].details, "Expected int or float or boolean or string")
        self.assertEqual(basic.run('<testing>', "(3+5")[1].details, "Expected ')'")
        self.assertEqual(basic.run('<testing>', "$function () => 4+5")[1].details, "Expected $")
        self.assertEqual(basic.run('<testing>', "@function{}")[1].details, "'function' is not defined")
        self.assertEqual(basic.run('<testing>', "<sign not in language>")[1].details,
                         "Expected int or float or boolean or string")  # TODO: give a better error msg
        self.assertEqual(basic.run('<testing>', "a+2")[1].details,
                         "'a' is not defined")
        self.assertEqual(basic.run('<testing>', "$secFunction$ () => 4+")[1].details,
                         "Expected int or float or boolean or string")


if __name__ == '__main__':
    unittest.main()
