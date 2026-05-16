import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range


class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.ranges = {}
        for i in range(8):
            self.create_subscription(
                Range,
                f'/ps{i}',
                lambda msg, i=i: self.sensor_callback(i, msg),
                10
            )
        self.timer = self.create_timer(0.1, self.move)

    def sensor_callback(self, index, msg):
        self.ranges[index] = msg.range

    def move(self):
        cmd = Twist()
        front_right = self.ranges.get(0, 999)
        front_left  = self.ranges.get(7, 999)
        front = min(front_right, front_left)
        if front < 0.06:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        else:
            cmd.linear.x = 0.05
            cmd.angular.z = 0.0
        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = WallAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()