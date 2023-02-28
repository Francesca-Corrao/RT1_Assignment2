#! /usr/bin/env python
"""
.. module:: nodeB
	:synopsis: Python module in charge of print number of goal reached and cancelled
.. moduleauthor:: Francesca Corrao

This node send a request to the *Goal* Service and print it's response, whcih contain the number of goal reached by the robot and the number of goal the user cancel.

Client of:
	ass/goal
"""

import rospy 
from pkg_assignment2.srv import Goal

if __name__ == '__main__':
	#initialized the rospy node
	rospy.init_node('nodeB_py')
	""" Initialize the node.
	"""
	
	#service client init
	rospy.wait_for_service("ass/goal")
	client = rospy.ServiceProxy("ass/goal", Goal) 
	""" client: Client for the Service Goal on topic ass/goal.
	"""
	resp = client(1) 
	""" resp(GoalResponse): contain the server response.
	"""
	print(resp)
