from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception('Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s' % kaitaistruct.__version__)

class SmsdModbus(KaitaiStruct):
    """
    .. seealso::
       Source - https://smd.ee/manuals/BLSD-20Modbus_PS.pdf
    
    
    .. seealso::
       Source - https://electroprivod.ru/pdf/drivers/BLSD-20Modbus_PS_2020_10_08.pdf
    """

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class Instruction(KaitaiStruct):

        class RegisterType(IntEnum):
            discrete_inputs = 0
            coils = 1
            inputs = 2
            holding_registers = 3

        class Command(IntEnum):
            stop_program = 0
            register_system_set = 1
            register_modbus_write = 2
            read_reg_modbus = 3
            delay = 4
            jmp = 5
            jeq = 6
            jneq = 7
            jgt = 8
            jlt = 9
            call = 10
            ret = 11
            loop = 12
            full_stop_program = 13

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw0 = self._io.read_u1()
            self.raw1 = self._io.read_u1()
            _on = self.command
            if _on == SmsdModbus.Instruction.Command.register_system_set:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.RegisterSystem(_io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.jeq:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Jump(self.is_relative, _io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.delay:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Delay(_io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.register_modbus_write:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.RegisterModbus(_io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.jmp:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Jump(self.is_relative, _io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.jneq:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Jump(self.is_relative, _io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.jgt:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Jump(self.is_relative, _io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.jlt:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Jump(self.is_relative, _io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.loop:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Loop(_io__raw_data, self, self._root)
            elif _on == SmsdModbus.Instruction.Command.call:
                self._raw_data = self._io.read_bytes(2)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdModbus.Instruction.Jump(False, _io__raw_data, self, self._root)
            else:
                self.data = self._io.read_bytes(2)

        class Delay(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.delay = self._io.read_u2le()

        class Loop(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.repeats = self._io.read_u1()
                self.commands = self._io.read_u1()

        class Jump(KaitaiStruct):

            def __init__(self, is_relative, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.is_relative = is_relative
                self._read()

            def _read(self):
                _on = self.is_relative
                if _on == True:
                    self.addr = SmsdModbus.Instruction.Jump.Relative(self._io, self, self._root)
                elif _on == False:
                    self.addr = SmsdModbus.Instruction.Jump.Absolute(self._io, self, self._root)

            class Relative(KaitaiStruct):

                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.addr = self._io.read_s2le()
                    if not self.addr >= -1024:
                        raise kaitaistruct.ValidationLessThanError(-1024, self.addr, self._io, u'/types/instruction/types/jump/types/relative/seq/0')
                    if not self.addr <= 1024:
                        raise kaitaistruct.ValidationGreaterThanError(1024, self.addr, self._io, u'/types/instruction/types/jump/types/relative/seq/0')

            class Absolute(KaitaiStruct):

                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.addr = self._io.read_u2le()
                    if not self.addr >= 0:
                        raise kaitaistruct.ValidationLessThanError(0, self.addr, self._io, u'/types/instruction/types/jump/types/absolute/seq/0')
                    if not self.addr <= 1024:
                        raise kaitaistruct.ValidationGreaterThanError(1024, self.addr, self._io, u'/types/instruction/types/jump/types/absolute/seq/0')

        class RegisterModbus(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.reg = self._io.read_u2le()

        class RegisterSystem(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.value = self._io.read_u2le()

        @property
        def command(self):
            if hasattr(self, '_m_command'):
                return self._m_command if hasattr(self, '_m_command') else None
            self._m_command = KaitaiStream.resolve_enum(SmsdModbus.Instruction.Command, self.raw0 & 127)
            return self._m_command if hasattr(self, '_m_command') else None

        @property
        def is_relative(self):
            """displacement type for movement commands."""
            if hasattr(self, '_m_is_relative'):
                return self._m_is_relative if hasattr(self, '_m_is_relative') else None
            self._m_is_relative = self.raw0 >> 7 & 1 == 1
            return self._m_is_relative if hasattr(self, '_m_is_relative') else None

        @property
        def register_address(self):
            """address of the system register AX_REG ... FX_REG with numbers 0 ... 5."""
            if hasattr(self, '_m_register_address'):
                return self._m_register_address if hasattr(self, '_m_register_address') else None
            self._m_register_address = self.raw1 & 15
            return self._m_register_address if hasattr(self, '_m_register_address') else None

        @property
        def register_type(self):
            """type of a Modbus register."""
            if hasattr(self, '_m_register_type'):
                return self._m_register_type if hasattr(self, '_m_register_type') else None
            self._m_register_type = KaitaiStream.resolve_enum(SmsdModbus.Instruction.RegisterType, self.raw1 >> 4 & 15)
            return self._m_register_type if hasattr(self, '_m_register_type') else None

    class Error(KaitaiStruct):
        """5023h register of modbus.
        errors that occur during controller operation
        """

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.voltage_out_of_range = self._io.read_bits_int_le(1) != 0
            self.short_circuit_winding = self._io.read_bits_int_le(1) != 0
            self.overheat_brake = self._io.read_bits_int_le(1) != 0
            self.overheat_power = self._io.read_bits_int_le(1) != 0
            self.not_connected_hall = self._io.read_bits_int_le(1) != 0
            self.emergency_stop = self._io.read_bits_int_le(1) != 0
            self.overheat_mcu = self._io.read_bits_int_le(1) != 0
            self.test_control_program = self._io.read_bits_int_le(1) != 0
            self.runtime = self._io.read_bits_int_le(1) != 0
            self.io_settings = self._io.read_bits_int_le(1) != 0
            self.output_analog = self._io.read_bits_int_le(1) != 0
            self.warning_breakpoint = self._io.read_bits_int_le(1) != 0
            self.register_out_of_range = self._io.read_bits_int_le(1) != 0
            self.parity = self._io.read_bits_int_le(1) != 0