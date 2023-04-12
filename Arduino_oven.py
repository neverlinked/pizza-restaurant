import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
import requests

arduino = CustomPymata4(com_port = "COM7")

BUTTON1PIN = 8
BUTTON2PIN = 9
BUZZER = 3
pin_red = LEDPINS= 4
pin_green = LEDPINS= 5
pin_blue = LEDPINS=6
pin_yellow = LEDPINS= 7
trigger = 0
add_time =0
def safetycheck(safety_break):
    global trigger
    trigger = safety_break[2]
def set_timer(time_up):
    global add_time
    add_time = time_up[2] 
def setup():
    arduino.set_pin_mode_digital_input_pullup(BUTTON1PIN, callback=safetycheck)
    arduino.set_pin_mode_digital_input_pullup(BUTTON2PIN, callback=set_timer)
    arduino.set_pin_mode_digital_output(BUZZER)
    arduino.displayOn()

    
def loop():
    time.sleep(1)
    arduino.displayShow('0')
    arduino.digital_pin_write(pin_green, 1)
    Timer = 0
    while trigger !=0:
        arduino.digital_read(BUTTON1PIN)
        time.sleep(0.5)
    
    Pizza_ready= 'Pizza is not sir Luigi'
    arduino_data = {"Pizza": Pizza_ready, }
    response = requests.post('http://localhost:5000/update_arduino', json = arduino_data)

    arduino.digital_pin_write(pin_green, 0)
    arduino.digital_pin_write(pin_blue, 1)
    while add_time !=0:
        arduino.displayShow(Timer)
        Timer +=10
        minutes = Timer // 60
        seconds = Timer % 60
        display_time = '{:02d}.{:02d}'.format(minutes, seconds)
        arduino.displayShow(display_time)
        arduino.digital_read(BUTTON2PIN)
        time.sleep(0.5)


    arduino.digital_pin_write(pin_yellow, 1)
    arduino.digital_pin_write(pin_blue, 0)
    print('Press the button to start the timer Sir Luigi')
    while trigger != 0:
        arduino.digital_read(BUTTON1PIN)
        time.sleep(0.5)

    while Timer !=0 and add_time!=0:
        arduino.digital_pin_write(pin_red, 1)
        arduino.digital_pin_write(pin_yellow, 0)
        minutes = Timer // 60
        seconds = Timer % 60
        display_time = '{:02d}.{:02d}'.format(minutes, seconds)
        Timer -=1
        time.sleep(1)
        arduino.displayShow(display_time)

    arduino.displayShow('0000')
    arduino.digital_pin_write(pin_green, 1)
    arduino.digital_pin_write(pin_red, 0)
    arduino.digital_pin_write(BUZZER, 1)
    arduino.play_tone(BUZZER, 1000, 500)
    Pizza_ready= 'Pizza is ready sir Luigi'
    time.sleep(5)
    arduino.digital_pin_write(BUZZER, 0) 
        
        
    arduino_data = {"Pizza": Pizza_ready, }
    response = requests.post('http://localhost:5000/update_arduino', json = arduino_data)
    time.sleep(6)



setup()
while True:
    try:
        loop()
    except KeyboardInterrupt: # Shutdown Firmata on Crtl+C.
        print ('Bye Bye')
        arduino.shutdown()
        sys.exit(0)  
