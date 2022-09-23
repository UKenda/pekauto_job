#!/usr/bin/python3

from cmath import pi
import math
import csv
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


post_length = 1.5 #[m]
data = []
first_data = True
old_row = []
x = 0
y = 0
z = 0
roll = 0
pithc = 0
yaw = 0
pi_deg = 180 #[deg]





#reading a csv file and saving in data
with open('data.csv', mode ='r')as file:
    csvFile = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
    for row in csvFile: 
        data.append(row)

x_vector = []
y_vector = []
z_vector = []
roll_vector = []
pithc_vector = []
yaw_vector = []
speed_vector = []
for row in data:
    #for first data it cannot calculate
    if first_data:
        first_data = False
        old_row = row
    else:

        #the yaw is calculated based on new and previus point (vector), and if the vector x component is negativ it has to add 180 deg 
        if(row[1]-old_row[1]) < 0:
            yaw = math.degrees(math.atan((row[2]-old_row[2])/(row[1]-old_row[1]))) + pi_deg
        else:
            yaw = math.degrees(math.atan((row[2]-old_row[2])/(row[1]-old_row[1])))
        
        x = row[1]/1000
        y = row[2]/1000
        roll = math.radians(row[3])
        pitch = math.radians(row[4])
        yaw = math.radians(yaw)
        #matrics for transforming the points
        gps_translation = [[1,0,0,x],[0,1,0,y],[0,0,1,post_length],[0,0,0,1]]
        roll_rotation = [[1,0,0,0],[0,math.cos(roll),-math.sin(roll),0],[0,math.sin(roll),math.cos(roll),0],[0,0,0,1]]
        pitch_rotation = [[math.cos(pitch),0,math.sin(pitch),0],[0,1,0,0],[-math.sin(pitch),0,math.cos(pitch),0],[0,0,0,1]]
        yaw_rotation = [[math.cos(yaw),-math.sin(yaw),0,0],[math.sin(yaw),math.cos(yaw),0,0],[0,0,1,0],[0,0,0,1]]

        '''
        base = gps_translation @ roll_rotation @ pitch_rotation @ yaw_rotation @ [0,0,-post_length,1]
        
        where |z = post_length|cr = cos(roll)|sr = sin(roll)|cp = cos(pitch)|sp = sin(pitch)|cy = cos(yaw)|sy = sin(yaw)|

        |x_new|   |1  0  0  x|       |1  0  0  0|       |cp 0 sp  0|        |cy -sy0  0|        |0 |
        |y_new| = |0  1  0  y|   @   |0 cr -sr 0|   @   |0  1  0  0|    @   |sy cy 0  0|    @   |0 |
        |z_new| = |0  0  1  z|   @   |0 sr cr  0|   @   |-sp0 cp  0|    @   |0  0  1  0|    @   |-z|
        |  1  |   |0  0  0  1|       |0  0  0  1|       |0  0  0  1|        |0  0  0  1|        |1 |
        
        '''
        base = np.dot(np.dot(np.dot(np.dot(gps_translation,roll_rotation),pitch_rotation),yaw_rotation),[[0],[0],[-post_length],[1]])
        z += base[2][0]
        x_vector.append(base[0][0])
        y_vector.append(base[1][0])
        z_vector.append(z)
        roll_vector.append(roll)
        pithc_vector.append(pitch)
        yaw_vector.append(yaw)
        speed_vector.append(math.sqrt((row[1]-old_row[1])**2 + (row[2]-old_row[2])**2)/1000/(row[0]-old_row[0]))

        old_row = row

# writing to csv file 
with open("calculated_data", 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow([" x [m]"," y [m]"," z [m]"," roll [deg]"," pitch [deg]"," yaw [deg]"," speed [m/s]"]) 
    i = 0
    for x in x_vector:
        csvwriter.writerow([x,y_vector[i],z_vector[i],math.degrees(roll_vector[i]),math.degrees(pithc_vector[i]),math.degrees(yaw_vector[i]),speed_vector[i]])
        i+=1

fig = plt.figure()

ax = plt.axes(projection ='3d')

# plotting
ax.plot3D(x_vector, y_vector, z_vector, 'green')
ax.set_title('3D line plot of path')
ax.set_xlim(7,10)
ax.set_ylim(-36,-30)
ax.set_zlim(-0.1,0.2)
plt.show()




        

   