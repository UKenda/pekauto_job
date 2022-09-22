#!/usr/bin/python3
import rospy
import tf
import math
from geometry_msgs.msg import Twist



def callback(msg):

    start = tf.TransformBroadcaster()
    start.sendTransform((9.521, -35.074, 0),
                        (0,0,0,1),
                        rospy.Time.now(),
                        "start",
                        "world")

    gnss_module = tf.TransformBroadcaster()
    gnss_module.sendTransform((msg.linear.x/1000, msg.linear.y/1000, msg.linear.z),
                            (tf.transformations.quaternion_from_euler(math.radians(msg.angular.x),
                                                                      math.radians(msg.angular.y), 
                                                                      math.radians(msg.angular.z))),
                            rospy.Time.now(),
                            "gnss_module",
                            "world")


rospy.init_node("calculation_node")
rospy.Subscriber("/data", Twist, callback)

rospy.spin()




