import control
import pykeyboard
import time

class ControlKeyboard(control.Control):
	def __init__(self, users, commands):
		control.Control.__init__(self, users, commands)
		self.k = pykeyboard.PyKeyboard()
		self.keysDown = {}
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
		if not cmd in self.keysDown[cmd]:
			self.keysDown[cmd] = deque()

		self.keysDown[cmd].append('press')
		self.keysDown[cmd].append('release')

	def update(self):
		if self.doLoad:
			self.k.press_key(self.k.function_keys[1])
			time.sleep(50)
			self.k.release_key(self.k.function_keys[1])

		if self.doSave:
			self.k.press_key(self.k.shift_key)
			time.sleep(50)
			self.k.press_key(self.k.function_keys[1])
			time.sleep(50)
			self.k.release_key(self.k.function_keys[1])
			self.k.release_key(self.k.release_key)

		for key in self.keysDown:
			if len(self.keysDown[key]) > 0:
				cmd = self.keysDown[key].popleft()

				if cmd == 'press':
					self.k.press_key(key)
				elif cmd == 'release':
					self.k.release_key(key)
