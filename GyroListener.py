# Imports for multiprocessing
from multiprocessing.connection import Client
# Imports for bluetooth
import gatt
import struct
#Imports for CSV
import time
import csv
import datetime
sum  = None
threshold = False


# Setting up bluetooth
def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))

def hexStrToInt(value):
	#print("initial hex string", value)
	#print("x coord", value[0:2])
	#print("y coord", value[2:4])
	#print("z coord", value[4:6])
	val = struct.unpack('>h', value[0:2])
	xyz = [0,0,0]
	xyz[0] = val[0]
	val = struct.unpack('>h', value[2:4])
	xyz[1] = val[0]
	val = struct.unpack('>h', value[4:6])
	xyz[2] = val[0]

	print("Gyro Sensor Values x,y,z")
	for v in xyz:
		print(v)

	return xyz

class HexiDevice(gatt.Device):

	def helloWorld(self):
		print("HELLO WORLD!")

	def connect_succeeded(self):
		super().connect_succeeded()
		print("[%s] Connected" % (self.mac_address))

	def connect_failed(self,error):
		super().connect_failed(error)
		print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

	def disconnect_succeeded(self):
		super().disconnect_succeeded()
		print("[%s] Disconnected" % (self.mac_address))


	def getGyro(self):
		chosen_service = next(
			s for s in self.services
			if s.uuid == '00002000-0000-1000-8000-00805f9b34fb')

		chosen_characteristic = next(
			c for c in chosen_service.characteristics
			if c.uuid == '00002002-0000-1000-8000-00805f9b34fb')

		chosen_characteristic.read_value()
		self.previous_val = 0
		manager.stop()



	def services_resolved(self):
		super().services_resolved()
		self.getGyro()

	def characteristic_read_value_failed(self, characteristic, error):
		print("READ FAILED ", error)

	def characteristic_enable_notifications_succeeded(self, characteristic):
		print("notifications succeeded!")


	def characteristic_enable_notifications_failed(self, characteristic, error):
		print("notifications failed! ", error)

	def characteristic_value_updated(self, characteristic, value):
		xyz = hexStrToInt(value)
		global sum
		sum = 0
		global threshold
		for v in xyz:
			sum = abs(v) + sum
		print("Sum ", sum)
		self.previous_val = xyz[0]
		global manager
		manager.stop()
		print("Characteristic updated")


def main():

	# Connect bluetooth
	DEVICE1 = "00:3E:50:04:00:36"
	DEVICE2 = "00:40:40:0C:00:4A"

	global manager
	global sum
	manager = gatt.DeviceManager(adapter_name='hci0')

	hexiwear1 = HexiDevice(mac_address=DEVICE1, manager=manager)
	hexiwear1.connect()

	# Multiprocessing client
	#cli = Client(('192.168.56.1', 5005))
	#cli = Client(('localhost',5005))

	manager.run()
	print("Gyro end")
	return sum

if __name__ == "__main__":
	main()
