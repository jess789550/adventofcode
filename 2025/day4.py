# Day 4

# Find out how many toilets rolls have less than 4 toilet rolls next to them
def less_than_four(file):
    # open file and read as list of lists
    with open(file) as f:
        grid = [list(line.strip()) for line in f]
    
    # track number of toilet rolls
    count = 0
    
    # Loop through matrix
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            adjacent = 0  # count number of adjacent rolls
                
            if grid[i][j] == '@': # selected roll
                if i-1 > -1 and j -1 > -1:
                    if grid[i-1][j-1] == '@':  # top left roll
                        adjacent += 1
                
                if i-1 > -1:
                    if grid[i-1][j] == '@':  # top centre roll
                        adjacent += 1
                
                if i-1 > -1 and j+1 < len(grid[i]):
                    if grid[i-1][j+1] == '@':  # top right roll
                        adjacent += 1
                
                if j-1 > -1:
                    if grid[i][j-1] == '@':  # left roll
                        adjacent += 1
               
                if j+1 < len(grid[i]):
                    if grid[i][j+1] == '@':  # right roll
                        adjacent += 1
                
                if i+1 < len(grid) and j-1 > -1:
                    if grid[i+1][j-1] == '@':  # bottom left roll
                        adjacent += 1
                
                if i+1 < len(grid):
                    if grid[i+1][j] == '@':  # bottom centre roll
                        adjacent += 1
                
                if i+1 < len(grid) and j+1 < len(grid[i]):
                    if grid[i+1][j+1] == '@':  # bottom right roll
                        adjacent += 1
            
                if adjacent < 4:  # see if less than 4 rolls are adjacent
                    count += 1
    
    return count


answer = less_than_four("day4_input.txt")
print(f"The number of accessible toilet rolls is {answer}")


# Find out how many toilets rolls have less than 4 toilet rolls next to them; iteratively remove rolls
def remove_rolls(grid, count=0):
    # Loop through matrix
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            adjacent = 0  # count number of adjacent rolls
                
            if grid[i][j] == '@': # selected roll
                if i-1 > -1 and j -1 > -1:
                    if grid[i-1][j-1] == '@':  # top left roll
                        adjacent += 1
                
                if i-1 > -1:
                    if grid[i-1][j] == '@':  # top centre roll
                        adjacent += 1
                
                if i-1 > -1 and j+1 < len(grid[i]):
                    if grid[i-1][j+1] == '@':  # top right roll
                        adjacent += 1
                
                if j-1 > -1:
                    if grid[i][j-1] == '@':  # left roll
                        adjacent += 1
               
                if j+1 < len(grid[i]):
                    if grid[i][j+1] == '@':  # right roll
                        adjacent += 1
                
                if i+1 < len(grid) and j-1 > -1:
                    if grid[i+1][j-1] == '@':  # bottom left roll
                        adjacent += 1
                
                if i+1 < len(grid):
                    if grid[i+1][j] == '@':  # bottom centre roll
                        adjacent += 1
                
                if i+1 < len(grid) and j+1 < len(grid[i]):
                    if grid[i+1][j+1] == '@':  # bottom right roll
                        adjacent += 1
            
                if adjacent < 4:  # see if less than 4 rolls are adjacent
                    count += 1
                    grid[i][j] = '.'
    
    return count


# open file and read as list of lists
with open("day4_input.txt") as f:
    grid = [list(line.strip()) for line in f]

previous_answer = remove_rolls(grid)
answer = remove_rolls(grid, previous_answer)

while previous_answer != answer:
    previous_answer = answer
    answer = remove_rolls(grid, answer)

print(f"The number of accessible toilet rolls is {answer}")
