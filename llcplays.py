#! /usr/bin/env python

#note that save and load savestates are hardcoded to e and q, respectively.

import irc.bot
import json
import logging
import math
import sys
from pykeyboard import PyKeyboard
import pygame
import subprocess

class IRCOptions():
	def __init__(self, server, port, channel, nickname, secret):
		self.server = server
		self.port = port
		self.channel = channel
		self.nickname = nickname
		self.secret = secret

class WindowOptions():
	def __init__(self, title, width, height, fontsize, fontname):
		self.title = title
		self.width = width
		self.height = height
		self.fontsize = fontsize
		self.fontname = fontname

class TwitchBot(irc.bot.SingleServerIRCBot):
	def __init__(self, ircopt):
		irc.bot.SingleServerIRCBot.__init__(self, [(ircopt.server, ircopt.port, ircopt.secret)], ircopt.nickname, ircopt.nickname)
		self.connection.set_rate_limit(0.75)
		self.channel = ircopt.channel
		self.subscribers = {}
		self.live = True
		self.restart = False

	def add_subscriber(self, identity, sub):
		self.subscribers[identity] = sub
		sub.on_add(self)

	def remove_subscriber(self, identity):
		self.subscribers[identity].on_remove()
		del self.subscribers[identity]

	def remove_all_subscribers(self):
		for sub in self.subscribers:
			self.subscribers[sub].on_remove()
		self.subscribers = {}

	def get_subscriber(self, identity):
		return self.subscribers[identity]

	def on_nicknameinuse(self, conn, event):
		logging.critical('Nickname was already in use! This should NEVER happen! Are you running multiple instances?')
		raise Exception('nickname in use')

	def on_welcome(self, conn, event):
		conn.join(self.channel)
		conn.privmsg(self.channel, 'Now online!')

	def on_privmsg(self, conn, event):
		for sub in self.subscribers:
			self.subscribers[sub].on_privmsg(conn, event)

	def on_pubmsg(self, conn, event):
		for sub in self.subscribers:
			self.subscribers[sub].on_pubmsg(conn, event)

	def on_dccmsg(self, conn, event):
		for sub in self.subscribers:
			self.subscribers[sub].on_dccmsg(conn, event)

	def on_dccchat(self, conn, event):
		for sub in self.subscribers:
			self.subscribers[sub].on_dccchat(conn, event)

	def event_loop(self, timeout = 0.2):
		self._connect()

		while self.live:
			self.ircobj.process_once(timeout)

			for sub in self.subscribers:
				self.subscribers[sub].on_update()

		self.disconnect()

class TwitchSubscriber():
	def __init__(self):
		pass

	def on_add(self, bot):
		pass

	def on_remove(self):
		pass

	def on_privmsg(self, c, e):
		pass

	def on_pubmsg(self, c, e):
		pass

	def on_dccmsg(self, c, e):
		pass

	def on_dccchat(self, c, e):
		pass

	def on_update(self):
		pass

class Admin(TwitchSubscriber):
	def __init__(self, admins):
		self.admins = admins
		self.admincommands = {
			'!die': self.do_die,
			'!restart': self.do_restart
		}

	def do_die(self):
		self.bot.connection.privmsg(self.bot.channel, 'The bot is going down for maintenance, NOW!')
		self.bot.live = False

	def do_restart(self):
		self.bot.connection.privmsg(self.bot.channel, 'The bot is restarting for maintenance, NOW!')
		self.bot.live = False
		self.bot.restart = True

	def on_add(self, bot):
		self.bot = bot

	def on_pubmsg(self, conn, event):
		if event.source.nick in self.admins and event.arguments[0] in self.admincommands:
			self.admincommands[event.arguments[0]]()

class Display(TwitchSubscriber):
	def __init__(self, winopt, users, commands):
		self.messages = [('Bot initialized!', '')]

		self.title = winopt.title
		self.width = winopt.width
		self.height = winopt.height
		self.fontsize = winopt.fontsize
		self.fontname = winopt.fontname
		self.users = users
		self.commands = commands

	def on_add(self, bot):
		self.bot = bot
		pygame.init()
		pygame.time.set_timer(pygame.USEREVENT + 0, 32768)
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.title)
		self.font = pygame.font.SysFont(self.fontname, self.fontsize)
		self.maxMessages = int(math.ceil(self.height / self.font.get_height())) + 1

	def on_remove(self):
		pygame.quit()

	def add_message(self, left, right):
		self.messages.insert(0, (left, right))

		if len(self.messages) > self.maxMessages:
			self.messages = self.messages[:self.maxMessages]

	def on_pubmsg(self, conn, event):
		if event.source.nick in self.users and event.arguments[0] in self.commands:
			self.add_message(event.source.nick, event.arguments[0])

	def on_update(self):
		if pygame.event.peek():
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.USEREVENT + 0:
					pygame.time.set_timer(pygame.USEREVENT + 0, 0)
					pygame.time.set_timer(pygame.USEREVENT + 1, 1000 * 60 * 5)
					self.bot.get_subscriber('control').raw_command('q')
				elif event.type == pygame.USEREVENT + 1:
					self.bot.get_subscriber('control').raw_command('e')

		self.screen.fill((0, 0, 0))

		for i in range(len(self.messages)):
			leftText = self.font.render(self.messages[i][0], 1, (255, 255, 255), (0, 0, 0))
			rightText = self.font.render(self.messages[i][1], 1, (255, 255, 255), (0, 0, 0))
			ypos = self.height - (i + 1) * self.font.get_height()
			self.screen.blit(leftText, (8, ypos))
			self.screen.blit(rightText, (self.width - (8 + self.font.size(self.messages[i][1])[0]), ypos))

		pygame.display.flip()

