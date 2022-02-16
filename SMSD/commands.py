from enum import Enum


class CommandWithArg:
	__slots__ = ("cmd", "arg")

	def __init__(self, cmd, args):
		self.cmd = cmd
		self.arg = arg

	def __str__(self):
		return self.cmd.value + str(self.arg)

	def __repr__(self):
		return self.__class__.__name__ + "(" + repr(self.cmd) + ", " + repr(self.arg) + ")"


class MotorPower(Enum):
	motorPowerON = enable = EN = "EN"
	motorPowerOFF = disable = DS = "DS"


class Direction(Enum):
	forward = DL = "DL"
	backward = DR = "DR"
	change = reverse = RS = "RS"


class Movement(Enum):
	continuous = perpertual = MV = "MV"
	continuous_til_input2 = MH = "MH"
	continuous_til_input1 = ML = "ML"
	continuous_til_input0 = HM = "HM"
	steps = move = MV = "MV"


class ControlFlow(Enum):
	loop = "SB"
	setLabel = LL = "LL"
	label_loop = jump_loop = JP = "JP"


class Parameters(Enum):
	acceleration = accel = "AL"
	speed = SD = "SD"
	startSpeed = SS = "SS"


class Command(Enum):
	finishLoading = ED = "ED"
	begin = BG = "BG"
	sleep = SP = "SP"


class StandaloneCommand(Enum):
	"""Commands that can be executed in standalone mode only"""

	loadToEEPROM = LD = "LD"  # Start loading to the controller – after the command controller is in the loading mode.
	readFromEEPROM = RD = "RD"  # Read the command sequence from the controller memory


class DirectCommand(Enum):
	"""Commands that can be executed in Direct Control mode only"""

	loadToBuffer = LB = "LB"  # Start loading to the operational buffer. If this command is received while driving, the motor is stopped and turned off.
	readFromBuffer = RB = "RB"  # Read the command sequence from the operational buffer. If this command is received while driving, the motor is stopped and turned off.


class ExecutionCommands(Enum):
	pause = PS = "PS"  # takes channel name
	startOrStop = ST = "ST"  # takes channel name


class RelayCommand(Enum):
	on = set_flag = SF = "SF"
	off = clear_flag = CF = "CF"


class WaitForInterruptCommand(Enum):
	BX1 = IN1 = WL = "WL"
	BX2 = IN2 = WH = "WH"


class FractionCommand(Enum):
	fraction = "ON"
	whole = "OF"


class CommandEncoder:
	__slots__ = ()

	def loadToEEPROM(self, channel=1):
		return CommandWithArgs(StandaloneCommand.loadToEEPROM, channel)

	def readFromEEPROM(self, channel=1):
		return CommandWithArgs(StandaloneCommand.readFromEEPROM, channel)

	def loadToBuffer(self, channel=1):
		return CommandWithArgs(StandaloneCommand.loadToBuffer, channel)

	def readFromBuffer(self, channel=1):
		return CommandWithArgs(StandaloneCommand.readFromBuffer, channel)

	def pause(self, channel=1):
		return CommandWithArgs(StandaloneCommand.pause, channel)

	def startOrStop(self, channel=1):
		return CommandWithArgs(StandaloneCommand.startOrStop, channel)

	def loop(ddd: int):
		assert 1 <= ddd <= 255
		return CommandWithArgs(Command.loop, ddd)

	SB = loop

	def acceleration(ddd: int):
		assert -1000 <= ddd <= 1000
		"Acceleration"
		return CommandWithArgs(Parameters.acceleration, ddd)

	AL = accel = acceleration

	def speed(ddd: int):
		assert 1 <= ddd <= 10000
		return CommandWithArgs(Parameters.speed, ddd)

	SD = speed

	def startSpeed(ddd: int):
		assert 1 <= ddd <= 2000
		return CommandWithArgs(Parameters.startSpeed, ddd)

	SS = startSpeed

	def steps(ddd: int):
		assert 1 <= ddd <= 10000000
		return CommandWithArgs(Movement.steps, ddd)

	move = MV = steps

	def label_loop(ddd: int):
		assert 1 <= ddd <= 255
		return "JP" + str(ddd)
		return CommandWithArgs(ControlFlow.label_loop, ddd)

	jump_loop = JP = label_loop

	def sleep(ddd: int):
		assert 1 <= ddd <= 100000000
		return CommandWithArgs(Command.sleep, ddd)

	SP = sleep


class ErrorCode(Enum):
	ok = "E10"
	error = "E13"
	completed = "E14"
	communication_err = "E15"
	cmd_err = "E16"
	cmd_arg_err = "E19"
