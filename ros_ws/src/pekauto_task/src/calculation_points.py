#!/usr/bin/python3
import rospy
import csv
import time

import math
import tf
import os 
import rospkg
import numpy as np


#inicialization
rospack = rospkg.RosPack()
rospy.init_node("csv_and_calculation_node")
post_length = 1.5 #[m]
data = []
old_row = []
x = 0
y = 0
z = 0
roll = 0
pithc = 0
yaw = 0
pi_deg = 180 #[deg]

with open(os.path.join(rospack.get_path("pekauto_task"), "src", "data.csv"), mode ='r')as file:
    csvFile = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
    for row in csvFile: 
        data.append(row)

#continius loop
while not rospy.is_shutdown():
    #reseting the variables for each new loop
    old_time = 0
    first_data = True
    old_row = []
    z = 0

    for row in data: 
        #for first data it cannot calculate
        if first_data:
            first_data = False
            old_row = row

        else:
            #it refresh at tge time that was recorded
            time.sleep(row[0]-old_row[0])

            #it calculate a hight, from pithc and the length that was traveled
            z = z + math.sin(-math.radians(old_row[4])) * math.sqrt((row[1]-old_row[1])**2 + (row[2]-old_row[2])**2)/1000

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
            gps_translation = [[1,0,0,x],[0,1,0,y],[0,0,1,post_length],[0,0,0,1]]
            roll_rotation = [[1,0,0,0],[0,math.cos(roll),-math.sin(roll),0],[0,math.sin(roll),math.cos(roll),0],[0,0,0,1]]
            pitch_rotation = [[math.cos(pitch),0,math.sin(pitch),0],[0,1,0,0],[-math.sin(pitch),0,math.cos(pitch),0],[0,0,0,1]]
            yaw_rotation = [[math.cos(yaw),-math.sin(yaw),0,0],[math.sin(yaw),math.cos(yaw),0,0],[0,0,1,0],[0,0,0,1]]

            base = np.dot(np.dot(np.dot(np.dot(gps_translation,roll_rotation),pitch_rotation),yaw_rotation),[[0],[0],[-post_length],[1]])
            base[2] = z

            #publishing a start point
            start = tf.TransformBroadcaster()
            start.sendTransform((9.48194, -34.867, 0),
                                (0,0,0,1),
                                rospy.Time.now(),
                                "start",
                                "world")
            #publishing a gnss point
            base_link = tf.TransformBroadcaster()
            base_link.sendTransform((base[0], base[1], base[2]),
                                    (tf.transformations.quaternion_from_euler(roll,pitch,yaw)),
                                    rospy.Time.now(),
                                    "base_link",
                                    "world")
            old_row = row


        
