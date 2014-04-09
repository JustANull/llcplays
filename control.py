import subscriber

LOAD_BUTTON = '1'
SAVE_BUTTON = '2'

class Control(subscriber.Subscriber):
	def __init__(self, users, commands):
		self.users = users
		self.commands = commands

	def message(self, kind, *args):
		if kind == 'pubmsg':
			allowedUser = True

			if self.users:
				allowedUser = args[1].source.nick in self.users

			if allowedUser and args[1].arguments[0] in self.commands:
				self.do_command(args[1].arguments[0])

	def raw_command(self, cmd):
		pass

	def do_command(self, cmd):
		pass
