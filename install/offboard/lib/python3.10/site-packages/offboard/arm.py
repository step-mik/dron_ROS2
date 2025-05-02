#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleCommand

class ArmNode(Node):
    def __init__(self):
        super().__init__('arm_node')

        # Vytvoření publisheru pro příkazy k motorům
        self.command_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', 10)

        # Timer pro opakování příkazu (každých 1 sekundu)
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.counter = 0
        self.arm()

    def arm(self):
        """Funkce pro armování motorů"""
        msg = VehicleCommand()
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        msg.command = VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM  # Armování motorů
        msg.param1 = 1.0  # Parametr pro armování (1.0 pro armování)
        msg.param2 = 0.0  # Parametr pro disarmování (0.0 pro disarmování)
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True  # Od externího systému

        # Odeslání příkazu pro armování
        self.command_pub.publish(msg)
        self.get_logger().info("Odesílám příkaz pro armování motorů.")

    def timer_callback(self):
        """Timer pro kontrolu stavu"""
        self.counter += 1
        if self.counter > 20:  # Po 5 opakováních zastavíme node
            self.get_logger().info("Armování motorů dokončeno.")
            self.destroy_node()  # Zničíme node po dokončení

def main(args=None):
    """Hlavní funkce pro spuštění ROS 2 uzlu"""
    rclpy.init(args=args)
    node = ArmNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

