import typing
from dataclasses import dataclass

from .vm import CPU, FlagID, RegID


class NanoOp:
	def __call__(self, cpu):
		raise NotImplementedError


class nop(NanoOp):
	def __call__(self, cpu):
		pass


class energize(NanoOp):
	def __call__(self, cpu):
		cpu.motorController.driver.energize()


class deenergize(NanoOp):
	def __call__(self, cpu):
		cpu.motorController.driver.deenergize()


class makeStep(NanoOp):
	def __call__(self, cpu):
		motorController.makeStep()


class sleep(NanoOp):
	amount: int

	def __call__(self, cpu):
		# sleep(self.amount) in real hardware
		pass


class sleep_interruptible(sleep):
	pass


class getFlag(NanoOp):
	flag: FlagID

	def __call__(self, cpu):
		cpu.cmpRes = cpu.flags[flag]


@dataclass
class set_immed(NanoOp):
	target: RegID
	immed: int

	def __call__(self, cpu):
		cpu.regs[self.target] = immed


@dataclass
class TwoRegOperandNanoOp(NanoOp):
	a: RegID
	b: RegID


class set(TwoRegOperandNanoOp):
	def __call__(self, cpu):
		cpu.regs[self.a] = cpu.regs[self.b]


class incr(TwoRegOperandNanoOp):
	def __call__(self, cpu):
		cpu.regs[self.a] += cpu.regs[self.b]


class eq(TwoRegOperandNanoOp):
	def __call__(self, cpu):
		cpu.cmpRes = cpu.regs[self.a] == cpu.regs[self.b]


class gt(TwoRegOperandNanoOp):
	def __call__(self, cpu):
		cpu.cmpRes = cpu.regs[self.a] > cpu.regs[self.b]


@dataclass
class NestedInstr(NanoOp):
	op: NanoOp


class repeat_untill(NestedInstr):
	def __call__(self, cpu):
		while cpu.cmpRes and not cpu.interruptLoop:
			self.op(cpu)


class repeat_ethernally(NestedInstr):
	def __call__(self, cpu):
		while not cpu.interruptLoop:
			self.op(cpu)


@dataclass
class repeat(NestedInstr):
	count: RegID

	def __call__(self, cpu):
		for i in range(cpu.regs[self.count]):
			if cpu.interruptLoop:
				break

			self.op(cpu)


class cond_true(NestedInstr):
	def __call__(self, cpu):
		if cpu.cmpRes:
			self.op(cpu)


class cond_false(NestedInstr):
	def __call__(self, cpu):
		if not cpu.cmpRes:
			self.op(cpu)


@dataclass
class group(NanoOp):
	ops: typing.Sequence[NanoOp]

	def __call__(self, cpu):
		for op in self.ops:
			op(cpu)
