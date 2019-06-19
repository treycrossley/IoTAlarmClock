#import libraries
import RPi.GPIO as GPIO
import time
import datetime

#set GPIO numbering mode and define output pins
LED1=7
pwm1 = None
bright = 1
alert_time = None
alarm_time = None
snooze = 300
#invalid_alarm = False


def getAlarm():
	global alarm_time
	file = open("alarm.txt", "r")
	alarm_str = file.readline()
	alarm_str = alarm_str.strip()
	print("alarm string",alarm_str)
	print("current time", datetime.datetime.now())
	alarm_time = datetime.datetime.strptime(alarm_str, '%m/%d/%y %H:%M:%S')
	print("alarm time", alarm_time)
	if (datetime.datetime.now() - alarm_time).total_seconds() > 0:
		print("INVALID ALARM TIME. GO TO THE FUTURE")
		invalid_alarm = true
		exit()

def cycle():
	global bright
	#Continue writing to the LED as long  as
	#current time is within the snooze limit
	while (datetime.datetime.now() - alarm_time).total_seconds() < snooze:

		print("Current time: ", datetime.datetime.now())
		print("Alert Time: ", alert_time)
		elapsed = abs(datetime.datetime.now() - alert_time)
		delt = abs(alarm_time - alert_time)
		#print("Total time: ", denom.total_seconds())
		frac = (elapsed.total_seconds() / delt.total_seconds())
		print("Frac: ", frac)
		bright = 100*frac
		print("Pre Brightness: ", bright)
		if bright > 100:
			bright = 100
		if bright < 0:
			bright = 0
		print("Bright: ", bright)
		pwm1.ChangeDutyCycle(bright)
		time.sleep(10)


def circuitSetup():
	global LED1
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED1, GPIO.OUT)
	global pwm1
	pwm1 = GPIO.PWM(LED1,1000)
	pwm1.start(0)


def endCircuit():
	GPIO.cleanup()

def main():
	global alert_time
	alert_time = datetime.datetime.now()
	getAlarm()
	if (alarm_time-alert_time).total_seconds() <= 0:
		print("Invalid alarm. Consider changing to a future time")
	else:
		circuitSetup()

		cycle()

		endCircuit()

if __name__ == '__main__':
	main()
