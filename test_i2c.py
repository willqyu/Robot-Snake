
from drivers.i2c import I2CResponder

# Mainloop

res = I2CResponder(
    i2c_device_id=1,
    sda_gpio=14, 
    scl_gpio=15, 
    responder_address=0x41
)

while True:
    if res.write_data_is_available():
        read_bytes = res.get_write_data(max_size=64)
        print(read_bytes)
    