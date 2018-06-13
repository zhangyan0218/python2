import logging


class Logger:
	def __init__(self, logName, logLevel, logFilePath):
		self.logger = logging.getLogger(logName)
		self.logger.setLevel(logLevel)

		fh = logging.FileHandler(logFilePath)
		fh.setLevel(logLevel)

		ch = logging.StreamHandler()
		ch.setLevel(logLevel)

		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

	def getlog(self):
		return self.logger