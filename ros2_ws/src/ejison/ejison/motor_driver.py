import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from core.msg import StepperCommand


WHEEL_RADIUS = 0.0325
WHEEL_BASE = 0.18
STEPS_PER_REV = 2048  # 28BYJ-48 motor


class MotorDriver(Node):
    def __init__(self):
        super().__init__("motor_driver")
        self.subscription = self.create_subscription(
            Twist, "/cmd_vel", self.command_callback, 10
        )
        self.publisher = self.create_publisher(StepperCommand, "/stepper_command", 10)
        self.logger = self.get_logger()

        self.logger.info("Motor driver initialized")

    def command_callback(self, msg: Twist):
        v = msg.linear.x
        w = msg.angular.z

        self.logger.info(f"Twist message x: {v}, z: {w}")

        left_vel = v - w * WHEEL_BASE / 2
        right_vel = v + w * WHEEL_BASE / 2

        left_rate = (left_vel / (2 * 3.1415 * WHEEL_RADIUS)) * STEPS_PER_REV
        right_rate = (right_vel / (2 * 3.1415 * WHEEL_RADIUS)) * STEPS_PER_REV

        cmd = StepperCommand()
        cmd.left_step_rate = left_rate
        cmd.right_step_rate = right_rate

        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    motor_driver = MotorDriver()
    rclpy.spin(motor_driver)
    motor_driver.destroy_node()
    rclpy.shutdown()
