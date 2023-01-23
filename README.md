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
Node A is the first an main node it's in charge of multiple things:
* Action client node, it takes from input the coordinates the robot has to reach and send them to the Action Server that makthe robot move in order to actually reach them. 
* Service server for node B writing the info about the number of goal reached or canceled on the topic 'ass/goal' using a custom Service 
* Publisher of custom messages on the topic 'ass/pos_vel'.

Let's see the pseudo code of the Node A, and the code of the different functions it uses.

#### main ####
```
python 
main:
  rospy.init() #init Rosnode
  subscribe to Odometry messages 
  start the service on the topic 'ass/goal'
  start the publish of Custom message on the topic 'ass/pos_vel'
  nodeA_client()
```
#### nodeA_client() ####
this is the function that start the action client, take the input from keyboard sernd to the action server and then cancel the goal if the user ask to.
After the coordinates to reach are passed to it by writing some float on the shell when asked, to cancel the goal it look in the terminal in a non blocking way and when 'y' is written it cancel the goal.
```
python
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

#### clbk_odom ####
this is a function called each time message is publish on the '/odom' topic and it will publish a message about the velocity of the robot an the distance it has from the target.





### Node B ###
it's just a service node

### Node C ###
is  a subscriber
