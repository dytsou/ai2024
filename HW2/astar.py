import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    """
    First, read the edges.csv file and store the graph as an adjacency list.
    Then, read the heuristic.csv file and store the heuristic values as a
    dictionary. Finally, implement the A* algorithm by using a priority queue
    with the distance and heuristic value to find the path from the start node
    to the end node. Finally, reconstruct the path from the start node to the
    end node and return the path, total distance, and the number of visited
    nodes.
    """
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
    # Heuristic values
    with open(heuristicFile, 'r') as file:
        header = next(file).strip().split(',')
    heuristic = {}
    with open(heuristicFile, 'r') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            node = int(row[0])
            if end == '1079387396': h = float(row[1])
            elif end == '1737223506': h = float(row[2])
            elif end == '8513026827': h = float(row[3])
            else: h = 0
            heuristic[node] = h 
    # A* Search
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
    heapq.heappush(pq, (heuristic[start], start)) # (distance + heuristic, node)
    while pq is not None:
        visited_times += 1
        current = heapq.heappop(pq)[1]
        if current == end: # If the current node is the end node, break
            break
        if visited[current]: # If the current node is already visited, skip
            continue
        visited[current] = True
        for neighbor, weight in graph[current]:
            if distance[current] + weight < distance[neighbor]:
                distance[neighbor] = distance[current] + weight
                parent[neighbor] = current
                heapq.heappush(pq, (distance[neighbor] + heuristic[neighbor], neighbor)) # Update the priority queue with the new heuristic value
    curr_path = []
    current = end
    while current is not None:
        curr_path.insert(0, current)
        current = parent[current]
    return curr_path, distance[end], visited_times
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
