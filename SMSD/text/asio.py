import asyncio
from queue import Queue

import serial_asyncio

from enum import Enum


class SMSDProtocol(asyncio.Protocol):
	__slots__ = ("commands", "buffer", "transport", "currentBatch", "tx", "isEndOfBatch", "expectedEcho")

	def __init__(self):
		self.buffer = bytearray()
		self.commands = []
		self.tx = Queue()
		self.currentBatch = []
		self.transport = None
		self.isEndOfBatch = True
		self.expectedEcho = None

	def connection_made(self, transport):
		self.transport = transport
		transport.serial.rts = False  # You can manipulate Serial object via transport
		transport.serial.read()

	def sendCommand(self, cmd):
		if isinstance(cmd, Enum):
			cmdStr = cmd.value
		else:
			cmdStr = cmd

		self.tx.put(cmdStr)
		self.sendCommandInCertainStates()

	def sendCommandInCertainStates(self):
		if self.isEndOfBatch:
			if not self.tx.empty():
				commandB = self.tx.get()
				self.expectedEcho = commandB
				self.transport.write(commandB.encode("ascii") + b"*")  # Write serial data via transport
				self.tx.task_done()
				self.isEndOfBatch = False

	def data_received(self, data):
		for c in data:
			self.isEndOfBatch = c == 0x07
			if c == ord("*"):
				cmd = self.buffer.decode("ascii")
				if self.expectedEcho is None:
					self.currentBatch.append(cmd)
					self.buffer = type(self.buffer)()
					print("Command received", repr(self.currentBatch[-1]))
				else:
					assert self.expectedEcho == cmd
					self.expectedEcho = None
			elif self.isEndOfBatch:
				self.commands.append(self.currentBatch)
				self.currentBatch = type(self.currentBatch)()
				print("Batch received", repr(self.commands[-1]))
			else:
				self.buffer.append(c)
		self.sendCommandInCertainStates()

	def connection_lost(self, exc):
		self.transport.loop.stop()

	def pause_writing(self):
		pass

	def resume_writing(self):
		pass
