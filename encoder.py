import RPi.GPIO as GPIO
import time

encoder_pin11 = 13 #motorA
encoder_pin12 = 12
# encoder_pin21 = 15 #motorB
# encoder_pin22 = 16
# encoder_pin31 = 21 #motorC
# encoder_pin32 = 22
# encoder_pin41 = 23 #motorD
# encoder_pin42 = 24

encoder1 = 0
# encoder2 = 0
# encoder3 = 0
# encoder4 = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup([encoder_pin11, encoder_pin12], GPIO.IN)
# GPIO.setup([encoder_pin21, encoder_pin22], GPIO.IN, GPIO.PUD_UP)
# GPIO.setup([encoder_pin31, encoder_pin32], GPIO.IN, GPIO.PUD_UP)
# GPIO.setup([encoder_pin41, encoder_pin42], GPIO.IN, GPIO.PUD_UP)
# GPIO.add_event_detect(encoder_pin11, GPIO.RISING, callback=add_encoder1)
# GPIO.add_event_detect(encoder_pin21, GPIO.RISING, callback=add_encoder2, bouncetime=1)
# GPIO.add_event_detect(encoder_pin31, GPIO.RISING, callback=add_encoder3, bouncetime=1)
# GPIO.add_event_detect(encoder_pin41, GPIO.RISING, callback=add_encoder4, bouncetime=1)

# def add_encoder1(x):
#     global encoder1
#     # print("interrupted!!")
#     value = GPIO.input(encoder_pin12)
#     if value == GPIO.HIGH:
#         encoder1 = encoder1 + 1
#     else:
#         encoder1 = encoder1 - 1
#     print('In :', encoder1)

# def add_encoder2(x):
#     global encoder2
#     value = GPIO.input(encoder_pin22)
#     #print("interrupted!!")
#     if value == GPIO.HIGH:
#         encoder2 = encoder2 + 1
#     else:
#         encoder2 = encoder2 - 1

# def add_encoder3(x):
#     global encoder3
#     value = GPIO.input(encoder_pin32)
#     #print("interrupted!!")
#     if value == GPIO.HIGH:
#         encoder3 = encoder3 + 1
#     else:
#         encoder3 = encoder3 - 1

# def add_encoder4(x):
#     global encoder4
#     value = GPIO.input(encoder_pin42)
#     #print("interrupted!!")
#     if value == GPIO.HIGH:
#         encoder4 = encoder4 + 1
#     else:
#         encoder4 = encoder4 - 1

# input_pin = 12

try:
    flag = True
    while True:
        if (GPIO.input(encoder_pin12) == GPIO.HIGH) and flag: 
            flag = False
            print("1")
        else:
            flag = True
            print("0")

        # print(encoder1)
        time.sleep(0.01)
except KeyboardInterrupt: # Catch CTRL+C and clean up
    GPIO.cleanup()