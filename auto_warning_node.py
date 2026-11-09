# AutoWarningNode: Listens to /test/echo (String messages from MQTT),
# checks if the received value is a number > 100, and if so,
# publishes a warning message to /test/warning.
# This enables simple automation/alerting based on incoming MQTT/ROS data.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

def is_number(s):
    # Helper function: returns True if s can be converted to a float
    try:
        float(s)
        return True
    except ValueError:
        return False

class AutoWarningNode(Node):
    def __init__(self):
        super().__init__('auto_warning_node')
        # Subscribe to /test/echo (String messages from MQTT bridge)
        self.sub = self.create_subscription(String, '/test/echo', self.callback, 10)
        # Publisher for /test/warning (String)
        self.pub = self.create_publisher(String, '/test/warning', 10)
        self.get_logger().info('AutoWarningNode started: listening on /test/echo')

    def callback(self, msg):
        # Remove whitespace and any extra quotes from the received string
        data = msg.data.strip().strip('"').strip("'")
        # If the data is a number and > 100, publish a warning
        if is_number(data) and float(data) > 100:
            warning = String()
            warning.data = f'WARNING: Value {data} exceeds threshold!'
            self.pub.publish(warning)
            self.get_logger().warn(warning.data)
        else:
            # Otherwise, just log the received value
            self.get_logger().info(f'Received: {data}')

def main(args=None):
    rclpy.init(args=args)
    node = AutoWarningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