class Control(TwitchSubscriber):
	def __init__(self, users, commands):
		self.users = users
		self.commands = commands

	def on_add(self, bot):
		self.bot = bot

	def on_pubmsg(self, conn, event):
		if event.source.nick in self.users and event.arguments[0] in self.commands:
			self.do_command(event.arguments[0])

	def raw_command(self, cmd):
		pass

	def do_command(self, cmd):
		pass

class ControlKeyboard(Control):
	def __init__(self, users, commands):
		Control.__init__(self, users, commands)
		self.k = PyKeyboard()

	def raw_command(self, cmd):
		self.k.tap_key(cmd)

	def do_command(self, cmd):
		self.k.tap_key(self.commands[cmd])

class ControlStdout(Control):
	def __init__(self, users, commands, fp = sys.stdout):
		Control.__init__(self, users, commands)
		self.fp = fp

	def raw_command(self, cmd):
		self.fp.write(cmd)
		self.fp.flush()

	def do_command(self, cmd):
		self.fp.write(self.commands[cmd])
		self.fp.flush()

class Moderator(TwitchSubscriber):
	def __init__(self, admins, bannedWords):
		self.admins = admins
		self.bannedWords = bannedWords

	def on_add(self, bot):
		self.bot = bot

	def on_pubmsg(self, conn, event):
		if not event.source.nick in self.admins:
			for word in self.bannedWords:
				if event.arguments[0].lower().find(word.lower()) != -1:
					self.bot.get_subscriber('display').add_message('kicked user:', event.source.nick)
					conn.privmsg(self.bot.channel, '.timeout ' + event.source.nick + ' 1')

class Subprocess(TwitchSubscriber):
	def __init__(self, commands):
		self.commands = commands

	def on_add(self, bot):
		self.process = popen(self.commands)

	def on_remove(self):
		self.process.terminate()

def main():
	#logging.basicConfig(level = logging.DEBUG)

	secret = ''
	with file('secret.json') as f:
		secret = json.load(f)[u'secret']

	ircopt = None
	winopt = None
	users = []
	admins = []
	commands = {}
	bannedWords = []
	with file('config.json') as f:
		config = json.load(f)
		irc = config[u'irc']
		window = config[u'window']

		ircopt = IRCOptions('irc.twitch.tv', irc[u'port'], irc[u'channel'], irc[u'username'], secret)
		winopt = WindowOptions(window[u'title'], window[u'width'], window[u'height'], window[u'fontsize'], window[u'fontname'])

		users = config[u'users']
		admins = config[u'admins']
		commands = config[u'commands']
		bannedWords = config[u'bannedWords']

	bot = TwitchBot(ircopt)
	bot.add_subscriber('admin', Admin(admins))
	bot.add_subscriber('display', Display(winopt, users, commands))
	bot.add_subscriber('moderator', Moderator(admins, bannedWords))
	#bot.add_subscriber('emulator', Subprocess(['run_emulator']))

	if len(sys.argv) == 1:
		bot.add_subscriber('control', ControlStdout(users, commands))
	elif len(sys.argv) == 2:
		if sys.argv[1] == 'keyboard':
			bot.add_subscriber('control', ControlKeyboard(users, commands))
		elif sys.argv[1] == 'stdout':
			bot.add_subscriber('control', ControlStdout(users, commands))
		else:
			raise Exception('bad command line arguments')
	elif len(sys.argv) == 3 and sys.argv[1] == 'stdout':
		bot.add_subscriber('control', ControlStdout(users, commands, open(sys.argv[2], 'w')))
	else:
		raise Exception('bad command line arguments')

	bot.event_loop()
	if bot.restart:
		bot.remove_all_subscribers()
		main()

if __name__ == '__main__':
	main()
