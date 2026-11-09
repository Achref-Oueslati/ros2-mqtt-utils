import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import csv
import math
import time
import signal
import sys

class LaserScanCSVExporter(Node):
    def __init__(self):
        super().__init__('laser_scan_csv_exporter')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan_mirror',  # Change to your topic if needed
            self.listener_callback,
            10)
        self.frame_index = 0
        self.csv_rows = []
        self.start_time = int(time.time() * 1000)
        # Register signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def listener_callback(self, msg):
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        ranges = msg.ranges
        range_min = msg.range_min
        range_max = msg.range_max
        timestamp = int(time.time() * 1000)
        for i, r in enumerate(ranges):
            angle_rad = angle_min + i * angle_increment
            angle_deg = math.degrees(angle_rad)
            if math.isfinite(r) and range_min <= r <= range_max and r > 0.05:
                x = r * math.cos(angle_rad)
                y = r * math.sin(angle_rad)
                range_val = r
            else:
                x = ''
                y = ''
                range_val = ''
            self.csv_rows.append([
                timestamp,
                self.frame_index,
                i,
                angle_deg,
                range_val,
                x,
                y
            ])
        self.frame_index += 1

    def handle_shutdown(self, signum, frame):
        print("\nStopping recording and exporting CSV...")
        self.export_csv()
        rclpy.shutdown()
        sys.exit(0)

    def export_csv(self):
        filename = f'LaserScan_Converted_Data_{self.start_time}.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp','frameIndex','pointIndex','angleDeg','range','x','y'])
            writer.writerows(self.csv_rows)
        print(f'Exported {self.frame_index} frames to {filename}')

def main(args=None):
    rclpy.init(args=args)
    exporter = LaserScanCSVExporter()
    try:
        rclpy.spin(exporter)
    except KeyboardInterrupt:
        exporter.handle_shutdown(None, None)

if __name__ == '__main__':
    main()