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
def readTerrain(imagePath):
    terrainImage = Image.open(imagePath)
    terrainData = terrainImage.load()
    return terrainImage, terrainData

# Read elevation data
def readElevation(elevationFile):
    elevation = []
    with open(elevationFile, 'r') as f:
        for line in f:
            elevationRow = list(map(float, line.split()[:395]))
            elevation.append(elevationRow)
    return elevation

# Read control points
def readControlPoints(path_File):
    points = []
    with open(path_File, 'r') as f:
        for line in f:
            x, y = map(int, line.split())
            points.append((x, y))
    return points

def cost(current, neighbor, elevation):
        x1, y1 = current
        x2, y2 = neighbor
        dx, dy = 10.29, 7.55
        d2d = math.sqrt(((x2 - x1) * dx) ** 2 + ((y2 - y1) * dy) ** 2)
        elevationDiff = elevation[y2][x2] - elevation[y1][x1]
        return d2d + abs(elevationDiff)

# A* search algorithm
def astar(start, goal, terrainData, elevation, imageWidth, imageHeight):
    def heuristic(a, b):
        (x1, y1), (x2, y2) = a, b
        dx, dy = 10.29, 7.55
        return math.sqrt(((x2 - x1) * dx) ** 2 + ((y2 - y1) * dy) ** 2)

    def getNeighbors(pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < imageWidth and 0 <= ny < imageHeight:
                neighbors.append((nx, ny))
        return neighbors

    openList = []
    heapq.heappush(openList, (0, start))
    cameFrom = {}
    costSoFar = {start: 0}

    while openList:
        _, current = heapq.heappop(openList)

        if current == goal:
            break

        for neighbor in getNeighbors(current):
            newCost = costSoFar[current] + cost(current, neighbor, elevation)
            if neighbor not in costSoFar or newCost < costSoFar[neighbor]:
                costSoFar[neighbor] = newCost
                priority = newCost + heuristic(goal, neighbor)
                heapq.heappush(openList, (priority, neighbor))
                cameFrom[neighbor] = current

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = cameFrom[current]
    path.append(start)
    path.reverse()
    return path

# Draw the optimal path on the image
def drawPath(image, path):
    draw = ImageDraw.Draw(image)
    for (x, y) in path:
        draw.point((x, y), fill=(118, 63, 231))

# Main function
def main():
    terrainImage, terrainData = readTerrain(sys.argv[1])
    elevation = readElevation(sys.argv[2])
    controlPoints = readControlPoints(sys.argv[3])
    outputImage = sys.argv[4]

    totalPath = []
    for i in range(len(controlPoints) - 1):
        start = controlPoints[i]
        goal = controlPoints[i + 1]
        path = astar(start, goal, terrainData, elevation, terrainImage.width, terrainImage.height)
        totalPath.extend(path)


    drawPath(terrainImage, totalPath)
    terrainImage.save(outputImage)


    totalLength = sum([cost(totalPath[i], totalPath[i + 1], elevation) for i in range(len(totalPath) - 1)])
    print(f"Total path length: {totalLength} meters")

if __name__ == "__main__":
    main()