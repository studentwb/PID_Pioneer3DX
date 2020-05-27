import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time

twist = 0;


def start():
    global pub
    pub = rospy.Publisher('/pioneer_1/RosAria/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/pioneer_1/RosAria/pose', Odometry, pozycja)
    rospy.init_node('vel_controller', anonymous=True)


def set_vel(v, w):
    global twist
    global pub
    twist = Twist()
    twist.linear.x = v
    twist.angular.z = w
    pub.publish(twist)


def pozycja(msg):
    global pose
    pose = str(msg.pose.pose.position.x)


if __name__ == '__main__':
    start()
    cel = input()
    uchyb_past = 0

    while (pozycja != cel):
        pozycja = float(pose[0:5])
        Kp = 0.7
        Td = 50
        uchyb = cel - pozycja
        sterowanie = Kp * uchyb + Td * (uchyb_past - uchyb)
        uchyb_past = uchyb
        set_vel(sterowanie * 0.2, 0)

        rospy.sleep(0.01)
        print
        "------------------------"
        print
        "Aktualna pozycja " + str(pozycja) + "\n" + "Pozostało do przejechania " + str(uchyb)
    print("------------------------")
    set_vel(0, 0)