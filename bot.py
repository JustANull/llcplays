import irc.bot
import publisher

class Twitch(irc.bot.SingleServerIRCBot):
	def __init__(self, ircopt):
		irc.bot.SingleServerIRCBot.__init__(self, [(ircopt.server, ircopt.port, ircopt.secret)], ircopt.nickname, ircopt.nickname)
		self.connection.set_rate_limit(0.75)	#if you send more than 20 messages in 30 seconds to Twitch, you get banned for 8 hours
		self.publisher = publisher.Publisher(self)
		self.channel = ircopt.channel
		self.live = True
		self.restart = False

	def on_nicknameinuse(self, conn, event):
		raise Exception('nickname in use')

	def on_welcome(self, conn, event):
		conn.join(self.channel)
		conn.privmsg(self.channel, 'Now online!')

	def on_privmsg(self, conn, event):
		self.publisher.message('privmsg', conn, event)

	def on_pubmsg(self, conn, event):
		self.publisher.message('pubmsg', conn, event)

	def on_dccmsg(self, conn, event):
		self.publisher.message('dccmsg', conn, event)

	def on_dccchat(self, conn, event):
		self.publisher.message('dccchat', conn, event)

	def event_loop(self, timeout = 0.1):
		self._connect()

		while self.live:
			self.ircobj.process_once(timeout)
			self.publisher.message('update')

		self.disconnect()

	def say(self, message):
		self.connection.privmsg(self.channel, message)

	def kick(self, username):
		self.connection.privmsg(self.channel, '.timeout ' + username + ' 1')
