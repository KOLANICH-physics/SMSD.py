from ...kaitai.smsd_lan import SmsdLan
from ..serializers import serializeInstructionPointer
from .Clock import Clockable


class InstructionProcessor(Clockable):
	__slots__ = ()

	def __call__(self, instruction):
		raise NotImplementedError

	@property
	def isReady(self) -> bool:
		return True


class ProgramLoader(InstructionProcessor):
	__slots__ = ("parent", "instructions")

	def __init__(self, parent):
		self.parent = parent
		self.instructions = []

	def commit(self):
		self.parent.instructions = self.instructions
		self.instructions = None

	def __call__(self, instruction):
		self.instructions.append(instruction)

	def tick(self) -> None:
		pass


class Program:
	__slots__ = (
		"instructions",
		"_instructionPointer",
	)

	def __init__(self):
		self.instructions = []
		self._instructionPointer = 0

	def executeNextInstr(self):
		self._instructionPointer += 1
		instr = self.instructions

	@property
	def instructionPointer(self):
		return self._instructionPointer

	@instructionPointer.setter
	def instructionPointer(self, v):
		self._instructionPointer = v

	def startLoading(self):
		return ProgramLoader(self)


class ProgramExecutor(InstructionProcessor):
	__slots__ = ("programIdx", "programs")

	def __init__(self, countOfPrograms: int = 4):
		self.programIdx = 0
		self.programs = [Program() for i in range(countOfPrograms)]

	@property
	def curProgram(self):
		return self.programs[self.programIdx]

	@property
	def curProgramInstrPointer(self):
		return self.curProgram.instructionPointer

	@property
	def fullInstructionPointer(self):
		return self.programIdx, self.curProgram.instructionPointer

	def __call__(self, instruction):
		instruction()

	def tick(self) -> None:
		pass


class InstructionProcessorInstructions:
	def ret(ps: "PowerStepSimulator", action: bool = False):
		"""specifies the end of a subprogram and to return back to the main program. If previously the command CMD_PowerSTEP01_CALL_PROGRAM was not called, the executing of CMD_PowerSTEP01_RETURN_PROGRAM will call an error."""
		print("ret", action)

	CMD_PowerSTEP01_RETURN_PROGRAM = ret

	def program_start_mem0(ps: "PowerStepSimulator", action: bool = False):
		"""&program_start_mem_doc starts executing a program from the Controller memory area."""

	CMD_PowerSTEP01_START_PROGRAM_MEM0 = program_start_mem0

	def program_start_mem1(ps: "PowerStepSimulator", action: bool = False):
		"""*program_start_mem_doc"""
		print("program_start_mem1", action)

	CMD_PowerSTEP01_START_PROGRAM_MEM1 = program_start_mem1

	def program_start_mem2(ps: "PowerStepSimulator", action: bool = False):
		"""*program_start_mem_doc"""
		print("program_start_mem2", action)

	CMD_PowerSTEP01_START_PROGRAM_MEM2 = program_start_mem2

	def program_start_mem3(ps: "PowerStepSimulator", action: bool = False):
		"""*program_start_mem_doc"""
		print("program_start_mem3", action)

	CMD_PowerSTEP01_START_PROGRAM_MEM3 = program_start_mem3

	def halt(ps: "PowerStepSimulator", action: bool = False):
		"""stops executing a program"""
		print("halt", action)

	CMD_PowerSTEP01_STOP_PROGRAM_MEM = halt

	def end(ps: "PowerStepSimulator", action: bool = False):
		"""marks the end of executing program"""
		print("end", action)

	CMD_PowerSTEP01_END = end

	def jump(ps: "PowerStepSimulator", argument: "InstructionPointer", action: bool = False):
		"""unconditional branch – jumps to a specified command number in a specified program number. The DATA field contains the information about a program memory number and a command sequence number:"""

		print("jump", action)

	CMD_PowerSTEP01_GOTO_PROGRAM = jump

	def call(ps: "PowerStepSimulator", argument: "InstructionPointer", action: bool = False):
		"""calls a subprogram. The DATA field contains the information about a program memory number and a command sequence number, which starts a subprogram:  For returning back to the main program, the subprogram should contain a RETURN command - CMD_PowerSTEP01_RETURN_PROGRAM. The subprogram is executed until the CMD_PowerSTEP01_RETURN_PROGRAM and after that returns to the next command of the main program after CMD_PowerSTEP01_CALL_PROGRAM."""

		print("call", action)

	CMD_PowerSTEP01_CALL_PROGRAM = call

	def instruction_pointer_get(ps: "PowerStepSimulator", action: bool = False):
		"""reads information about current executing command number and program number from the controller."""
		# print("instruction_pointer_get", action)  # -> jump_target(argument_raw)
		return SmsdLan.Response.Code.instruction_pointer, serializeInstructionPointer(*ps.executor.fullInstructionPointer)

	CMD_PowerSTEP01_GET_STACK = instruction_pointer_get

	def loop(ps: "PowerStepSimulator", argument: "Loop", action: bool = False):
		"""loop – the Controller repeats specified times specified number of commands (start from the first command after this command. The DATA field contains the information about commands number and cycles number: bits 0..9 of the DATA field contain the commands number, bits 10..19 of the DATA field contain the cycles number."""
		print("loop", action)

	CMD_PowerSTEP01_LOOP_PROGRAM = loop
