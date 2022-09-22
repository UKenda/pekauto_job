#!/usr/bin/python3
import rospy
import csv
import time
from geometry_msgs.msg import Twist
import math
import tf


pub_msg = Twist()
pi_deg = 180
pole_lenght = 1.5
rospy.init_node("csv_and_calculation_node")

#reading the CSV file
while not rospy.is_shutdown():
    old_time = 0
    old_row = []
    z = 0
    with open('/home/ubuntu/pekauto_urban_kenda/data.csv', mode ='r')as file:

        csvFile = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
        for row in csvFile: # each row is a list
            if old_time == 0:
                old_time = row[0]
                old_row = row
                pub_msg.angular.z = math.atan(row[2]/row[1])
                pub_msg.linear.z = pole_lenght

            else:
                time.sleep(row[0]-old_row[0])
                z = z + math.sin(-math.radians(old_row[4])) * math.sqrt((row[1]-old_row[1])**2 + (row[2]-old_row[2])**2)/1000
                
                pub_msg.linear.z = z + pole_lenght


                if(row[1]-old_row[1]) < 0:
                    pub_msg.angular.z = math.degrees(math.atan((row[2]-old_row[2])/(row[1]-old_row[1]))) + pi_deg
                else:
                    pub_msg.angular.z = math.degrees(math.atan((row[2]-old_row[2])/(row[1]-old_row[1])))

                old_row = row
            pub_msg.linear.x = row[1]
            pub_msg.linear.y = row[2]
            pub_msg.angular.x = row[3]
            pub_msg.angular.y = row[4]

            start = tf.TransformBroadcaster()
            start.sendTransform((9.521, -35.074, 0),
                                (0,0,0,1),
                                rospy.Time.now(),
                                "start",
                                "world")

            gnss_module = tf.TransformBroadcaster()
            gnss_module.sendTransform((pub_msg.linear.x/1000, pub_msg.linear.y/1000, pub_msg.linear.z),
                                    (tf.transformations.quaternion_from_euler(math.radians(pub_msg.angular.x),
                                                                            math.radians(pub_msg.angular.y), 
                                                                            math.radians(pub_msg.angular.z))),
                                    rospy.Time.now(),
                                    "gnss_module",
                                    "world")
