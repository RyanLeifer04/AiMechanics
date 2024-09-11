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

