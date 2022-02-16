import re
import typing
from enum import IntEnum
from io import BytesIO
from ipaddress import IPv4Address, IPv4Interface
from pathlib import Path

from kaitaistruct import KaitaiStream, ValidationFailedError, ValidationExprError

from ..kaitai.smsd_lan import SmsdLan
from ..kaitai.smsd_limits import SmsdLimits
from SaneIO.core import SIO1HiNLoMux, SIOTransport, UnsafelyMuxableSIO1HiNLoMux
from SaneIO.protocols.serial import AsyncSIO_UARTServer
from SaneIO.protocols.tcp import AsyncSIO_TCPServer
from .powerStepSim import PowerStepResponder
from .serializers import calcChecksum, netMaskIntoPrefixLengthFromBytes, serializeMessage, serializeNetworkConfig, serializeResponse, serializeVersionInfo
from .uart import SMSDLAN_SIOTransport_UART

_DEFAULT_NETMASK = 16


class NetworkConfig:
	__slots__ = ("mac", "ip", "gateway", "dns", "port", "dhcpMode")

	def __init__(self, mac=bytes((0x00, 0xF8, 0xDC, 0x3F, 0x00, 0x00)), ip: IPv4Interface = IPv4Interface((bytes((192, 168, 1, 2)), _DEFAULT_NETMASK)), gateway: IPv4Interface = IPv4Interface((bytes((192, 168, 1, 1)), _DEFAULT_NETMASK)), dns: IPv4Address = IPv4Address(bytes((0, 0, 0, 0))), port: int = 5000, dhcpMode: int = 1):
		self.mac = mac
		self.ip = ip
		self.gateway = gateway
		self.dns = dns
		self.port = port
		self.dhcpMode = dhcpMode


smsdLimits = SmsdLimits(None)


class CommandParseException(Exception):
	__slots__ = ()

	@property
	def cmd(self) -> SmsdLan:
		return self.args[0]

	@property
	def code(self) -> SmsdLan.Response.Code:
		return self.args[1]

	@property
	def src_path(self) -> str:
		return self.args[2]


def parseCommand(commandRaw: bytes) -> SmsdLan:
	with BytesIO(commandRaw) as f:
		s = KaitaiStream(f)
		cmd = SmsdLan(smsdLimits, s)
		try:
			cmd._read()
		except ValidationExprError as ex:
			if ex.src_path == "/seq/1":
				raise CommandParseException(cmd, SmsdLan.Response.Code.wrong_checksum, ex.src_path) from ex
		except ValidationFailedError as ex:
			if ex.src_path == "/types/header/seq/4":
				raise CommandParseException(cmd, SmsdLan.Response.Code.wrong_length, ex.src_path) from ex
			else:
				raise CommandParseException(cmd, SmsdLan.Response.Code.out_of_range, ex.src_path) from ex
	return cmd


