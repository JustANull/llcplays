import control
import sys

class ControlStdout(control.Control):
	def __init__(self, users, commands, fp = sys.stdout):
		control.Control.__init__(self, users, commands)
		self.fp = fp

	def raw_command(self, cmd):
		self.fp.write(cmd)
		self.fp.flush()

	def do_command(self, cmd):
		self.fp.write(self.commands[cmd])
		self.fp.flush()
