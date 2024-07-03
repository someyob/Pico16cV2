
# Use
# https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/usage
# 'circup' to manage packages on this device
# eg 'circup install adafruit_debouncer'

import time
import board
import busio
from time import sleep, monotonic
from circuitpython_i2c_lcd import I2cLcd
from PICO_16C_keypad import *

from digitalio import DigitalInOut, Pull

import keypad

version_string = "Pico 16C v0.9"
release_string = "29 Jun 2024   KJ"

#### Display init
i2c = busio.I2C(board.GP21, board.GP20)   # SCL, SDA
# circuitpython seems to require locking the i2c bus
while i2c.try_lock():
    pass

DEFAULT_I2C_ADDR = 0x27
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)


def splash():
    lcd.backlight_on()
    print(version_string)
    print(release_string)
    lcd.clear()
    lcd.putstr(version_string)
    lcd.move_to(0, 1)
    lcd.putstr(release_string)
    sleep(3)
    return

base_char = [ 'b', 'o', 'd', 'h', ' ' ]   # displays nothing when in float
shift_char = [' ', 'f', 'g', ' ']
float_str = 'float'
arrow_overflow_right = [ 0x00, 0x08, 0x0C, 0x0E, 0x0C, 0x08, 0x00, 0x00]
arrow_overflow_left = [ 0x00, 0x02, 0x06, 0x0E, 0x06, 0x02, 0x00, 0x00]
overflow_right_flag = 1
overflow_left_flag = 2

def display_Xreg(calc):
    # lcd.clear()
    lcd.move_to(0,0)
    OFlow = 0
    if calc.base == BASE_STATE_BIN:
        calc.Xstr = f'{calc.Xreg:>16b}'
    elif calc.base == BASE_STATE_OCT:
        calc.Xstr = f'{calc.Xreg:>16o}'
    elif calc.base == BASE_STATE_DEC:
        calc.Xstr = f'{calc.Xreg:>16}'
    elif calc.base == BASE_STATE_HEX:
        calc.Xstr = f'{calc.Xreg:>16x}'.upper()
    elif calc.base == BASE_STATE_FLOAT:
        num_places = calc.decimalPlaces
        if calc.entry_in_progress:
            if calc.decimals_entered == 0:
                num_places = 1
            else:
                num_places = calc.decimals_entered
        if calc.ExponentMode or calc.ExponentEntry:
            calc.Xstr = f'{calc.Xreg:.{num_places}e}'
        else:
            calc.Xstr = f'{calc.Xreg:.{num_places}f}'    # show what user is entering, truncate later
    OFlow = 0
    if len(calc.Xstr) > 16:
        if calc.strindex == 0:
            calc.Xstr = calc.Xstr[-16:]
            OFlow += overflow_left_flag
        else:
            calc.Xstr = calc.Xstr[-16-calc.strindex:-calc.strindex]
            OFlow = overflow_right_flag + overflow_left_flag
            if len(calc.Xstr) != 16:
                OFlow -= overflow_left_flag
            while len(calc.Xstr) < 16:
                calc.Xstr = ' ' + calc.Xstr
    # print(strindex, ">", Xstr, "<")
    lcd.putstr(calc.Xstr)
    return OFlow

    
def print_calc_modes(calc, OFlow):  
    lcd.move_to(15, 1)
    lcd.putchar(base_char[calc.base])

    if calc.shift == SHIFT_STATE_FLOAT:
        lcd.move_to(0, 1)
        lcd.putstr('float (0-9,.)')
    else:
        lcd.move_to(1, 1)
        lcd.putchar(shift_char[calc.shift])
    
    if calc.ExponentEntry:
        lcd.move_to(3, 1)
        lcd.putstr('exp')
            
    cust_char = base_char[calc.base]    # ????
    if OFlow & overflow_left_flag: 
        lcd.move_to(13, 1)
        lcd.custom_char(0, arrow_overflow_left)
        lcd.putchar(chr(0))
    
    if OFlow & overflow_right_flag:  
        lcd.move_to(14, 1)
        lcd.custom_char(1, arrow_overflow_right)
        lcd.putchar(chr(1))
        
    if calc.CarryBit:
        lcd.move_to(11, 1)
        lcd.putchar('c')
    return
    
def display_status(calc):
    lcd.clear()
    lcd.move_to(3, 0)
    lcd.putstr(f'{calc.complement}-{calc.wordSize}-{calc.flagIndicators:0{4}b}')
    return
    
def refresh_screen(calc):
    lcd.clear()
    # time.sleep(0.1)
    
    # OFlow = display_Xreg(calc.Xreg, calc.base, calc.strindex, calc.decimalPlaces, calc.entry_in_progress)
    OFlow = display_Xreg(calc)
    print_calc_modes(calc, OFlow)
    return

def print_status(calc):
    if calc.base == BASE_STATE_FLOAT:
        print("\nT  %.9f" % calc.Treg)
        print("Z  %.9f" % calc.Zreg)
        print("Y  %.9f" % calc.Yreg)
        print("X  %.9f" % calc.Xreg)
        print("LX %.9f" % calc.LastX)
    else:
        print("\nT  ", calc.Treg)
        print("Z  ", calc.Zreg)
        print("Y  ", calc.Yreg)
        print("X  ", calc.Xreg)
        print("LX ", calc.LastX)
    print("Base (", base_char[calc.base], "),  Shift (", shift_char[calc.shift], ")")
    print(">", calc.Xbuff, "< input buffer", calc.decimals_entered)
    # print("strindex = ", calc.strindex)

    # gc.collect()
    #start_mem = gc.mem_free()
    #print( "Point 1 Available memory: {} bytes".format(start_mem) ) 
    return

def paste_Xreg(calc):
    if calc.base == BASE_STATE_BIN:
        Xstr = f'{calc.Xreg:b}'
    elif calc.base == BASE_STATE_OCT:
        Xstr = f'{calc.Xreg:o}'
    elif calc.base == BASE_STATE_DEC:
        Xstr = f'{calc.Xreg}'
    elif calc.base == BASE_STATE_HEX:
        Xstr = f'{calc.Xreg:x}'.upper()
    elif calc.base == BASE_STATE_FLOAT:
        Xstr = f'{calc.Xreg:.{3}f}' 
    layout.write(Xstr)
    return 

def main_loop():

    splash()
    lcd.clear()
    
    calculator = Calculator()
    refresh_screen(calculator)
    print_status(calculator)   

    while True:
        if calculator.check_timeout() and calculator.calcstate == STATE_ON:
            lcd.backlight_off()
            # print("Timed out")
            calculator.wait_keypress()
            lcd.backlight_on()
             
        calculator.check_keypress()
        
        if (calculator.key >= 0):
            key_event = getattr(calculator, key_functions[calculator.key])
            key_event(calculator.key)             
            if calculator.calcstate == STATE_OFF:
                lcd.clear()
                lcd.backlight_off()
            else:
                lcd.backlight_on()
                if calculator.macroState == MACRO_STATE_1:
                    paste_Xreg(calculator)  # paste Xbuff into whatever app is open
                    calculator.macroState = MACRO_STATE_OFF
                if calculator.showSplash:
                    splash()
                    calculator.wait_keypress()
                    calculator.showSplash = False
                if calculator.showStatus:
                    display_status(calculator)
                    calculator.wait_keypress()
                    calculator.showStatus = False
                      
                refresh_screen(calculator)
                print_status(calculator)
       
    return
    

#if __name__ == "__main__":
main_loop()