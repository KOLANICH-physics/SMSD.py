from ...kaitai.smsd_lan import SmsdLan
from ..serializers import serializeMotorMode
from .Clock import Clockable

AccelerationStatus = SmsdLan.PowerstepStatus.AccelerationStatus


class MotorDriver(Clockable):
	__slots__ = ("windings", "currentHold", "currentWork", "model", "isInCurrentMode")

	def __init__(self, countOfWindings: int = 2):
		self.windings = [False] * countOfWindings
		self.currentHold = 1.0  # type: float
		self.currentWork = 0.1  # type: float
		self.model = 0  # type: int
		self.isInCurrentMode = False  # type: bool

	@property
	def isDeenergized(self) -> bool:
		return not any(self.windings)

	def tick(self) -> None:
		pass


class MotorController(Clockable):
	ELECTRICAL_MICROSTEPS_LOG = 7

	def __init__(self):
		self.microstepLog = 0  # type: int

		self._microsteps = 0  # type: int
		self.accelerationCurrent = 0  # type: int
		self.accelerationSet = 0  # type: int
		self.decellerationSet = 0  # type: int
		self.speedCurrent = 0  # type: int
		self.speedTarget = 0  # type: int
		self.speedMin = 0  # type: int
		self.speedMax = 0  # type: int
		self.speedFullStep = 0  # type: int

		self.driver = MotorDriver()  # type: MotorDriver

	@property
	def microstepsMask(self) -> int:
		return (1 << self.microstepLog) - 1

	@property
	def fullSteps(self) -> int:
		return self._microsteps >> self.microstepLog

	@property
	def microsteps(self) -> int:
		return self._microsteps & self.microstepsMask

	@property
	def electricalMicrosteps(self) -> int:
		return self._microsteps << (self.__class__.ELECTRICAL_MICROSTEPS_LOG - self.microstepLog)

	@property
	def isDirectionForward(self) -> bool:
		return self.speedCurrent >= 0

	@property
	def accelerationStatus(self) -> AccelerationStatus:
		if self.accelerationCurrent == 0:
			if self.speedCurrent == 0:
				return AccelerationStatus.stop
			else:
				return AccelerationStatus.constant_speed
		else:
			if self.accelerationCurrent > 0:
				return AccelerationStatus.accelerates
			else:
				return AccelerationStatus.decelerates

	def tick(self) -> None:
		#self.motor.speedCurrent += self.accelerationCurrent
		self.driver.tick()


