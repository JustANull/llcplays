import subscriber

class Moderator(subscriber.Subscriber):
	def __init__(self, admins, bannedWords):
		self.admins = admins
		self.bannedWords = bannedWords

	def on_add(self, publisher):
		self.publisher = publisher

	def message(self, kind, *args):
		if kind == 'pubmsg' and not args[1].source.nick in self.admins:
			for word in self.bannedWords:
				if args[1].arguments[0].lower().find(word.lower()) != -1:
					self.publisher.parent.kick(args[1].source.nick)
