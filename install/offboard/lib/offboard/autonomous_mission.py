#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleCommand

class Mission(Node):
    def __init__(self):
        super().__init__('autonomous_mission')
        self.cmd_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', 10)
        self.timer = self.create_timer(1.0, self.send_arm_command)

    def send_arm_command(self):
        cmd = VehicleCommand()
        cmd.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        cmd.param1 = 1.0
        cmd.command = VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM
        cmd.target_system = 1
        cmd.target_component = 1
        cmd.source_system = 1
        cmd.source_component = 1
        cmd.from_external = True
        self.cmd_pub.publish(cmd)
        self.get_logger().info("Sent ARM command!")

def main(args=None):
    rclpy.init(args=args)
    node = Mission()
    rclpy.spin(node)
    rclpy.shutdown()

