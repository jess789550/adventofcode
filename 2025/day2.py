# Day 2

# Part 1: find invalid IDs that have repeat digits if you split it in half
def invalid(input):
    # Read file
    with open(input) as f:
        lines = f.readlines()
    
    # Parse list removing whitespace and splitting ranges
    id_list = lines[0].strip().split(",")
    
    # Set count to 0
    count = 0
    
    # Loop through ranges
    for item in id_list:
        start = int(item.split("-")[0])
        end = int(item.split("-")[1])
        for id in range(start, end+1):
            length = len(str(id))
            if str(id)[0:int(length/2)] == str(id)[int(length/2):length]:
                count += id
    
    return count


answer = invalid("day2_input.txt")
print(f"The sum of invalid IDs is {answer}.")


# Part 2: digits can repeat more than twice
def invalid_2(input):
    # Read file
    with open(input) as f:
        lines = f.readlines()
    
    # Parse list removing whitespace and splitting ranges
    id_list = lines[0].strip().split(",")
    
    # Set count to 0
    count = 0
    
    # Loop through ranges
    for item in id_list:
        start = int(item.split("-")[0])
        end = int(item.split("-")[1])
        for id in range(start, end+1):
            length = len(str(id))
            for k in range(1, length):
                chunks = [str(id)[i:i+k] for i in range(0, len(str(id)), k)]
                if len(set(chunks)) == 1:
                    print(id)
                    print(set(chunks))
                    count += id
                    break
    
    return count


answer = invalid_2("day2_input.txt")
print(f"The sum of invalid IDs is {answer}.")
