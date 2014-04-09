import control
import pykeyboard

class ControlKeyboard(control.Control):
	def __init__(self, users, commands):
		control.Control.__init__(self, users, commands)
		self.k = pykeyboard.PyKeyboard()
		self.keysDown = {}

	def raw_command(self, cmd):
		self.keysDown[cmd] = 1
		self.k.press_key(cmd)

	def do_command(self, cmd):
		self.keysDown[self.commands[cmd]] = 1
		self.k.release_key(self.commands[cmd])

	def update(self):
		for key in self.keysDown:
			if self.keysDown[key] == 0:
				self.k.release_key(key)
				self.keysDown[key] = -1
			else:
				self.keysDown[key] = 0
