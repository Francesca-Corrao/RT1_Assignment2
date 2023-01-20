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
	global position, desired_position
	global send
    # position
	position = msg.pose.pose.position
	linear = msg.twist.twist.linear
	v_angular =msg.twist.twist.angular
    #print(position_)
	send.x=position.x-desired_position.x
	send.y=position.y-desired_position.y
	send.vel_x=linear.x
	send.vel_y=linear.y
	#publish (x,y,vel_x, vel_y)
	#print(send)
	pub.publish(send)

def clbk_srv(req):
	global reached, canc
	return GoalResponse(reached, canc)

	
def nodeA_client():
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
	
	#subscribe to odom to get the position
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
	#service server
	srv = rospy.Service("ass/goal", Goal, clbk_srv)
	#publisher of custom messages
	pub=rospy.Publisher("ass/pos_vel", Custom, queue_size=10)
	#star the action client
	nodeA_client()
		 
	 
	
	

