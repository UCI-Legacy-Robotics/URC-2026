#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import socket
import struct
from spectro_sensor.srv import GetSpectroData


CAN_INTERFACE = "can0"
REQUEST_ID = 0x4C8
RESPONSE_ID = 0x028


class SpectroSensorNode(Node):

    def __init__(self):
        super().__init__('spectro_sensor_node')

        self.sock = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.sock.bind((CAN_INTERFACE,))
        self.sock.settimeout(5.0)

        self.srv = self.create_service(
            GetSpectroData,
            'get_spectro_data',
            self.handle_request
        )

        self.get_logger().info("Spectro Sensor Service Ready")

    def build_can_frame(self, can_id, data=b''):
        can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        return struct.pack("=IB3x8s", can_id, can_dlc, data)

    def parse_can_frame(self, frame):
        can_id, can_dlc, data = struct.unpack("=IB3x8s", frame)
        return can_id, can_dlc, data[:can_dlc]

    def send_request(self):
        frame = self.build_can_frame(REQUEST_ID, b'')
        self.sock.send(frame)

    def wait_for_response(self):
        while True:
            frame = self.sock.recv(16)
            can_id, can_dlc, data = self.parse_can_frame(frame)

            if can_id == RESPONSE_ID and can_dlc == 8:
                voltage = struct.unpack('<f', data[0:4])[0]
                absorbance = struct.unpack('<f', data[4:8])[0]
                return voltage, absorbance

    def handle_request(self, request, response):
        try:
            self.send_request()
            voltage, absorbance = self.wait_for_response()

            response.voltage = float(voltage)
            response.absorbance = float(absorbance)

            self.get_logger().info(
                f"Spectro data returned: V={voltage:.3f}, A={absorbance:.4f}"
            )

        except Exception as e:
            self.get_logger().error(f"CAN error: {e}")
            response.voltage = -1.0
            response.absorbance = -1.0

        return response

    def destroy_node(self):
        self.sock.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SpectroSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
