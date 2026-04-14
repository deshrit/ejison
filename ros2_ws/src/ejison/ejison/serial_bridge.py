import rclpy
from rclpy.node import Node
import serial
from core.msg import StepperCommand, WheelSteps
import time

DEFAULT_SERIAL_PORT = "/dev/ttyACM0"
DEFAULT_BAUD_RATE = 115200


MAX_SPEED = 200


class SerialBridge(Node):
    def __init__(self):
        super().__init__("serial_bridge")
        self.logger = self.get_logger()
        self.subscription = self.create_subscription(
            StepperCommand, "/stepper_command", self._command_callback, 10
        )
        self.publisher = self.create_publisher(WheelSteps, "/wheel_steps", 10)
        self.ser = self._init_serial()
        self.read_timer = self.create_timer(0.1, self._read_serial)

    def _get_serial(self) -> serial.Serial:
        ser = serial.Serial(DEFAULT_SERIAL_PORT, DEFAULT_BAUD_RATE, timeout=0.1)
        time.sleep(1.0)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        return ser

    def _write_cmd(self, ser: serial.Serial, cmd: str) -> None:
        if ser.is_open:
            ser.write((cmd + "\n").encode())
            ser.flush()
            self.logger.info(f"Command written: {cmd}")
            return
        self.logger.warning(f"Serial is not open; Error writing cmd: {cmd}")

    def _init_serial(self) -> serial.Serial:
        ser = self._get_serial()
        self.logger.info("Serial Initialized")
        self._write_cmd(ser, "d")  # Start publishing
        return ser

    def _command_callback(self, msg: StepperCommand) -> None:
        left = int(msg.left_step_rate)
        right = int(msg.right_step_rate)
        left = max(min(left, MAX_SPEED), -MAX_SPEED)
        right = max(min(right, MAX_SPEED), -MAX_SPEED)
        cmd = f"d {left} {right}"
        self._write_cmd(self.ser, cmd)

    def _read_serial(self) -> None:
        msg = WheelSteps()
        if self.ser.is_open:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode(errors="ignore").strip()
                try:
                    left, right = map(int, data.split())
                    msg.left_steps = left
                    msg.right_steps = right
                    msg.stamp = self.get_clock().now().to_msg()
                    self.publisher.publish(msg)
                    self.logger.info(f"Left step: {left}, Right step: {right}")
                except Exception:
                    self.logger.warn(f"Bad serial read: {data}")
            return
        self.logger.warning("Serial is not open")

    def destroy_node(self):
        super().destroy_node()
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.logger.info("Serial port closed")


def main(args=None):
    rclpy.init(args=args)
    serial_bridge = SerialBridge()
    try:
        rclpy.spin(serial_bridge)
    except KeyboardInterrupt:
        pass
    finally:
        serial_bridge.destroy_node()
