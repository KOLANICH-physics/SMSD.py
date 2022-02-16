from ...kaitai.smsd_lan import SmsdLan
from ..serializers import *
from .instructionProcessors import *
from .instructions import *
from .motor import *
from .PowerStepSimulator import *


class PowerStepResponder:
	__slots__ = ("ps",)

	def __init__(self):
		self.ps = PowerStepSimulator()

	def __call__(self, cmd):
		processor = getattr(Instructions, cmd.operation.name, None)
		if processor:
			arg = cmd.argument
			if isinstance(arg, SmsdLan.PowerstepCommand.ZeroInt):
				result = processor(self.ps, cmd.action)
			else:
				# print("arg", arg)
				result = processor(self.ps, arg, cmd.action)
			if isinstance(result, tuple):
				if len(result) == 2:
					respCode, respValue = result
				else:
					raise ValueError("Processor func should either return a tuple (code, result) or None")
			else:
				respCode = SmsdLan.Response.Code.success
				respValue = 0

			return SmsdLan.Type.response, self.serializeResponse(respCode, respValue)
		else:
			print(self.__class__.__name__ + ": No processor for ", cmd.operation.name)

	def serializeResponse(self, code, return_data: int):
		ps = self.ps
		m = ps.motorController
		return serializeResponse(is_deenergized=m.driver.isDeenergized, is_ready=ps.instructionProcessor.isReady, is_sw_on=False, has_sw_event_happenned=False, is_rotating_direction_forward=m.isDirectionForward, accelerationStatus=m.accelerationStatus, is_command_error=False, code=code, return_data=return_data)

	def startTicking(self):
		self.ps.startTicking()