class MotorInstructions:
	def position_absolute_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads the current motor position"""
		# print("position_absolute_get", action)  # -> current_electrical_step_microstep
		return SmsdLan.Response.Code.position_absolute, ps.motorController.microsteps

	CMD_PowerSTEP01_GET_ABS_POS = position_absolute_get

	def position_microstepping_electrical_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads the current motor electrical microstepping position"""
		# print("position_microstepping_electrical_get", action)  # -> current_electrical_step_microstep

		return SmsdLan.Response.Code.position_microstepping_electrical, ps.motorController.electricalMicrosteps

	CMD_PowerSTEP01_GET_EL_POS = position_microstepping_electrical_get

	def speed_current_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads the current motor speed.
		The important notice: for the correct response to the CMD_PowerSTEP01_GET_SPEED command the minimum speed should be set = 0x00 by command CMD_PowerSTEP01_SET_MIN_SPEED before sending the command CMD_PowerSTEP01_GET_SPEED. Otherwise the result could be wrong for low speed movement and stops"""

		# print("speed_get", action)  # -> speed_verify_range(argument_raw, 15, 15600)

		return SmsdLan.Response.Code.speed_current, ps.motorController.speedCurrent

	CMD_PowerSTEP01_GET_SPEED = speed_current_get

	# the ones for which limits are documented
	def speed_min_set(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""sets the motor minimum speed. The DATA field should contain the speed value in range 0 – 950 steps/sec.
		Attention: the speed commands are always set as full steps per second."""
		print("speed_min_set", argument.speed, action)
		ps.motorController.speedMin = argument.speed

	CMD_PowerSTEP01_SET_MIN_SPEED = speed_min_set

	def speed_min_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads the current set minimum motor speed"""
		# print("speed_min_get", action)  # -> speed_verify_range(argument_raw, 0, 950)
		return SmsdLan.Response.Code.speed_min, ps.motorController.speedMin

	CMD_PowerSTEP01_GET_MIN_SPEED = speed_min_get

	def speed_max_set(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""sets the motor maximum speed. The DATA field should contain the speed value in range 16 – 15600 steps/sec.
		Attention: the speed commands are always set as full steps per second."""
		print("speed_max_set", argument.speed, action)
		ps.motorController.speedMax = argument.speed

	CMD_PowerSTEP01_SET_MAX_SPEED = speed_max_set

	def speed_max_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads the current set maximum motor speed"""
		print("speed_max_get", action)  # -> speed_verify_range(argument_raw, 16, 15600)
		return SmsdLan.Response.Code.speed_max, ps.motorController.speedMax

	CMD_PowerSTEP01_GET_MAX_SPEED = speed_max_get

	def speed_full_step_set(ps: "PowerStepSimulator", argument: "SpeedVerifyRange", action: bool = False):
		"""sets the running speed, when the motor switches to a full step mode. The DATA field should contain the speed value in range 15 – 15600 steps/sec.
		Attention: the speed commands are always set as full steps per second."""
		print("speed_full_step_set", argument.speed, action)
		ps.motorController.speedFullStep = argument.speed

	CMD_PowerSTEP01_SET_FS_SPEED = speed_full_step_set

	def acceleration_set(ps: "PowerStepSimulator", argument: "AccelerationVerifyRange", action: bool = False):
		"""sets the motor acceleration to getting the motor maximum speed. The DATA field should contain the acceleration value in range 15 – 59000 steps/sec2."""
		print("acceleration_set", argument.acceleration, action)
		ps.motorController.accelerationSet = argument.acceleration

	CMD_PowerSTEP01_SET_ACC = acceleration_set

	def decelleration_set(ps: "PowerStepSimulator", argument: "AccelerationVerifyRange", action: bool = False):
		"""sets the motor deceleration. The DATA field should contain the DECELERATION value in range 15 – 59000 steps/sec2."""
		print("decelleration_set", argument.acceleration, action)
		ps.motorController.decellerationSet = argument.acceleration

	CMD_PowerSTEP01_SET_DEC = decelleration_set

	def motor_mode_set(ps: "PowerStepSimulator", argument: "MotorMode", action: bool = False):
		"""
		sets motor and control parameters:
		* current or voltage
		* motor model (determines motor analog parameters: max. current per phase, resistance per phase, inductance per phase, Step angle)
		* microstepping mode
		* operating current
		* holding current"""
		print("mode_set", argument, action)
		mc = ps.motorController
		d = mc.driver
		d.currentHold = argument.hold_current
		d.currentWork = argument.work_current
		mc.microstepLog = argument.microstepping_nlog
		d.model = argument.motor_model
		d.isInCurrentMode = argument.is_in_current_mode

	CMD_PowerSTEP01_SET_MODE = motor_mode_set

	def motor_mode_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads motor control parameters from the controller
		those in CMD_PowerSTEP01_SET_MODE + number of program, which is available to be started by external signals"""
		print("mode_get", action)  # -> motor_mode
		mc = ps.motorController
		d = mc.driver
		SmsdLan.Response.Code.mode, serializeMotorMode(program_n=0, hold_current=d.currentHold, work_current=d.currentWork, microstepping_nlog=mc.microstepLog, motor_model=d.model, is_in_current_mode=d.isInCurrentMode)

	CMD_PowerSTEP01_GET_MODE = motor_mode_get
