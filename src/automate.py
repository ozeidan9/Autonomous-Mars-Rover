from enum import auto
from operator import indexOf
import numpy as np
import math

# map = np.zeros((240,360)) 
point=[]
# map = np.zeros((360,240))
poi = [[26,26],[180,26],[334,26],[334,214],[180,214],[26,214],[120,120],[240,120]]  # Points of interest
# Add corners of arena to poi
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
    print("8")

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


# def straight_path(path):
#     new_path = []
#     x = []
#     y = []
#     new_path.append((path[0][0], path[0][1]))
#     count = 0
#     m = 0
#     m_prev = -1

   

#     m_count = 0
#     for i in range(1,len(path)):
#         if (path[i][0] - path[i-1][0])!=0:
#             m = (path[i][1] - path[i-1][1]) / (path[i][0] - path[i-1][0]) #dy/dx
#             # print(m)

#         # print(m)
#         condition = abs(m - m_prev)<=0.8  # bool condition
#         if condition:
#             m_count+=1
#         # print(abs(m - m_prev))
#         if condition==False and m_count!=0:
#             # new_path.append((path[i-1][0], path[i-1][1]))
#             new_path.append((path[i][0], path[i][1]))
#             new_path.append((path[i-m_count-1][0], path[i-m_count-1][1]))
#             m_count = 0

#         m_prev = m



#     if new_path[len(new_path)-1]!=path[len(path)-1]:
#         new_path.append(path[len(path)-1])

#     return new_path



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

        print(m)
        condition = abs(m - m_prev)<=0.8  # bool condition
        if condition:
            m_count+=1
        # print(abs(m - m_prev))
        if condition==False and m_count!=0:
            # new_path.append((path[i-1][0], path[i-1][1]))
            new_path.append((path[i][0], path[i][1]))

            point_check = new_path.index((path[i-m_count-2][0], path[i-m_count-2][1]))
            if not (point_check>=0):
                new_path.append((path[i-m_count-2][0], path[i-m_count-2][1]))

            # print(m_count)
            m_count = 0

        m_prev = m


    if new_path[len(new_path)-1]!=path[len(path)-1]:
        new_path.append(path[len(path)-1])

    return new_path




# def make_circle(map, cx, cy):
#     for x in range(cx - 10, cx + 10):
#         for y in range(cy - 10, cy + 10):
#             if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= 10 and 0<=x<240 and 0<=y<360:
#                 map[x][y] = 1

def make_circle(map_temp, cx, cy , radius):
    for x in range(cx - radius, cx + radius):
        for y in range(cy - radius, cy + radius):
            if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= radius and 0<=x<240 and 0<=y<360:
                map_temp[x][y] = 1


def make_border(map_temp):
    # left border
    for y in range(0, 360):
        for x in range(0, 11):
            map_temp[y][x] = 1

    # right border
    for y in range(0, 360):
        for x in range(229, 240):
            map_temp[y][x] = 1
    # bottom border
    for y in range(0, 10):
        for x in range(0, 240):
            map_temp[y][x] = 1

    # top border
    for y in range(349, 360):
        for x in range(0, 240):
            map_temp[y][x] = 1




def extract_commands(path_array): #outputs array of [angle1, distance1, angle2, distance2]
    path_output = []
    for i in range(0, len(path_array)-1):
        if (path_array[i+1][1]-path_array[i][1])>=0 and (path_array[i+1][0]-path_array[i][0])<0:
            # print("case 1")
            
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
                while distance > 60:
                    path_output.append(60+16384)
                    distance -= 60
                path_output.append(int(distance)+16384)



        elif (path_array[i+1][1]-path_array[i][1])<0:
            # print("case 2")
            adjacent = path_array[i+1][0] - path_array[i][0]
            opposite = path_array[i+1][1] - path_array[i][1]

            if adjacent==0:
                pos_angle = 0
            else:
                pos_angle = math.degrees(np.arctan(opposite/adjacent))
                pos_angle += 180

                distance = pow(pow(adjacent, 2) + pow(opposite, 2), 0.5)
                path_output.append(int(pos_angle))
                # path_output.append(int(distance)+16384)
                while distance > 60:
                    path_output.append(60+16384)
                    distance -= 60
                path_output.append(int(distance)+16384)

        elif (path_array[i+1][1]-path_array[i][1])>=0 and (path_array[i+1][0]-path_array[i][0])<0:
            # print("case 3")
            

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
                while distance > 60:
                    path_output.append(60+16384)
                    distance -= 60
                path_output.append(int(distance)+16384)

        else: # dx and dy both >=0
            # print("case 4")
            
            adjacent = path_array[i+1][0] - path_array[i][0]
            opposite = path_array[i+1][1] - path_array[i][1]
            print(adjacent)
            print(opposite)
            if adjacent==0:
                pos_angle = 0
            else:
                pos_angle = math.degrees(np.arctan(opposite/adjacent))
                distance = pow(pow(adjacent, 2) + pow(opposite, 2), 0.5)
                path_output.append(int(pos_angle))
                while distance > 60:
                    path_output.append(60+16384)
                    distance -= 60
                path_output.append(int(distance)+16384)


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
def automate_route(map_temp, location ,end):
    print("start is: ")
    print(location)
    print("end is: ")
    print(end)
    a_star_path = astar(map_temp, (location[0], location[1]), end)
    #print("past astar")
    straight_route = straight_path(a_star_path)
    #print("Straight route")
    print(straight_route)
    comms =  extract_commands(straight_route)
    print(comms)
    return comms

