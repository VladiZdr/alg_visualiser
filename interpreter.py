from collections import defaultdict, deque

# Dictionary to store variable names and values, defaulting to 0 for undefined variables
variables_dict = defaultdict(int)
# Stack to manage loops (specifically while loops) and their positions
while_stack = deque()
# List to keep track of the order in which lines are executed
order_of_execution = []

def decode_code(code):
    """
    Main function to parse and determine the execution order for each line in the code.
    """
    variables_dict.clear()    # Clear previous variables
    while_stack.clear()       # Clear previous loops
    order_of_execution.clear() # Clear previous execution order
    
    lines = code.splitlines()  # Split the code into lines
    i = 0                      # Line index
    last_level = 0             # Track the last indentation level
    jumped_last_it = False     # To track if the last loop iteration was jumped

    while i < len(lines):
        curr_level = get_level(lines[i])  # Get indentation level of current line
        
        # If finished with the current loop, jump back to the while condition
        if not jumped_last_it and curr_level < last_level and while_stack: 
            i = while_stack.pop()
            jumped_last_it = True
            continue
        jumped_last_it = False

        order_of_execution.append(i)  # Add current line to execution order
        decode_result = execute_next(lines[i], curr_level)  # Decode the current line
        
        if decode_result == "Error: Unsupported operation":
            return decode_result

        # If the condition is false, skip to the next line outside the current block
        if not decode_result:
            i = skip_lines_after_false_condition(lines, i, curr_level)
        # If while condition is true, save index to jump back to in `while_stack`
        elif "while" in lines[i][curr_level:]:
            while_stack.append(i)
        # If called return end program
        elif "return" in lines[i][curr_level:]:
            return decode_result
        last_level = curr_level  # Update the last indentation level
        i += 1    # Move to the next line
    
    return decode_result

def execute_next(line, curr_level):
    """
    Executes a line of code after stripping indentation.
    """
    if "return" in line[curr_level:]:
        variables_dict["returned"] = variables_dict[line[7:]]
    return decode_line(line[curr_level:])

def decode_line(line):
    """
    Decodes and evaluates a single line of code.
    """
    if line[:3] == "if ":
        return eval_if(line[3:])  # Evaluate if-condition
        
    if line[:6] == "while ":
        return eval_if(line[6:])  # Evaluate while-condition
    
    if line[:6] == "return":
        # Handle return statement
        if line[7:] in variables_dict:
            return "return "+  str(variables_dict[line[7:]])
        return line
    
    if contains_assignment_and_operation(line):
        return eval_expr(line)  # Evaluate a standard expression
    return "Error: Unsupported operation"

def eval_if(expr):
    """
    Evaluates conditional expressions (if or while) and returns a boolean.
    """
    i = 0
    i = skip_spaces(expr, i)  # Skip leading spaces

    left_side = ""
    while expr[i] not in ("=", "<", ">", " "):
        left_side += expr[i]
        i += 1

    i = skip_spaces(expr, i)  # Skip spaces
    comp = expr[i]            # Get comparison operator
    i += 1

    # Check for multi-character operators like <=, >=, ==
    if expr[i] == '=':
        comp += expr[i]
        i += 1

    i = skip_spaces(expr, i)

    right_side = ""
    for ch in expr[i:]:
        if ch in (' ', ':'):
            break
        right_side += ch

    # Convert left and right expressions to integer values if possible
    if left_side[0].isdigit():
        left_side_val = int(left_side)
    else:
        left_side_val = variables_dict[left_side]
    if right_side[0].isdigit():
        right_side_val = int(right_side)
    else:
        right_side_val = variables_dict[right_side]

    # Evaluate comparison based on operator and return result
    for ch in comp:
        if (ch == '=' and left_side_val == right_side_val):
            return True
        if (ch == '<' and left_side_val < right_side_val):
            return True
        if (ch == '>' and left_side_val > right_side_val):
            return True

    return False

def eval_expr(line):
    """
    Parses and evaluates expressions, including assignment and arithmetic operations.
    """
    i = 0
    left_side = ""
    while line[i] != '=' and i < len(line):
        if line[i] != ' ':
            left_side += line[i]
        i += 1

    i += 1  # Skip '=' character

    i = skip_spaces(line, i)  # Skip spaces
    
    # Parse the first operand
    first_right = ""
    while i < len(line) and line[i] != ' ' and line[i] != '+' and line[i] != '-' and line[i] != '/' and line[i] != '*' and line[i] != '%':
        first_right += line[i]
        i += 1
    
    i = skip_spaces(line, i)
    if i >= len(line):
        return "Error: Unsupported operation"
    # Get the operator
    op = line[i]
    i += 1
    i = skip_spaces(line, i)

    # Parse the second operand
    second_right = ""
    for ch in line[i:]:
        if ch == ' ':
            break
        second_right += ch
        i += 1

    # Convert operand strings to values
    first_right_val = int(first_right) if first_right.isdigit() else variables_dict[first_right]
    second_right_val = int(second_right) if second_right.isdigit() else variables_dict[second_right]
    
    # Perform the operation and store the result
    return perform_op(left_side, first_right_val, second_right_val, op)

def perform_op(left_side, first_right_val, second_right_val, op):
    """
    Executes arithmetic operations and stores the result in `variables_dict`.
    """
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
            return "Error: Unsupported operation"
    elif op == '%':
        if second_right_val != 0:
            variables_dict[left_side] = first_right_val % second_right_val
        else:
            return "Error: Unsupported operation"
    else:
        return "Error: Unsupported operation"

    return variables_dict[left_side]

def skip_spaces(line, i):
    """
    Skips spaces in the line starting from index `i`.
    """
    while i < len(line) and line[i] == ' ':
        i += 1
    return i

def skip_lines_after_false_condition(lines, i, curr_level):
    """
    Skips lines until a line with an indentation level less than or equal to `curr_level` is found.
    """
    i += 1  # Move to the next line
    while i < len(lines):
        tmp_level = get_level(lines[i])

        # Stop if we reach a line with the same or less indentation
        if tmp_level <= curr_level:
            break

        i += 1

    return i - 1  # Return the index of the last skipped line

def get_level(line):
    """
    Determines the indentation level (number of tabs) for a given line.
    """
    curr_level = 0
    while curr_level < len(line) and line[curr_level] == '\t':
        curr_level += 1
    return curr_level

def contains_assignment_and_operation(line):
    # Check for '=' in the line and at least one arithmetic operation
    return '=' in line and any(op in line for op in ['+', '-', '*', '/'])
