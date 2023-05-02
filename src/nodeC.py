#! /usr/bin/env python
"""
.. module:: nodeC
	:synopsis: Python module in charge of print robot current velocity and distance from target whit a certain frequency.
.. moduleauthor:: Francesca Corrao

This node subscribes to the messages *Custom* published by :mod:`nodeA` and updates the value of robot current velocity and distance from target. Then it printes them with a frequency which is set in the ros parameter *my_freq*.

Subscriber:
	ass/pos_vel
	
Ros parameter:
	my_freq
"""
import rospy
import time
from pkg_assignment2.msg import Custom
from nav_msgs.msg import Odometry

global x,y,vel_x, vel_y


def clbk(msg):
	"""
	Callback function executed each time a new message of type *Custom* is publish on the topic 'ass/pos_vel'.
	The function updates the value of the node variables containg information about robot current velocity and distance from target.

	"""

	global x,y,vel_x, vel_y
	x=msg.x 
	y=msg.y
	vel_x=msg.vel_x
	vel_y=msg.vel_y
	
	
if __name__== '__main__':
	global x,y,vel_x, vel_y
	x=0 
	""" x(float) distance from target on x axis
	"""
	y=0 
	""" y(float) distance from target on y axis
	"""
	vel_x=0 
	""" vel_x(float) linear velocity of the robot on x axis
	"""
	vel_y=0 
	""" vel_y(float) linear velocity of the robot on y axis
	"""
	#initialize rospy node
	rospy.init_node("nodeC_py")
	sub = rospy.Subscriber("ass/pos_vel", Custom, clbk); 
	""" sub: Subscriber to ass/pos_vel
	"""
	freq=rospy.get_param("my_freq")
	while not rospy.is_shutdown():
		time.sleep(freq)
		rospy.loginfo("target_distance (x:%f, y:%f) velocity(v_x:%f, v_y %f)", x, y, vel_x, vel_y)
		

