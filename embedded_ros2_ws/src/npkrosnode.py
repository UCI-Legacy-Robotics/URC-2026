#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
import time

# Import custom service (not quite sure how to do this part, sorry. I tried looking into it)
# from soil_sensor.srv import GetSoilData


class SoilSensorNode(Node):

    def __init__(self):
        super().__init__('soil_sensor_node')

        # Open serial once
        self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

        # Create service
        self.srv = self.create_service(
            GetSoilData,
            'get_soil_data',
            self.handle_request
        )

        self.get_logger().info("Soil Sensor Service Ready")

    def send_request(self, cmd_hex):
        try:
            self.ser.write(bytes.fromhex(cmd_hex))
            time.sleep(0.1)
            return self.ser.read(11)
        except Exception as e:
            self.get_logger().error(f"Comm error: {e}")
            return None

    def parse_value(self, data, div=1):
        if data and len(data) >= 7:
            val = int.from_bytes(data[3:5], byteorder='big')
            return val / div
        return None

    def handle_request(self, request, response):

        # 1. pH
        res_ph = self.send_request("01 03 00 06 00 01 64 0B")
        ph = self.parse_value(res_ph, 100)

        # 2. Humidity
        res_h = self.send_request("01 03 00 12 00 01 24 0F")
        hum = self.parse_value(res_h, 10)

        # 3. Temperature
        res_t = self.send_request("01 03 00 13 00 01 75 CF")
        temp = self.parse_value(res_t, 10)

        # 4. Conductivity
        res_ec = self.send_request("01 03 00 15 00 01 95 CE")
        ec = self.parse_value(res_ec, 1)

        # 5. NPK
        res_npk = self.send_request("01 03 00 1E 00 03 65 CD")

        n = p = k = None
        if res_npk and len(res_npk) >= 11:
            n = int.from_bytes(res_npk[3:5], byteorder='big')
            p = int.from_bytes(res_npk[5:7], byteorder='big')
            k = int.from_bytes(res_npk[7:9], byteorder='big')

        # Fill response
        response.ph = float(ph) if ph is not None else -1.0
        response.moisture = float(hum) if hum is not None else -1.0
        response.temperature = float(temp) if temp is not None else -1.0
        response.conductivity = float(ec) if ec is not None else -1.0
        response.nitrogen = float(n) if n is not None else -1.0
        response.phosphorus = float(p) if p is not None else -1.0
        response.potassium = float(k) if k is not None else -1.0

        self.get_logger().info("Soil data returned")

        return response

    def destroy_node(self):
        self.ser.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SoilSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()