from enum import Enum


class CommandWithArgs:
	__slots__ = ("cmd", "arg")

	def __init__(self, cmd, arg):
		self.cmd = cmd
		self.arg = arg

	def __str__(self):
		return self.cmd.value + str(self.arg)

	def __repr__(self):
		return self.__class__.__name__ + "(" + repr(self.cmd) + ", " + repr(self.arg) + ")"


class MotorPower(Enum):
	motorPowerON = enable = EN = "EN"
	motorPowerOFF = disable = DS = "DS"


MotorPower.motorPowerOFF.__doc__ = "Remove power off the motor."
MotorPower.motorPowerON.__doc__ = "Put power on the motor."


class Direction(Enum):
	left = forward = DL = "DL"
	right = backward = DR = "DR"
	reverse = change = RS = "RS"


Direction.left.__doc__ = "Set direction to left/forward"
Direction.right.__doc__ = "Set direction to right/backward"
Direction.change.__doc__ = "Change direction"


class Movement(Enum):
	move = MV = "MV"
	move_til_highest = continuous_til_input2 = MH = "MH"
	move_til_lowest = continuous_til_input1 = ML = "ML"
	continuous_til_input0 = HM = "HM"


Movement.continuous_til_input0.__doc__ = "Move till input signal on the input dedicated for zero limit switch"
Movement.continuous_til_input1.__doc__ = 'Move till input signal on the "lowest" input'
Movement.continuous_til_input2.__doc__ = 'Move till input signal on the "highest" input'
Movement.move.__doc__ = "Move the motor, either endlessly, or for n steps"


class ControlFlow(Enum):
	loop = "SB"
	setLabel = LL = "LL"
	label_loop = jump_loop = JP = "JP"


ControlFlow.setLabel.__doc__ = "Set jump label"
ControlFlow.label_loop.__doc__ = "Repeat the program starting from the label"
ControlFlow.loop.__doc__ = "Repeat the whole program."


class Parameters(Enum):
	acceleration = accel = "AL"
	speed = SD = "SD"
	startSpeed = SS = "SS"


Parameters.acceleration.__doc__ = "Acceleration"
Parameters.speed.__doc__ = "Speed to rotate the motor"
Parameters.startSpeed.__doc__ = "Initial speed, is subject to the acceleration"


class Command(Enum):
	finishLoading = ED = "ED"
	begin = BG = "BG"
	sleep = SP = "SP"


Command.begin.__doc__ = "Marks the start of the program. Begins transaction?"
Command.sleep.__doc__ = "Pause/sllep program for n seconds"
Command.finishLoading.__doc__ = "Marks the end of the program. Ends transaction?"


class StandaloneCommand(Enum):
	"""Commands that can be executed in standalone mode only"""

	loadToEEPROM = LD = "LD"
	readFromEEPROM = RD = "RD"


StandaloneCommand.loadToEEPROM.__doc__ = "Upload commands from PC to EEPROM buffer, moves controller into loading mode. Burns EEPROM, don't use."
StandaloneCommand.readFromEEPROM.__doc__ = "Output contents of the EEPROM buffer for programs."


class DirectCommand(Enum):
	"""Commands that can be executed in Direct Control mode only"""

	loadToRAM = LB = "LB"
	readFromRAM = RB = "RB"


DirectCommand.loadToRAM.__doc__ = "Upload commands from PC to in-memory buffer. When this command is received while driving, the motor is stopped and turned off."
DirectCommand.readFromRAM.__doc__ = "Output contents of the in-memory buffer. When this command is received while driving, the motor is stopped and turned off."


class ExecutionCommands(Enum):
	pause = PS = "PS"  # takes channel name
	startOrStop = ST = "ST"  # takes channel name


ExecutionCommands.startOrStop.__doc__ = "Start or stop program execution of a program"
ExecutionCommands.pause.__doc__ = "Pause program execution"


class RelayCommand(Enum):
	on = set_flag = SF = "SF"
	off = clear_flag = CF = "CF"


RelayCommand.on.__doc__ = "Output high"
RelayCommand.off.__doc__ = "Output low"


class WaitForInterruptCommand(Enum):
	wait_lowest = BX1 = IN1 = WL = "WL"
	wait_highest = BX2 = IN2 = WH = "WH"


WaitForInterruptCommand.WL.__doc__ = 'Wait for signal on input considered "lowest" (#1)'
WaitForInterruptCommand.WH.__doc__ = 'Wait for signal on input considered "highest" (#2)'


class MicrosteppingCommand(Enum):
	on = micro = "ON"
	off = whole = "OF"


MicrosteppingCommand.micro.__doc__ = "Enable microstepping"
MicrosteppingCommand.whole.__doc__ = "Disable microstepping"


class CommandEncoder:
	__slots__ = ()

	def loadToEEPROM(self, channel=1):
		return CommandWithArgs(StandaloneCommand.loadToEEPROM, channel)

	def readFromEEPROM(self, channel=1):
		return CommandWithArgs(StandaloneCommand.readFromEEPROM, channel)

	def loadToRAM(self, channel=1):
		return CommandWithArgs(StandaloneCommand.loadToRAM, channel)

	def readFromRAM(self, channel=1):
		return CommandWithArgs(StandaloneCommand.readFromRAM, channel)

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
