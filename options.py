class IRC():
	def __init__(self, server, port, channel, nickname, secret):
		self.server = server
		self.port = port
		self.channel = channel
		self.nickname = nickname
		self.secret = secret

class Window():
	def __init__(self, title, width, height, fontsize, fontname):
		self.title = title
		self.width = width
		self.height = height
		self.fontsize = fontsize
		self.fontname = fontname
