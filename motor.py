import machine

class Motor:
    def __init__(self, pin_en: machine.Pin, pin_a : machine.Pin, pin_b : machine.Pin) -> None:
        self.en = pin_en
        self.pin_a = pin_a
        self.pin_b = pin_b
        
        self.speed = 0
        self.dir = True

    def spin(self, dir : int, speed : int):
        if dir:
            self.pin_a.value(1)
            self.pin_b.value(0)
            self.en.value(1)
        
        else:
            self.pin_a.value(0)
            self.pin_b.value(1)
            self.en.value(1)
    
    def stop(self):
        self.en.value(0)
        self.pin_a.value(0)
        self.pin_b.value(0)