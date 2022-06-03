import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import math
import random
Longitina =[]
Latina =[]
Alien =[]




def draw(Longitina, Latina, Alien):
    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(Longitina, Latina, zorder=1, c=Alien, s=10)
    ax.set_title('Mapped Unknown')
    ax.set_xlim(-50,50)
    ax.set_ylim(-50,50)
    plt.savefig('Mapped_Unknown.jpg')

def update(long, lat, colour):
    Longitina.append(long)
    Latina.append(lat)
    Alien.append(colour)
    

def alien(x,y,Rangle,colour,aangle,dist):
    dx=dist*math.sin(aangle + Rangle)
    dy=dist*math.cos(aangle + Rangle)
    long=x+dx
    lat=y+dy
    update(long, lat, colour)


print('rover-x:')
x = 0
print('rover-y:')
y = 0
print('rov angle')
print('colour:')
colour = '#00f'
print('angle')
aangle = 0
print('distance')
dist = float(28.284)   
for i in range(8):
    Rangle = i*math.pi/4
    alien(x,y,Rangle,colour,aangle,dist)
for i in range(8):
    Rangle = i*math.pi/4
    x=10
    y=10
    colour = '#f00'
    alien(x,y,Rangle,colour,aangle,dist)
# for i in range(8):
#     Rangle = i*math.pi/16
#     dist= random.randrange(50)
#     alien(x,y,Rangle,colour,aangle,dist)
    
draw(Longitina, Latina, Alien)