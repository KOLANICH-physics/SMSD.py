from .Clock import Clock, Clockable
from .gpio import GPIO
from .instructionProcessors import ProgramExecutor
from .motor import MotorController


class PowerStepSimulator(Clockable):
	__slots__ = ("mode", "zeroPosition", "motorController", "gpio", "executor", "instructionProcessor", "clock")

	def __init__(self):
		self.mode = None
		self.zeroPosition = 0  # type: int
		self.motorController = MotorController()  # type: MotorController
		self.gpio = GPIO()  # type: GPIO
		self.executor = ProgramExecutor()  # type: InstructionProcessor
		self.instructionProcessor = self.executor
		self.clock = Clock((self.gpio, self.instructionProcessor, self.motorController))  # type: Clock

	def startTicking(self):
		self.clock.startTicking()

	def startLoading(self):
		self.instructionProcessor = self.executor.curProgram.startLoading()

	def commitLoading(self):
		if isinstance(self.instructionProcessor, ProgramLoader):
			self.instructionProcessor.commit()

		self.instructionProcessor = self.executor

	def emitMessage(self, typ, payload):
		pass

	def tick(self):
		self.clock.tick()
