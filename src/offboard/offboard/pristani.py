#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import VehicleCommand, OffboardControlMode


class PristaniNode(Node):
    def __init__(self):
        super().__init__('pristani_node')

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.command_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos)
        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos)

        self.counter = 0
        self.timer = self.create_timer(0.2, self.timer_callback)

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

    def send_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.position = True
        self.offboard_mode_pub.publish(msg)

    def timer_callback(self):
        # Pošleme OFFBOARD control mode
        self.send_offboard_control_mode()

        # Po 2 sekunde pošleme příkaz k přistání
        if self.counter == 10:
            self.get_logger().info('🛬 Odesílám příkaz k přistání...')
            self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)

        # Po přistání vypneme motory
        elif self.counter == 30:
            self.get_logger().info('🛑 Vypínám motory (disarm)...')
            self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, param1=0.0)

        # Po několika vteřinách ukončíme node
        elif self.counter > 40:
            self.get_logger().info('✅ Přistání dokončeno. Ukončuji node.')
            self.destroy_node()

        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = PristaniNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

