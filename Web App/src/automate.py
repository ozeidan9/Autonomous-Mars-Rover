from enum import auto
from operator import indexOf
import numpy as np

# map = np.zeros((240,360)) 
point=[]

poi = [ [] ]  # Points of interest
# Add corners of arena to poi
poi.append([26,26])#0
poi.append([180,26])#1
poi.append([334,26])#2
poi.append([334,214])#3
poi.append([180,214])#4
poi.append([26,214])#5
poi.append([120,120])#6
poi.append([240,120])#7


class Node(): #node class for A* pathfinding -> f = g + h

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Rover(): #node class for A* pathfinding -> f = g + h

    def __init__(self=None):

        self.distance = 0
        self.angle = 0

        self.x = 0
        self.y = 0
      

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


def straight_path(path):
    new_path = []
    x = []
    y = []
    new_path.append((path[0][0], path[0][1]))
    count = 0
    m = 0
    m_prev = -1

    print("gradient")

    m_count = 0
    for i in range(1,len(path)):
        if (path[i][0] - path[i-1][0])!=0:
            m = (path[i][1] - path[i-1][1]) / (path[i][0] - path[i-1][0]) #dy/dx
            # print(m)

        # print(m)
        condition = abs(m - m_prev)<=0.8  # bool condition
        if condition:
            m_count+=1
        # print(abs(m - m_prev))
        if condition==False and m_count!=0:
            # new_path.append((path[i-1][0], path[i-1][1]))
            new_path.append((path[i][0], path[i][1]))
            new_path.append((path[i-m_count][0], path[i-m_count][1]))
            m_count = 0

        m_prev = m



    if new_path[len(new_path)-1]!=path[len(path)-1]:
        new_path.append(path[len(path)-1])

    return new_path



def make_circle(map, cx, cy):
    for x in range(cx - 10, cx + 10):
        for y in range(cy - 10, cy + 10):
            if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= 10 and 0<=x<240 and 0<=y<360:
                map[x][y] = 1


def extract_commands(path_array): #outputs array of [angle1, distance1, angle2, distance2]
    
    for i in range(0, len(path_array)):
        if (path_array[i+1][1]-path_array[i+1][1])>=0:
            next_coordinate = path_array[i+1]     #find max row element (max x element) -> axis=0 is row
            start_coordinate = path_array[0]            # initial [x,y] coordinate
            adjacent = next_coordinate[1] - start_coordinate[1]
            opposite = next_coordinate[0] - start_coordinate[0]
            pos_angle = np.arctan(opposite/adjacent)
            distance = sqrt((opposite)^2 + (opposite)^2)
            path_output = []
            path_output.append(pos_angle)
            path_output.append(distance)

        if (path_array[i+1][1]-path_array[i+1][1])<0:
            next_coordinate = path_array[i+1]     #find max row element (max x element) -> axis=0 is row
            start_coordinate = path_array[0]            # initial [x,y] coordinate
            adjacent = next_coordinate[1] - start_coordinate[1]
            opposite = next_coordinate[0] - start_coordinate[0]
            pos_angle = np.arctan(opposite/adjacent)
            pos_angle += 180
            distance = sqrt((opposite)^2 + (opposite)^2)
            path_output = []
            path_output.append(pos_angle)
            path_output.append(distance)

    return path_output


def automate_route(map, start, end):
    a_star_path = astar(map, start, end)
    straight_route = straight_path(map)
    return extract_commands


def sendtodrive(path_output):
    for name in nicknames:
        if name=="rover":
            index = indexOf(name)
            break

    client = clients[index]
    #Add queue system...
    client.send["yo"]



#adv def CurvatiousBundaliciousBattyBunds():
def update_start(x,y,angle):
    if x == 20:
        if y==20:
            #driveto(26,26,90)
            stateinner= 0
        if y==220:
            #driveto(26,214,180)
            stateinner= 5
    if x == 340:
        if y==20:
            #driveto(334,26,-90)
            stateinner= 2
        if y==220:
            #driveto(324,214,0)
            stateinner= 3
    return (stateinner)
    

# def driveto(x,y,angle):

#     init_x = rover.x
#     init_y = rover.y
#     curr_loc = [init_x, init_y]

#     new_loc = calc_loc(angle,  ,curr_loc)
#     rover.x = new_loc[0]
#     rover.y = new_loc[1]



def nextpoint(state, poi,map):
    line_path = automate_route(map ,poi[point-1], poi[point])  # line_path = [angle1, d1, angle2, d2]
    return (line_path)
    #send to drive
    #sendtodrive
    

def command(point,state):
    line_path = automate_route(map ,poi[point], poi[point+1]) 
    if (point == 1 or point == 4):
        command.clear()
        command.append("6155") # left 155
        command.append("7155") #right 155
        

    if (point == 6 or point == 7):
        command.append("6180") # left 180
        command.append("6180") # left 180 
        
    else:
        command.append("9000") #radar on
        command.append("6065") # left 65
        command.append("7065") #right 65
        command.append("9100") #radar off
        print(command)
        return command

def exe(x,y,angle,state,serverstate):
    if serverstate == 1 :
        state=update_start(x,y)
    if serverstate==0:
        commandlist = command(point,state)
    
    return commandlist
    
