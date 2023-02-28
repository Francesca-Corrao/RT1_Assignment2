"""
.. module:: nodeA
	:platform: unix
	:synopsis: Python module in charge of sending the position the robot has to reach
.. moduleauthor:: Francesca Corrao

This node implement a controller for the robot in the envoiroment of the package `assignmnet_2_2022 <https://github.com/CarmineD8/assignment_2_2022>`.
It ask the user to insert the coordinates the robot has to reach and then giv ethe user to cancel them until the robot hasn't reached them.
The nodes also publish the robot's velocity and position and it's the server of a service providing information about the number of position reached and cancelled.

Subscriber:
	/odom

Publisher:
	ass/pos_vel

Server:
	ass/goal
	
Action Client:
	/reaching_goal
	
"""

#! /usr/bin/env python

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
import time
import math
import select
import sys
from geometry_msgs.msg import  Pose, Point, PoseStamped, Vector3
from nav_msgs.msg import Odometry
from pkg_assignment2.msg import Custom
from pkg_assignment2.srv import Goal, GoalResponse

target = PoseStamped()
position = Point()
desired_position = Point()
dist_precision = 0.5
v_linear =Vector3()
v_angular = Vector3()
send=Custom()
canc=0
reached=0

def clbk_odom(msg):
	"""
	callback function that publish robot velocity and distance from the desired position.
	It reads robot current position and velocity and compute the distance from the desired position.
	Then set the correct field of the message to pubblish and publish it.
	This will be then used by :mod:`nodeC`
	
	Args:
	msg(nav_msgs::Odometry)
	
	"""

	global position, desired_position
	global send
    #read position of the robot from msg
	position = msg.pose.pose.position
	#read linear and angular velocity of the robot from msg
	linear = msg.twist.twist.linear
	v_angular =msg.twist.twist.angular
	#set the field of the msg to publish 
	send.x=position.x-desired_position.x
	send.y=position.y-desired_position.y
	send.vel_x=linear.x
	send.vel_y=linear.y
	#publish msg
	pub.publish(send)

def clbk_srv(req):
	"""
	callback function executed upon request by the service server.
	The function send as response the number of goal(position) reached by the robot and the number of goal cancelled.
	The service and this function are used by :mod:`nodeB`
	
	Args:
	req(GoalRequest): null
	
	"""
	global reached, canc
	#send the service response
	return GoalResponse(reached, canc)

	
def nodeA_client():
	"""
	This function initialize a *assignment_2_2022.msg::Planning* Action client and wait for the server.
	Once a server is found in a while loop the function:
	-asks the user to insert the cordinate to reach
	-sends them to the action server 
	-cancel the goal if the user asks to
	Once the goal is reached or canceled the instructions above are executed again.
		
	The cordinates to reach are of type *geometry_msgs::Point* and only the value of x and y are set by the user. They are taken from input as two different float and then set the corresponding field of the *geometry_msgs::Point* variable.
	The coordinates to reach are then send to the *assignment_2_2022.msg::Planning* ActionServer as goal
	 	
	"""
	
	#create the action client
	global target, position, desired_position, dist_precision,send,canc, reached
	client = actionlib.SimpleActionClient('/reaching_goal', 	assignment_2_2022.msg.PlanningAction)
	print("Node A")
	client.wait_for_server()
	print("server found")
	
	while(1):
		print("Taking new coordinates to reach (x,y)")
		#take input from keyboard(x,y)
		val= input("Enter the value(integer) of x to reach:\n");
		x=float(val);
		val= input("Enter the value(integer) of y to reach:\n");
		y=float(val);
		
		#update the target pose
		target.pose.position.x=x
		target.pose.position.y=y
		
		desired_position.x=x
		desired_position.y=y
		#set the pose to be the goal
		goal = assignment_2_2022.msg.PlanningGoal(target_pose = target)
	
		#send the goal
		client.send_goal(goal)
		
		err_pos = math.sqrt(pow(desired_position.y - position.y, 2) +
                        pow(desired_position.x - position.x, 2))
		#while target isn't reach
		print("When you want to cancel the goal press y on keyboard")
		while(err_pos>dist_precision):
			put = select.select([sys.stdin],[],[],1)[0]
			err_pos = math.sqrt(pow(desired_position.y - position.y, 2) +
                        pow(desired_position.x - position.x, 2))
			if err_pos<dist_precision :
				break
			if put: 
				v=sys.stdin.readline().rstrip()

				if v=='y':
				#cancel the goal
					client.cancel_goal()
					canc+=1
					print("goal cancelled")
					break
				else:
				#don't cancel the goal
					print("invalid input-reaching the goal")
			else:
				err_pos = math.sqrt(pow(desired_position.y - position.y, 2) +
                        pow(desired_position.x - position.x, 2))
		if(err_pos<dist_precision):
			reached+=1
			print("Goal reached !")


if __name__ == '__main__':
	#initialize the rospy node 
	rospy.init_node('nodeA_py') 
	""" initialize the node
	"""
	
	#subscribe to odom to get the position
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
	""" sub_odom: Subscriber to \odom to receive messages describing robot position and velocity
	"""
	#service server
	srv = rospy.Service("ass/goal", Goal, clbk_srv)
	""" srv: Server for the Service Goal on topic ass/goal
	"""
	#publisher of custom messages
	pub=rospy.Publisher("ass/pos_vel", Custom, queue_size=10)
	""" pub: Publisher for the robot's velocity and distance from target on topic ass/pos_vel
	"""
	#star the action client
	nodeA_client()
		 
	 
	
	

