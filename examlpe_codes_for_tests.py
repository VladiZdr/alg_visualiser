class Example_Codes():
    code1 = "number = 16 + 1"
    code2 = "number = 16 + 1\nnumber = 0 + 0"
    code3 = "number = 16 + 1\nnumber = 0 + 0\nreturn number"
    code4 = "res = 0 + 0\ntmp = res + 1\nreturn res"

    code5 = "number = 16 + 1\nif 17 >= 16:\n\tnumber = 0 + 0\nreturn number"
    code6 = "number = 16 + 1\nif number >= 16:\n\tnumber = 0 + 0\nreturn number"
    code7 = "number = 16 + 1\nif number < 16:\n\tnumber = 0 + 0\nreturn number"
    code8 = "number = 16 + 1\nif number < 16:\n\tnumber = 0 + 0\n\tnumber = 0 + 50\n\tnumber = 0 + 50\n\tnumber = 0 + 50\n\tnumber = 0 + 50\nreturn number"

    code9 = "number = 5 + 0\nwhile number > 5:\n\tnumber = number - 1\nreturn number"
    code10 = "number = 0 + 0\nwhile number < 5:\n\tnumber = number + 1\nreturn number"
    code11 = "number = 5 + 0\nwhile number > 0:\n\tnumber = number - 1\nreturn number"
    code12 = "number = 5 + 0\nres = 0 + 0\nwhile number > 0:\n\tnumber = number - 1\n\tnumber2 = 5 + 0\n\twhile number2 < 5:\n\t\tnumber2 = number2 + 1\n\t\tres = res + 1\nreturn res"
    code13 = "number = 5 + 0\nres = 0 + 0\nwhile number > 0:\n\tnumber = number - 1\n\tnumber2 = 0 + 0\n\twhile number2 < 5:\n\t\tnumber2 = number2 + 1\n\t\tres = res + 1\nreturn number2"
    code14 = "number = 5 + 0\nres = 0 + 0\nwhile number > 0:\n\tnumber = number - 1\n\tres = 5 + res\nreturn res"

    def __init__(self) :
        pass