import serial
import time
import os

class GPS:
	def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
		self.port = port
		self.baudrate = baudrate
		self.ser = serial.Serial(port=self.port, baudrate=self.baudrate) 
		self.initialized = False
		self.current_milli_time = lambda: int(round(time.time() * 1000))
		self.valid_coords = False
		self.valid_satellites = False

	def attach(self):
		if self.initialized is True:
			return False
		
		self.port.write(str.encode('AT+CGNSPWR=1' + '\r\n')) #Power on the GPS antenna, should return OK
		if wait_for_reply('OK\r\n', 2000) is not True:
			return False
		
		self.port.write(str.encode('AT+CGNSTST=1' + '\r\n'))
		if wait_for_reply('OK\r\n', 2000) is not True:
			return False
		

		self.initialized = True
		return True

	def detach(self):
		self.port.write(str.encode('AT+CGNSPWR=0' + '\r\n')) #Power off the GPS antenna, should return OK
		self.initialized = False

	def get_readings(self):
		if self.ser.in_waiting:
			received_nmea = self.ser.readline()

			tokens = received_nmea.split(',')
			readings = None
			# If the sentence is a RMC sentence and the data is valid
			if tokens[0] == '$GPRMC':
				self.valid_satellites = False
				if tokens[1] != '':
					time = tokens[1]
					hour = time[:2]
					minutes = time[2:4]
					seconds = time[4:6]
					centiseconds = time[7:]

					date = tokens[9]
					day = date[:2]
					month = date[2:4]
					year = date[4:]

					readings = GPS_readings.GPS_readings(hour=hour,minutes=minutes, seconds=seconds, centiseconds=centiseconds,
				 							day=day, month=month, year=year)
				
				if tokens[2] == 'A':
					latitude = tokens[3]
					latitude_direction = tokens[4]

					longitude = tokens[5]
					longitude_direction = tokens[6]

					readings.latitude = latitude
					readings.latitude_direction = latitude_direction
					readings.longitude = longitude
					readings.longitude_direction = longitude_direction

					self.valid_coords = True

			if tokens[0] == '$GPGSV':
				self.valid_satellites = True
				self.valid_coords = False
				num_satellites = tokens[3]
				if readings is not None: 
					readings.num_satellites = num_satellites
				else:
					readings = GPS_readings.GPS_readings(num_satellites=num_satellites)
			return readings

		else:
			return None


	def wait_for_reply(self, reply, timeout):
		start_time = self.current_milli_time()
		while (self.current_milli_time() - start_time) < timeout:
			if self.ser.in_waiting:
				line = self.ser.readline()
				if line == reply:
					return True

		return False


