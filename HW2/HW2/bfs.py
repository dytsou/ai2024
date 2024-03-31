import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
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
            if s not in graph:
                graph[s] = []
            graph[s].append(t)
            if t not in graph:
                graph[t] = []
            graph[t].append(s)

    # BFS 
    visited = {}
    distance = {}
    parent = {}
    for node in graph:
        visited[node] = False
        distance[node] = float('inf')
        parent[node] = None
    queue = []
    queue.append(start)
    visited[start] = True
    distance[start] = 0
    visited_times = 0
    while queue is not None:
        visited_times += 1
        current = queue.pop(0)
        if current == end:
            break
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                parent[neighbor] = current
                queue.append(neighbor)
    curr_path = []
    current = end
    while current is not None:
        curr_path.insert(0, current)
        current = parent[current]
    return curr_path, distance[end], visited_times
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
