#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint


class DopreduNode(Node):
    def __init__(self):
        super().__init__('dopredu_node')

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos)
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos)

        self.counter = 0
        self.timer = self.create_timer(0.1, self.timer_callback)

    def send_offboard_control_mode(self):
        """Ensure the drone is in OFFBOARD mode"""
        msg = OffboardControlMode()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = True  # Position control
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        self.offboard_mode_pub.publish(msg)
        self.get_logger().info("OFFBOARD mode activated.")

    def send_setpoint(self, x, y, z):
        """Send the desired setpoint"""
        msg = TrajectorySetpoint()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = [x, y, z]
        msg.yaw = 0.0  # Optional: Yaw control
        self.trajectory_pub.publish(msg)
        self.get_logger().info(f"Sending setpoint: x={x}, y={y}, z={z}")

    def timer_callback(self):
        """Callback for timer to send control messages"""
        # Keep sending the OFFBOARD mode message
        self.send_offboard_control_mode()

        # Let the drone fly forward to 10 meters in the x direction (no backward motion)
        if self.counter < 30:
            self.send_setpoint(x=10.0, y=0.0, z=-5.0)  # Increased distance for visible movement
        elif self.counter > 30:
            self.get_logger().info('Dron zůstává na místě. Ukončuji node.')
            self.destroy_node()

        self.counter += 1


def main(args=None):
    """Main function to run the ROS 2 node"""
    rclpy.init(args=args)
    node = DopreduNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

