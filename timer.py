import subscriber
import time

class Timer(subscriber.Subscriber):
	def __init__(self, time, fn):
		self.accum = 0
		self.time = time
		self.fn = fn

	def on_add(self, bot):
		self.then = time.time()
		self.now = time.time()

	def message(self, kind, *args):
		if kind == 'update':
			self.then = self.now
			self.now = time.time()
			self.accum = self.accum + self.now - self.then
			print self.accum

			if self.accum >= self.time:
				self.accum -= self.time
				self.fn()
