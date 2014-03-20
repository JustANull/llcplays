import subprocess
import subscriber

class Process(subscriber.Subscriber):
	def __init__(self, commands):
		self.commands = commands

	def on_add(self, publisher):
		self.process = subprocess.Popen(self.commands)

	def on_remove(self):
		self.process.terminate()
