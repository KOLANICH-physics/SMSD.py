import typing
from hashlib import blake2s
from struct import Struct
from .commands import (Command, ControlFlow, DirectCommand, Direction, ExecutionCommands, MicrosteppingCommand, MotorPower, Movement, Parameters, RelayCommand, StandaloneCommand, WaitForInterruptCommand)
from enum import Enum


class uint8_t(int):
	__slots__ = ()


class uint16_t(int):
	__slots__ = ()


twoShorts = Struct("<HH")


def halfIntHash(full: bytes) -> uint16_t:
	(a, b) = twoShorts.unpack(full)
	return a ^ b


def hashtableLookup(s: typing.Any) -> typing.Optional[typing.Any]:
	hC = gHT.c.h
	t = gHT.t
	(reduced, half, full) = singleByteHashStrings(gHT.c.p, hC.o2b(s))
	idx = perfectHashRemap(hC, reduced)
	(control, res) = t[idx]
	if control != half:
		raise KeyError(s)
	return res


def singleByteHashStrings(powCfg: "POWConfig", d: bytes):
	h = blake2s(key=powCfg.nonce, digest_size=4)
	h.update(d)
	full = h.digest()
	half = halfIntHash(full)
	reduced = powCfg.reducer(*full)
	return (reduced, half, full)


def perfectHashRemap(hashConfig: "HashConfig", i: int) -> int:
	i -= hashConfig.offset
	return i % hashConfig.t + hashConfig.r[i // hashConfig.t]


nN = (None, None)
hashedHashTable = (
	(57952, WaitForInterruptCommand.wait_lowest),
	(54793, RelayCommand.off),
	(35936, Direction.backward),
	(10882, Parameters.startSpeed),
	(53071, MotorPower.motorPowerOFF),
	(18448, Parameters.speed),
	(64860, ControlFlow.label_loop),
	(56943, Direction.forward),
	(44099, Direction.forward),
	(44460, ExecutionCommands.pause),
	(48393, Direction.change),
	(42157, ControlFlow.label_loop),
	(13627, ControlFlow.setLabel),
	(17603, Movement.move_til_lowest),
	(37643, ControlFlow.loop),
	(20960, ExecutionCommands.startOrStop),
	(19349, Parameters.acceleration),
	(48516, Direction.change),
	(24401, ExecutionCommands.pause),
	(43127, WaitForInterruptCommand.wait_lowest),
	(52627, MotorPower.motorPowerON),
	(43607, Movement.move),
	(18733, RelayCommand.on),
	(39443, Movement.continuous_til_input0),
	(63409, Movement.move),
	(8821, MicrosteppingCommand.on),
	nN,
	(4315, MotorPower.motorPowerON),
	(55745, Command.begin),
	(20850, Direction.backward),
	(34089, Command.sleep),
	nN,
	(57617, Parameters.speed),
	(35824, StandaloneCommand.loadToEEPROM),
	(30825, Parameters.startSpeed),
	nN,
	(51076, StandaloneCommand.loadToEEPROM),
	(58900, DirectCommand.loadToRAM),
	(48899, Command.begin),
	(52044, ControlFlow.setLabel),
	(49985, RelayCommand.off),
	(29915, Movement.move_til_highest),
	(9818, WaitForInterruptCommand.wait_highest),
	(14636, ExecutionCommands.startOrStop),
	(36013, Command.finishLoading),
	(44971, WaitForInterruptCommand.wait_highest),
	(62243, MicrosteppingCommand.off),
	(50960, Parameters.acceleration),
	(23084, MotorPower.motorPowerOFF),
	(17252, Command.sleep),
	(63829, RelayCommand.on),
	(47972, Command.finishLoading),
)


class gHT:
	class c:
		class p:
			nonce = b"\xb8`Mu"

			def reducer(d: int, c: int, b: int, a: int) -> uint8_t:
				return a - b + c - d & 255

		class h:
			t = 13
			r = (30, 39, 4, -1, 10, 0, 40, 13, 16, 25, -1, 37, 33)
			offset = 84

			def o2b(s: str) -> bytes:
				if not isinstance(s, bytes):
					s = s.encode("cp1251")
				return s

	t = hashedHashTable
