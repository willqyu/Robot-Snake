import machine
import time

# Define the pin numbers for X and Y axes of the joystick
x_axis_pin_num = 26  # Replace 26 with the actual pin number for X-axis
y_axis_pin_num = 27  # Replace 27 with the actual pin number for Y-axis

# Initialize analog pins for reading joystick values
x_axis_pin = machine.ADC(x_axis_pin_num)
y_axis_pin = machine.ADC(y_axis_pin_num)
led = machine.Pin("LED", machine.Pin.OUT)


pwm_1 = machine.PWM(machine.Pin(14))
pwm_1.freq(50)
pwm_2 = machine.PWM(machine.Pin(15))
pwm_2.freq(50)

MAX_JOY = 65565
MIN_JOY = 272
X_OFFSET = -0.03
Y_OFFSET = -0.01
JOY_RANGE = MAX_JOY - MIN_JOY

# Define a function to read analog values from the joystick
def read_joystick():
    x_value = x_axis_pin.read_u16()  # Read analog value for X-axis
    y_value = y_axis_pin.read_u16()  # Read analog value for Y-axis
    return x_value, y_value

def norm_joy(val, offset):
    val = (val-MIN_JOY) / JOY_RANGE
    normed = round((val-offset)*2 - 1, 2)
    if -0.05 < normed < 0.05:
        return 0
    else:
        return min(max(normed,-1.0), 1.0)
    
def set_angle(pwm, angle):
    # Map the angle (0-180) to the PWM duty cycle (500-2500)
    duty_cycle = 500 + ((angle / 180.0) * 2000)
    duty_cycle *= (65535 / 20000)
    print(duty_cycle)
    
    pwm.duty_u16(int(duty_cycle))

# Main loop to continuously read and print joystick values
while True:
    x_val, y_val = read_joystick()
    # print("X-axis:", x_val / 65535, "Y-axis:", y_val/65535)
    norm_x = norm_joy(x_val, X_OFFSET)
    norm_y = norm_joy(y_val, Y_OFFSET)
    
    print(norm_x, norm_y)
    if norm_x != 0 or norm_y != 0:
        led.value(1)
    else:
        led.value(0)
    
    set_angle(pwm_1, int(180 * (norm_x + 1) / 2))
    set_angle(pwm_2, int(180 * (norm_y + 1) / 2))
    time.sleep(0.1)

    

    
