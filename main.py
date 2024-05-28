import machine
import time
from drivers.motor import Motor, Servo

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

    
def set_angle(pwm, angle):
    # Map the angle (0-180) to the PWM duty cycle (500-2500)
    duty_cycle = 500 + ((angle / 180.0) * 2000)
    duty_cycle *= (65535 / 20000)
    print(duty_cycle)
    
    pwm.duty_u16(int(duty_cycle))

pwm_1 = machine.PWM(machine.Pin(14))
pwm_1.freq(50)
pwm_2 = machine.PWM(machine.Pin(15))
pwm_2.freq(50)

board = Board()

#reset

board.servo_1.set_angle(0)
board.servo_2.set_angle(0)

while True:
    board.led_info.value(1)
    angle = int(input())
    board.servo_1.set_angle(angle)
    board.servo_2.set_angle(angle)
    