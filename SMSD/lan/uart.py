import re
from queue import Queue

from SaneIO.core import SIOTransport, StreamingHalfDuplexInBandSignalling_SIOTransport

__all__ = ("SMSDLANUART_SIOTransport",)

START_MARKER = 0xFA
END_MARKER = 0xFB
ESCAPE_MARKER = 0xFE

START_MARKER_BYTES = bytes((START_MARKER,))
END_MARKER_BYTES = bytes((END_MARKER,))
ESCAPE_MARKER_BYTES = bytes((ESCAPE_MARKER,))

escapedBytes = bytes((START_MARKER, END_MARKER, ESCAPE_MARKER))


def _perm(b: int) -> int:
	return b ^ 0x80


deUartRx = re.compile(ESCAPE_MARKER_BYTES + b"([" + bytes(_perm(el) for el in escapedBytes) + b"])")


def deUARTReplacer(m: re.Match):
	return bytes((_perm(m.group(1)[0]),))


uartRx = re.compile(b"[" + escapedBytes + b"]")


def UARTReplacer(m: re.Match):
	return bytes(
		(
			ESCAPE_MARKER,
			_perm(m.group(0)[0]),
		)
	)


def escapeForUART(data: bytes) -> bytes:
	return START_MARKER_BYTES + uartRx.subn(UARTReplacer, data)[0] + END_MARKER_BYTES


def unescapeForUART(data: bytes) -> bytes:
	if data[0] == START_MARKER and data[-1] == END_MARKER:
		data = data[1:-1]

		return deUartRx.subn(deUARTReplacer, data)[0]

	raise ValueError("Invalid SMSD LAN UART packet")


class SMSDLAN_SIOTransport_UART(StreamingHalfDuplexInBandSignalling_SIOTransport):
	"""Sans-IO-style protocol for decoding UART SMSD LAN protocol into raw LAN protocol"""

	__slots__ = (
		"buffer",
		"inCommand",
	)

	def __init__(self):
		super().__init__()
		self.buffer = bytearray()
		self.inCommand = False

	def canSend(self) -> bool:
		return not self.inCommand

	def receiveByte(self, b: int):
		if not self.inCommand:
			if b == START_MARKER:
				self.inCommand = True
				self.buffer.append(b)
		else:
			self.buffer.append(b)
			if b == END_MARKER:
				self.inCommand = False
				deuarted = unescapeForUART(self.buffer)
				self.buffer = type(self.buffer)()
				self.higher.onReceive(self, deuarted)
				self.sendCommandsInCertainStates()

	def filterSentBytes(self, b: bytes) -> bytes:
		return escapeForUART(b)

	def ifThisResponder(self, data: bytes):
		return self.inCommand or data[0] == START_MARKER
