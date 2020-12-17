def do_math(expression: str)->int:
    number = ''
    valid_symbols = '-+()*'
    #invalid symbol check
    for eachletter in expression:
        if eachletter.isdigit() or eachletter in valid_symbols:
            continue
        else:
            return None
    #emptystring check
    if len(expression) == 0:
        return None
    #Integer literal
    if '(' not in expression and ')' not in expression and '+' not in expression and '-' not in expression and '*' not in expression:
        return int(expression)
    output_stack = []
    operator_stack = []
    operators = '-+*'
    for eachoperator in operators:
        for eachoperator2 in operators:
            if (eachoperator+eachoperator2) in expression:
                return None
    for eachletter in expression:
        if eachletter.isdigit():
            number += eachletter
            #output_stack.append(eachletter)
        else:
            output_stack.append(number)
            number = ''
            if eachletter in operators:
                while len(operator_stack) > 0 and pop_list(operator_stack) != '(' and (operators.index(pop_list(operator_stack)) > operators.index(eachletter) or (operators.index(pop_list(operator_stack)) == operators.index(eachletter) and expression.index(pop_list(operator_stack)) < expression.index(eachletter))):
                    output_stack.append(pop_list(operator_stack))
                    del operator_stack[-1]
                operator_stack.append(eachletter)
            elif eachletter == '(':
                operator_stack.append(eachletter)
            elif eachletter == ')':
                try:
                    while pop_list(operator_stack) != '(':
                        output_stack.append(pop_list(operator_stack))
                        del operator_stack[-1]
                    del operator_stack[-1]
                except:
                    return None
    if len(number) > 0:
        output_stack.append(number)
    if len(operator_stack) > 0:
        while len(operator_stack) > 0:
            if pop_list(operator_stack) == '(':
                return None
            output_stack.append(pop_list(operator_stack))
            del operator_stack[-1]
        return convert_infix(output_stack)
    else:
        return convert_infix(output_stack)
        
    
    
    
def pop_list(alist):
    return alist[-1]
    
    
def convert_infix(output_stack:str)->int:
    while(len(output_stack) > 1):
        for i in range(len(output_stack)):
            if len(output_stack[:i]) >= 2:
                if output_stack[i] == '+':
                    first_number = output_stack[i-2]
                    second_number = output_stack[i-1]
                    output_stack[i-2] = ''
                    output_stack[i-1] = ''
                    output_stack[i] = int(second_number) + int(first_number)
                    output_stack = [x for x in output_stack if x != '']
                    break
                    #output_stack.insert(i-1,second_number + first_number)
                elif output_stack[i] == '-':
                    first_number = output_stack[i-2]
                    second_number = output_stack[i-1]
                    output_stack[i-2] = ''
                    output_stack[i-1] = ''
                    output_stack[i] = int(first_number) - int(second_number)
                    output_stack = [x for x in output_stack if x != '']
                    break
                    #output_stack.insert(i-1,second_number - first_number)
                elif output_stack[i] == '*':
                    first_number = output_stack[i-2]
                    second_number = output_stack[i-1]
                    output_stack[i-2] = ''
                    output_stack[i-1] = ''
                    output_stack[i] = int(second_number) * int(first_number)
                    output_stack = [x for x in output_stack if x != '']
                    break
    return output_stack[0] if len(output_stack) == 1 else None                      
