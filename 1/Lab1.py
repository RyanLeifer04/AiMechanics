import heapq

def read_image(filename):
    image = open(filename,'r')
    return image

def count_lines(filepath):
    with open(filepath, 'r') as file:
        return sum(1 for line in file)

def readElevation(filename,x,y):
    elevations = open(filename,'r')
    elevs = []
    lines = count_lines(filename)
    i = 0
    while i < lines:
        elevs.append(elevations.readline().split())
        i += 1
    return float(elevs[x][y])


def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# A* function for finding the shortest path in a matrix of strings
def astar(matrix, start, goal, cost_map):
    rows, cols = len(matrix), len(matrix[0])
    
    # Priority queue for A* (min-heap), initialized with the start node
    open_list = []
    heapq.heappush(open_list, (0 + manhattan_distance(start, goal), 0, start))
    
    # Dictionaries to store the cost of reaching nodes and the best paths
    g_cost = {start: 0}
    came_from = {start: None}
    
    while open_list:
        # Pop the node with the lowest f(n) = g(n) + h(n)
        _, current_g_cost, current = heapq.heappop(open_list)
        
        # If the goal is reached, reconstruct the path
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return the path in the correct order
        
        # Explore neighbors (up, down, left, right)
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            
            # Check if the neighbor is within bounds
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                neighbor_key = matrix[neighbor[0]][neighbor[1]]
                step_cost = cost_map[neighbor_key]
                new_g_cost = current_g_cost + step_cost
                
                # If the new path to the neighbor is shorter, update its cost and path
                if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_g_cost
                    f_cost = new_g_cost + manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, new_g_cost, neighbor))
                    came_from[neighbor] = current
    
    # If no path is found, return None
    return None
