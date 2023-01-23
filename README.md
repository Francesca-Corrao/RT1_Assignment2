Research Track I: Assignment 2
================================
This the repository for the solution of Research Track 1 second assignment.
The goal of the assignment is to develop a ROS package containing the develop of three Ros nodes to interact with the envoriment provided in the package https://github.com/CarmineD8/assignment_2_2022 that make the robot move in an arena.
The assignment was develop by write the nodes in Python, and add the necessary directory and modify the CMake File in order to make everything work proprely.
In order to make the execution of the code more user friendly a launch file can be found.

How to run the solution
------------------------
First the repository need to be downloaded with the command
``` git clone https://github.com/Francesca-Corrao/RT1_Assignmen2 ```
this need to be done inside the src folder of a ROS workspace, then the folder created need to be renamed into 'pkg_assignmnet2'.

As said before to make easy the execution of the file a launch file was made. So what need to be done is:
* start the ROS core: writing the command  ``` roscore``` in a terminal or execute it in background with the command 
* open two different terminal
* in one terminal launch the enviroment provided writing ``` roslaunch assignment_2_2022 assignment1.launch```
* in the other terminal launch the node developed writing  ``` roslaunch pkg_assignmnet2 ass2.launch ```.
The launch file only start nodeA and nodeC because they are the only nodes who have to work all the time. 
NodeB execute only when called, and to run it in a terminal need to write the command ```rosrun pkg_assignment2 nodeB.py ```

How it works
-----------------

### Node A ###
Node A is the main node and it's in charge of multiple things:
* Action client node, it takes from input the coordinates the robot has to reach and send them to the Action Server that makthe robot move in order to actually reach them. 
* Service server send when a request is made the info about the number of goal reached or canceled on the topic 'ass/goal' using a custom Service Goal.
* Publisher of custom messages (defined as Custom) on the topic 'ass/pos_vel'.

Let's see the pseudo code of the Node A, and the code of the different functions used.

#### main ####
```python 
#import all the necessary library
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

#define global variables used by different function
target = PoseStamped()
position = Point()
t_precision = 0.5
send=Custom()
canc=0
reached=0

main:
  rospy.init() #init Rosnode
  rospy.Subscriber('/odom', Odometry, clbk_odom) #subscribe to Odometry messages 
  rospy.Service("ass/goal", Goal, clbk_srv) #start the service on the topic 'ass/goal'
  pub=rospy.Publisher("ass/pos_vel", Custom, queue_size=10) #start the publish of Custom message on the topic 'ass/pos_vel'
  nodeA_client()
```
#### nodeA_client() ####
this is the function that start the action client, take the input from keyboard sernd to the action server and then cancel the goal if the user ask to.
After the coordinates to reach are passed to it by writing some float on the shell when asked, to cancel the goal it look in the terminal in a non blocking way and when 'y' is written it cancel the goal.
``` python 
def nodeA_client();
  client = actionlib.SimpleActionClient() #start action client
  client.wait_for_server() #wait until the action server isn't start
  while(true):
    x=input(x); #take x value
    y=input(y) #take y value
    target.x=x
    target.y=y
    
    goal = assignment_2_2022.msg.PlanningGoal(target) #set the goal to be the coordinates taken as input
    client.send_goal(goal) #send the goal to the server
    
    err_pos #compute error position
    dist_precision #threshold to reach the goal
    while(err_pos>dist_precision):
      select(stadin) #look if there are info on standard in
      recompute err_pos
      if select:
        v=read from stdin
        if v='y':
          client.cancel_goal()
          cancel +=1
          break
        else: 
          printf("input non valid")
          break
      else:
        recompute err_pos
    if(err_pos < dist_precision):
      reached +=1
```

#### clbk_odom() ####
this is a function called each time message is publish on the '/odom' topic and it will publish a message about the velocity of the robot an the distance it has from the target.
```python 
def clbk_odom(msg):
  position = msg.position
  linear = msg.linear
  send.x=position.x-target.x
	send.y=position.y-target.y
	send.vel_x=linear.x
	send.vel_y=linear.y
  pub.publish(send) #publish the customer server
```
#### clbk_serv() ####
function called each time the service it's requested
```python
  def clbk_srv():
    return GoalResponse(reached, canc)
```

### Node B ###
It's a node that make a request to the service server on topic 'ass/goal' to know the number of goal reached and the number of goal cancelled. After it receive the response and print the result obtained it end its execution.

### Node C ###
It's a node subscribed to the custtome message public on the topic 'ass/pos' from which read the distance the robot has from the target  and the velocity of the robot and print them whit a frequency set in a ros parameter.

### Launch file ###
the launch file it's a very helpful tool for a ROS package because it could start nodes, set parameter and call other launch files. 

The launch file written for this assignment it's in charge to set the parameter use by NodeC to set the frequency to print the informations read and then launch NodeA and NodeC.
It doesn't launch NodeB because it's execution end once it print the result and if it's launched at the beginning there aren't any goal send yet so it will print only 0,0.


