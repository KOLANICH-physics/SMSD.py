import typing
from struct import Struct


def calcChecksum(data) -> int:
	v = 0xFF
	for el in data:
		v = (v + el) & 0xFF
	return v ^ 0xFF


singleU4LE = Struct("<I")
singleU2LE = Struct("<H")


errorCountersStruct = Struct("<17I")


def parseErrorCounters(d: bytes):
	(starts, xt, timeouts, chip_powerstep01_init, chip_w5500_init, fram_init, lan, fram_exchange, interrupts, overcurrents, overvoltages, overheatings_chip_powerstep01, overheatings_brake, chip_powerstep01_command_transfer, unkn_uvlo_powerstep, unkn_stall_powerstep, program_errors) = errorCountersStruct.unpack(d)


def serializeLoop(cycles, commands) -> int:
	return (cycles << 10) | commands


def serializeMicrosteps(microsteps: int) -> int:
	fullMask = (1 << 22) - 1
	return microsteps & fullMask


powerstepCommandStruct = Struct("<I")


def serializePowerStepCommand(argument_raw: int, command: int, action: int, reserved: int) -> bytes:
	return powerstepCommandStruct.pack((argument_raw << 10) | (command << 4) | (action << 3) | reserved)


def serializeMac(mac):
	return bytes(mac.mac)


def serializeIPv4(ipv4):
	return bytes(ipv4.ipv4)


def serializeLanConfig(cfg):
	return serializeMac(cfg.mac) + serializeIPv4(cfg.my_ip) + erializeIPv4(cfg.subnet_mask) + erializeIPv4(cfg.gateway) + erializeIPv4(cfg.dns) + struct.pack("<H", port) + bytes((dhcp_mode,))


powerStepStatusStruct = Struct("<BB")


def serializePowerStepStatusFirstByte(is_deenergized: bool, is_ready: bool, is_sw_on: bool, has_sw_event_happenned: bool, is_rotating_direction_forward: bool, accelerationStatus: "AccelerationStatus", is_command_error: bool) -> int:
	return (int(is_deenergized) << 0) | (int(is_ready) << 1) | (int(is_sw_on) << 2) | (int(has_sw_event_happenned) << 3) | (int(is_rotating_direction_forward) << 4) | (int(accelerationStatus) << 5) | (int(is_command_error) << 7)


def serializePowerStepStatus(is_deenergized: bool, is_ready: bool, is_sw_on: bool, has_sw_event_happenned: bool, is_rotating_direction_forward: bool, accelerationStatus: "AccelerationStatus", is_command_error: bool, reserved: int = 0) -> bytes:
	return powerStepStatusStruct.pack(serializePowerStepStatusFirstByte(is_deenergized, is_ready, is_sw_on, has_sw_event_happenned, is_rotating_direction_forward, accelerationStatus, is_command_error), reserved)


responseStruct = Struct("<BI")


def serializeResponse(is_deenergized: bool, is_ready: bool, is_sw_on: bool, has_sw_event_happenned: bool, is_rotating_direction_forward: bool, accelerationStatus: "AccelerationStatus", is_command_error: bool, code, return_data: int) -> bytes:
	return serializePowerStepStatus(is_deenergized, is_ready, is_sw_on, has_sw_event_happenned, is_rotating_direction_forward, accelerationStatus, is_command_error) + responseStruct.pack(code, return_data)


versionInfoStruct = Struct("<HHHHB")


def parseVersionInfo():
	unkn0, unkn1, unkn2, unkn3, unkn4 = versionInfoStruct.unpack(data)
	return unkn0, unkn1, unkn2, unkn3, unkn4


def serializeVersionInfo(unkn0=0, unkn1=0, unkn2=0, unkn3=0, unkn4=0):
	return versionInfoStruct.pack(unkn0, unkn1, unkn2, unkn3, unkn4)


headerStruct = Struct("<BBBBH")


def serializeHeader(xor_sum: int, version: int, typ, iD: int, length: int) -> bytes:
	return headerStruct.pack(xor_sum, version, typ, iD, length)


currentProtocolVersion = 2


def serializeMessage(typ, iD, payload):
	hdr = serializeHeader(xor_sum=0, version=currentProtocolVersion, typ=typ, iD=iD, length=len(payload))
	summed = (hdr + payload)[1:]
	return bytes((calcChecksum(summed),)) + summed


def packBits(bools: typing.Collection[bool]) -> int:
	res = 0
	for i, b in enumerate(bools):
		res |= int(b) << i
	return res


def serializeEventStatus(inputs, masks, events) -> int:
	assert len(inputs) == len(masks) == len(events) == 8
	return packBits(inputs + masks + events)


def serializeInstructionPointer(program, command) -> int:
	return (program << 8) | command


def serializeMotorMode(program_n: int, hold_current: float, work_current: float, microstepping_nlog: int, motor_model: "MotorModel", is_in_current_mode: bool):
	if hold_current > 1:
		raise ValueError("Hold current cannot be more than 1")
	hold_current -= 0.25
	if hold_current < 0:
		raise ValueError("Hold current cannot be less than 0.25")
	hold_current_raw = int(round(hold_current / 0.25))

	work_current_raw = int(round(work_current / 0.1))

	res = (program_n << 20) | (hold_current_raw << 17) | (work_current_raw << 10) | (microstepping_nlog << 7) | (motor_model << 1) | int(is_in_current_mode)
	return res


networkConfigTail = Struct("<HB")


def serializeNetworkConfig(mac: bytes, my_ip: bytes, subnet_mask: bytes, gatewayIP: bytes, dnsIP: bytes, port: int, dhcp_mode: int):
	return mac + my_ip + subnet_mask + gatewayIP + dnsIP + networkConfigTail.pack(port, dhcp_mode)


def netMaskIntoPrefixLengthFromBytes(d: bytes) -> int:
	return singleU4LE.unpack(b"\xff\xff\x00\x00")[0].bit_length()