class Responder(SIOTransport):
	__slots__ = ("server", "powerStepResponder", "commands")

	VERSION_INFO = ((0x0, 0x0), (0x0, 0x0), 2)

	DEBUG = False

	def __init__(self, server, powerStepResponder: PowerStepResponder = None):
		super().__init__()
		self.server = server

		if powerStepResponder is None:
			powerStepResponder = PowerStepResponder()

		self.powerStepResponder = powerStepResponder
		self.commands = []

	def __call__(self, proto, cmd):
		processor = getattr(self, cmd.header.type.name, None)
		if processor:
			whatToRespond = processor(proto, cmd)
			if whatToRespond is None:
				pass
			elif isinstance(whatToRespond, tuple) and len(whatToRespond) == 2:
				resType, resPayload = whatToRespond
				if resType is None:
					resType = cmd.header.type
				resp = serializeMessage(typ=resType, iD=cmd.header.id, payload=resPayload)
				self.sendCommand(proto, resp)
			else:
				raise ValueError(self.__class__.__name__ + ": Responder method has returned invalid stuff. It must either be None or (type, payload) tuple", whatToRespond)

		else:
			print(self.__class__.__name__ + ": No processor for ", cmd.header.type)
			self.sendCommand(proto, serializeMessage(typ=SmsdLan.Type.response, iD=cmd.header.id, payload=self.powerStepResponder.serializeResponse(SmsdLan.Response.Code.wrong_command, 0)))

	def password(self, proto, cmd):
		print("Password", cmd.data)
		return SmsdLan.Type.response, self.powerStepResponder.serializeResponse(SmsdLan.Response.Code.auth_success, 0)

	def version_data(self, proto, cmd):
		VERSION_INFO = self.__class__.VERSION_INFO
		return None, serializeVersionInfo(VERSION_INFO[0][0], VERSION_INFO[0][1], VERSION_INFO[1][0], VERSION_INFO[1][1], VERSION_INFO[2])

	def power_step(self, proto, cmd):
		return self.powerStepResponder(cmd.data)

	def network_config_set(self, proto, cmd):
		cfg = cmd.data
		maskPrefixLength = netMaskIntoPrefixLengthFromBytes(cfg.subnet_mask.ipv4)
		self.server.networkConfig = NetworkConfig(mac=cfg.mac.mac, ip=IPv4Interface((cfg.my_ip.ipv4, maskPrefixLength)), gateway=IPv4Interface((cfg.gateway.ipv4, maskPrefixLength)), dns=IPv4Address(cfg.dns.ipv4), port=cfg.port, dhcpMode=cfg.dhcp_mode)

	def network_config_get(self, proto, cmd):
		cfg = self.server.networkConfig
		return None, serializeNetworkConfig(cfg.mac, cfg.ip.packed, cfg.ip.netmask.packed, cfg.gateway.packed, cfg.dns.packed, cfg.port, cfg.dhcpMode)

	def sendCommand(self, proto, cmd: bytes):
		return proto.sendBytes(cmd)

	# SIOTransport interface

	def onReceive(self, proto, commandRaw: bytes):
		if self.__class__.DEBUG:
			print("Received", commandRaw)

		try:
			cmd = parseCommand(commandRaw)
			ok = True
		except CommandParseException as ex:
			cmd = ex.cmd
			if ex.code == SmsdLan.Response.Code.wrong_length:
				print("Length specified in the header has exceeded the specified upper limit:", commandRaw)
			elif ex.code == SmsdLan.Response.Code.wrong_checksum:
				print("Wrong checksum for the command:", commandRaw)
			else:
				print("A value has failed validation: ", ex)
			self.sendCommand(proto, self.powerStepResponder.serializeResponse(ex.code, 0))
			ok = False

		# print("cmd", cmd, cmd.header.type)
		self.commands.append(cmd)
		if ok:
			self(proto, cmd)

	def checkChecksum(self, commandRaw: bytes):
		ourChecksum = calcChecksum(commandRaw[1:])
		return commandRaw[0] == ourChecksum

	def ifThisResponder(self, data: bytes):
		return self.checkChecksum(data)


class Server(SIOTransport):
	__slots__ = (
		"upper",
		"networkConfig",
		"rawMux",
		"uartFramerAndEscaper",
		"tcpServer",
		"uartTCPServer",
		"uartEscapedMux",
		"uartServer"
	)

	def __init__(self):
		super().__init__()

		resp = Responder(self)
		self.bindHigher(resp)

		self.networkConfig = NetworkConfig(ip=IPv4Interface(("127.0.0.1", 32)))

		self.rawMux = SIO1HiNLoMux()
		self.rawMux.bindHigher(self)

		self.uartFramerAndEscaper = SMSDLAN_SIOTransport_UART()
		self.uartEscapedMux = UnsafelyMuxableSIO1HiNLoMux()
		self.uartEscapedMux.bindHigher(self.uartFramerAndEscaper)

		self.uartFramerAndEscaper.bindHigher(self.rawMux)

		self.tcpServer = None
		self.uartTCPServer = None
		self.uartServer = None

	async def _startUARTServer(self, port: typing.Union[Path, str]):
		self.uartServer = await AsyncSIO_UARTServer.create(port)
		self.uartServer.bindHigher(self.uartEscapedMux)
		return self.uartServer

	def startUARTServer(self, port: typing.Union[Path, str]):
		if port not in self.uartEscapedMux:
			return self._startUARTServer(port)
		else:
			raise RuntimeError("Server already running on this port!", port)

	async def startTCPServer(self):
		self.tcpServer = await AsyncSIO_TCPServer.create(self.rawMux, host=str(self.networkConfig.ip.ip), port=self.networkConfig.port)
		return self.tcpServer

	async def startUARTTCPServer(self, port: int = 14379):
		"""The same as TCP, but the data is segmented and escaped like in UART protocol.
		Intended to be used to be connected by VirtualBox virtual COM port in TCP mode"""
		self.uartTCPServer = await AsyncSIO_TCPServer.create(self.uartEscapedMux, host=str(self.networkConfig.ip.ip), port=port)
		return self.uartTCPServer


# SMC-Program-LAN-v.7.0.6 requires the response to be sent within a strict time window (50 ms by default). It can be extended by editing the config files manually.
