#!/usr/bin/env python3

import rclpy
import warnings
try: # gets rid of those warnings about no GPIO pin available when running on non PI hardware
    from gpiozero.devices import PinFactoryFallback
    warnings.simplefilter('ignore', PinFactoryFallback)
except Exception:
    pass
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Bool, String

from gpiozero import PWMOutputDevice
from gpiozero.exc import BadPinFactory


class BlenderMotorNode(Node):
    def __init__(self):
        super().__init__('blender_motor_node')
        self.get_logger().info('Blender motor node has started!')

        # setup default parameters
        self.declare_parameter('gpio_pin', 12) 
        self.declare_parameter('pwm_frequency', 100)
        self.declare_parameter('duty_cycle', 0.5)

        # read the parameters values
        self.gpio_pin = self.get_parameter('gpio_pin').value
        self.pwm_frequency = self.get_parameter('pwm_frequency').value
        self.duty_cycle = self.get_parameter('duty_cycle').value

        # make sure duty cycle stays between 0 and 1
        if not (0.0 <= self.duty_cycle <= 1.0):
            raise ValueError(
                f'Duty cycle must be between 0 and 1, you provided {self.duty_cycle}'
                )
        
        # initialize the PWM output device, two modes: real hardware or simulation mode if PI is not detected
        self.pwm = None
        try:
            self.pwm = PWMOutputDevice(
                self.gpio_pin, 
                initial_value=0.0, # motor is off at startup
                frequency=self.pwm_frequency
            )
            self.get_logger().info('PWM device initialized on PI successfully.')
        except BadPinFactory:
            self.get_logger().warning(
                'NO GPIO pin availabe, Running in simulation mode(PI is not detected).'
                )
        
        self.motor_on = False # will keep track of the motor state

        # register the runtime parameter change callback
        self.add_on_set_parameters_callback(self.on_parameter_change)

        # Subscriber: will listen for ON/OFF cmds
        self.cmd_subscription = self.create_subscription(
            Bool,
            'blender_motor_cmd',
            self.cmd_callback,
            10,
        )

        # Publisher: will report the motor status (ON/OFF) on a topic
        self.status_publisher = self.create_publisher(
            String,
            'blender_motor_status',
            10,
        )

        # timer: publishes the motor status at 1 Hz
        self.status_timer = self.create_timer(1.0, self.publish_status)
        
        # display the parameters values
        self.get_logger().info('Blender motor node has started!')
        self.get_logger().info(f'GPIO Pin: {self.gpio_pin}')
        self.get_logger().info(f'PWM Frequency: {self.pwm_frequency} Hz')
        self.get_logger().info(f'Duty Cycle: {self.duty_cycle}')
        self.get_logger().info("Waiting for motor commands on 'blender_motor_cmd' topic...")
        self.get_logger().info("Publishing motor status on 'blender_motor_status' topic at 1 Hz...")

    def on_parameter_change(self, params):
        """ Validate and apply the runtime parameter changes """
        for param in params:
            if param.name == 'pwm_frequency':
                new_freq = param.value
                if not isinstance(new_freq, int) or new_freq <= 0:
                    return SetParametersResult(
                        successful=False,
                        reason=f'pwm_frequency must be a positive integer, got {new_freq}'
                    )
                self.pwm_frequency = new_freq
                if self.pwm is not None:
                    self.pwm.frequency = new_freq
                self.get_logger().info(f'PWM frequency updated to {new_freq} Hz')

            elif param.name == 'duty_cycle':
                new_duty = param.value
                if not (0.0 <= new_duty <= 1.0):
                    return SetParametersResult(
                        successful=False,
                        reason=f'duty_cycle must be between 0.0 and 1.0, got {new_duty}'
                    )
                self.duty_cycle = new_duty
                # if motor is on currently, then we will change the new duty cycle immediately
                if self.motor_on and self.pwm is not None:
                    self.pwm.value = new_duty
                self.get_logger().info(f'Duty cycle updated to {new_duty}')

            elif param.name == 'gpio_pin':
                # chaning the pin at runtime, we dont want this so we will just log a warning and ignore the change
                return SetParametersResult(
                    successful=False,
                    reason='Changing gpio_pin at runtime is not supported. Restart the node if you want to do this.'
                )
        return SetParametersResult(successful=True)

    # callback function to handle incoming ON/OFF commands
    def cmd_callback(self, msg: Bool):
        """Handle incomming ON/OFF cmds"""
        if msg.data:
            self._motor_on()
        else:
            self._motor_off()

    def _motor_on(self):
        self.motor_on = True
        if self.pwm is not None:
            self.pwm.value = self.duty_cycle
            self.get_logger().info(f'MOTOR IS ON (duty cycle: {self.duty_cycle})')
        else:
            self.get_logger().info(f'MOTOR IS ON (simulation mode, duty cycle: {self.duty_cycle})')

    def _motor_off(self):
        self.motor_on = False
        if self.pwm is not None:
            self.pwm.value = 0.0
            self.get_logger().info('MOTOR IS OFF')
        else:
            self.get_logger().info('MOTOR IS OFF (simulation mode)')
    
    def publish_status(self):
        """Publish the motor status (ON/OFF) at 1 Hz"""
        state = 'ON' if self.motor_on else 'OFF'
        mode = 'HW' if self.pwm is not None else 'SIM'
        msg = String()
        msg.data = (
            f'[{mode}] Motor is {state} | '
            f'frequency: {self.pwm_frequency} Hz | '
            f'duty cycle: {self.duty_cycle}'
        )
        self.status_publisher.publish(msg)

    def destroy_node(self):
        # realse the GPIO pin wehn the node is destroyed
        if self.pwm is not None:
            try:
                self.pwm.value = 0.0  # stop the motor
                self.pwm.close()  # release the GPIO pin
            except Exception as e:
                self.get_logger().warning(f'Failed to release GPIO pin: {e}')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = BlenderMotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()