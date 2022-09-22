#!/usr/bin/python3

import math
import csv
import numpy as np


print ("inicialization")
post_length = 1500 #[mm]
data = []

#reading the CSV file
with open('data.csv', mode ='r')as file:

    csvFile = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
    for row in csvFile: # each row is a list
        data.append(row)


i=0
projected_data=[]
for point in data:

    #print(point[1])
    x_err = math.sin(math.radians(point[4]))*post_length
    true_x = point[1] - x_err
    #print(true_x)
    y_err = math.sin(math.radians(point[3]))*post_length
    true_y = point[2] - y_err
    #print(true_y)
    projected_data.append([point[0],true_x,true_y])

print("vector of base")
print("time[s] | x[mm] | y[mm] ")
print(projected_data)
print("")
'''

first = True
i=0
old_point = []
heading = []
for point in projected_data:
    if first :
        old_point = point
        first = False
    else:
        diff_x = old_point[1] - point[1]
        diff_y = old_point[2] - point[2]
        #print("heading: x: ",diff_x,"y: ",diff_y)
        speed = math.sqrt(diff_x ** 2 + diff_y **2)/(point[0] - old_point[0])
        #print ("speed [m/s]: ", speed/1000)
        angle = math.atan(diff_y/diff_x)
        #print("angle", angle*180/pi)
        old_point = point
        heading.append([point[0],diff_x,diff_y,angle*180/pi,speed/1000])
        i+=1

print("Vector of heading")
print("time[s] | x[mm] | y[mm] | angle[deg] | speed[m/s]")
print(np.array(heading))
'''
   