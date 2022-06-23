
import numpy as np
import math


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)





def smooth(path, weight_data = 0.5, weight_smooth = 0.2, tolerance = 0.00001):
    
    # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]

    change = 1
    while change > tolerance:
        change = 0
        for i in range(1,len(path)-1):
            for j in range(len(path[0])):
                ori = newpath[i][j]
                newpath[i][j] = newpath[i][j] + weight_data*(path[i][j]-newpath[i][j])
                newpath[i][j] = newpath[i][j] + weight_smooth*(newpath[i+1][j]+newpath[i-1][j]-2*newpath[i][j])
                change += abs(ori - newpath[i][j])
    
    return newpath 


def straight(path):
    new_path = []
    x = []
    y = []
    new_path.append((path[0][0], path[0][1]))
    count = 0
    m = 0
    m_prev = -1


    m_count = 0
    for i in range(1,len(path)):
        if (path[i][0] - path[i-1][0])!=0:
            m = (path[i][1] - path[i-1][1]) / (path[i][0] - path[i-1][0]) #dy/dx
            # print(m)
        condition = abs(m - m_prev)<=1  # bool condition
        if condition:
            m_count+=1

        if not condition and m_count!=0:
            # new_path.append((path[i-1][0], path[i-1][1]))
            new_path.append((path[i][0], path[i][1]))
            new_path.append((path[i-m_count][0], path[i-m_count][1]))
            m_count = 0

        m_prev = m

        # if (path[i][0]==path[i-1][0]) or (path[i][1]==path[i-1][1]):
        #     count+=1
        #     # if (count==2):
        #     #     new_path.append((path[i-2][0], path[i-2][1]))
        #     #     count = 0

        # if (path[i][0]!=path[i-1][0]) and (path[i][1]!=path[i-1][1]) and count!=0:
        #     new_path.append((path[i-1][0], path[i-1][1]))
        #     new_path.append((path[i-count-1][0], path[i-count-1][1]))
        #     count = 0


    if new_path[len(new_path)-1]!=path[len(path)-1]:
        new_path.append(path[len(path)-1])

    return new_path



# def dead_zone(map, alien): #9x9 square deadzoen centred at alien or building
    
#     x = alien[0]
#     y = alien[1]

    
#     for i in range(x-5, x+5):
#         for k in range(y-5, y+5):

#             if 0<=i<240 and 0<=y<360:
#                 map[i,k] = 1
    
#     return map


def dead_zone(map, alien): #9x9 square deadzoen centred at alien or building
    
    x = alien[0]
    y = alien[1]

    
    for i in range(x-10, x+10):
        for k in range(y-10, y+10):

            if 0<=i<240 and 0<=y<360:
                map[i,k] = 1
                
                print( "(" + str(i) + ","+str(k)+")" )

    
    return map


def make_circle(map, cx, cy):
    for x in range(cx - 10, cx + 10):
        for y in range(cy - 10, cy + 10):
            if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= 10 and 0<=x<240 and 0<=y<360:
                map[x][y] = 1




def main():

    # maze = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    #         [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    #         [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #         [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    #         [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # maze = np.zeros((240, 360))
    
    maze = np.zeros((360, 240))

    start = (30, 100)
    end = (100, 65)

    # dead_zone(maze, [50, 100])
    # dead_zone(maze, [90, 65]) 

    make_circle(maze, 50, 100)
    make_circle(maze, 90, 65)


    # dead_zone(maze, [200, 10]) 
    # dead_zone(maze, [15, 15])

    # print(maze)

    path = astar(maze, start, end)
    print("A star: ")
    print(path)

    print("x is: ")
    for i in range(0, len(path)):
        print(path[i][0])

    print("y is: ")
    for i in range(0, len(path)):
        print(path[i][1])


    # print(maze)
    smooth_path = smooth(path)
    print("Smoothening: ")
    print(smooth_path)

    print("smooth x is: ")
    for i in range(0, len(smooth_path)):
        print(smooth_path[i][0])

    print("smooth y is: ")
    for i in range(0, len(smooth_path)):
        print(smooth_path[i][1])

    critical_points = straight(path)
    print("Critical point algo: ")
    print(critical_points)

    print("critical x is: ")
    for i in range(0, len(critical_points)):
        print(critical_points[i][0])

    print("critical y is: ")
    for i in range(0, len(critical_points)):
        print(critical_points[i][1])

if __name__ == '__main__':
    main()
