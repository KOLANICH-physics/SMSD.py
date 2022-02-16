from ...kaitai.smsd_lan import SmsdLan
from .gpio import GPIOInstructions
from .instructionProcessors import InstructionProcessorInstructions
from .motor import MotorInstructions


class Instructions(MotorInstructions, GPIOInstructions, InstructionProcessorInstructions):
	def zero_set(ps: "PowerStepSimulator", action: bool = False):
		"""sets ZERO position (to clear internal steps counter and specify a current position as a ZERO position)"""
		print("zero_set", action)

	CMD_PowerSTEP01_RESET_POS = zero_set

	def reset_powerstep01(ps: "PowerStepSimulator", action: bool = False):
		"""hardware and software reset of the PowerSTEP01 stepper motor control module, but not of the whole Controller."""
		print("reset_powerstep01", action)
		ps.__init__()

	CMD_PowerSTEP01_RESET_POWERSTEP01 = reset_powerstep01

	def control_mode_set_en_step_dir(ps: "PowerStepSimulator", action: bool = False):
		"""changes the control mode to pulse control using external input signals EN, STEP, DIR."""
		print("control_mode_set_en_step_dir", action)

	CMD_PowerSTEP01_STEP_CLOCK = control_mode_set_en_step_dir

	def usb_stop(ps: "PowerStepSimulator", action: bool = False):
		"""stops data transfer via USB interface"""
		print("usb_stop", action)

	CMD_PowerSTEP01_STOP_USB = usb_stop

	def status_and_clear_errors_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads the current state of the controller, and the Controller clears all error flags."""
		print("status_and_clear_errors_get", action)

	CMD_PowerSTEP01_GET_STATUS_AND_CLR = status_and_clear_errors_get

	###########

	def speed_forward(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""starts motor rotation in forward direction at designated speed. The DATA field should contain the final rotation speed value."""
		print("speed_forward", argument.speed, action)
		ps.motorController

	CMD_PowerSTEP01_RUN_F = speed_forward

	def speed_reverse(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""starts motor rotation in backward direction at designated speed. The DATA field should contain the final rotation speed value."""
		print("speed_reverse", argument.speed, action)
		ps.motorController

	CMD_PowerSTEP01_RUN_R = speed_reverse

	def stop_soft_hold(ps: "PowerStepSimulator", action: bool = False):
		"""smooth decelerating of the stepper motor and stop. After that the motor holds the current position (with preset holding current)."""
		print("stop_soft_hold", action)

	CMD_PowerSTEP01_SOFT_STOP = stop_soft_hold

	def stop_hard_hold(ps: "PowerStepSimulator", action: bool = False):
		"""sudden stop of the stepper motor and holding the current position (with preset holding current)."""
		print("stop_hard_hold", action)

	CMD_PowerSTEP01_HARD_STOP = stop_hard_hold

	def stop_soft_deenergize(ps: "PowerStepSimulator", action: bool = False):
		"""smooth decelerating of the stepper motor and stop. After that the motor phases are deenergized"""
		print("stop_soft_deenergize", action)

	CMD_PowerSTEP01_SOFT_HI_Z = stop_soft_deenergize

	def stop_hard_deenergize(ps: "PowerStepSimulator", action: bool = False):
		"""sudden stop of the stepper motor and deenergizing the stepper motor"""
		print("stop_hard_deenergize", action)

	CMD_PowerSTEP01_HARD_HI_Z = stop_hard_deenergize

	############

	def sleep(ps: "PowerStepSimulator", argument: "TimeVerifyRange", action: bool = False):
		"""sets pause. The DATA field contains the waiting time measured as ms. Allowed value range 0 – 3600000 ms"""
		print("sleep", action)

	CMD_PowerSTEP01_SET_WAIT = sleep

	def sleep_interruptible(ps: "PowerStepSimulator", argument: "TimeVerifyRange", action: bool = False):
		"""sets a pause. The DATA field contains the waiting time measured as ms. Allowed value range 0 – 3600000 ms. Unlike with the similar command CMD_PowerSTEP01_SET_WAIT, executing of this command can be interrupted by input signals IN0, IN1 or SET_ZERO. This command is valid for 2d version of communication protocol only."""
		print("sleep_interruptible", action)

	CMD_PowerSTEP01_SET_WAIT_2 = sleep_interruptible

	def jump_if_in0(ps: "PowerStepSimulator", argument: "InstructionPointer", action: bool = False):
		"""conditional branch – jumps to a specified command number in a specified program number if there is a signal at the input IN0. The DATA field contains the information about a program memory number and a command sequence number:"""

	CMD_PowerSTEP01_GOTO_PROGRAM_IF_IN0 = jump_if_in0

	def jump_if_in1(ps: "PowerStepSimulator", argument: "InstructionPointer", action: bool = False):
		"""conditional branch – jumps to a specified command number in a specified program number if there is a signal at the input IN1. The DATA field contains the information about a program memory number and a command sequence number:"""

		print("jump_if_in1", action)

	CMD_PowerSTEP01_GOTO_PROGRAM_IF_IN1 = jump_if_in1

	def jump_if_at_zero(ps: "PowerStepSimulator", argument: "InstructionPointer", action: bool = False):
		"""conditional branch – jumps to a specified command number in a specified program number if the current position value is 0. The DATA field contains the information about a program memory number and a command sequence number:"""

		print("jump_if_at_zero", action)

	CMD_PowerSTEP01_GOTO_PROGRAM_IF_ZERO = jump_if_at_zero

	def jump_if_zero(ps: "PowerStepSimulator", argument: "InstructionPointer", action: bool = False):
		"""conditional branch – jumps to a specified command number in a specified program number if there is a signal at the input SET_ZERO. The DATA field contains the information about a program memory number and a command sequence number:  This command is valid for 2d version of communication protocol only."""

		print("jump_if_zero", action)

	################################################

	# absolute positions
	def move_to_position_forward(ps: "PowerStepSimulator", argument: "Microsteps", action: bool = False):
		"""for motor displacement to the specified position in forward direction. The DATA field should contain the position value. The motion speed is determined by specified minimum and maximum speed and acceleration value."""

		print("move_to_position_forward", action)

	CMD_PowerSTEP01_GO_TO_F = move_to_position_forward

	def move_to_position_reverse(ps: "PowerStepSimulator", argument: "Microsteps", action: bool = False):
		"""for motor displacement to the specified position in backward direction. The DATA field should contain the position value. The motion speed is determined by specified minimum and maximum speed and acceleration value."""

		print("move_to_position_reverse", action)

	CMD_PowerSTEP01_GO_TO_R = move_to_position_reverse

	def move_to_position(ps: "PowerStepSimulator", argument: "Microsteps", action: bool = False):
		"""shortest movement to the specified position"""
		print("move_to_position", action)

	CMD_PowerSTEP01_GO_TO = move_to_position

	def move_to_recorded_zero(ps: "PowerStepSimulator", action: bool = False):
		"""movement to the ZERO position (remembered using move_untill_zero_*_set_zero ?)"""
		print("move_to_recorded_zero", action)

	CMD_PowerSTEP01_GO_ZERO = move_to_recorded_zero

	def move_to_recorded_label(ps: "PowerStepSimulator", action: bool = False):
		"""movement to the LABEL position (remembered using move_untill_in1_*_set_label ?)"""
		print("move_to_recorded_label", action)

	CMD_PowerSTEP01_GO_LABEL = move_to_recorded_label

	# the ones for which limits are NOT documented, but we assume they are the same
	def move_untill_zero_forward_set_zero(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""searches for zero position in a forward direction. The movement continues until signal to SET_ZERO input received. The DATA field determines the motion speed during searching the zero position.
        Attention: the speed commands are always set as full steps per second."""

		print("move_untill_zero_forward_set_zero", action)

	CMD_PowerSTEP01_SCAN_ZERO_F = move_untill_zero_forward_set_zero

	def move_untill_zero_reverse_set_zero(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""for searching zero position in a backward direction. The movement continues until signal to SET_ZERO input received. The DATA field determines the motion speed during searching the zero position.
        Attention: the speed commands are always set as full steps per second."""

		print("move_untill_zero_reverse_set_zero", action)

	CMD_PowerSTEP01_SCAN_ZERO_R = move_untill_zero_reverse_set_zero

	def move_untill_in1_forward_set_label(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""for searching LABEL position in a forward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position.
        Attention: the speed commands are always set as full steps per second."""

		print("move_untill_in1_forward_set_label", action)

	CMD_PowerSTEP01_SCAN_LABEL_F = move_untill_in1_forward_set_label

	def move_untill_in1_reverse_set_label(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""for searching LABEL position in a backward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position.
        Attention: the speed commands are always set as full steps per second."""

		print("move_untill_in1_reverse_set_label", action)

	CMD_PowerSTEP01_SCAN_LABEL_R = move_untill_in1_reverse_set_label

	def move_untill_in1_forward_set_mark(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""searches for LABEL position in a forward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position. The motor stops according the deceleration value, current position is set as “Mark” position. Attention: the speed commands are always set as full steps per second. This command is valid for 2d version of communication protocol only."""

		print("move_untill_in1_forward_set_mark", action)

	CMD_PowerSTEP01_SCAN_MARK2_F = move_untill_in1_forward_set_mark

	def move_untill_in1_reverse_set_mark(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""searches for LABEL position in backward direction. The movement continues until signal to IN1 input received. The DATA field determines the motion speed during searching the LABEL position. The motor stops according the deceleration value, current position is set as “Mark” position. Attention: the speed commands are always set as full steps per second. This command is valid for 2d version of communication protocol only."""

		print("move_untill_in1_reverse_set_mark", action)

	CMD_PowerSTEP01_SCAN_MARK2_R = move_untill_in1_reverse_set_mark

	# relative positions
	def move_steps_forward(ps: "PowerStepSimulator", argument: "Microsteps", action: bool = False):
		"""for motor displacement in forward direction. The DATA field should contain the displacement value. The motion speed is determined by specified minimum and maximum speed and acceleration value. The motor should be stopped before executing this command (field Mot_Status of the powerSTEP_STATUS_Type structure = 0)."""

		print("move_steps_forward", action)

	CMD_PowerSTEP01_MOVE_F = move_steps_forward

	def move_steps_reverse(ps: "PowerStepSimulator", argument: "Microsteps", action: bool = False):
		"""for motor displacement in backward direction. The DATA field should contain the displacement value. The motion speed is determined by specified minimum and maximum speed and acceleration value. The motor should be stopped before executing this command (field Mot_Status of the powerSTEP_STATUS_Type structure = 0)."""

		print("move_steps_reverse", action)

	CMD_PowerSTEP01_MOVE_R = move_steps_reverse

	def move_untill_sw_forward(ps: "PowerStepSimulator", argument: "SignalVerifyRange", action: bool = False):
		"""motor forward motion at the maximum speed until receiving a signal at the input SW (taking into account the signal masking). After that the motor decelerates and stops. The MASK state of the signal can be changed by the executing command CMD_PowerSTEP01_SET_MASK_EVENT"""
		print("move_untill_sw_forward", action)

	CMD_PowerSTEP01_GO_UNTIL_F = move_untill_sw_forward

	def move_untill_sw_reverse(ps: "PowerStepSimulator", argument: "SignalVerifyRange", action: bool = False):
		"""motor backward motion at the maximum speed until receiving a signal at the input SW (taking into account the signal masking). After that the motor decelerates and stops. The MASK state of the signal can be changed by the executing command CMD_PowerSTEP01_SET_MASK_EVENT"""
		print("move_untill_sw_reverse", action)

	CMD_PowerSTEP01_GO_UNTIL_R = move_untill_sw_reverse
