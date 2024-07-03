
# https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/prepare

import board
import busio
from time import sleep, monotonic
import keypad
from circuitpython_i2c_lcd import I2cLcd

#### Display init
i2c = busio.I2C(board.GP21, board.GP20)   # SCL, SDA
# circuitpython seems to require locking the i2c bus
while i2c.try_lock():
    pass

DEFAULT_I2C_ADDR = 0x27
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

version_string = "Keypad test"
release_string = "29 June 2024 KJ"

def splash():
    lcd.backlight_on()
    print(version_string)
    print(release_string)
    lcd.clear()
    lcd.putstr(version_string)
    lcd.move_to(0, 1)
    lcd.putstr(release_string)
    sleep(3)
    lcd.clear()
    return

splash();
km = keypad.KeyMatrix(
    row_pins=(board.GP9, board.GP8, board.GP7, board.GP6, board.GP27),
    column_pins=(board.GP15, board.GP14, board.GP13, board.GP12,
                 board.GP11, board.GP10, board.GP5, board.GP4,
                 board.GP3, board.GP2),
    columns_to_anodes=True)

while True:
    event = km.events.get()
    if event:
        print(event)
        lcd.clear()
        lcd.putstr(str(event))
