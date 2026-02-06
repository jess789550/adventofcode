# Day 7

# Function that calculates number of splits
def splits(file):
    with open(file) as f:
        lines = [line.strip().split() for line in f]
    
    for l in lines[0]:
        start = l.index("S")
    
    # Keep track of positions
    indices = []
    indices.append(start)
    
    # Keep track of beams
    total = 0
    
    for line in lines:
        indices_to_remove = []
    
        for i in indices:
            if line[0][i] == ".":
                line[0] = line[0][:i] + "|" + line[0][i+1:]
            if line[0][i] == "^":
                line[0] = line[0][:i-1] + "|" + "^" + "|" + line[0][i+2:]
                total += 1
                indices_to_remove.append(i)

        # Write out modifications to a file (for part 2)
        with open("modified_day7_input.txt", 'a') as m:
            m.write(line[0] + "\n")
    
        for r in indices_to_remove:
            indices.remove(r)
            indices.append(r-1)
            indices.append(r+1)
            indices = list(set(indices))
    
    return total


answer = splits("day7_input.txt")
print(f"The total number of splits is {answer}")


# Total number of potential paths (ChatGPT helped)
def timelines(file):
    with open(file) as f:
        lines = [line.strip().split() for line in f]
    
    # track number of columns
    cols = len(lines[0][0])

    # track number of paths for each column
    paths = [0]*cols

    # get starting path from first row
    for i, c in enumerate(lines[0][0]):
        if c == 'S':
            paths[i] = 1
    
    # loop through other rows
    for row in lines[1:]:
        new_paths = [0]*cols  # track new paths
        for i, c in enumerate(row[0]):
            if c == '|':
                new_paths[i] += paths[i]  # retain previous number of paths in this column
            elif c == '^':
                if i-1 >= 0:  # make sure index exists
                    new_paths[i-1] += paths[i]  # if path exists then add previous paths for this column to left hand path column
                if i+1 < cols:  # make sure index exists
                    new_paths[i+1] += paths[i]  # if path exists then add previous paths for this column to right hand path column
        paths = new_paths  # update paths for each column
    
    return sum(paths)  # sum paths for each column


answer = timelines("modified_day7_input.txt")
print(f"The total number of timelines is {answer}")
