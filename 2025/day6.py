# Day 6

# Function that adds or multiplies numbers vertically
def vertical_math(file):
    with open(file) as f:
        lines = [line.strip().split() for line in f]
    
    # operators
    operators = lines[-1]
    
    # remove operators from lines
    lines = lines[:-1]
    
    # track total
    total = 0

    # loop through each column
    for col in range(len(lines[0])):
        col_total = int(lines[0][col])

        for row in range(1, len(lines)):
            if operators[col] == "+":
                col_total += int(lines[row][col])
            else:
                col_total *= int(lines[row][col])
        
        total += col_total
    
    return total

answer = vertical_math("day6_input.txt")
print(f"The total is {answer}")


# Function that adds or multiplies numbers vertically
def vertical_math_2(file):
    with open(file) as f:
        lines = [line.strip("\n") for line in f]
    
    # operators
    operators = lines[-1]
    indices = []
    for operator in list(enumerate(operators)):
        if operator[1] != ' ':
            indices.append(operator[0])
    
    indices.append(len(lines[-1])) # Need to add extra index for the loop later so that last calculation is carried out

    # remove operators from lines
    lines = lines[:-1]
    
    # track total
    total = 0
    
    # Rewrite lines with correct numbers
    newlines = []
    
    for col in range(len(lines[0])):
        newnum = ""
        for row in lines:
            newnum += row[col]
        newlines.append(''.join(newnum.split()))
    
    # Loop through operators
    for i in range(0,len(indices)-1):
        start = indices[i]
        end = indices[i+1]
        operator = operators[indices[i]]
        small_total = int(newlines[start])
        
        # Loop through numbers
        for j in range(start+1, end):
            if operator == '+' and newlines[j] != '':
                small_total += int(newlines[j])
            elif operator == '*' and newlines[j] != '':
                small_total *= int(newlines[j])
            else:
                continue
        
        total += small_total
    
    return total

answer = vertical_math_2("day6_input.txt")
print(f"The total is {answer}")