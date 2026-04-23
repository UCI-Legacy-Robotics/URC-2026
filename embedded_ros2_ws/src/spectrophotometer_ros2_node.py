import socket
import struct
import rclpy
from rclpy.node import Node

from mission_interfaces.srv import GetSpectro


CAN_INTERFACE = "can0"
REQUEST_ID = 0x4C8
RESPONSE_ID = 0x028


class SpectroNode(Node):
    def __init__(self):
        super().__init__('spectro_node')

        self.srv = self.create_service(
            GetSpectro,
            'get_spectro_data',
            self.handle_spectro_request
        )

        self.get_logger().info('Spectro service ready: /get_spectro_data')

    def build_can_frame(self, can_id, data=b''):
        can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        return struct.pack("=IB3x8s", can_id, can_dlc, data)

    def parse_can_frame(self, frame):
        can_id, can_dlc, data = struct.unpack("=IB3x8s", frame)
        return can_id, can_dlc, data[:can_dlc]

    def handle_spectro_request(self, request, response):
        try:
            s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
            s.bind((CAN_INTERFACE,))
            s.settimeout(5.0)

            # send empty request frame to ESP32
            request_frame = self.build_can_frame(REQUEST_ID, b'')
            s.send(request_frame)

            self.get_logger().info('Sent CAN request to spectrophotometer.')

            while True:
                frame = s.recv(16)
                can_id, can_dlc, data = self.parse_can_frame(frame)

                if can_id == RESPONSE_ID and can_dlc == 8:
                    voltage = struct.unpack('<f', data[0:4])[0]
                    absorbance = struct.unpack('<f', data[4:8])[0]

                    response.voltage = voltage
                    response.absorbance = absorbance
                    response.success = True
                    response.message = 'Measurement received successfully.'

                    self.get_logger().info(
                        f'Received spectro data: voltage={voltage:.3f} V, absorbance={absorbance:.4f}'
                    )

                    s.close()
                    return response

        except socket.timeout:
            response.voltage = 0.0
            response.absorbance = 0.0
            response.success = False
            response.message = 'Timed out waiting for CAN response.'
            self.get_logger().error(response.message)

        except Exception as e:
            response.voltage = 0.0
            response.absorbance = 0.0
            response.success = False
            response.message = f'Error: {str(e)}'
            self.get_logger().error(response.message)

        return response


def main(args=None):
    rclpy.init(args=args)
    node = SpectroNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
