import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2

PUBLISH_RATE = 1.0 / 15.0  # 15 FPS


class CamNode(Node):
    def __init__(self):
        super().__init__("cam_node")
        self.publisher = self.create_publisher(Image, "/image_raw", 10)
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.timer = self.create_timer(PUBLISH_RATE, self.timer_callback)
        self.bridge = CvBridge()
        self.logger = self.get_logger()
        self.frame_count = 0

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.logger.warning("Failed to capture frame")
            return
        msg = self.bridge.cv2_to_imgmsg(frame)
        self.publisher.publish(msg)
        self.logger.info("Frame published %d" % (self.frame_count))
        self.frame_count += 1


def main(args=None):
    rclpy.init(args=args)
    cam = CamNode()
    rclpy.spin(cam)
    cam.destroy_node()
    rclpy.shutdown()
