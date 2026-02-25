# Day 11

# Function that finds the number of paths from "you" to "out"
def you_out(file, start="you", target="out"):
    """
    ChatGPT uses depth-first search
    """
    graph = dict()
    with open(file) as f:
        lines = f.readlines()
    
    for line in lines:
        key = line.split(":")[0]
        values = line.split()[1:]
        graph[key] = values
    
    def dfs(node, visited):  # "you", set()
        if node == target:  # if "out" then target met so add 1 to total_paths
            return 1
        
        visited.add(node) # add each visited node to the set
        total_paths = 0
        
        for neighbor in graph.get(node, []):  # Get values associated with key
            if neighbor not in visited:
                total_paths += dfs(neighbor, visited.copy())  # repeat process but with new key, copy set
        
        return total_paths
    
    return dfs(start, set())


answer = you_out("day11_input.txt")
print(f"There are {answer} different paths leading from you to out.")



# Function that finds the number of paths from "svr" to "out" that also visits "dac" and "fft"
def svr_out(file, start="svr", target="out"):
    """
    ChatGPT generated. Takes too long.
    """
    graph = {}
        
    with open(file) as f:
        for line in f:
            key, values = line.strip().split(":")
            graph[key] = values.split()
    
    required = {"dac", "fft"}
    
    def dfs(node, visited, required_seen):
        if node in visited:
            return 0
    
        visited.add(node)
    
        if node in required:
            required_seen = required_seen | {node}
    
        if node == target:
            result = 1 if required_seen == required else 0
        else:
            result = 0
            for neighbor in graph.get(node, []):
                result += dfs(neighbor, visited, required_seen)
    
        visited.remove(node)
        return result
    
    return dfs(start, set(), set())


answer = svr_out("day11_input.txt")
print(f"There are {answer} different paths leading from svr to out and including dac and fft.")


"""
Answers:
https://www.reddit.com/r/adventofcode/comments/1pjp1rm/2025_day_11_solutions/

Some solutions used functools lru_cache() or cache() to cache the paths and make the function run quicker:
https://github.com/euporphium/pyaoc/blob/main/aoc/2025/solutions/day11_part2.py

lru_cache() is a Decorator to wrap a function with a memoizing callable that saves up to the maxsize most recent calls.
https://docs.python.org/3/library/functools.html#functools.lru_cache
"""
