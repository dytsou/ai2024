import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    """
    First, read the edges.csv file and store the graph as an adjacency list.
    Then, implement the DFS algorithm by using a stack to find the path from
    the start node to the end node. Finally, reconstruct the path from the
    start node to the end node and return the path, total distance, and the
    number of visited nodes.
    """
    # Read the edges.csv file and store the graph as an adjacency list
    with open(edgeFile, 'r') as file:
        header = next(file).strip().split(',')  # Skip the header
    graph = {}
    with open(edgeFile, 'r') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            s = int(row[0])
            t = int(row[1])
            d = float(row[2])
            if s not in graph:
                graph[s] = []
            graph[s].append((t, d))
            if t not in graph:
                graph[t] = []
            # graph[t].append((s, d))
            
    # DFS
    visited = {}
    distance = {}
    parent = {}
    for node in graph: # Initialize
        visited[node] = False
        distance[node] = float('inf')
        parent[node] = None
    stack = []
    stack.append(start)
    visited[start] = True
    distance[start] = 0
    visited_times = 0
    while stack: # while stack is not empty
        visited_times += 1
        current = stack.pop()
        if current == end:
            break
        for neighbor, weight in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current] + weight
                parent[neighbor] = current
                stack.append(neighbor)
    # Reconstruct the path
    curr_path = []
    current = end   
    while current is not None: # Reaching the start node
        curr_path.insert(0, current)
        current = parent[current]
    return curr_path, distance[end], visited_times
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
