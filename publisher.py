class Publisher():
	def __init__(self, parent):
		self.parent = parent
		self.subscribers = {}

	def add_subscriber(self, identity, sub):
		self.subscribers[identity] = sub
		sub.on_add(self)

	def remove_subscriber(self, identity):
		self.subscribers[identity].on_remove()
		del self.subscribers[identity]

	def remove_all_subscribers(self):
		for identity in self.subscribers:
			self.subscribers[identity].on_remove()

		self.subscribers = {}

	def get_subscriber(self, identity):
		return self.subscribers[identity]

	def message(self, kind, *args):
		for identity in self.subscribers:
			self.subscribers[identity].message(kind, *args)
