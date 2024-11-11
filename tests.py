import unittest
import interface
import interpreter
from examlpe_codes_for_tests import Example_Codes

class Tests(unittest.TestCase):
    def test_decode_line(self):
        self.assertEqual(interpreter.decode_line("if num > 16:"), False)
        self.assertEqual(interpreter.decode_line("if 17 > 16:"), True)
        self.assertEqual(interpreter.decode_line("if num == 0:"), True)
        self.assertEqual(interpreter.decode_line("if 16 >= 16:"), True)

        self.assertEqual(interpreter.decode_line("while 16 >= 16:"), True)
        self.assertEqual(interpreter.decode_line("while 15 >= 16:"), False)
        self.assertEqual(interpreter.decode_line("while num >= 16:"), False)

        self.assertEqual(interpreter.decode_line("return 16"), "16")
        self.assertEqual(interpreter.decode_line("return string text"), "string text")

        self.assertEqual(interpreter.decode_line("number = 0 + 1"), 1)
        self.assertEqual(interpreter.decode_line("number = 10 * 1"), 10)
        self.assertEqual(interpreter.decode_line("number = value + 1"), 1)
        self.assertEqual(interpreter.decode_line("number = 10 / 0"), "Error: Division by zero")

    def test_if_and_arithmetic(self):
        examlpes = Example_Codes()
        self.assertEqual(interpreter.decode_code(examlpes.code1), 17)
        self.assertEqual(interpreter.decode_code(examlpes.code1_1), 18)
        self.assertEqual(interpreter.decode_code(examlpes.code2), 0)
        self.assertEqual(interpreter.decode_code(examlpes.code3), 0)
        self.assertEqual(interpreter.decode_code(examlpes.code4), 0)
        self.assertEqual(interpreter.decode_code(examlpes.code5), 0)
        self.assertEqual(interpreter.decode_code(examlpes.code6), 0)
        self.assertEqual(interpreter.decode_code(examlpes.code7), 17)
        self.assertEqual(interpreter.decode_code(examlpes.code8), 17)
        self.assertEqual(interpreter.decode_code(examlpes.code8_1), 1)
        self.assertEqual(interpreter.decode_code(examlpes.code8_2), 18)
        self.assertEqual(interpreter.decode_code(examlpes.code8_3), 1)

    def test_while(self):
        examlpes = Example_Codes()
        self.assertEqual(interpreter.decode_code(examlpes.code9), 5)
        self.assertEqual(interpreter.decode_code(examlpes.code10), 5)
        self.assertEqual(interpreter.decode_code(examlpes.code11), 0)
        
    def test_nested_while(self):
        examlpes = Example_Codes()
        self.assertEqual(interpreter.decode_code(examlpes.code12), 0)
        self.assertEqual(interpreter.decode_code(examlpes.code13), 25)
        self.assertEqual(interpreter.decode_code(examlpes.code14), 30)
    
    def test_update_vals(self):
        examlpes = Example_Codes()
        my_window = interface.MyWindow()
        interpreter.variables_dict["number1"] = 1
        interpreter.variables_dict["number2"] = 1
        interpreter.variables_dict["number3"] = 1
        interpreter.variables_dict["number4"] = 1
        interpreter.variables_dict["number5"] = 1
        interpreter.variables_dict["number6"] = 1
        #self.assertEqual(my_window.update_vals_fun(), examlpes.res_test1)
        interpreter.variables_dict["number6"] = 10
        #self.assertEqual(my_window.update_vals_fun(), examlpes.res_test2)
        


if __name__ == "__main__":
    unittest.main()#defaultTest="Tests.test_update_vals"