#!/usr/bin/env python
import rospy
import actionlib
import time
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from std_msgs.msg import String

###### Code infomation ######
# Version V1.2.0            #
# Date    Sep.24 2020       #
# Note    *From Yuntech     #
#         *Fix bugs         #
#############################

class map_navigation():
    def __init__(self):
        #set point
        #home
        self.xHome = -0.00216
        self.yHome = 0.0155
        #Table 1
        self.xTable1 = 4.05
        self.yTable1 = 0.557
        #Table 2
        self.xTable2 = 3.71
        self.yTable2 = -1.06
        #Table 3
        self.xTable3 = 6.94
        self.yTable3 = 0.636
        #Table 4
        self.xTable4 = 5.8
        self.yTable4 = -0.822
        
        #Others
        self.goalReached = False
        self.datatemp = '' #Check info from zbar
        self.times = 0 #Times for callback
        
        #make a node and ready
        rospy.init_node('qr_code_py', anonymous=True)
        rospy.loginfo("qr_code ready")
        
        #ask for table and to go
        self.table()

        rospy.loginfo("Wait for zbar_opencv")

        while(self.times != 2):
            #wait for qr code 
            rospy.Subscriber('zbar_opencv_code', String, self.callback)

        rospy.loginfo("exit")    


    #Check data from zbar and do something
    def callback(self,data):
        if data.data != self.datatemp:
            #Print qr code
            rospy.loginfo("ready2")
            
            if data.data == 'Cola':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xHome, self.yHome)
                self.check(self.goalReached)
                self.table()

            elif data.data == 'apple juice':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xHome, self.yHome)
                self.check(self.goalReached)
                self.table()

            elif data.data == 'water':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xHome, self.yHome)
                self.check(self.goalReached)
                self.table()

            elif data.data == 'none':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xHome, self.yHome)
                self.check(self.goalReached)
        
            rospy.loginfo("   ")
            self.datatemp = data.data
            self.times +=  1
            rospy.loginfo("Wait for zbar_opencv")


    #chooce table
    def chooce(self):
        self.choice = ''
        #print infomation
        rospy.loginfo("|--------TIRT2021--------|")
        rospy.loginfo("|PRESSE A KEY:           |")
        rospy.loginfo("|'1',Table1              |")
        rospy.loginfo("|'2',Table2              |")
        rospy.loginfo("|'3',Table3              |")
        rospy.loginfo("|'4',Table4              |")
        rospy.loginfo("|'q',Quit(beta)          |")
        rospy.loginfo("|------------------------|")
        rospy.loginfo('Where to go')
        
        self.choice = input()
        return self.choice


    #Send point to move_base node 
    def moveToGoal(self,xGoal,yGoal):
        #define a client for to send goal requests to the move_base server through a SimpleActionClient
        ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        #wait for the action server to come up
        while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
            rospy.loginfo("Waiting for the move_base action server to come up")

        goal = MoveBaseGoal()

        #set up the frame parameters
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # moving towards the goal*/
        goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo("Sending goal location ...")
        ac.send_goal(goal)

        #for x in range(30):
        ac.wait_for_result(rospy.Duration(60))
            #rospy.sleep(1.0)
            #rospy.loginfo("%d",ac.get_state())

        if(ac.get_state() ==  GoalStatus.SUCCEEDED):
            rospy.loginfo("You have reached the destination")
            return True

        else:
            rospy.loginfo("The robot failed to reach the destination")
            return False


    #chooce table
    def table(self): 
        self.choice = self.chooce()

        #Chack each table          
        if (self.choice == 1):
            self.goalReached = self.moveToGoal(self.xTable1, self.yTable1)
            self.check(self.goalReached)
                        
        elif (self.choice == 2):
            self.goalReached = self.moveToGoal(self.xTable2, self.yTable2)
            self.check(self.goalReached)
            
        elif (self.choice == 3):
            self.goalReached = self.moveToGoal(self.xTable3, self.yTable3)
            self.check(self.goalReached)
            
        elif (self.choice == 4):
            self.goalReached = self.moveToGoal(self.xTable4, self.yTable4)
            self.check(self.goalReached)
            
        #delsy 3s
        rospy.loginfo("Waiting...")
        time.sleep(3)
        rospy.loginfo("Next")


    #Check for robot 
    def check(self,goalReached):
        if (self.goalReached):
            rospy.loginfo("Congratulations!")
            
        else:
            rospy.loginfo("Hard Luck!")

        return 0


if __name__ == '__main__':
        map_navigation()
        rospy.spin()       
