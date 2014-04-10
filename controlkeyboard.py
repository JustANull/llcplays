import control
import pykeyboard
import time

class ControlKeyboard(control.Control):
	def __init__(self, users, commands):
		control.Control.__init__(self, users, commands)
		self.k = pykeyboard.PyKeyboard()
		self.keysDown = []
		self.doLoad = False
		self.doSave = False

	def raw_command(self, cmd):
		self.press_key(cmd)

	def do_command(self, cmd):
		self.press_key(self.commands[cmd])

	def save(self):
		self.doSave = True

	def load(self):
		self.doLoad = True

	def press_key(self, cmd):
		self.keysDown.append(cmd)

	def update(self):
		if self.doLoad:
			self.doLoad = False
			self.k.press_key(self.k.function_keys[1])
			time.sleep(0.05)
			self.k.release_key(self.k.function_keys[1])

		if self.doSave:
			self.doSave = False
			self.k.press_key(self.k.shift_key)
			time.sleep(0.05)
			self.k.press_key(self.k.function_keys[1])
			time.sleep(0.05)
			self.k.release_key(self.k.function_keys[1])
			self.k.release_key(self.k.shift_key)

		for key in self.keysDown:
			self.k.press_key(key)

		time.sleep(0.05)

		for key in self.keysDown:
			self.k.release_key(key)

		self.keysDown = []
