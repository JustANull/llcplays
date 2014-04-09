import subscriber

class CommandFilter(subscriber.Subscriber):
	def __init__(self, filteredWords):
		self.filteredWords = filteredWords

	def on_add(self, publisher):
		self.publisher = publisher

	def message(self, kind, *args):
		if kind == 'pubmsg':
			for word in self.filteredWords:
				if args[1].arguments[0].lower().find(word.lower()) != -1:
					self.publisher.parent.kick(args[1].source.nick)
