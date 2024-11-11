class Example_Codes():
    code1 = "number = 16 + 1"
    code1_1 = "number = 16 + 1\nnumber = number + 1\nreturn number"
    code2 = "number = 16 + 1\nnumber = 0 + 0"
    code3 = "number = 16 + 1\nnumber = 0 + 0\nreturn number"
    code4 = "res = 0 + 0\ntmp = res + 1\nreturn res"
    #if statements
    code5 = "number = 16 + 1\nif 17 >= 16:\n\tnumber = 0 + 0\nreturn number"
    code6 = "number = 16 + 1\nif number >= 16:\n\tnumber = 0 + 0\nreturn number"
    code7 = "number = 16 + 1\nif number < 16:\n\tnumber = 0 + 0\nreturn number"
    code8 = "number = 16 + 1\nif number < 16:\n\tnumber = 0 + 0\n\tnumber = 0 + 50\n\tnumber = 0 + 50\n\tnumber = 0 + 50\n\tnumber = 0 + 50\nreturn number"
    code8_1 = "number = 16 + 1\nif number > 16:\n\tif number == 17:\n\t\tnumber = 0 + 0\nnumber = number + 1\nreturn number" 
    code8_2 = "number = 16 + 1\nif number < 16:\n\tif number == 17:\n\t\tnumber = 0 + 0\nnumber = number + 1\nreturn number" 
    code8_3 = "number = 16 + 0\nif number >= 16:\n\tnumber = number + 1\n\tif number == 17:\n\t\tnumber = 0 + 0\nnumber = number + 1\nreturn number" 
    #loops
    code9 = "number = 5 + 0\nwhile number > 5:\n\tnumber = number - 1\nreturn number"
    code10 = "number = 0 + 0\nwhile number < 5:\n\tnumber = number + 1\nreturn number"
    code11 = "number = 5 + 0\nwhile number > 0:\n\tnumber = number - 1\nreturn number"
    #nested loops
    code12 = "number = 5 + 0\nres = 0 + 0\nwhile number > 0:\n\tnumber = number - 1\n\tnumber2 = 5 + 0\n\twhile number2 < 5:\n\t\tnumber2 = number2 + 1\n\t\tres = res + 1\nres = res + number\nreturn number"
    code13 = "number = 5 + 0\nres = 0 + 0\nwhile number > 0:\n\tnumber = number - 1\n\tnumber2 = 5 + 0\n\twhile number2 > 0:\n\t\tnumber2 = number2 - 1\n\t\tres = res + 1\nreturn res"
    code14 = "number = 0 + 0\nwhile number < 30:\n\twhile number < 10:\n\t\tnumber = number + 1\n\t\twhile number < 20:\n\t\t\tnumber = number + 1\n\tnumber = number + 1\nreturn number"

    #tests for interface___________________________________________________________________________________________________________________________
    res_test1 = "number1 = 1\nnumber2 = 1\nnumber3 = 1\nnumber4 = 1\nnumber5 = 1\nnumber6 = 1\n"
    res_test2 = "number1 = 1\nnumber2 = 1\nnumber3 = 1\nnumber4 = 1\nnumber5 = 1\nnumber6 = 10\n"
    code15 = "number = 5 + 0\nres = 0 + 0\nwhile number > 4:\n\tnumber = number - 1\n\tnumber2 = 5 + 0\n\twhile number2 > 4:\n\t\tnumber2 = number2 - 1\n\t\tres = res + 1\nreturn res"

    placeholder_t_for_code_segment = """
    \"var\" = \"par1\" \"operator\" \"par2\" -> \"par\" = const | \"var\"
    while \"condition\": -> tab and while code
    if \"condition\": -> tab and if code
    !no empty lines!
    """
    def __init__(self) :
        pass