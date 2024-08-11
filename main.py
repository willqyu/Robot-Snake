from drivers.i2c import I2CResponder
import machine
import time
from drivers.motor import Motor, Servo

DEVICE_ADDRESS = 0x46

res = I2CResponder(
    i2c_device_id=0,
    sda_gpio=16, 
    scl_gpio=17, 
    responder_address=DEVICE_ADDRESS
)

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

    def parse_bytes(self, read_bytes):
        if read_bytes[0] != 17 or len(read_bytes) != 7:
            print("<!> Board cannot parse!")
            return
        
        motor_1_en = read_bytes[1]
        motor_1_speed = read_bytes[2]
        motor_2_en = read_bytes[3]
        motor_2_speed = read_bytes[4]
        servo_1_ang = read_bytes[5]
        servo_2_ang = read_bytes[6]

        self.motor_1.spin(motor_1_en, motor_1_speed)  
        self.motor_2.spin(motor_2_en, motor_2_speed)

        self.servo_1.set_angle(servo_1_ang)
        self.servo_2.set_angle(servo_2_ang)      

    def reset(self):
        self.servo_1.set_angle(90)
        self.servo_2.set_angle(90)
        self.motor_1.stop()
        self.motor_2.stop()
  



pwm_1 = machine.PWM(machine.Pin(14))
pwm_1.freq(50)
pwm_2 = machine.PWM(machine.Pin(15))
pwm_2.freq(50)


# Initialization functions
board = Board()
board.reset()

board.led_info.value(1)



while True:
    try:
        if res.write_data_is_available():
            read_bytes = [0]
            timeout = 255
            while read_bytes[-1] != 255 and timeout > 0:
                new_bytes = res.get_write_data(max_size=64)
                print("[INFO] --- " + str(new_bytes))
                read_bytes += new_bytes
                timeout -= 1
            read_bytes.pop(0)
            read_bytes.pop()
            print("[INFO] Received: " + str(read_bytes))
            board.parse_bytes(read_bytes)

        if res.read_is_pending():
            res.put_read_data(0xff)

    except KeyboardInterrupt:
        break


    