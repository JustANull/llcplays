import control
import math
import pygame
import subscriber

class Display(subscriber.Subscriber):
	def __init__(self, winopt, users, commands):
		self.messages = []

		self.title = winopt.title
		self.width = winopt.width
		self.height = winopt.height
		self.fontsize = winopt.fontsize
		self.fontname = winopt.fontname
		self.users = users
		self.commands = commands

	def on_add(self, publisher):
		self.publisher = publisher
		pygame.init()
		pygame.time.set_timer(pygame.USEREVENT + 0, 10000)	#in 10 seconds, load the saved game; assume that emulator is started
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('')
		self.font = pygame.font.SysFont(self.fontname, self.fontsize)
		self.maxMessages = int(math.ceil(self.height / self.font.get_height())) - 1
		self.add_message('Bot initialized!', '')

	def on_remove(self):
		pygame.quit()

	def render(self):
		self.screen.fill((0, 0, 0))

		xpos = (self.width - self.font.size(self.title)[0]) / 2
		self.screen.blit(self.font.render(self.title, 1, (255, 255, 255)), (xpos, 0))

		for i in range(len(self.messages)):
			leftText = self.font.render(self.messages[i][0], 1, (255, 255, 255))
			rightText = self.font.render(self.messages[i][1], 1, (255, 255, 255))
			ypos = self.height - (i + 1) * self.font.get_height()
			self.screen.blit(leftText, (8, ypos))
			self.screen.blit(rightText, (self.width - (8 + self.font.size(self.messages[i][1])[0]), ypos))

		pygame.display.flip()

	def add_message(self, left, right):
		self.messages.insert(0, (left, right))

		if len(self.messages) > self.maxMessages:
			self.messages = self.messages[:self.maxMessages]

		self.render()

	def set_title(self, title):
		self.title = title
		self.render()

	def message(self, kind, *args):
		if kind == 'pubmsg':
			allowedUser = True

			if self.users:
				allowedUser = args[1].source.nick in self.users

			if allowedUser and args[1].arguments[0] in self.commands:
				self.add_message(args[1].source.nick, args[1].arguments[0])
		elif kind == 'update':
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.publisher.parent.say('The bot is going down!')
					self.publisher.parent.live = False
				elif event.type == pygame.USEREVENT + 0:
					pygame.time.set_timer(pygame.USEREVENT + 0, 0)            	#stop loading the game every 10 seconds
					pygame.time.set_timer(pygame.USEREVENT + 1, 1000 * 60 * 5)	#start saving it every 5 minutes
					self.publisher.get_subscriber('control').raw_command(control.LOAD_BUTTON)
				elif event.type == pygame.USEREVENT + 1:
					self.publisher.get_subscriber('control').raw_command(control.SAVE_BUTTON)
