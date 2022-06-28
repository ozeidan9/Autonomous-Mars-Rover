from enum import auto
from operator import indexOf
import numpy as np
import tcpserver
import math

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
investigated=False
knownloacation=False

class Node(): #node class for A* pathfinding -> f = g + h

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# class Rover(): #node class for A* pathfinding -> f = g + h

#     def __init__(self=None):

#         self.distance = 0
#         self.angle = 0

#         self.x = 0
#         self.y = 0
      

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
            new_path.append((path[i-m_count-1][0], path[i-m_count-1][1]))
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


def make_border(map):

    # left border
    for y in range(0, 360):
        for x in range(0, 11):
            map[y][x] = 1

    # right border
    for y in range(0, 360):
        for x in range(229, 240):
            map[y][x] = 1

    # bottom border
    for y in range(0, 10):
        for x in range(0, 240):
            map[y][x] = 1

    # top border
    for y in range(349, 360):
        for x in range(0, 240):
            map[y][x] = 1




def extract_commands(path_array): #outputs array of [angle1, distance1, angle2, distance2]
    path_output = []
    for i in range(0, len(path_array)-1):
        if (path_array[i+1][1]-path_array[i][1])>=0 and (path_array[i+1][0]-path_array[i][0])<0:
            print("case 1")
            
            adjacent = path_array[i+1][0] - path_array[i][0]
            opposite = path_array[i+1][1] - path_array[i][1]
            print(adjacent)
            print(opposite)
            if adjacent==0:
                pos_angle = 0
            else:
                pos_angle = math.degrees(np.arctan(opposite/adjacent))
                pos_angle += 360
                distance = pow(pow(adjacent, 2) + pow(opposite, 2), 0.5)
                path_output.append(int(pos_angle))
                path_output.append(int(distance))



        elif (path_array[i+1][1]-path_array[i][1])<0:
            print("case 2")
            adjacent = path_array[i+1][0] - path_array[i][0]
            opposite = path_array[i+1][1] - path_array[i][1]

            if adjacent==0:
                pos_angle = 0
            else:
                pos_angle = math.degrees(np.arctan(opposite/adjacent))
                pos_angle += 180

                distance = pow(pow(adjacent, 2) + pow(opposite, 2), 0.5)
                path_output.append(int(pos_angle))
                path_output.append(int(distance))

        elif (path_array[i+1][1]-path_array[i][1])>=0 and (path_array[i+1][0]-path_array[i][0])<0:
            print("case 3")
            

            adjacent = path_array[i+1][0] - path_array[i][0]
            opposite = path_array[i+1][1] - path_array[i][1]
            print(adjacent)
            print(opposite)
            # print("opposite is: "+ str(opposite))
            # print("adjacent is: "+ str(adjacent))
            if adjacent==0:
                pos_angle = 0
            else:
                pos_angle = math.degrees(np.arctan(opposite/adjacent))
                distance = pow(pow(adjacent, 2) + pow(opposite, 2), 0.5)
                path_output.append(int(pos_angle))
                path_output.append(int(distance))


    return path_output


################
#################
##################
##################################
##############################################
##################################
##############################
##############
##
def automate_route(map, loc ,end):
    a_star_path = astar(map, (loc[0], loc[1]), end)
    straight_route = straight_path(a_star_path)
    print("Straight route")
    print(straight_route)
    return extract_commands(straight_route)

#adv def CurvatiousBundaliciousBattyBunds():
def update_start(map, x,y):
    if x == 20:
        if y==20:
            command=automate_route(map, (x,y) ,(26,26))
            #driveto(26,26,90)
            point=0
        if y==220:
            command=automate_route(map, (x,y) ,(26,214))
            #driveto(26,214,180)
            point=5
    if x == 340:
        if y==20:
            command=automate_route(map, (x,y) ,(334,26))
            #driveto(334,26,-90)
            point= 2
        if y==220:
            command=automate_route(map, (x,y) ,(334,214))
            #driveto(324,214,0)
            point= 3
    return (point,command)

def exe(sav_loc,point):
    if investigated == True:
        commands = automate_route(map ,sav_loc, poi[point+1])
        investigated=False
    elif investigated == False:
        commands.clear() 
        if (point == 1 or point == 4):
            commands.append(205) # left 155
            commands.append(155) #right 155
            point=point+1
            investigated=True
        

        if (point == 6 or point == 7):
            commands.append(180) # left 180
            commands.append(180) # left 180
            point=point+1
            investigated=True
            
        else:
            commands.append(32768) #radar on
            commands.append(295) # left 65
            commands.append(65) #right 65
            commands.append(49152) #radar off
            point=point+1
            investigated=True
    else:
        commands = automate_route(map ,sav_loc, poi[point+1])

    return commands

    
