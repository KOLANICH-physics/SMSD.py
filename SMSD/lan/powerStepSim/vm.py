from enum import IntEnum


class CPU:
	def __init__(self):
		self.regs = [0] * len(RegisterID)
		self.cmpRes = False
		self.interruptLoop = False
		self.queue = []


class RegID(IntEnum):
	none = 0
	ip = 1
	program = 2
	uip = 3
	zero = 4
	label = 5
	mark = 6
	position = 7
	sleepCounter = 8
	currentSpeed = 9
	targetSpeed = 10
	currentAcceleration = 11
	targetAcceleration = 12
	countOfSpeedSteps = 13


class FlagID(IntEnum):
	none = 0
	SET_ZERO = 1
	IN0 = 2
	IN1 = 3