#adv def CurvatiousBundaliciousBattyBunds():
def update_start(map_temp, x,y):
    if x == 20:
        if y==20:
            command=automate_route(map_temp, (x,y) ,(26,26))
            angle=90
            #driveto(26,26,90)  
            point=0
        if y==220:
            command=automate_route(map_temp, (x,y) ,(26,214))
            angle=180
            #driveto(26,214,180)
            point=5
    if x == 340:
        if y==20:
            command=automate_route(map_temp, (x,y) ,(334,26))
            angle=0
            #driveto(334,26,-90)
            point= 2
        if y==220:
            command=automate_route(map_temp, (x,y) ,(334,214))
            angle = 270
            #driveto(324,214,0)
            point= 3
    return (point,command,angle)

def exe(sav_loc, point, reachedpoint, investigated,map):
    dalist=[]
    commands=[]
    print("investigated")
    print(investigated)
    print("reachedpoint: ")
    print(reachedpoint)
    print("current poi: ")
    print(poi[point])
    print("point")
    print(point)
    ####change for aceptence range###########
    if investigated == True:
        print("Moving to point#########################################################################################")
        commands = automate_route(map ,(sav_loc[0],sav_loc[1]), (poi[point+1][0],poi[point+1][1]))
        investigated=False
        reachedpoint=False
    elif investigated == False and reachedpoint==True:
        print("investigateing----------------------------------------------------------------------------------------------------------")
        #################### need to change investigation protocals###############
        if point == 1: # mid edge
            commands.append(295) # left 155
            commands.append(90) #right 155
            point=point+1
            investigated=True
            reachedpoint = False
        elif point==0:
            #commands.append(32768) #radar on
            commands.append(25) # left 65
            commands.append(90) #right 65
            #commands.append(49152) #radar off
            point=point+1
            investigated=True
            reachedpoint = False
            
        elif point==2:
            commands.append(32768) #radar on
            commands.append(295) # left 65
            commands.append(0) #right 65
            commands.append(49152) #radar off
            point=point+1
            investigated=True
            reachedpoint = False

        elif point==3:
            commands.append(32768) #radar on
            commands.append(205) # left 65
            commands.append(270) #right 65
            commands.append(49152) #radar off
            point=point+1
            investigated=True
            reachedpoint = False


        elif point == 4:  # mid edge 
            commands.append(115) # left 155
            commands.append(270) #right 155
            point=point+1
            investigated=True
            reachedpoint = False

        
        elif point==5:
            commands.append(32768) #radar on
            commands.append(115) # left 180
            commands.append(180) # left 180
            commands.append(49152) #radar off
            point=point+1
            investigated=True
            reachedpoint = False

        elif point == 6:    #mid 360
            commands.append(180) # left 180
            commands.append(280) # left 180
            commands.append(90)
            point=point+1
            investigated=True
            reachedpoint = False

        elif point == 7 :
            commands.append(180) # left 180
            commands.append(280) # left 180
            commands.append(90)
            point=point+1
            investigated=True
            reachedpoint = False


    elif reachedpoint==False:
        print("reachedpoint=false")
        commands = automate_route(map ,(sav_loc[0],sav_loc[1]), (poi[point][0],poi[point][1]))

    dalist.append(point)
    dalist.append(commands)
    dalist.append(reachedpoint)
    print(dalist)
    return dalist

    
