# ROS 2 and MQTT Utilities

A small collection of ROS 2 MQTT bridge configurations and utility nodes for testing bidirectional message flow, generating threshold warnings, and exporting lidar scans to CSV. This directory is a set of scripts and configuration examples, not a complete installable ROS 2 package.

## Requirements

- ROS 2 with `rclpy`, `std_msgs`, and `sensor_msgs`
- The `mqtt_client` ROS 2 package for the bridge examples
- Access to an MQTT broker

Source your ROS 2 installation in each terminal before running ROS commands:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
```

## MQTT Bridge Configurations

| File | Purpose | ROS topics | MQTT topics |
|---|---|---|---|
| [`params.primitive.yaml`](params.primitive.yaml) | Bidirectional primitive/string message tests | `/ping/primitive`, `/test/primitive`, `/pong/primitive`, `/test/echo` | `pingpong/primitive`, `test/primitive` |
| [`params.yaml`](params.yaml) | Basic ping/pong example | `/ping/ros`, `/pong/ros` | `pingpong/ros` |
| [`led_bridge/led_bridge.yaml`](led_bridge/led_bridge.yaml) | LED control and echo example | `/led/control`, `/led/echo` | `led/control` |

The broker host in each file is a placeholder (`your-mqtt-broker.example`). Replace it with a broker you own or are authorized to use before running the bridge. Do not add broker passwords, tokens, or other credentials to tracked YAML files.

Start the primitive bridge from this directory:

```bash
ros2 launch mqtt_client standalone.launch.xml \
  params_file:="$(pwd)/params.primitive.yaml"
```

In another sourced terminal, publish from ROS and listen for the MQTT-to-ROS response:

```bash
ros2 topic pub --once /test/primitive std_msgs/msg/String \
  "{data: 'hello from ROS'}"
ros2 topic echo /test/echo
```

For the reverse direction, publish `hello from MQTT` to `test/primitive` using an MQTT client and listen in ROS:

```bash
ros2 topic echo /test/echo
```

The bridge uses primitive mode, so JSON sent as a string remains plain string data; it is not decoded into a ROS message structure.

## Utility Nodes

### Threshold warning

[`auto_warning_node.py`](auto_warning_node.py) subscribes to `/test/echo` (`std_msgs/msg/String`). It publishes a warning on `/test/warning` when the message parses as a number greater than `100`; other values are logged.

```bash
python3 auto_warning_node.py
```

In another sourced terminal:

```bash
ros2 topic pub --once /test/echo std_msgs/msg/String "{data: '150'}"
ros2 topic echo /test/warning
```

### Lidar scan CSV export

[`scan_mirror_to_csv.py`](scan_mirror_to_csv.py) subscribes to `/scan_mirror` (`sensor_msgs/msg/LaserScan`). On shutdown with Ctrl+C, it writes valid ranges and their Cartesian coordinates to a timestamped `LaserScan_Converted_Data_*.csv` file in the current working directory.

```bash
python3 scan_mirror_to_csv.py
```

Make sure a ROS node is publishing `/scan_mirror` before recording. The exporter keeps scan rows in memory until shutdown, so long recordings require sufficient memory.

## Repository Contents

```text
.
├── README.md
├── auto_warning_node.py
├── scan_mirror_to_csv.py
├── params.yaml
├── params.primitive.yaml
└── led_bridge/
    └── led_bridge.yaml
```

The previous `commands.txt` was a manual test log; its useful setup and test commands are consolidated here.
