import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class SimpleNavigationController(Node):
    def __init__(self):
        #2. Initialze a ros node
        super().__init__('SimpleNavigationController')

        #3. Create a subscriber to the /scan topic using as a callback function the already existing function inside the class called clbk_laser
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.clbk_laser, qos_profile_sensor_data)
        # prevent unused variable warning
        self.scan_sub 
        #4. Create a publisher to the /cmd_vel topic
        self.cmdvel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        #default values for the lidar variables as a placeholder until the actual sensor values are recieved through from the ros topic
        self.lidar_left_front = 100
        self.lidar_right_front = 100
        self.finished = False

        # self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0     

    #Callback function for the Turtlebots Lidar topic ("/scan")
    def clbk_laser(self, msg):
        self.lidar_left_front = msg.ranges[40]
        self.lidar_right_front = msg.ranges[320]

    def timer_callback(self):
        # msg = String()
        # msg.data = 'Hello World: %d' % self.i
        # self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1

        #Creates a message from type Twist
        vel_msg = Twist()
        #Defines the speed at which the robot will move forward (value between 0 and 1)
        vel_msg.linear.x = 0.1
        #Defines the speed at which the robot will turn around its own axis (value between -1 and 1)
        vel_msg.angular.z = 0.0

        lidar_threshold = 0.35
        vel_msg.angular.z = 0.0
        print("left_front: ",self.lidar_left_front, " right_front: ", self.lidar_right_front)
        if self.lidar_left_front < lidar_threshold and self.lidar_right_front < lidar_threshold:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            self.finished = True
        else:
            if self.lidar_left_front < lidar_threshold:
                vel_msg.angular.z -= 0.45
            if self.lidar_right_front < lidar_threshold:
                vel_msg.angular.z += 0.45

        #Publish vel_msg
        self.cmdvel_pub.publish(vel_msg)

        # if self.finished:
        #     print("finished")
        #     self.destroy_node()

    def runNavigation(self):
        #Creates a message from type Twist
        vel_msg = Twist()
        #Defines the speed at which the robot will move forward (value between 0 and 1)
        vel_msg.linear.x = 0.7
        #Defines the speed at which the robot will turn around its own axis (value between -1 and 1)
        vel_msg.angular.z = 0.0

        #Defines the frequency in Hz in which the following loop will run
        # r = self.create_rate(10.0)
        finished = False
        while not finished:
            print("running")
            #Set vel_msg.linear.x and vel_msg.angular.z depending on the values from self.lidar_left_front and self.lidar_right_front
            #When the robot reaches the finish of the obstacle course set finished to True

            lidar_threshold = 1.5
            vel_msg.angular.z = 0.0
            if self.lidar_left_front < lidar_threshold and self.lidar_right_front < lidar_threshold:
                vel_msg.linear.x = 0.0
                vel_msg.angular.z = 0.0
                finished = True
            else:
                if self.lidar_left_front < lidar_threshold:
                    vel_msg.angular.z -= 0.5
                if self.lidar_right_front < lidar_threshold:
                    vel_msg.angular.z += 0.5

            #Publish vel_msg
            self.cmdvel_pub.publish(vel_msg)

            #sleeps for the time needed to ensure that the loop will be executed with the previously defined frequency
            # r.sleep()

        return True


def main(args=None):
    rclpy.init(args=args)

    controller = SimpleNavigationController()

    rclpy.spin(controller)
    # future = controller.runNavigation()
    # print("test")
    # rclpy.spin_until_future_complete(controller,future)
    # controller.runNavigation()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()