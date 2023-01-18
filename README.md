Research Track I: Assignment 2
================================
This the repository for the solution of Research Track 1 second assignment.
The goal of the assignment is to develop a ROS package containg the develop of three Ros nodes to interact with the envoriment in the package https://github.com/CarmineD8/assignment_2_2022.
The assignment was develop by write the nodes in Python, and add the necessary directory and modify the CMake File in order to make everything work proprely.
In order to make the execution of the code more user friendly a launch file can be found.

How to run the solution
------------------------
First the repository need to be downloaded with the command
'''git clone https://github.com/Francesca-Corrao/RT1_Assignmen2'''
this need to be done inside the src folder of a ROS workspace, then the folder created need to be renamed into 'pkg_assignmnet2'.

As said before to make easy the execution of the file a launch file was made. So what need to be done is:
* start the ROS core: writing the command  ''' roscore''' in a terminal or execute it in background with the command 
* open two different terminal
* in one terminal launch the enviroment provided writing ''' roslaunch assignment_2_2022 assignment1.launch'''
* in the other terminal launch the node developed writing  ''' roslaunch pkg_assignmnet2 ass2.launch'''

How it works
-----------------

### Node A ###
Node A is the first an main node in which 

### Node B ###
it's just a service node

### Node C ###
is  a subscriber
