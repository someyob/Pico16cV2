# Pico16cV2

I've always wanted an HP 16C calculator, the gold standard for early programmers.  In those years, I was too poor, needed to focus on Scientific Calculators in university.  These days, prices are crazy on the used market.

While newer incarnations existed, (e.g. SwissMicro https://www.swissmicros.com/product/dm16l) looked great, they did't scratch my other itches, which were to play with microcontrollers and learn a new language (python).  The primary use for the thing will be (and is now) as a tool to help with the design and assembly language programming of a 6502-based computer.  This computer is based off of the Ben Eater instructional videos, which I highly recommend.

The prototype was done with cheap aliexpress parts and prototoboard, and can be seen here:  https://github.com/someyob/Pico-16C

Because I wasn't happy with the keypads (primarily), and hoped to make a more professional version, I did up a citcuit in KiCAD and sent away to have the PCBs done at PCBway.  (the build was sponsored by PCBway, and my thoughts on the product and the company will be posted on my Hackaday.io page).

The original prototype and version 2 getting assembled:

![PXL_20240628_131755973](https://github.com/someyob/Pico16cV2/assets/3163755/25468ea8-ef2b-4aa9-bc28-55c718759146)

I used brown keyswitches with transparent 2-piece keycaps to create the keyboard, a standard i2c 1602 lcd display (2 lines of 16 characters), and a Raspberry Pi Pico.  The coding is done in CircuitPython.  The result is much bigger than a real 16C, but that wasn't a huge impediment for me.  The biggest challenge, aside from coding, was to make the keycaps look good.  I think it's an improvement over the prototype.

The fully assembled v2 is shown here:

![v2 pic 1](https://github.com/someyob/Pico16cV2/assets/3163755/ffce5687-d008-411e-879d-82381a2b5b73)
![v2 pic 2](https://github.com/someyob/Pico16cV2/assets/3163755/54f5a8bd-7e78-4390-a408-b5d4ea60b60a)

At this point, lots of extra functionality still has to go in here, but it does the basic stuff, and in the same fashion as the true 16C (using RPN).

You may note that there's some unpopulated components on the PCB.  In order to take advantage of the space, and create other optional capabilities, I added two rotary encoders and included them (each includes a push-button) in the keypad matrix.  This way, I can use the same pcb as a basis for a macro keyboard.  There's also breakouts of the unused Pi Pico GPIO as well as a spot for an LED, should it find a use.

More notes on the build and the software to come.
