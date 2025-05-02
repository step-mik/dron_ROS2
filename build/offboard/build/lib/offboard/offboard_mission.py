#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleStatus
import time


class OffboardMission(Node):
    def __init__(self):
        super().__init__('offboard_mission')
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos)
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos)
        self.command_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos)

        self.status_sub = self.create_subscription(VehicleStatus, '/fmu/out/vehicle_status', self.status_cb, qos)
        self.vehicle_status = VehicleStatus()

        self.counter = 0
        self.phase = 'waiting'
        self.hover_start_time = None
        self.timer = self.create_timer(0.1, self.control_loop)

    def status_cb(self, msg):
        self.vehicle_status = msg

    def send_vehicle_command(self, command, param1=0.0, param2=0.0):
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.param1 = param1
        msg.param2 = param2
        msg.command = command
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        self.command_pub.publish(msg)

    def send_offboard_mode(self):
        msg = OffboardControlMode()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        self.offboard_mode_pub.publish(msg)

    def send_position(self, x, y, z, yaw=0.0):
        msg = TrajectorySetpoint()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = [x, y, z]
        msg.yaw = yaw
        self.trajectory_pub.publish(msg)

    def control_loop(self):
        self.send_offboard_mode()

        if self.counter == 10 and self.phase == 'waiting':
            self.get_logger().info('Switching to OFFBOARD and arming...')
            self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
            self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)
            self.phase = 'takeoff'

        elif self.phase == 'takeoff':
            self.send_position(0.0, 0.0, -5.0)
            if self.counter > 30:
                self.hover_start_time = self.get_clock().now().seconds_nanoseconds()[0]
                self.phase = 'hover'
                self.get_logger().info('Hovering...')

        elif self.phase == 'hover':
            self.send_position(0.0, 0.0, -5.0)
            current_time = self.get_clock().now().seconds_nanoseconds()[0]
            if current_time - self.hover_start_time > 10:
                self.get_logger().info('Landing...')
                self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)
                self.phase = 'land'

        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = OffboardMission()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

