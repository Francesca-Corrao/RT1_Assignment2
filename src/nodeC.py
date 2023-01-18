#! /usr/bin/env python
import rospy
import time
from pkg_assignment2.msg import Custom
from nav_msgs.msg import Odometry

global x,y,vel_x, vel_y


def clbk(msg):
	global x,y,vel_x, vel_y
	x=msg.x 
	y=msg.y
	vel_x=msg.vel_x
	vel_y=msg.vel_y
	

def clbk_odom(msg):
	rospy.loginfo("odom)position (x:%f, y:%f) velocity(v_x:%f, v_y %f)", msg.pose.pose.position.x, msg.pose.pose.position.y, msg.twist.twist.linear.x, msg.twist.twist.linear.y)
	
	
if __name__== '__main__':
	global x,y,vel_x, vel_y
	x=0
	y=0
	vel_x=0
	vel_y=0
	#initialize rospy node
	rospy.init_node("nodeC_py")
	sub = rospy.Subscriber("ass/pos_vel", Custom, clbk);
	#sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
	freq=rospy.get_param("my_freq")
	while not rospy.is_shutdown():
		time.sleep(freq)
		rospy.loginfo("position (x:%f, y:%f) velocity(v_x:%f, v_y %f)", x, y, vel_x, vel_y)
		

