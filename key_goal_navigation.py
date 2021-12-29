#! /usr/bin/python3


from rospy.core import is_shutdown
from rospy.topics import Publisher
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import rospy
from move_base_msgs.msg import MoveBaseActionResult

import sys
import select
import time


goal_msg = PoseStamped()

tables = []

# add goal table position.
# tables.append([x, y, z, x, y, z, w])
# tables.append("Table 0's position data")
# tables.append("Table 1's position data")
# tables.append("Table 2's position data")
# tables.append("Table 3's position data")


tables.append([2.619, 0.9, 0.0, 0.0, 0.0, 0.654, 0.7563])
tables.append([0.52, 3.32, 0.0, 0.0, 0.0, 0.97, 0.244])
tables.append([-0.2, 1.46, 0.0, 0.0, 0.0, 0.913, -0.4068])
tables.append([-2.21, 3.41, 0.0, 0.0, 0.0, -0.456, 0.89])

status = 0

def result_cb(result):
    global status

    # canceled
    if result.status.status == 2:
        status = 2

    # reached
    if result.status.status == 3:
        # status = 3
        
        # Wait for 10s, return to table 0
        rospy.loginfo("Reached table, wait for 10 secs.")
        time.sleep(10)
        goal_publisher(0)
    
def goal_publisher(table_num):
    global goal_msg
    goal_msg.header.frame_id='map'
    goal_msg.pose.position.x = tables[table_num][0]
    goal_msg.pose.position.y = tables[table_num][1]
    goal_msg.pose.position.z = tables[table_num][2]
    goal_msg.pose.orientation.x = tables[table_num][3]
    goal_msg.pose.orientation.y = tables[table_num][4]
    goal_msg.pose.orientation.z = tables[table_num][5]
    goal_msg.pose.orientation.w = tables[table_num][6]
    
    goal_pub.publish(goal_msg)


if __name__=='__main__':
    rospy.init_node('goal_sender', anonymous=True)
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    reach_sub = rospy.Subscriber('/move_base/result', MoveBaseActionResult, result_cb)
    # 1 Hz (not continuous)
    rate = rospy.Rate(1)

    # Get keyboard input
    while not rospy.is_shutdown():
        # table_number = int(input("choose a table"))
        input_key = select.select([sys.stdin],[], [], 1)[0]
        if input_key:
            table_number = int(sys.stdin.readline().rstrip())

            print("TN : ", table_number)
            if table_number in [0, 1, 2, 3]:
                goal_publisher(table_number)
        
        rate.sleep()
    
    rospy.spin()
