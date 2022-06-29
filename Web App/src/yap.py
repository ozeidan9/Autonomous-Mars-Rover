import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Polygon
import time
import automate

# import random
# Longitina =[]
# Latina =[]
# Alien =[]
n=1

def calc_loc(Rangle,sav_dist,dist,sav_loc):#
    loc=[]
    dist1=dist-sav_dist
    angle=(math.pi*(Rangle))/180
    dx=dist1*math.sin(angle)
    dy=dist1*math.cos(angle)
    x=sav_loc[0]+dx
    y=sav_loc[1]+dy
    loc.append(x)
    loc.append(y)
    return(loc)

def draw(Longitina, Latina, Alien,x,y,Rangle):
    #displays POI's
    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(Longitina, Latina, zorder=1, c=Alien, s=20)
    # ax.set_title('Mapped Unknown')
    ax.set_xlim(0,360)
    ax.set_ylim(0,240)

    tot=(math.pi*(Rangle))/180
    dx1=8*math.sin(tot)
    dy1=8*math.cos(tot)
    x=x+dx1
    y=y+dy1
   
   #draw rover position/angle
    tangle=20
    tsize=20

    tota=(math.pi*(Rangle + tangle))/180
    dx=-tsize*math.sin(tota)
    dy=-tsize*math.cos(tota)
    wing1x=x+dx
    wing1y=y+dy
    totb=(math.pi*(Rangle - tangle))/180
    dx=-tsize*math.sin(totb)
    dy=-tsize*math.cos(totb)
    wing2x=x+dx
    wing2y=y+dy
    # print(x)
    # print(y)
    # print(wing1x)
    # print(wing1y)
    # print(wing2x)
    # print(wing2y)
    pts = np.array([[x,y], [wing1x,wing1y],[wing2x,wing2y]])
    p = Polygon(pts, closed=False)
    ax = plt.gca()
    ax.add_patch(p) 
    time.sleep(5)
    plt.savefig('./components/comp-resources/Mapped_Unknown.jpg')


def update(long, lat, colour, Longitina, Latina, Alien,x,y,Rangle):
    Longitina.append(long)
    Latina.append(lat)
    Alien.append(colour)
    draw(Longitina, Latina, Alien,x,y,Rangle)
    

def alien(x,y,Rangle,colour,dist,Longitina,Latina,Alien):
    tot=(math.pi*(Rangle))/180
    dx=dist*math.sin(tot)
    dy=dist*math.cos(tot)
    long=x+dx
    lat=y+dy 
    if colour != '#ffffff':
        #print("im shouldnt be")
        stripes=dist>>7
        rad = (2*stripes)+10  #deadzone = 10?
        #automate.make_circle(map,long,lat, rad)
        update(long, lat, colour,Longitina,Latina,Alien,x,y,Rangle)
    else:
        draw(Longitina, Latina, Alien,x,y,Rangle)

# print('rover-x:')
# x = 0
# print('rover-y:')
# y = 0
# print('rov angle')
# print('colour:')
# colour = '#00f'
# print('angle')
# aangle = 0
# print('distance')
# dist = float(28.284)   
# for i in range(8):
#     Rangle = i*math.pi/4
#     alien(x,y,Rangle,colour,aangle,dist)
# for i in range(8):
#     Rangle = i*math.pi/4
#     x=10
#     y=10
#     colour = '#f00'
#     alien(x,y,Rangle,colour,aangle,dist)
# for i in range(8):
#     Rangle = i*math.pi/16
#     dist= random.randrange(50)
#     alien(x,y,Rangle,colour,aangle,dist)
    
# draw(Longitina, Latina, Alien)