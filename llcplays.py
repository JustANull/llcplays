#! /usr/bin/env python

import json
import sys

import bot
import options

import admin
import commandfilter
import display
import moderator
import process
import timer

def main():
	#logging.basicConfig(level = logging.DEBUG)

	secret = ''
	with file('secret.json') as f:
		secret = json.load(f)[u'secret']

	ircopt = None
	winopt = None
	users = None
	admins = []
	commands = {}
	bannedWords = []
	with file('config.json') as f:
		config = json.load(f)
		irc = config[u'irc']
		window = config[u'window']

		ircopt = options.IRC(irc[u'server'], irc[u'port'], irc[u'channel'], irc[u'username'], secret)
		winopt = options.Window(window[u'title'], window[u'width'], window[u'height'], window[u'fontsize'], window[u'fontname'])

		if not window[u'enabled']:
			winopt = None

		if u'users' in config:
			users = config[u'users']
		admins = config[u'admins']
		commands = config[u'commands']
		bannedWords = config[u'bannedWords']
		filteredWords = config[u'filteredWords']

	daemon = bot.Twitch(ircopt)

	def doLoad():
		daemon.publisher.get_subscriber('loadTimer').fn = lambda: None;
		daemon.publisher.get_subscriber('control').load()

	def doSave():
		daemon.publisher.get_subscriber('control').save()

	daemon.publisher.add_subscriber('loadTimer', timer.Timer(20, doLoad))
	daemon.publisher.add_subscriber('saveTimer', timer.Timer(60 * 5, doSave))

	daemon.publisher.add_subscriber('admin', admin.Admin(admins))
	daemon.publisher.add_subscriber('commandfilter', commandfilter.CommandFilter(filteredWords))
	daemon.publisher.add_subscriber('moderator', moderator.Moderator(admins, bannedWords))

	if winopt:
		daemon.publisher.add_subscriber('display', display.Display(winopt, users, commands))
	else:
		daemon.publisher.add_subscriber('display', display.DummyDisplay())

	control = None
	if len(sys.argv) == 1:
		import controlkeyboard
		control = controlkeyboard.ControlKeyboard(users, commands)
	elif len(sys.argv) == 2:
		if sys.argv[1] == 'stdout':
			import controlstdout
			control = controlstdout.ControlStdout(users, commands)
		else:
			raise Exception('bad command line arguments')
	elif len(sys.argv) == 3 and sys.argv[1] == 'stdout':
		import controlstdout
		control = controlstdout.ControlStdout(users, commands, open(sys.argv[2], 'w'))
	else:
		raise Exception('bad command line arguments')
	daemon.publisher.add_subscriber('control', control)

	daemon.event_loop()
	daemon.publisher.remove_all_subscribers()

	if daemon.restart:
		main()

if __name__ == '__main__':
	main()
