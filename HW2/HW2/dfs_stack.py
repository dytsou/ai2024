import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    # Read the edges.csv file and store the graph as an adjacency list
    start = str(start)
    end = str(end)
    graph = {}
    with open(edgeFile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] not in graph:
                graph[row[0]] = []
            graph[row[0]].append(row[1])
            if row[1] not in graph:
                graph[row[1]] = []
            graph[row[1]].append(row[0])
            
    # DFS
    visited = {}
    distance = {}
    parent = {}
    for node in graph:
        visited[node] = False
        distance[node] = float('inf')
        parent[node] = None
    stack = []
    stack.append(start)
    visited[start] = True
    distance[start] = 0
    visited_times = 0
    while stack:
        visited_times += 1
        current = stack.pop()
        if current == end:
            break
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                parent[neighbor] = current
                stack.append(neighbor)
    curr_path = []
    current = end   
    while current is not None:
        curr_path.insert(0, current)
        current = parent[current]
    return curr_path, distance[end], visited_times
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
