import threading
import typing
from time import sleep


class Clockable:
	__slots__ = ()

	def tick(self) -> None:
		"""Called on every tick of the clock"""

		raise NotImplementedError


class Clock(Clockable):
	__slots__ = ("period", "time", "tickingThread", "clockables")

	def __init__(self, clockables: typing.Collection[Clockable]):
		self.clockables = clockables
		self.period = 1  # type: float
		self.time = 0  # type: int
		self.tickingThread = None  # type: threading.Thread

	def startTicking(self):
		if self.tickingThread is None:
			self.tickingThread = threading.Thread(target=self._tickingThreadFunc)
			self.tickingThread.start()
		else:
			raise RuntimeError("Ticking timer is already started", self.tickingThread)

	def tick(self) -> None:
		self.time += 1
		for clockable in self.clockables:
			clockable.tick()

	def _tickingThreadFunc(self):
		while True:
			self.tick()
			sleep(self.period)
