import subscriber

class Admin(subscriber.Subscriber):
	def __init__(self, admins):
		self.admins = admins
		self.admincommands = {
			'!die':    	self.do_die,
			'!restart':	self.do_restart,
			'!save':   	self.do_save,
			'!load':   	self.do_load
		}

	def do_die(self):
		self.publisher.parent.say('The bot is going down for maintenance, NOW!')
		self.publisher.parent.live = False

	def do_restart(self):
		self.publisher.parent.say('The bot is restarting, NOW!')
		self.publisher.parent.live = False
		self.publisher.parent.restart = True

	def do_save(self):
		self.publisher.get_subscriber('display').add_message('Saved the game.', '')
		self.publisher.get_subscriber('control').save()

	def do_load(self):
		self.publisher.get_subscriber('display').add_message('Loaded the game.', '')
		self.publisher.get_subscriber('control').load()

	def on_add(self, publisher):
		self.publisher = publisher

	def message(self, kind, *args):
		if kind == 'pubmsg' and args[1].source.nick in self.admins and args[1].arguments[0] in self.admincommands:
			self.admincommands[args[1].arguments[0]]()
