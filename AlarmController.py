import GyroListener
import LightProtocol
#import DataParser
import datetime
import csv
alarm_time = None
snooze = 300
xyz = [0, 0 ,0]

def setGyro(x,y,z):
	global xyz
	xyz[0] = x
	xyz[1] = y
	xyz[2] = z

def getGyro():
	global xyz
	return xyz

def getAlarm():
	global alarm_time
	file = open("alarm.txt", "r")
	alarm_str = file.readline()
	alarm_str = alarm_str.strip()
	#print("alarm string",alarm_str)
	#print("current time", datetime.datetime.now())
	alarm_time = datetime.datetime.strptime(alarm_str, '%m/%d/%y %H:%M:%S')
	#print("alarm time", alarm_time)
	if (datetime.datetime.now() - alarm_time).total_seconds() > 0:
		print("INVALID ALARM TIME. GO TO THE FUTURE")
		invalid_alarm = true
		exit()


def initializeCSV():
	with open('data.csv', mode='w+') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
		for i in range(0,6):
			csv_writer.writerow([datetime.datetime.now(), 0, 0, 0])


def main():
	global xyz
	#initializeCSV()
	getAlarm()
	threshold = 5000
	while 1:
		try:
			#Grab a data reading of the gyroscope
			#And write it to data CSV file
			global xyz
			print("ENTERING GYRO LISTENER")

			sum = GyroListener.main()
			#print("Alarm Sum = ", sum)
			
			#Test data to see if it hits threshold
			#If it does, start light protocol
			if sum > threshold:
				print("PASSES THRESHOLD")
				break

			#If Enough time has elapsed, start light protocl
			if (datetime.datetime.now() - alarm_time).total_seconds() > snooze:
				print("TIME TO WAKE UP")
				break

			#Else, keep the loop going!

		except KeyboardInterrupt:
			sys.exit(0)

	print("LIGHT THIS BABY UP")
	LightProtocol.main()

if __name__ == "__main__":
	main()
