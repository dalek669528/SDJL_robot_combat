import RPi.GPIO as GPIO
import time

# Pin definition
pwm_pin = 18 # adjust brightness for signal
led_pin = 23 # blink when switch pressed
clk_pin = 14 # rotary clock
but_pin = 24 # button input
dat_pin = 25 # rotary data input

DUTY_CYCLE = 50 # initial duty cycle
DUTY_STEP = 10 # increments for pwm

# Pin Setup
GPIO.setmode(GPIO.BCM) # Broadcom numbering
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, 50) # initialize pwm led
GPIO.setup(but_pin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(clk_pin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(dat_pin, GPIO.IN, GPIO.PUD_UP)
pwm.start(DUTY_CYCLE)

def set_duty(value):
    """Limit duty range to 0-100"""
    global DUTY_CYCLE
    if value > 100:
        value = 100
    elif value < 0:
        value = 0
    DUTY_CYCLE = value
    #print('New Brighness: %s' % DUTY_CYCLE)
    pwm.ChangeDutyCycle(DUTY_CYCLE)

def rotary_on_change(channel):
    """Called whenever the encoder moves"""
    global DUTY_CYCLE
    #print('Old Brighness: %s' % DUTY_CYCLE)
    if GPIO.input(dat_pin): #forward
        #print("Going up")
        set_duty(DUTY_CYCLE + DUTY_STEP)
    else: # rotate backward
        #print("Going down")
        set_duty(DUTY_CYCLE - DUTY_STEP)

def blink_led(channel=None):
    """uh... make it blink"""
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.075)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.075)


print("Here we go! Press CTRL+C to exit")

try:
    GPIO.output(led_pin, GPIO.LOW)

    # configure rotary callback
    GPIO.add_event_detect(clk_pin,
                          GPIO.FALLING,
                          callback=rotary_on_change,
                          bouncetime=200)
    
    # configure button callback
    GPIO.add_event_detect(but_pin,
                            GPIO.FALLING,
                            callback=blink_led,
                            bouncetime=200)
    # main loop
    while 1:
        print("Current Brightness: %s" % DUTY_CYCLE)
        time.sleep(1)

except KeyboardInterrupt: # Catch CTRL+C and clean up
    pwm.stop()
    GPIO.cleanup()