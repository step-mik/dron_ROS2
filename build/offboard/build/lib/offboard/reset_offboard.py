#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode

class OffboardResetNode(Node):
    def __init__(self):
        super().__init__('offboard_reset_node')
        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        
        # Odesíláme režim OFFBOARD
        msg = OffboardControlMode()
        msg.position = True  # Zajistíme, že režim OFFBOARD bude aktivní pro pozici
        self.offboard_mode_pub.publish(msg)
        self.get_logger().info('Režim OFFBOARD resetován.')

        # Po odeslání příkazu ukončíme node
        self.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = OffboardResetNode()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

