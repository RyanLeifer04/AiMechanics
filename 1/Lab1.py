#Ryan Leifer
import sys
from PIL import Image, ImageDraw
import heapq
import math

# Terrain RGB values
TERRAIN_SPEEDS = {
    (248, 148, 18): 1.0,   # Open land
    (255, 192, 0): 1.5,    # Rough meadow
    (255, 255, 255): 1.2,  # Easy movement forest
    (2, 208, 60): 2.0,     # Slow run forest
    (2, 136, 40): 3.0,     # Walk forest
    (5, 73, 24): float('inf'),  # Impassable vegetation
    (0, 0, 255): float('inf'),  # Lake/Swamp/Marsh
    (71, 51, 3): 0.8,      # Paved road
    (0, 0, 0): 0.7,        # Footpath
    (205, 0, 101): float('inf'), # Out of bounds
}

# Read terrain image
def read_terrain(image_path):
    terrain_image = Image.open(image_path)
    terrain_data = terrain_image.load()
    return terrain_image, terrain_data

# Read elevation data
def read_elevation(elevation_file):
    elevation = []
    with open(elevation_file, 'r') as f:
        for line in f:
            elevation_row = list(map(float, line.split()[:395]))
            elevation.append(elevation_row)
    return elevation

# Read control points
def read_control_points(path_file):
    points = []
    with open(path_file, 'r') as f:
        for line in f:
            x, y = map(int, line.split())
            points.append((x, y))
    return points

# A* search algorithm
def astar(start, goal, terrain_data, elevation, image_width, image_height):
    def heuristic(a, b):
        (x1, y1), (x2, y2) = a, b
        dx, dy = 10.29, 7.55
        return math.sqrt(((x2 - x1) * dx) ** 2 + ((y2 - y1) * dy) ** 2)

    def cost(current, neighbor):
        x1, y1 = current
        x2, y2 = neighbor
        dx, dy = 10.29, 7.55
        d2d = math.sqrt(((x2 - x1) * dx) ** 2 + ((y2 - y1) * dy) ** 2)
        elevation_diff = elevation[y2][x2] - elevation[y1][x1]
        return d2d + abs(elevation_diff)

    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < image_width and 0 <= ny < image_height:
                neighbors.append((nx, ny))
        return neighbors

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            new_cost = cost_so_far[current] + cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                heapq.heappush(open_list, (priority, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Draw the optimal path on the image
def draw_path(image, path):
    draw = ImageDraw.Draw(image)
    for (x, y) in path:
        draw.point((x, y), fill=(118, 63, 231))

# Main function
def main():
    terrain_image, terrain_data = read_terrain(sys.argv[1])
    elevation = read_elevation(sys.argv[2])
    control_points = read_control_points(sys.argv[3])
    output_image = sys.argv[4]

    total_path = []
    for i in range(len(control_points) - 1):
        start = control_points[i]
        goal = control_points[i + 1]
        path = astar(start, goal, terrain_data, elevation, terrain_image.width, terrain_image.height)
        total_path.extend(path)


    draw_path(terrain_image, total_path)
    terrain_image.save(output_image)


    total_length = sum([cost(total_path[i], total_path[i + 1]) for i in range(len(total_path) - 1)])
    print(f"Total path length: {total_length} meters")

if __name__ == "__main__":
    main()




# import heapq

# def read_image(filename):
#     image = open(filename,'r')
#     return image

# def count_lines(filepath):
#     with open(filepath, 'r') as file:
#         return sum(1 for line in file)

# def readElevation(filename,x,y):
#     elevations = open(filename,'r')
#     elevs = []
#     lines = count_lines(filename)
#     i = 0
#     while i < lines:
#         elevs.append(elevations.readline().split())
#         i += 1
#     return float(elevs[x][y])


# def manhattan_distance(node, goal):
#     return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# # A* function for finding the shortest path in a matrix of strings
# def astar(matrix, start, goal, cost_map):
#     rows, cols = len(matrix), len(matrix[0])
    
#     # Priority queue for A* (min-heap), initialized with the start node
#     open_list = []
#     heapq.heappush(open_list, (0 + manhattan_distance(start, goal), 0, start))
    
#     # Dictionaries to store the cost of reaching nodes and the best paths
#     g_cost = {start: 0}
#     came_from = {start: None}
    
#     while open_list:
#         # Pop the node with the lowest f(n) = g(n) + h(n)
#         _, current_g_cost, current = heapq.heappop(open_list)
        
#         # If the goal is reached, reconstruct the path
#         if current == goal:
#             path = []
#             while current is not None:
#                 path.append(current)
#                 current = came_from[current]
#             return path[::-1]  # Return the path in the correct order
        
#         # Explore neighbors (up, down, left, right)
#         for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
#             neighbor = (current[0] + direction[0], current[1] + direction[1])
            
#             # Check if the neighbor is within bounds
#             if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
#                 neighbor_key = matrix[neighbor[0]][neighbor[1]]
#                 step_cost = cost_map[neighbor_key]
#                 new_g_cost = current_g_cost + step_cost
                
#                 # If the new path to the neighbor is shorter, update its cost and path
#                 if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
#                     g_cost[neighbor] = new_g_cost
#                     f_cost = new_g_cost + manhattan_distance(neighbor, goal)
#                     heapq.heappush(open_list, (f_cost, new_g_cost, neighbor))
#                     came_from[neighbor] = current
    
#     # If no path is found, return None
#     return None
