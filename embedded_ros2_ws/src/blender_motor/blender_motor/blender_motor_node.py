#!/usr/bin/env python3

import warnings

# Silence gpiozero "fallback" warnings on non-Pi machines
try:
    from gpiozero.devices import PinFactoryFallback

    warnings.simplefilter("ignore", PinFactoryFallback)
except Exception:
    pass

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

from gpiozero import PWMOutputDevice
from gpiozero.exc import BadPinFactory

class BlenderMotorNode(Node):
    def __init__(self):
        super().__init__('blender_motor_node')

        # Parameters (BCM numbering)
        self.declare_parameter('gpio_pin', 12)
        self.declare_parameter('duty_cycle', 0.5)  # 0.0 to 1.0
        self.declare_parameter('enable_on_start', False)

        self.gpio_bcm = int(self.get_parameter('gpio_pin').value)
        self.duty_cycle = float(self.get_parameter('duty_cycle').value)
        self.enable_on_start = bool(self.get_parameter('enable_on_start').value)
        self.enabled = False
        self.pwm = None

        if not (0.0 <= self.duty_cycle <= 1.0):
            raise ValueError("duty_cycle must be between 0.0 and 1.0")
        
        # Try to init PWM (will fail on non-Pi thus DRY-RUN mode)
        try:
            self.pwm = PWMOutputDevice(self.gpio_bcm, initial_value=0.0)
        except BadPinFactory as e:
            self.get_logger().warning(
                f"GPIO not available on this machine (expected on non-Pi). "
                f"Running in DRY-RUN mode. Details: {e}"
            )
            self.pwm = None

        # ROS2 Service
        self.srv = self.create_service(SetBool, 'blender_motor/set_enabled', self.handle_set_enabled)

        # Give initial state
        if self.enable_on_start:
            self._on()
        else:
            self._off()
        
        self.get_logger().info(
            f"Ready. GPIO(BCM)={self.gpio_bcm}, duty={self.duty_cycle}. "
            "Service: /blender_motor/set_enabled"
        )

    def _on(self):
        if self.pwm is None:
            self.enabled = True
            self.get_logger().info(f"[DRY-RUN] Blender motor ON (duty={self.duty_cycle})")
            return
        self.pwm.value = self.duty_cycle
        self.enabled = True
        self.get_logger().info('Blender motor ON')

    def _off(self):
        if self.pwm is None:
            self.enabled = False
            self.get_logger().info("[DRY-RUN] Blender motor OFF")
            return
        self.pwm.value = 0.0
        self.enabled = False
        self.get_logger().info('Blender motor OFF')

    def handle_set_enabled(self, request, response):
        if request.data:
            self._on()
            response.success = True
            response.message = 'Blender motor enabled'
        else:
            self._off()
            response.success = True
            response.message = 'Blender motor disabled'
        return response
    
    def destroy_node(self):
        # Avoid extra ROS logging during teardown when context may already be shutting down
        try:
            if self.pwm is not None:
                try:
                    self.pwm.value = 0.0
                except Exception:
                    pass
                try:
                    self.pwm.close()
                except Exception:
                    pass
        finally:
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = BlenderMotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
        except Exception:
            pass
        # Prevent "shutdown already called" errors under ros2 launch
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception:
            pass

if __name__ == '__main__':
    main()