import rclpy
from rclpy.node import Node
from controller import Robot


class WallAvoider(Node):
    def __init__(self, robot):
        super().__init__('wall_avoider')
        self.robot = robot
        timestep = int(robot.getBasicTimeStep())

        self.sensors = []
        for i in range(8):
            ps = robot.getDevice(f'ps{i}')
            ps.enable(timestep)
            self.sensors.append(ps)

        self.left_motor = robot.getDevice('left wheel motor')
        self.right_motor = robot.getDevice('right wheel motor')
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

        self.timestep = timestep
        self.get_logger().info('Wall avoider ready!')

    def step(self):
        if self.robot.step(self.timestep) == -1:
            return False

        front = max(self.sensors[0].getValue(), self.sensors[7].getValue())

        if front > 80:
            self.left_motor.setVelocity(-3.0)
            self.right_motor.setVelocity(3.0)
        else:
            self.left_motor.setVelocity(3.0)
            self.right_motor.setVelocity(3.0)

        return True


def main(args=None):
    rclpy.init(args=args)
    robot = Robot()
    node = WallAvoider(robot)

    while rclpy.ok():
        if not node.step():
            break
        rclpy.spin_once(node, timeout_sec=0)

    node.destroy_node()
    rclpy.shutdown()