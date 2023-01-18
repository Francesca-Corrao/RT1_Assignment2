#! /usr/bin/env python

import rospy 
from pkg_assignment2.srv import Goal

if __name__ == '__main__':
	#initialized the rospy node
	rospy.init_node('nodeB_py')
	
	#service client init
	rospy.wait_for_service("ass/goal")
	client = rospy.ServiceProxy("ass/goal", Goal)
	resp = client(1)
	print(resp)
