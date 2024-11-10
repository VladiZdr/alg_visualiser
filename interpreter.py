from collections import defaultdict,deque

variables_dict = defaultdict(int)
while_stack = deque()

def decode_code(code):
    lines = code.splitlines()
    i = 0
    last_level = 0
    jumped_last_it = False
    while i < len(lines):
        curr_level = 0
        while lines[i][curr_level] == '\t':
            curr_level+=1
        
        #if finished with curr while code lines jump back to while condition
        if not jumped_last_it and curr_level < last_level and  while_stack: 
            i = while_stack.pop()
            jumped_last_it = True
            continue
        jumped_last_it = False
        decode_result = decode_line(lines[i][curr_level:])

        #if a condition is not satisfied find next line to execute
        if not decode_result:
            i = skip_lines_after_false_condition(lines, i, curr_level)
        #if True and while condition save i for jump
        elif "while" in lines[i][curr_level:]:
            while_stack.append(i)

        last_level = curr_level
        i += 1    
        

    return decode_result


def decode_line(line):
    if line[:3] == "if ":
        #print("if")
        return eval_if(line[3:])
    
    if line[:6] == "while ":
        #print("while")
        #print(eval_if(line[6:]))
        return eval_if(line[6:])
    
    if line[:7] == "return ":
        if line[7:] in variables_dict:
            #print(f"end {variables_dict[line[7:]]}")
            return variables_dict[line[7:]]
        #print(f"end {line[7:]}")
        return line[7:]
    
    #eval expr
    return  eval_expr(line)
    

def eval_if(expr):
    i = 0
    i = skip_spaces(expr,i)
    left_side = ""
    while expr[i] != "=" and expr[i] != '<' and expr[i] != '>' and expr[i] != ' ':
        left_side += expr[i]
        i+=1

    i = skip_spaces(expr,i)
    comp = expr[i]
    i+=1
    if expr[i] == '=':
        comp += expr[i]
        i+=1

    i = skip_spaces(expr,i)

    right_side = ""
    for ch in expr[i:]:
        if ch == ' ' or ch == ':':
            break
        right_side += ch

    if left_side[0] >= '0' and left_side <= '9':
        left_side_val = int(left_side)
    else:
        left_side_val = variables_dict[left_side]
    if right_side[0] >= '0' and right_side <= '9':
        right_side_val = int(right_side)
    else:
        right_side_val = variables_dict[right_side]

    for ch in comp:
        if (ch == '=' and left_side_val == right_side_val):
            return True
        if (ch == '<' and left_side_val < right_side_val):
            return True
        if (ch == '>' and left_side_val > right_side_val):
            return True
        
    return False



def eval_expr(line):
    i = 0
    left_side = ""
    while line[i] != '=' :
        if(line[i] != ' '):
            left_side += line[i]
        i+=1
    
    #skip '='
    i+=1

    #skip empty spaces
    i = skip_spaces(line,i)

    # variable1
    first_right = ""
    first_right_val = 0
    while line[i] != ' ':
        first_right += line[i]
        i+=1
    
    i = skip_spaces(line,i)

    #get operator
    op = line[i]
    i+=1
    i = skip_spaces(line,i)

    # variable2
    second_right = ""
    second_right_val = 0
    for ch in line[i:]:
        if ch == ' ':
            break
        second_right += ch
        i+=1

    #string -> int
    if first_right[0] <= '9' and first_right[0] >= '0':
        first_right_val = int(first_right)
    else:
        first_right_val = variables_dict[first_right]

    if second_right[0] <= '9' and second_right[0] >= '0':
        second_right_val = int(second_right)
    else:
        second_right_val = variables_dict[second_right]
    
    #perform operation and store result
    return perform_op(left_side,first_right_val,second_right_val,op)

def perform_op(left_side,first_right_val,second_right_val,op):
    if op == '+':
        variables_dict[left_side] = first_right_val + second_right_val
    elif op == '-':
        variables_dict[left_side] = first_right_val - second_right_val
    elif op == '*':
        variables_dict[left_side] = first_right_val * second_right_val
    elif op == '/':
        if second_right_val != 0:
            variables_dict[left_side] = first_right_val / second_right_val
        else:
            return "Error: Division by zero"
    elif op == '%':
        if second_right_val != 0:
            variables_dict[left_side] = first_right_val % second_right_val
        else:
            return ("Error: Modulus by zero")
    else:
        return ("Error: Unsupported operation")

    return  variables_dict[left_side]

def skip_spaces(line,i):
    while line[i] == ' ':
        i+=1
    return i

def skip_lines_after_false_condition(lines, i, curr_level):
    # Start with the next line
    i += 1  
    while i < len(lines):
        tmp_level = 0
        
        # Count tabs at the start of the current line to determine its level
        while tmp_level < len(lines[i]) and lines[i][tmp_level] == '\t':
            tmp_level += 1

        # If the level is less than or equal to `curr_level`, stop
        if tmp_level <= curr_level:
            break

        # Move to the next line
        i += 1

    # Return the index of the last line before the level was less than or equal to `curr_level`
    return i - 1