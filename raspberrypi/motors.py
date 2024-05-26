import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG= 23
ECHO =24


def init():
 TRIG= 23
 ECHO =24
 GPIO.setmode(GPIO.BCM)
 GPIO.setup (TRIG, GPIO.OUT)
 GPIO.setup (ECHO, GPIO.IN) 

 GPIO.setup(17, GPIO.OUT)
 GPIO.setup(22, GPIO.OUT)
 GPIO.setup(16, GPIO.OUT)
 GPIO.setup(26, GPIO.OUT)

def forward(sec):
 GPIO.output(17, True)
 GPIO.output(22, False)
 GPIO.output(16, True) 
 GPIO.output(26, False)
 time.sleep(sec)
 #GPIO.cleanup()

def reverse(sec):
 GPIO.output(17, False)
 GPIO.output(22, True)
 GPIO.output(16, False) 
 GPIO.output(26, True)
 time.sleep(sec)
 #GPIO.cleanup()

def stop(sec):
 GPIO.output(17, False)
 GPIO.output(22, False)
 GPIO.output(16, False) 
 GPIO.output(26, False)
 time.sleep(sec)
 #GPIO.cleanup()

def turn(sec):
 GPIO.output(17, True)
 GPIO.output(22, False)
 GPIO.output(16, False) 
 GPIO.output(26, True)
 time.sleep(sec)


def measure_distance():
 #GPIO.output(23, False)
 print('testing')
 GPIO.output (23, True) 
 time.sleep(0.00001) 
 GPIO.output (23, False)
 while GPIO.input (ECHO)==0: 
  pulse_start = time.time()
 while GPIO.input (ECHO)==1:
  pulse_end = time.time()
 pulse_duration = pulse_end - pulse_start
 distance = pulse_duration * 17150
 distance = round(distance, 2)
 print("Distance:",distance, "cm")
 return distance 

try:
 while True:
  init()
  time.sleep(0.005)
  distance =  measure_distance() 
  if distance < 40:
   turn(0)
  else:
   forward(0)
  
except KeyboardInterrupt: 
 stop(0) 
 GPIO.cleanup()
