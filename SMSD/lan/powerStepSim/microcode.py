import typing
from dataclasses import dataclass

from . import nanoops as nO
from .vm import *

from motorAccelerationPlanner import ArbitraryPositionChangePlan
from motorAccelerationPlanner import *



makeStepsSingleEpoch = nO.repeat(nO.makeStep(), RegID.currentSpeed)

moveEthernally = nO.repeat_ethernally(makeStepsSingleEpoch)
hardStop = nO.set_immed(RegID.currentSpeed, 0)  # and don't emit make steps commands


def initAcceleration(accel: int) -> nO.set_immed:
	return nO.set_immed(RegID.currentAcceleration, accel)


doAcceleration = (
	nO.incr(RegID.currentSpeed, RegID.currentAcceleration),
	makeStepsSingleEpoch,
)


def accelerateWithAccelerationSingleEpoch(accel: int):
	return (initAcceleration(accel), *doAcceleration)


def speedChangePlan2Microcode(plan: SpeedChangePlan):
	res = []
	if plan.accelerationEpochs > 1:
		res.extend(
			(
				nO.group(
					(
						nO.set_immed(RegID.countOfSpeedSteps, plan.accelerationEpochs),
						accelerateWithAccelerationSingleEpoch(plan.acceleration),
					)
				),
				nO.repeat(
					nO.group(
						(
							nO.incr(RegID.currentSpeed, RegID.currentAcceleration),
							makeStepsSingleEpoch,
						)
					),
					RegID.countOfSpeedSteps,
				),
			)
		)
	elif plan.accelerationEpochs == 1:
		res.extend(accelerateWithAccelerationSingleEpoch(plan.acceleration))
	if plan.residualEpoch:
		res.extend(accelerateWithAccelerationSingleEpoch(plan.residualEpoch))
	return res


def changeSpeedArbitrarily(currentSpeed: int, setSpeed: int):
	"""Changes speed from `currentSpeed` to `setSpeed` taking into account acceleration limits"""
	uops = []

	if areTheSameSign(setSpeed, currentSpeed):
		uops.extend(speedChangePlan2Microcode(SpeedChangePlan.compute(currentSpeed, setSpeed, deccelLimit, accelLimit)))
	else:
		uops.extend(speedChangePlan2Microcode(SpeedChangePlan.compute(currentSpeed, 0, deccelLimit, accelLimit)))
		uops.extend(speedChangePlan2Microcode(SpeedChangePlan.compute(0, setSpeed, deccelLimit, accelLimit)))
	return uops


