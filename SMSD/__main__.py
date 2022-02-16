from pathlib import Path

from plumbum import cli


class CLI(cli.Application):
	"""Tools to work with SMSD controllers."""


@CLI.subcommand("emulator")
class CLIEmulator(cli.Application):
	"""Starts an emulator."""


@CLIEmulator.subcommand("lan")
class CLIEmulatorLan(cli.Application):
	"""Starts an emulator for LAN models"""


@CLIEmulatorLan.subcommand("net")
class CLIEmulatorLanNet(cli.Application):
	def main(self):
		import asyncio

		from SMSD.lan.protocol import Server

		s = Server()
		l = asyncio.get_event_loop()
		l.run_until_complete(s.startTCPServer())
		l.run_until_complete(s.tcpServer.server.serve_forever())


CLIEmulatorLanNet.__doc__ = CLIEmulatorLan.__doc__ + " as a TCP server, to which you can connect using SMC-PROGRAM-LAN running on host."


@CLIEmulatorLan.subcommand("net-uart")
class CLIEmulatorLanNetUart(cli.Application):
	def main(self):
		import asyncio

		from SMSD.lan.protocol import Server

		s = Server()
		l = asyncio.get_event_loop()
		l.run_until_complete(s.startUARTTCPServer())
		l.run_until_complete(s.uartTCPServer.server.serve_forever())


CLIEmulatorLanNetUart.__doc__ = CLIEmulatorLan.__doc__ + " as a TCP server, to which you can connect VirtualBox by setting up providing a virtual COM port in TCP mode and using using SMC-PROGRAM-LAN in the guest to connect that virtual COM port."


@CLIEmulatorLan.subcommand("uart")
class CLIEmulatorLanUart(cli.Application):
	def main(self, port: Path):
		import asyncio

		from SMSD.lan.protocol import Server

		s = Server()
		l = asyncio.get_event_loop()
		l.run_until_complete(s.uartServer(port))
		l.run_until_complete(s.uartServer.server.serve_forever())


CLIEmulatorLanUart.__doc__ = CLIEmulatorLan.__doc__ + " as a PTY device. Disclaimer: won't work with VirtualBox and Wine as it is."

if __name__ == "__main__":
	CLI.run()
