# Day 5

# Count the number of valid IDs in set ranges
def valid_ids(file):
    # open file and read
    with open(file) as f:
        lines = f.readlines()
    
    # find blank line that split ranges and IDs
    blank_line = lines.index("\n") 
    
    # create empty list to store ranges
    ranges = []
    
    for line in lines[:blank_line]:
        ranges.append(line.strip())
    
    # create empty list to store ids
    ids = []
    
    for line in lines[blank_line+1:]:
        ids.append(line.strip())
    
    # keep track of count
    count = 0
    
    # loop through ranges and ids
    for i in ids:
        i = int(i)

        for r in ranges:
            r_split = r.split("-")
            start = int(r_split[0])
            end = int(r_split[1])
            
            if i >= start and i <= end:
                count += 1
                break
    
    return count


answer = valid_ids("day5_input.txt")
print(f"The number of valid IDs is {answer}")


# All fresh IDs possible (takes too long)
def all_fresh_ids(file):
    # open file and read
    with open(file) as f:
        lines = f.readlines()
    
    # find blank line that split ranges and IDs
    blank_line = lines.index("\n") 
    
    # create empty list to store ranges
    ranges = []
    
    for line in lines[:blank_line]:
        ranges.append(line.strip())

    # keep track of possible IDs
    fresh_ids = []

    # loop through ranges and ids
    for r in ranges:
        r_split = r.split("-")
        start = int(r_split[0])
        end = int(r_split[1]) + 1
        for i in range(start, end):
            fresh_ids.append(i)
        
    count = len(set(fresh_ids))

    return count


# ChatGPT answer
def all_fresh_ids_2(file):
    with open(file) as f:
        lines = [line.strip() for line in f]  # remove whitespace when parsing text file
    
    blank_line = lines.index("")
    
    # Parse ranges
    ranges = []
    for line in lines[:blank_line]:
        start, end = map(int, line.split("-"))  # maps first number before "-" to start variable and second number to end variable
        ranges.append((start, end))  # adds tuple to list
    
    # Sort ranges by start
    ranges.sort()
    
    merged_count = 0
    current_start, current_end = ranges[0]  # track start and end
    
    for start, end in ranges[1:]:  # loop over ranges
        if start <= current_end + 1:
            # Overlapping or adjacent
            current_end = max(current_end, end) # extend range if overlapping
        else:
            # Finish previous range
            merged_count += current_end - current_start + 1
            current_start, current_end = start, end  # overwrite current_start and current_end
    
    # Add final range
    merged_count += current_end - current_start + 1
    
    return merged_count


answer = all_fresh_ids_2("day5_input.txt")
print(f"The number of valid IDs is {answer}")