class Microcode:
	def _changeSpeed(cpu: CPU, setSpeed: int):
		return changeSpeedArbitrarily(cpu[RegID.currentSpeed], targetSpeed)

	def _moveEthernallyWithSpeed(cpu: CPU, setSpeed: int):
		return (*_changeSpeed(cpu, setSpeed), moveEthernally)

	def speed_forward(cpu: CPU, setSpeed: int, action: bool = False):
		return _moveEthernallyWithSpeed(ps, setSpeed)

	def speed_reverse(cpu: CPU, setSpeed: int, action: bool = False):
		return _moveEthernallyWithSpeed(ps, setSpeed)

	def stop_soft_hold(cpu: CPU, action: bool = False):
		return (_changeSpeed(ps, 0), energize())

	def stop_hard_hold(cpu: CPU, action: bool = False):
		return (hardStop, energize())

	def stop_soft_deenergize(cpu: CPU, action: bool = False):
		return (_changeSpeed(ps, 0), deenergize())

	def stop_hard_deenergize(cpu: CPU, action: bool = False):
		return (hardStop, deenergize())

	def sleep(cpu: CPU, realTime: int, action: bool = False):
		return (sleep(realTime),)

	def sleep_interruptible(cpu: CPU, realTime: int, action: bool = False):
		return (sleep_interruptible(realTime),)

	def _conditionalJump(newIP: "InstructionPointer"):
		return cond_true(
			group(
				(
					set_immed(RegID.program, newIP.program),
					set_immed(RegID.ip, newIP.ip),
				)
			)
		)

	def _jumpIfInput(flagID: FlagID, newIP: "InstructionPointer"):
		return (getFlag(flagID), _conditionalJump(newIP))

	def jump_if_in0(cpu: CPU, newIP: "InstructionPointer", action: bool = False):
		return cls._jumpIfInput(FlagID.IN0, newIP)

	def jump_if_in1(cpu: CPU, newIP: "InstructionPointer", action: bool = False):
		return cls._jumpIfInput(FlagID.IN1, newIP)

	def jump_if_at_zero(cpu: CPU, newIP: "InstructionPointer", action: bool = False):
		return (eq(RegID.zero, RegID.position), _conditionalJump(newIP))

	def jump_if_zero(cpu: CPU, newIP: "InstructionPointer", action: bool = False):
		return cls._jumpIfInput(FlagID.SET_ZERO, newIP)

	def _moveToPosition(cpu: CPU, position: int):
		sched = ArbitraryPositionChangePlan.compute()
		...  # ???? ToDO???

	# absolute positions
	def move_to_position_forward(cpu: CPU, position: int, action: bool = False):
		_moveToPosition(position)

	def move_to_position_reverse(cpu: CPU, position: int, action: bool = False):
		_moveToPosition(position)

	def move_to_position(cpu: CPU, position: int, action: bool = False):
		_moveToPosition(position)

	def move_to_recorded_zero(cpu: CPU, action: bool = False):
		_moveToPosition(ZERO)

	def move_to_recorded_label(cpu: CPU, action: bool = False):
		_moveToPosition(LABEL)

	# the ones for which limits are NOT documented, but we assume they are the same
	def move_untill_zero_forward_set_zero(cpu: CPU, setSpeed: int, action: bool = False):
		"""searches for zero position in a forward direction. The movement continues until signal to SET_ZERO input received. The DATA field determines the motion speed during searching the zero position.
		Attention: the speed commands are always set as full steps per second."""

		print("move_untill_zero_forward_set_zero", action)

	def move_untill_zero_reverse_set_zero(cpu: CPU, setSpeed: int, action: bool = False):
		"""for searching zero position in a backward direction. The movement continues until signal to SET_ZERO input received. The DATA field determines the motion speed during searching the zero position.
		Attention: the speed commands are always set as full steps per second."""

		print("move_untill_zero_reverse_set_zero", action)

	def move_untill_in1_forward_set_label(cpu: CPU, setSpeed: int, action: bool = False):
		"""for searching LABEL position in a forward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position.
		Attention: the speed commands are always set as full steps per second."""

		print("move_untill_in1_forward_set_label", action)

	def move_untill_in1_reverse_set_label(cpu: CPU, setSpeed: int, action: bool = False):
		"""for searching LABEL position in a backward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position.
		Attention: the speed commands are always set as full steps per second."""

		print("move_untill_in1_reverse_set_label", action)

	def move_untill_in1_forward_set_mark(cpu: CPU, setSpeed: int, action: bool = False):
		"""searches for LABEL position in a forward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position. The motor stops according the deceleration value, current position is set as “Mark” position. Attention: the speed commands are always set as full steps per second. This command is valid for 2d version of communication protocol only."""

		print("move_untill_in1_forward_set_mark", action)

	def move_untill_in1_reverse_set_mark(cpu: CPU, setSpeed: int, action: bool = False):
		"""searches for LABEL position in backward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position. The motor stops according the deceleration value, current position is set as “Mark” position. Attention: the speed commands are always set as full steps per second. This command is valid for 2d version of communication protocol only."""

		print("move_untill_in1_reverse_set_mark", action)

	# relative positions
	def move_steps_forward(cpu: CPU, position: int, action: bool = False):
		"""for motor displacement in forward direction. The DATA field should contain the displacement value. The motion speed is determined by specified minimum and maximum speed and acceleration value. The motor should be stopped before executing this command (field Mot_Status of the powerSTEP_STATUS_Type structure = 0)."""

		print("move_steps_forward", action)

	def move_steps_reverse(cpu: CPU, position: int, action: bool = False):
		"""for motor displacement in backward direction. The DATA field should contain the displacement value. The motion speed is determined by specified minimum and maximum speed and acceleration value. The motor should be stopped before executing this command (field Mot_Status of the powerSTEP_STATUS_Type structure = 0)."""

		print("move_steps_reverse", action)

	def move_untill_sw_forward(cpu: CPU, argument: "SignalVerifyRange", action: bool = False):
		"""motor forward motion at the maximum speed until receiving a signal at the input SW (taking into account the signal masking). After that the motor decelerates and stops. The MASK state of the signal can be changed by the executing command CMD_PowerSTEP01_SET_MASK_EVENT"""
		print("move_untill_sw_forward", action)

	def move_untill_sw_reverse(cpu: CPU, argument: "SignalVerifyRange", action: bool = False):
		"""motor backward motion at the maximum speed until receiving a signal at the input SW (taking into account the signal masking). After that the motor decelerates and stops. The MASK state of the signal can be changed by the executing command CMD_PowerSTEP01_SET_MASK_EVENT"""
		print("move_untill_sw_reverse", action)
