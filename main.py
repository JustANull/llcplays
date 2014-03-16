import irc.bot
import json
from pykeyboard import PyKeyboard

class LLCPlays(irc.bot.SingleServerIRCBot):
	def __init__(self, channel, nickname, secret, server, port=6667):
		with file('glue.json') as f:
			glue = json.load(f)
			self.users = glue[u'users']
			self.admins = glue[u'admins']
			self.commands = glue[u'commands']

		irc.bot.SingleServerIRCBot.__init__(self, [(server, port, secret)], nickname, nickname)
		self.channel = channel
		self.k = PyKeyboard()
		self.admincommands = {
			'!die':	lambda: self.die(),
		}

	def on_nicknameinuse(self, c, e):
		c.nick(c.getnickname() + '_')

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		pass

	def on_pubmsg(self, c, e):
		self.process(e, e.arguments[0])

	def on_dccmsg(self, c, e):
		pass

	def on_dccchat(self, c, e):
		pass

	def process(self, e, cmd):
		nick = e.source.nick
		c = self.connection

		if nick in self.users and cmd in self.commands:
			self.k.tap_key(self.commands[cmd])
		if nick in self.admins and cmd in self.admincommands:
			self.admincommands[cmd]()

if __name__ == '__main__':
	bot = LLCPlays('#llcplays', 'llcplays', "ENTER PASSWORD HERE", 'irc.twitch.tv')
	bot.start()
