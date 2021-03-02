#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

#syslog configuration
#import logging
#import logging.handlers
#import socket
#my_logger_91 = logging.getLogger('MY_Logger_91')
#my_logger_161 = logging.getLogger('MY_Logger_161')

#my_logger_91.setLevel(logging.INFO)
#my_logger_161.setLevel(logging.INFO)

#define Syslog handler (UDP)
#handler_91 = logging.handlers.SysLogHandler(address = ('x.x.x.x',514), socktype = socket.SOCK_DGRAM)
#handler_161 = logging.handlers.SysLogHandler(address = ('x.x.x.x',514), socktype = socket.SOCK_DGRAM)

#x.x.x.x is the syslog ip, or can be localhost

#my_logger_91.addHandler(handler_91)
#my_logger_161.addHandler(handler_161)

#end of syslog configuration

from datetime import datetime
from time import sleep
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

GPIO.setmode(GPIO.BCM)

#pin for the led
ledpin = 13

GPIO.setup(ledpin, GPIO.OUT)

#pin for sensor
pin = 26

connection = mysql.connector.connect(host='localhost', database='RaspberryPI', user='test', password='password')
cursor=connection.cursor(prepared=True)

def laser_detector (pin):
	light = 0

	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(0.1)

	GPIO.setup(pin, GPIO.IN)

	while True:
		if (GPIO.input(pin) == GPIO.LOW):
			if (light == 0):
				continue
			print 'no laser detected'
			value = "Motion Detected"
			now = datetime.now()
			now = now.strftime("%Y-%m-%d %H:%M:%S\n")
			print now
                        #send to syslog
                        #my_logger_91.info("Prototype02 - no laser detected\n")
                        #my_logger_91.handlers[0].flush()
                        #my_logger_161.info("Prototype02 - no laser detected\n")
                        #my_logger_161.handlers[0].flush()
                        
			mysql_insert_query = """INSERT INTO Laser (date_time,value) VALUES (%s,%s)"""
			records=(now,value)
			cursor.execute(mysql_insert_query,records)
			connection.commit()

			GPIO.output(ledpin, GPIO.LOW)
			light = 0
			sleep(0.1)
		else:
			if (light == 1):
				continue
			print 'laser detected'
			now = datetime.now()
			now = now.strftime("%Y-%m-%d %H:%M:%S\n")
			print now
                        #send to syslog
                        #my_logger_91.info("Prototype02 - laser detected\n")
                        #my_logger_91.handlers[0].flush()
                        #my_logger_161.info("Prototype02 - laser detected\n")
                        #my_logger_161.handlers[0].flush()
                        

			GPIO.output(ledpin, GPIO.HIGH)
			light = 1
			sleep(0.1)
try:
	while True:
		print laser_detector(pin)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
