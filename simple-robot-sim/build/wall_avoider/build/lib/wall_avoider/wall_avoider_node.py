import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            Range,
            '/epuck/range',
            self.sensor_callback,
            10
        )
        self.too_close = False
        self.timer = self.create_timer(0.1, self.move)

    def sensor_callback(self, msg):
        self.too_close = msg.range < 0.1
    
    def move(self):
        cmd = Twist()
        if self.too_close:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        else:
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0
        self.publisher.publish(cmd)

def main(args=None):
        rclpy.init(args=args)
        node = WallAvoider()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()