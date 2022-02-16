import serial
import serial_asyncio

from .asio import SMSDProtocol


async def SMSD(eventLoop, port: str):
	coro = serial_asyncio.create_serial_connection(
		eventLoop,
		SMSDProtocol,
		port,
		baudrate=9600,
		bytesize=8,  # CS8
		parity=serial.PARITY_EVEN,  # PARENB
		stopbits=1,
	)
	transport, protocol = await coro
	return protocol
 
