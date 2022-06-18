import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Polygon
import time

# import random
# Longitina =[]
# Latina =[]
# Alien =[]
n=1

def draw(Longitina, Latina, Alien,x,y,Rangle,n):
    #displays POI's
    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(Longitina, Latina, zorder=1, c=Alien, s=10)
    # ax.set_title('Mapped Unknown')
    ax.set_xlim(0,360)
    ax.set_ylim(0,240)
   
   #draw rover position/angle
    tangle=30
    tsize=2.5

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
    pts = np.array([[x,y], [wing1x,wing1y],[wing2x,wing2y]])
    p = Polygon(pts, closed=False)
    ax = plt.gca()
    ax.add_patch(p) 
    time.sleep(5)
    plt.savefig('./command/src/components/comp-resources/Mapped_Unknown.jpg')


def update(long, lat, colour, Longitina, Latina, Alien,x,y,Rangle,n):
    Longitina.append(long)
    Latina.append(lat)
    Alien.append(colour)
    draw(Longitina, Latina, Alien,x,y,Rangle,n)
    

def alien(x,y,Rangle,colour,aangle,dist,Longitina,Latina,Alien,n):
    tot=(math.pi*(aangle + Rangle))/180
    dx=dist*math.sin(tot)
    #print(dx)
    dy=dist*math.cos(tot)
    #print(dy)
    long=x+dx
    #print(long)
    lat=y+dy
    #print(lat) 
    if colour != '#ffffff':
        update(long, lat, colour,Longitina,Latina,Alien,x,y,Rangle,n)
    else:
        draw(Longitina, Latina, Alien,x,y,Rangle,n)

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