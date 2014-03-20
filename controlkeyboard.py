import control
import pykeyboard

class ControlKeyboard(control.Control):
	def __init__(self, users, commands):
		control.Control.__init__(self, users, commands)
		self.k = pykeyboard.PyKeyboard()

	def raw_command(self, cmd):
		self.k.tap_key(cmd)

	def do_command(self, cmd):
		self.k.tap_key(self.commands[cmd])
