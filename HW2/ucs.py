import csv
import heapq
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    """
    First, read the edges.csv file and store the graph as an adjacency list.
    Then, implement the UCS algorithm by using a priority queue to find the
    path from the start node to the end node. Finally, reconstruct the path
    from the start node to the end node and return the path, total distance,
    and the number of visited nodes.
    """
    # Read the edges.csv file and store the graph as an adjacency list
    with open(edgeFile, 'r') as file:
        header = next(file).strip().split(',') # Skip the header
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
    # UCS
    visited = {}
    distance = {}
    parent = {}
    for node in graph: # Initialize
        visited[node] = False
        distance[node] = float('inf')
        parent[node] = None
    distance[start] = 0
    visited_times = 0
    pq = []
    heapq.heappush(pq, (0, start)) # (distance, node)
    while pq:
        visited_times += 1
        current = heapq.heappop(pq)[1] 
        if current == end: # If the current node is the end node, break
            break
        if visited[current]: # If the current node is already visited, skip
            continue
        visited[current] = True
        for neighbor, weight in graph[current]:
            if distance[current] + weight < distance[neighbor]: # Relaxation
                distance[neighbor] = distance[current] + weight
                parent[neighbor] = current
                heapq.heappush(pq, (distance[neighbor], neighbor)) # Update the priority queue with the new distance
    curr_path = []
    current = end
    while current is not None:  # Reaching the start node
        curr_path.insert(0, current)
        current = parent[current]
    return curr_path, distance[end], visited_times
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
