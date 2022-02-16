from ...kaitai.smsd_lan import SmsdLan
from ..serializers import serializeEventStatus
from .Clock import Clockable


class GPIOStepState:
	__slots__ = ("inputs", "events")

	def __init__(self, parent: "GPIO"):
		self.inputs = [False] * parent.inputsCount
		self.events = [False] * parent.inputsCount


class GPIO(Clockable):
	__slots__ = ("inputsCount", "inputState", "externallySetInputs", "prevInputState", "masks", "events", "outputs", "relay", "cont")

	def __init__(self, inputsCount: int = 8, outs: int = 2):
		self.inputsCount = inputsCount  # type: int
		self.inputState = self.spawnState()  # type: GPIOStepState
		self.prevInputState = self.inputState  # type: GPIOStepState

		self.externallySetInputs = [None] * inputsCount
		self.masks = [True] * inputsCount

		self.cont = False  # type: bool

		self.outputs = [False] * outs
		self.relay = False  # type: bool

	def spawnState(self) -> GPIOStepState:
		return GPIOStepState(self)

	def tick(self) -> None:
		prevInputState = self.inputState

		newInputState = self.spawnState()
		self.mutateInputState(newInputState)

		for i, (prev, cur) in enumerate(zip(prevInputState.inputs, newInputState.inputs)):
			if self.masks[i] and not prev and cur:
				newInputState.events[i] = True

		self.prevInputState = prevInputState
		self.inputState = newInputState

	def mutateInputState(self, newInputState):
		"""Currently just copies the prev state if not externally set"""

		for i, el in enumerate(self.prevInputState.inputs):
			ext = self.externallySetInputs[i]
			if ext is not None:
				newInputState.inputs[i] = ext
				self.externallySetInputs[i] = None
			else:
				newInputState.inputs[i] = el


class GPIOInstructions:
	def relay_get(ps: "PowerStepSimulator", action: bool = False):
		"""read a current state of the controller relay"""
		# print("relay_get", action)

		return SmsdLan.Response.Code.relay_set if ps.gpio.relay else SmsdLan.Response.Code.relay_clear, 0

	CMD_PowerSTEP01_GET_RELE = relay_get

	def relay_on(ps: "PowerStepSimulator", action: bool = False):
		"""turn on the controller relay"""
		print("relay_on", action)
		ps.gpio.relay = True
		return SmsdLan.Response.Code.relay_set, 0

	CMD_PowerSTEP01_SET_RELE = relay_on

	def relay_off(ps: "PowerStepSimulator", action: bool = False):
		"""turn off the controller relay"""
		print("relay_off", action)
		ps.gpio.relay = False
		return SmsdLan.Response.Code.relay_clear, 0

	CMD_PowerSTEP01_CLR_RELE = relay_off

	########

	def events_status_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads information about current signals inputs state:
        * whether events happenned,
        * if they are masked
        * if we are waiting for them"""

		# print("events_status_get", action)  # -> events_status
		g = ps.gpio
		return SmsdLan.Response.Code.events_status, serializeEventStatus(g.inputState.inputs, g.masks, g.inputState.events)

	CMD_PowerSTEP01_STATUS_IN_EVENT = events_status_get

	def event_mask_set(ps: "PowerStepSimulator", argument: "EventMaskFromInt", action: bool = False):
		"""masks input signals. If the input signal MASK value = 1 – the Controller handles the signal state at the physical input. If the signal MASK is 0 – the controller doesn’t take a care the physical input state."""
		bits = [el.value for el in argument.is_enabled]
		print("event_mask_set", action, bits)
		g = ps.gpio
		for i, bit in enumerate(bits):
			g.masks[i] = bit

	CMD_PowerSTEP01_SET_MASK_EVENT = event_mask_set

	#################

	def wait_for_in0(ps: "PowerStepSimulator", action: bool = False):
		"""wait until receiving a signal to the input IN0"""
		# print("wait_for_in0", action)

	CMD_PowerSTEP01_WAIT_IN0 = wait_for_in0

	def wait_for_in1(ps: "PowerStepSimulator", action: bool = False):
		"""wait until receiving a signal to the input IN1"""
		# print("wait_for_in1", action)

	CMD_PowerSTEP01_WAIT_IN1 = wait_for_in1

	def wait_for_continue(ps: "PowerStepSimulator", action: bool = False):
		"""waits for synchronization signal at the input CONTINUE, which is used for synchronization of executing programs in different controllers. This command is valid for 2d version of communication protocol only."""
		# print("wait_for_continue", action)

	CMD_PowerSTEP01_WAIT_CONTINUE = wait_for_continue
