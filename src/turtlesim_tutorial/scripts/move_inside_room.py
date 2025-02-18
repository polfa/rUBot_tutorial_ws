#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import sys

robot_x = 0
robot_y = 0

def pose_callback(pose):
    global robot_x, robot_y, robot_z
    robot_x = pose.x
    robot_y = pose.y
    robot_z = pose.theta
    rospy.loginfo("Robot X = %f\t Robot Y = %f\n",pose.x, pose.y)

def move_turtle(lin_vel,ang_vel,distance):
    global robot_x, robot_y, robot_z
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose',Pose, pose_callback)
    rate = rospy.Rate(10) # 10hz
    vel = Twist()
    while not rospy.is_shutdown():
        vel.linear.x = lin_vel
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = ang_vel
        if (robot_x == 0 or robot_y == 0):
            pass
        elif(robot_x <= 4 or robot_y <= 4 or robot_y >= 7 or robot_x >= 7):
            rospy.loginfo("Robot hits a wall")
            rospy.logwarn("Stopping robot")
            break
        pub.publish(vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('move_inside_room', anonymous=False)#Has to be called here at the begining!
        v= rospy.get_param("~v")
        w= rospy.get_param("~w")
        d= rospy.get_param("~d")
        move_turtle(v,w,d)
    except rospy.ROSInterruptException:
        pass