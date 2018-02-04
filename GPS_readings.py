class GPS_readings:
	def __init__(self, latitude=None, latitude_dir=None, longitude=None, longitude_dir=None,
		year=None, month=None, day=None, hour=None, minutes=None, seconds=None, centiseconds=None,
		num_satellites=None, speed=None, heading=None, altitude=None):
		self.latitude = latitude
		self.latitude_dir = latitude_dir
		self.longitude = longitude
		self.longitude_dir = longitude_dir
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minutes = minutes
		self.seconds = seconds
		self.centiseconds = centiseconds
		self.num_satellites = num_satellites
		self.speed = speed
		self.heading = heading
		self.altitude = altitude