#! /usr/bin/env python

import irc.bot
import json
import logging
import math
import sys
from pykeyboard import PyKeyboard
import pygame

class IRCOptions():
	def __init__(self, server, port, channel, nickname, secret):
		self.server = server
		self.port = port
		self.channel = channel
		self.nickname = nickname
		self.secret = secret

class WindowOptions():
	def __init__(self, width, height, fontsize, fontname):
		self.width = width
		self.height = height
		self.fontsize = fontsize
		self.fontname = fontname

class LLCPlays(irc.bot.SingleServerIRCBot):
	def __init__(self, ircopt, winopt, users, admins, commands):
		logging.debug('Initializing IRC bot...')
		irc.bot.SingleServerIRCBot.__init__(self, [(ircopt.server, ircopt.port, ircopt.secret)], ircopt.nickname, ircopt.nickname)

		self.channel = ircopt.channel

		self.width = winopt.width
		self.height = winopt.height
		self.fontsize = winopt.fontsize
		self.fontname = winopt.fontname

		self.users = users
		self.admins = admins
		self.commands = commands

		self.messages = [('Bot initialized!', '')]
		self.maxMessages = 0 #initialized later

		self.allowMessages = True

	def doDie(self):
		self.allowMessages = False
		self.messages = [('for maintenance NOW!', ''), ('The server is going down', '')]
		pygame.time.set_timer(pygame.USEREVENT + 0, 10000)

	def doRestart(self):
		self.allowMessages = False
		self.messages = [('Please standby for restart...', '')]
		pygame.time.set_timer(pygame.USEREVENT + 1, 10000)

	def on_nicknameinuse(self, c, e):
		logging.critical('Nickname was already in use! This should NEVER happen! Are you running multiple instances?')
		raise Exception('nickname in use')

	def on_welcome(self, c, e):
		logging.debug('Welcomed to the server. Joining the channel...')
		c.join(self.channel)

	def on_privmsg(self, c, e):
		logging.debug('Received a private message??')
		pass

	def on_pubmsg(self, c, e):
		logging.debug('Received a public message from ' + e.source.nick + '.')
		self.process(e, e.arguments[0])

	def on_dccmsg(self, c, e):
		logging.debug('Received a dcc message??')
		pass

	def on_dccchat(self, c, e):
		logging.debug('Received dcc chat??')
		pass

	def process(self, e, cmd):
		nick = e.source.nick
		c = self.connection

		if self.allowMessages:
			if nick in self.users and cmd in self.commands:
				logging.debug('Command accepted: ' + cmd)
				self.messages.insert(0, (nick, cmd))
				if len(self.messages) > self.maxMessages:
					self.messages = self.messages[:self.maxMessages]

				self.command(self.commands[cmd])
			if nick in self.admins:
				if cmd == '!die':
					self.doDie()
				elif cmd == '!restart':
					self.doRestart()

	def initPygame(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.font = pygame.font.SysFont('Courier', self.fontsize)
		self.maxMessages = int(math.ceil(self.height / self.font.get_height())) + 1

	def eventLoop(self, timeout = 0.2):
		logging.debug('Connecting to server...')
		self._connect()
		logging.debug('Initializing pygame...')
		self.initPygame()
		logging.debug('Beginning event loop...')

		while 1:
			self.ircobj.process_once(timeout)

			if pygame.event.peek():
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.disconnect()
						sys.exit()
					elif event.type == pygame.USEREVENT + 0:
						self.disconnect()
						sys.exit()
					elif event.type == pygame.USEREVENT + 1:
						self.disconnect()
						pygame.quit()
						return

			self.screen.fill((0, 0, 0))

			for i in range(len(self.messages)):
				leftText = self.font.render(self.messages[i][0], 1, (255, 255, 255), (0, 0, 0))
				rightText = self.font.render(self.messages[i][1], 1, (255, 255, 255), (0, 0, 0))
				ypos = self.height - (i + 1) * self.font.get_height()
				self.screen.blit(leftText, (8, ypos))
				self.screen.blit(rightText, (self.width - (8 + self.font.size(self.messages[i][1])[0]), ypos))

			pygame.display.flip()

	def command(self, cmd):
		logging.critical('Somebody instantiated the base class! This should NEVER happen!')
		raise Exception('virtual method call')

class LLCPlaysKeyboard(LLCPlays):
	def __init__(self, ircopt, winopt, users, admins, commands):
		LLCPlays.__init__(self, ircopt, winopt, users, admins, commands)
		self.k = PyKeyboard()

	def command(self, cmd):
		self.k.tap_key(cmd)

class LLCPlaysStdout(LLCPlays):
	def __init__(self, ircopt, winopt, users, admins, commands, fp = sys.stdout):
		LLCPlays.__init__(self, ircopt, winopt, users, admins, commands)
		self.fp = fp

	def command(self, cmd):
		self.fp.write(cmd)
		self.fp.flush()

def main():
	#logging.basicConfig(level=logging.DEBUG)

	while 1:
		ircopt = None
		with file('secret.json') as f:
			secret = json.load(f)
			ircopt = IRCOptions('irc.twitch.tv', 6667, '#llcplays', 'llcplays', secret[u'secret'])

		winopt = None
		users = []
		admins = []
		commands = {}
		with file('config.json') as f:
			config = json.load(f)
			winopt = WindowOptions(config[u'window'][u'width'], config[u'window'][u'height'], config[u'window'][u'fontsize'], config[u'window'][u'fontname'])
			users = config[u'users']
			admins = config[u'admins']
			commands = config[u'commands']

		bot = None
		if len(sys.argv) == 1:
			bot = LLCPlaysStdout(ircopt, winopt, users, admins, commands)
		elif len(sys.argv) == 2:
			if sys.argv[1] == 'keyboard':
				bot = LLCPlaysKeyboard(ircopt, winopt, users, admins, commands)
			elif sys.argv[1] == 'stdout':
				bot = LLCPlaysStdout(ircopt, winopt, users, admins, commands)
			else:
				logging.critical('The regex of options is: (|keyboard|(stdout (filename)?))')
				raise Exception("bad command line arguments")
		elif len(sys.argv) == 3 and sys.argv[1] == 'stdout':
			bot = LLCPlaysStdout(ircopt, winopt, users, admins, commands, open(sys.argv[2], 'w'))
		else:
			logging.critical('The regex of options is: (|keyboard|(stdout (filename)?))')
			raise Exception("bad command line arguments")

		bot.eventLoop()

if __name__ == '__main__':
	main()
