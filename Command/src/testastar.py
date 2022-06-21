
import numpy as np


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





# def smooth(path, weight_data = 0.5, weight_smooth = 0.2, tolerance = 0.00001):
    
#     # Make a deep copy of path into newpath
#     newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
#     for i in range(len(path)):
#         for j in range(len(path[0])):
#             newpath[i][j] = path[i][j]

#     change = 1
#     while change > tolerance:
#         change = 0
#         for i in range(1,len(path)-1):
#             for j in range(len(path[0])):
#                 ori = newpath[i][j]
#                 newpath[i][j] = newpath[i][j] + weight_data*(path[i][j]-newpath[i][j])
#                 newpath[i][j] = newpath[i][j] + weight_smooth*(newpath[i+1][j]+newpath[i-1][j]-2*newpath[i][j])
#                 change += abs(ori - newpath[i][j])
    
#     return newpath 


def straight(path):
    new_path = []
    x = []
    y = []
    new_path.append((path[0][0], path[0][1]))
    count = 0
    m = 0
    m_prev = -1


    # for j in range(1,len(path)):
    #     x.append(path[j][0])
    #     y.append(path[0][1])


    for i in range(1,len(path)):
        # slope, intercept = np.polyfit(x,y,1)
        # m = (path[i][0] - path[i-1][0]) / (path[i][1] - path[i-1][1])
        # print(m)
        # if m == m_prev:
        #     print("yo")
        #     # count+=1
        #     # if count==1:
        #     new_path.append([path[i][0], path[i][1]])

        #     count = 0

        # m_prev = m

        if (path[i][0]==path[i-1][0]) or (path[i][1]==path[i-1][1]):
            count+=1
            if (count==2):
                new_path.append((path[i-2][0], path[i-2][1]))
                count = 0

    # print(new_path[len(new_path)-1])
    # print(path[len(path)-1])
    if new_path[len(new_path)-1]!=path[len(path)-1]:
        new_path.append(path[len(path)-1])

    return new_path




def main():

    maze = [[0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 3)
    end = (5, 0)

    path = astar(maze, start, end)
    print(path)

    # smooth_path = smooth(path)
    # print(smooth_path)

    critical_points = straight(path)
    print(critical_points)

if __name__ == '__main__':
    main()
