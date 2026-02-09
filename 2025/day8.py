# Day 8 (ChatGPT helped)
import numpy as np
from itertools import combinations  # https://docs.python.org/3/library/itertools.html
from scipy.spatial.distance import euclidean  # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html
from scipy.sparse import csr_matrix  # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
from scipy.sparse.csgraph import connected_components  # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.connected_components.html

# Function that clusters 3D points by the shortest 1000 distances
def cluster_1000(file):
    # Points parsed as numpy array
    points = np.loadtxt(file, delimiter=",", dtype=int)

    n = len(points)

    # Compute all pairwise distances
    edges = []
    for i, j in combinations(range(n), 2):  # When given an array of size n, generate all possible combinations of r elements e.g. [(1, 2), (2, 3), (1, 3)]; generate combination of indices
        d = euclidean(points[i], points[j])  # Computes the Euclidean distance between two 1-D arrays.
        edges.append((d, i, j))  # track distance, index1, index2

    # Sort by distance
    edges.sort(key=lambda x: x[0])  # d=x[0], i=x[1], j=x[2]

    # Take only the 1000 shortest connections
    top_edges = edges[:1000]

    # Build adjacency matrix
    rows, cols = [], []
    for d, i, j in top_edges:
        rows += [i, j]
        cols += [j, i]

    data = np.ones(len(rows))  # array of 1's
    graph = csr_matrix((data, (rows, cols)), shape=(n, n))  # Compressed Sparse Row matrix <1000x1000 sparse matrix of type '<class 'numpy.float64'>' with 2000 stored elements in Compressed Sparse Row format>

    # Find connected components
    n_components, labels = connected_components(graph)  # Analyse the connected components of a sparse graph

    # Count points per cluster
    unique_labels, counts = np.unique(labels, return_counts=True)  # labels are like the name of the cluster

    # Sort cluster sizes descending
    sorted_sizes = np.sort(counts)[::-1]  # np.sort() sorts ASC but [::1] flips it around so it's DESC

    # Take the 3 largest
    top_3_sizes = sorted_sizes[:3]

    # Calculate product
    product = np.prod(top_3_sizes)

    return product


answer = cluster_1000("day8_input.txt")
print(f"The product of the sizes of the 3 largest circuits is {answer}")


# Union-Find (Disjoint Set) helpers
class UnionFind:
    def __init__(self, n):
        # Each element starts in its own group.
        # parent[i] = i means "i is the leader of its group"
        self.parent = []
        for i in range(n):
            self.parent.append(i)

    def find_group(self, x):
        # Follow parents until we reach the group leader
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def connect(self, a, b):
        # Find the group leaders for a and b
        group_a = self.find_group(a)
        group_b = self.find_group(b)

        # If they are already in the same group,
        # connecting them would create a loop
        if group_a == group_b:
            return False

        # Otherwise, connect group B to group A
        self.parent[group_b] = group_a
        return True
    

# Function that clusters 3D points and finds last two coordinates added
def cluster(file):
    # Points parsed as numpy array
    points = np.loadtxt(file, delimiter=",", dtype=int)
    
    n = len(points)
    
    # Compute all pairwise distances
    edges = []
    for i, j in combinations(range(n), 2):  # When given an array of size n, generate all possible combinations of r elements e.g. [(1, 2), (2, 3), (1, 3)]; generate combination of indices
        d = euclidean(points[i], points[j])  # Computes the Euclidean distance between two 1-D arrays.
        edges.append((d, i, j))  # track distance, index1, index2
    
    # Sort by distance
    edges.sort(key=lambda x: x[0])  # d=x[0], i=x[1], j=x[2]
    
    uf = UnionFind(n)  # Use Minimum Spanning Tree algorithm to find which points are connected to the cluster
    last_edge = None
    
    # Kruskal's algorithm
    for d, i, j in edges:
        if uf.connect(i, j):
            last_edge = (i, j)  # find last edge added to cluster
    
    # Get x-coordinates
    x1 = points[last_edge[0]][0]
    x2 = points[last_edge[1]][0]
    
    # Find product of x-coordinates
    product = x1 * x2
    
    return product


answer = cluster("day8_input.txt")
print(f"The product of the x-coordinates of the 2 last junctions to be connected is {answer}")
