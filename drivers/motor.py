import machine

class Motor:
    def __init__(self, pin_en: machine.Pin, pin_a : machine.Pin, pin_b : machine.Pin) -> None:
        
        self.pin_a = pin_a
        self.pin_b = pin_b
        
        self.en = machine.PWM(pin_en)
        self.en.freq(50)
        self.angle = 0

    def spin(self, dir : int, speed : int):
        # speed is a number between 0 and 100 -> %

        if speed <= 0:
            self.stop()
            return
        
        clamped_speed = max(min(100, speed), 0)
        scaled_speed = int(clamped_speed * 65535 / 100)
        self.en.duty_u16(scaled_speed)

        if dir:
            self.pin_a.value(1)
            self.pin_b.value(0)
        
        else:
            self.pin_a.value(0)
            self.pin_b.value(1)
        
        
    
    def stop(self):
        print("stopping")
        self.en.duty_u16(0)
        self.pin_a.value(0)
        self.pin_b.value(0)

class Servo:
    def __init__(self, pin_pwm: machine.Pin) -> None:
        self.pwm = machine.PWM(pin_pwm)
        self.pwm.freq(50)
        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle

        # Map the angle (0-180) to the PWM duty cycle (500-2500)
        duty_cycle = 500 + ((angle / 180.0) * 2000)
        duty_cycle *= (65535 / 20000)
        print(duty_cycle)
    
        self.pwm.duty_u16(int(duty_cycle))