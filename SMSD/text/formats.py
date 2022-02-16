from dataclasses import dataclass
import re
import typing
from struct import pack, unpack
from enum import Enum

from .commands import Command, CommandWithArgs, ControlFlow, DirectCommand, Direction, ExecutionCommands, MicrosteppingCommand, MotorPower, Movement, Parameters, RelayCommand, StandaloneCommand, WaitForInterruptCommand
from .hash import hashtableLookup


def derot(el, key=0x7E):
	return bytes(((c - key) & 0xFF) for c in el)


def rot(el, key=0x7E):
	return derot(el, -key)


ENCODING = "cp1251"


def decodeSmcStream(d: bytes) -> typing.Iterable[str]:
	res = derot(d).decode(ENCODING).split("\r\n")
	if not res[-1]:
		res = res[:-1]
	return res


rawHashTable = {
	'начало программы': Command.begin,
	'движение влево': Direction.forward,
	'движение вправо': Direction.backward,
	'реверс': Direction.change,
	'установить сигнал "разрешение"': MotorPower.motorPowerON,
	'снять сигнал "разрешение"': MotorPower.motorPowerOFF,
	'режим дробления шага': MicrosteppingCommand.on,
	'режим целого шага': MicrosteppingCommand.off,
	'скорость': Parameters.speed,
	'начальная скорость': Parameters.startSpeed,
	'остановка на': Command.sleep,
	'ускорение': Parameters.acceleration,
	'выполнить': Movement.move,
	'установить флаг': RelayCommand.on,
	'ждать младший флаг': WaitForInterruptCommand.wait_lowest,
	'ждать старший флаг': WaitForInterruptCommand.wait_highest,
	'снять флаг': RelayCommand.off,
	'установить метку': ControlFlow.setLabel,
	'выполнить от метки': ControlFlow.label_loop,
	'начать загрузку:': StandaloneCommand.loadToEEPROM,
	'завершить загрузку': Command.finishLoading,
	'начать/закончить работу:': ExecutionCommands.startOrStop,
	'поставить/снять паузу:': ExecutionCommands.pause,

	'program begin': Command.begin,
	'forward motion': Direction.forward,
	'backward motion': Direction.backward,
	'reverse': Direction.change,
	'set "disable"': MotorPower.motorPowerOFF,
	'set "enable"': MotorPower.motorPowerON,
	'acceleration': Parameters.acceleration,
	'speed': Parameters.speed,
	'start speed': Parameters.startSpeed,
	'move till zero limit switch': Movement.continuous_til_input0,
	'move till input signal ml': Movement.move_til_lowest,
	'move till input signal mh': Movement.move_til_highest,
	'move': Movement.move,
	'pause for': Command.sleep,
	'set signal to output': RelayCommand.on,
	'clear signal from output': RelayCommand.off,
	'wait signal wl to input': WaitForInterruptCommand.wait_lowest,
	'wait signal wh to input': WaitForInterruptCommand.wait_highest,
	'set label': ControlFlow.setLabel,
	'repeat from label': ControlFlow.label_loop,
	'record commands to buffer': DirectCommand.loadToRAM,
	'repeat buffer': ControlFlow.loop,
	'start commands recording:': StandaloneCommand.loadToEEPROM,
	'end commands recording': Command.finishLoading,
	'start/stop program executing:': ExecutionCommands.startOrStop,
	'set/take off pause:': ExecutionCommands.pause,
}


argRe = re.compile("(-?\d+)")

#def hashtableLookup(s: str) -> typing.Optional[Enum]:
#	return rawHashTable.get(s, None)


def decodeKnownCommandFromHumanText(rawString: str):
	rawString = rawString.lower().strip()
	
	splitted = argRe.split(rawString, 1)
	
	if len(splitted) == 3:
		cmd, arg, rest = splitted
		cmd = cmd.strip()
		arg = int(arg)
		rest = rest.strip()
	else:
		cmd = rawString
		arg = None
		rest = None

	cmd = hashtableLookup(cmd)
	if cmd:
		return CommandWithArgs(cmd, arg)


def _decode_smcStream(d: bytes):
	for el in decodeSmcStream(d):
		res = decodeKnownCommandFromHumanText(el)
		yield res


def decode_smcStream(d: bytes):
	return list(_decode_smcStream(d))
