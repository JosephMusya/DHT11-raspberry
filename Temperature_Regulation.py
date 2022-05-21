'''
Temperature Control System - ON OFF Controller
GROUP MEMBERS
1. Musya Joseph
2. Paul Macharia
3. Janet Chepkirui
4. Joseph Maina
5. Amos Munene
6. Dorothy Orina
7. Kelvin Pere
8. Timmons King'au

# Copyright (c) 2021 
# Author: Musya Joseph

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this code and associated documentation files, to deal
# in the code without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the code, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''
import I2C_LCD #LCD library
from time import * #time library
import RPi.GPIO as GPIO
import Adafruit_DHT #Temperature sensor lib

#Declaring push buttons
#setting the pushbutton and ignoring the gpio warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting up the GPIO as the input pins
GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)
#Displayin the welcome Message
disp = I2C_LCD.lcd()
disp.lcd_display_string("Temperature CTRL", 1)
disp.lcd_display_string("DMS GROUP",2,4)
sleep(1) #wait for 1 sec b4 clear screen(LCD)
disp.lcd_clear() #clear the LCD

accuracy = 0.5 #Accuracy of our system
set_p = 21.0 #default setpoint
MAX_TEMP = 40.0
MIN_TEMP = 10.0
sensor = Adafruit_DHT.DHT11
pin = 4  #Temp sensot pin

#setting up the required temp
def set_up():
    global set_p
    disp.lcd_clear()
    while True:
        set_p = (set_p)
        OK = GPIO.input(9)
        ADD = GPIO.input(8)
        MINUS = GPIO.input(25)

        if ADD is 0:
            set_p = set_p + .1 #incrementing the temp by 0.1
            
            sleep(0.1)
        if MINUS is 0:
            set_p = set_p - .1 #decrementing the temp by 0.1
            sleep(0.1)
            
        set_p = float(set_p)  
        disp.lcd_display_string("Enter Desired", 1,0)
        disp.lcd_display_string("Temp:",2,0)
        disp.lcd_display_string(str(round(set_p,1)),2,6)
        set_p = set_p
        
        if OK is 0:
            disp.lcd_clear()
            if float(set_p) > MAX_TEMP:
                set_p = 40.0
            elif float(set_p) < MIN_TEMP:
                set_p = 10.0
            set_p = str(round(set_p,1))
            disp.lcd_display_string("Temperature Set>",1)
            disp.lcd_display_string(set_p, 2,7)
            sleep(3)
            disp.lcd_clear()
            main(set_p)
            break
        
        while (ADD and MINUS and OK is 1): #No key being pressed            if ADD or MINUS is 0:
                break
        
#main function***
def main(set_p):
    temp,t = 0,0 #delaring temps
    while True:
        CHANGE = GPIO.input(11)
        humidity,temp = Adafruit_DHT.read(sensor, pin)
        if temp is not None:
            t = temp
        if temp is None:
            t = t
        disp.lcd_display_string("Curr Temp:",1)
        disp.lcd_display_string(str(t),1,10)
        disp.lcd_display_string("SetPoint:", 2)
        disp.lcd_display_string(str(set_p), 2,10)

        set_p = float(set_p)
        if t > set_p + accuracy and t is not 0:
            GPIO.output(17, True)
            print("Fan ON")
            pass
        elif t < set_p - accuracy and t is not 0:
            GPIO.output(17, False)
            print("Heater ON")
            pass
        elif t > set_p - accuracy or t < set_p + accuracy:
            print("OK...ALL OFF")
            GPIO.output(17, False)
            pass
        elif t is 0:
            pass
        
        set_p = str(set_p)
        
        if CHANGE is 0:
            disp.lcd_clear()
            set_up()
            break
        
if __name__ == "__main__":
    print("starting")
    main(set_p)