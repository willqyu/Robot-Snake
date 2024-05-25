import machine
import time
from motor import Motor, Servo

class Pins:
    LED_INFO = 0
    MOTOR_EN_1 = 4
    MOTOR_1_A = 3
    MOTOR_1_B = 2
    MOTOR_EN_2 = 8
    MOTOR_2_A = 7
    MOTOR_2_B = 6
    SERVO_1 = 14
    SERVO_2 = 15

    GPIO_10 = 10
    GPIO_11 = 11
    GPIO_12 = 12
    GPIO_13 = 13
    

def flash(pin):
    pin.value(1)
    time.sleep_ms(500)
    pin.value(0)



class Board:
    def __init__(self):
        self.led_info = machine.Pin(Pins.LED_INFO, machine.Pin.OUT)

        motor_en_1 = machine.Pin(Pins.MOTOR_EN_1, machine.Pin.OUT)
        motor_1_a = machine.Pin(Pins.MOTOR_1_A, machine.Pin.OUT)
        motor_1_b = machine.Pin(Pins.MOTOR_1_B, machine.Pin.OUT)
        self.motor_1 = Motor(motor_en_1, motor_1_a, motor_1_b)

        motor_en_2 = machine.Pin(Pins.MOTOR_EN_2, machine.Pin.OUT)
        motor_2_a = machine.Pin(Pins.MOTOR_2_A, machine.Pin.OUT)
        motor_2_b = machine.Pin(Pins.MOTOR_2_B, machine.Pin.OUT)
        self.motor_2 = Motor(motor_en_2, motor_2_a, motor_2_b)

        servo_pwm_1 = machine.Pin(Pins.SERVO_1)
        servo_pwm_2 = machine.Pin(Pins.SERVO_2)
        self.servo_1 = Servo(servo_pwm_1)
        self.servo_2 = Servo(servo_pwm_2)

    

board = Board()

while True:
    board.motor_2.spin(1, 1)
    board.motor_1.spin(0, 1)
    time.sleep(2)
    board.motor_1.stop()
    board.motor_2.stop()
    time.sleep(2)
    board.servo_1.set_angle(0)
    time.sleep(2)
    board.servo_1.set_angle(90)
    

