import math
import numpy as np

map = np.zeros((240,360)) 
point=[]

poi1 = [ [] ]  # Points of interest
# Add corners of arena to poi
poi1.append([26,26])#0
poi1.append([180,26])#1
poi1.append([334,26])#2
poi1.append([334,214])#3
poi1.append([180,214])#4
poi1.append([26,214])#5


poi2 =[[]]

poi2.append([120,120])
poi2.append([240,120])


def driveto(x,y):
    return(1)
def update_start(x,y):
    if x == 20:
        if y==20:
            driveto(26,26)
            stateinner= 0
        if y==220:
            driveto(26,214)
            stateinner= 5
    if x == 340:
        if y==20:
            driveto(334,26)
            stateinner= 2
        if y==220:
            driveto(324,214)
            stateinner= 3
    return (stateinner)
    
def nextpoint(stateinner,stateouter):
    point=5%stateinner
            

def drive( x, y ):      #takes in current position of rover, don't we also need angle? 
    
     
    while 0<y<360 and 0<x<240 and (manual == False):
        
        print("brev")


class Node(): #node class for A* pathfinding -> f = g + h

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

def a_star(map, start, end): # closed box dead zone of 10x10 cm  
    # Create start and end node
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0     # A* algorothm formula for start node
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0           # A* algorothm formula for end node

    open = []   
    completed = []


    #Loop until we find the end node
    while len(open)>0:

        currentNode = open[0]  # retrieve the current node
        curr_index = 0
        for index, item in enumerate(open):
            if item.f < currentNode.f:
                currentNode = item
                curr_index = index

        # Pop current off open list, add to closed list
        open.pop(curr_index)
        completed.append(currentNode)

        # Found the goal
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (currentNode.position[0] + new_position[0], currentNode.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(currentNode, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in completed:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open.append(child)


def num_to_xy(astar_output):
    #convert number points from a star output array to x,y coordinate system of map
    print("happy days")
    path_array = ["placeholder"]
    return path_array



def smoothbrudha(path_array): #outputs array of [angle, distance, angle, diustande]
    max_x_coordnate =np.argmax( np.max(path_array, axis=0) )     #find max row element (max x element) -> axis=0 is row
    start_coordinate = path_array[0]            # initial [x,y] coordinate
    dy1 = max_x_coordnate[1] - start_coordinate[1]
    dx1 = max_x_coordnate[1] - start_coordinate[1]
    angle1 = np.arctan(dy1/dx1)
    distance1 = (dy1)^2 + (dx1)^2
    path_output = []
    path_output.append(angle1)
    path_output.append(distance1)

    end_coordinate = path_array[len(path_array)-1] 

    if max_x_coordnate==end_coordinate:
        path_output.append(0)
        path_output.append(0)
        
    else:
        dy2 = max_x_coordnate[1] - end_coordinate[1]
        dx2 = max_x_coordnate[1] - end_coordinate[1]
        angle2 = np.arctan(dy1/dx1) + angle1                # basic trig fam
        distance2 = (dy2)^2 + (dx2)^2
        path_output = []
        path_output.append(angle2)
        path_output.append(distance2)
    
    return path_output

    
    
    # for pos in path_array:
        
        




#adv def CurvatiousBundaliciousBattyBunds():