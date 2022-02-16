from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception('Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s' % kaitaistruct.__version__)
from . import checksum_simple_additive_u1

class SmsdLan(KaitaiStruct):
    """It is possible to connect to devices either via TCP or via a virtual COM port through USB.
    It is required to transfer data as whole information packets, every packet conforms the structure, described in this manual. Every packet contains only one data transmission command. It is not possible to transfer more than one data transmission command inside one information packet. Every information packet should be continuously transferred, without interruptions. After receiving an information packet, the controller handles it and sends a response, the response is sent the same physical line as the command was received. A sequence of bytes in the information packets is inverted – “little-endian”, (Intel).
    These parameters can be changed afterwards by commands sent through a USB or Ethernet connection.
    RS-232 parameters (USB connection):
    · Baud rate - 115200
    · Data bits - 8
    · Parity – none
    · Stop bits – 1
    
    .. seealso::
       Source - https://smd.ee/manuals/smsd-lan-communication-protocol.pdf
    
    
    .. seealso::
       Source - https://electroprivod.ru/pdf/smsd-4.2lan-communication-protocol.pdf
    """

    class Type(IntEnum):
        password = 0
        response = 1
        power_step = 2
        powerstem_write_mem_0 = 3
        powerstem_write_mem_1 = 4
        powerstem_write_mem_2 = 5
        powerstem_write_mem_3 = 6
        powerstem_read_mem_0 = 7
        powerstem_read_mem_1 = 8
        powerstem_read_mem_2 = 9
        powerstem_read_mem_3 = 10
        network_config_set = 11
        network_config_get = 12
        password_set = 13
        error_counters = 14
        unknown_15 = 15
        version_data = 16

    def __init__(self, limits, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.limits = limits

    def _read(self):
        self.header = SmsdLan.Header(self._io, self, self._root)
        self.header._read()
        self.check_checksum = self._io.read_bytes(0)
        _ = self.check_checksum
        if not (len(_) == 0 and self.recomputed_checksum.value == self.header.checksum):
            raise kaitaistruct.ValidationExprError(self.check_checksum, self._io, u'/seq/1')
        if self.header.len:
            _on = self.header.type
            if _on == SmsdLan.Type.powerstem_read_mem_2:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.Empty(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_read_mem_1:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.Empty(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_read_mem_0:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.Empty(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.version_data:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.VersionData(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.network_config_get:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.Empty(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_write_mem_2:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.PowerstepCommands(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.network_config_set:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.NetworkConfig(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.power_step:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.PowerstepCommand(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.response:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.Response(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_write_mem_0:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.PowerstepCommands(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_read_mem_3:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.Empty(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_write_mem_1:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.PowerstepCommands(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.error_counters:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.ErrorCounters(_io__raw_data, self, self._root)
                self.data._read()
            elif _on == SmsdLan.Type.powerstem_write_mem_3:
                self._raw_data = self._io.read_bytes(self.header.len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = SmsdLan.PowerstepCommands(_io__raw_data, self, self._root)
                self.data._read()
            else:
                self.data = self._io.read_bytes(self.header.len)

    class VersionData(KaitaiStruct):
        """undocumented type. But in the manual for another controller something is found.
        
        .. seealso::
           6.8. Identification registers - https://smd.ee/manuals/BLSD-20Modbus_PS.pdf
        """

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.hardware = SmsdLan.VersionData.Version(self._io, self, self._root)
            self.hardware._read()
            self.firmware = SmsdLan.VersionData.Version(self._io, self, self._root)
            self.firmware._read()
            self.protocol = self._io.read_u1()

        class Version(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.major = self._io.read_u2le()
                self.minor = self._io.read_u2le()

            def __repr__(self):
                return u'Version(' + str(self.major) + u', ' + str(self.minor) + u')'

    class SmsdChecksum(KaitaiStruct):

        def __init__(self, data, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.data = data

        def _read(self):
            self.original_checksum = checksum_simple_additive_u1.ChecksumSimpleAdditiveU1(255, self.data, self._io)
            self.original_checksum._read()

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value if hasattr(self, '_m_value') else None
            self._m_value = (self.original_checksum.value ^ 255) & 255
            return self._m_value if hasattr(self, '_m_value') else None

    class Empty(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.must_have_zero_size = self._io.read_bytes_full()
            _ = self.must_have_zero_size
            if not len(_) == 0:
                raise kaitaistruct.ValidationExprError(self.must_have_zero_size, self._io, u'/types/empty/seq/0')

    class SpeedVerifyRange(KaitaiStruct):

        def __init__(self, speed, min_allowed, max_allowed, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.speed = speed
            self.min_allowed = min_allowed
            self.max_allowed = max_allowed

        def _read(self):
            self.hack = self._io.read_bytes(0)
            _ = self.hack
            if not (self.min_allowed <= self.speed and self.speed <= self.max_allowed and (len(_) == 0)):
                raise kaitaistruct.ValidationExprError(self.hack, self._io, u'/types/speed_verify_range/seq/0')

    class PowerstepCommands(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.commands = []
            i = 0
            while not self._io.is_eof():
                _t_commands = SmsdLan.PowerstepCommand(self._io, self, self._root)
                _t_commands._read()
                self.commands.append(_t_commands)
                i += 1

    class MotorMode(KaitaiStruct):

        class MotorModel(IntEnum):
            sm4247 = 7
            sm5776 = 25
            sm8680_parallel = 33
            sm8680_serial = 34
            sm110201 = 43

        def __init__(self, raw, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.raw = raw

        def _read(self):
            self.hack = self._io.read_bytes(0)
            _ = self.hack
            if not (1 <= self.work_current_raw and self.work_current_raw <= 80 and (len(_) == 0)):
                raise kaitaistruct.ValidationExprError(self.hack, self._io, u'/types/motor_mode/seq/0')

        @property
        def hold_current(self):
            """share of an operating current."""
            if hasattr(self, '_m_hold_current'):
                return self._m_hold_current if hasattr(self, '_m_hold_current') else None
            self._m_hold_current = self.hold_current_percent / 100
            return self._m_hold_current if hasattr(self, '_m_hold_current') else None

        @property
        def microstepping_nlog(self):
            if hasattr(self, '_m_microstepping_nlog'):
                return self._m_microstepping_nlog if hasattr(self, '_m_microstepping_nlog') else None
            self._m_microstepping_nlog = self.raw >> 7 & 7
            return self._m_microstepping_nlog if hasattr(self, '_m_microstepping_nlog') else None

        @property
        def microstepping_denominator(self):
            if hasattr(self, '_m_microstepping_denominator'):
                return self._m_microstepping_denominator if hasattr(self, '_m_microstepping_denominator') else None
            self._m_microstepping_denominator = 1 << self.microstepping_nlog
            return self._m_microstepping_denominator if hasattr(self, '_m_microstepping_denominator') else None

        @property
        def work_current(self):
            """operating current for the current control mode."""
            if hasattr(self, '_m_work_current'):
                return self._m_work_current if hasattr(self, '_m_work_current') else None
            self._m_work_current = self.work_current_raw / 10
            return self._m_work_current if hasattr(self, '_m_work_current') else None

        @property
        def motor_model(self):
            """motor type for the voltage control mode. See the table in the docs for the limitation values."""
            if hasattr(self, '_m_motor_model'):
                return self._m_motor_model if hasattr(self, '_m_motor_model') else None
            self._m_motor_model = KaitaiStream.resolve_enum(SmsdLan.MotorMode.MotorModel, self.raw >> 1 & 63)
            return self._m_motor_model if hasattr(self, '_m_motor_model') else None

        @property
        def reserved(self):
            if hasattr(self, '_m_reserved'):
                return self._m_reserved if hasattr(self, '_m_reserved') else None
            self._m_reserved = self.raw >> 21
            return self._m_reserved if hasattr(self, '_m_reserved') else None

        @property
        def hold_current_percent(self):
            if hasattr(self, '_m_hold_current_percent'):
                return self._m_hold_current_percent if hasattr(self, '_m_hold_current_percent') else None
            self._m_hold_current_percent = (self.hold_current_raw + 1) * 25
            return self._m_hold_current_percent if hasattr(self, '_m_hold_current_percent') else None

        @property
        def is_in_current_mode(self):
            """motor control mode
            false: voltage
            true: current
            """
            if hasattr(self, '_m_is_in_current_mode'):
                return self._m_is_in_current_mode if hasattr(self, '_m_is_in_current_mode') else None
            self._m_is_in_current_mode = self.raw & 1 == 1
            return self._m_is_in_current_mode if hasattr(self, '_m_is_in_current_mode') else None

        @property
        def hold_current_raw(self):
            if hasattr(self, '_m_hold_current_raw'):
                return self._m_hold_current_raw if hasattr(self, '_m_hold_current_raw') else None
            self._m_hold_current_raw = self.raw >> 17 & 3
            return self._m_hold_current_raw if hasattr(self, '_m_hold_current_raw') else None

        @property
        def program_n(self):
            if hasattr(self, '_m_program_n'):
                return self._m_program_n if hasattr(self, '_m_program_n') else None
            self._m_program_n = self.raw >> 19 & 3
            return self._m_program_n if hasattr(self, '_m_program_n') else None

        @property
        def work_current_raw(self):
            if hasattr(self, '_m_work_current_raw'):
                return self._m_work_current_raw if hasattr(self, '_m_work_current_raw') else None
            self._m_work_current_raw = self.raw >> 10 & 127
            return self._m_work_current_raw if hasattr(self, '_m_work_current_raw') else None

        def __repr__(self):
            return u'MotorMode<' + (u'A' if self.is_in_current_mode else u'V') + u', ' + u'model=' + str(self.motor_model.value) + u', ' + u'1/' + str(self.microstepping_denominator) + u', ' + str(self.work_current_raw // 10) + u' A, ' + str(self.hold_current_percent) + u'%, ' + str(self.program_n) + u', ' + (str(self.reserved) if self.reserved != 0 else u'') + u'>'

    class ErrorCounters(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.starts = self._io.read_u4le()
            self.xt = self._io.read_u4le()
            self.timeouts = self._io.read_u4le()
            self.chip_powerstep01_init = self._io.read_u4le()
            self.chip_w5500_init = self._io.read_u4le()
            self.fram_init = self._io.read_u4le()
            self.lan = self._io.read_u4le()
            self.fram_exchange = self._io.read_u4le()
            self.interrupts = self._io.read_u4le()
            self.overcurrents = self._io.read_u4le()
            self.overvoltages = self._io.read_u4le()
            self.overheatings_chip_powerstep01 = self._io.read_u4le()
            self.overheatings_brake = self._io.read_u4le()
            self.chip_powerstep01_command_transfer = self._io.read_u4le()
            self.unkn_uvlo_powerstep = self._io.read_u4le()
            self.unkn_stall_powerstep = self._io.read_u4le()
            self.program_errors = self._io.read_u4le()

    class Response(KaitaiStruct):

        class Code(IntEnum):
            success = 0
            auth_success = 1
            auth_failure = 2
            rate_limited = 3
            wrong_checksum = 4
            wrong_command = 5
            wrong_length = 6
            out_of_range = 7
            fail_write = 8
            fail_read = 9
            fail_program = 10
            fail_write_setup = 11
            no_next = 12
            end_programs = 13
            events_status = 14
            mode = 15
            position_absolute = 16
            position_microstepping_electrical = 17
            speed_current = 18
            speed_min = 19
            speed_max = 20
            instruction_pointer = 21
            relay_set = 22
            relay_clear = 23

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.powerstep_status = SmsdLan.PowerstepStatus(self._io, self, self._root)
            self.powerstep_status._read()
            self.code = KaitaiStream.resolve_enum(SmsdLan.Response.Code, self._io.read_u1())
            _on = self.code
            if _on == SmsdLan.Response.Code.speed_max:
                self._raw_return_data = self._io.read_bytes(4)
                _io__raw_return_data = KaitaiStream(BytesIO(self._raw_return_data))
                self.return_data = SmsdLan.Response.DecodeFromInt(self.code, _io__raw_return_data, self, self._root)
                self.return_data._read()
            elif _on == SmsdLan.Response.Code.speed_min:
                self._raw_return_data = self._io.read_bytes(4)
                _io__raw_return_data = KaitaiStream(BytesIO(self._raw_return_data))
                self.return_data = SmsdLan.Response.DecodeFromInt(self.code, _io__raw_return_data, self, self._root)
                self.return_data._read()
            elif _on == SmsdLan.Response.Code.events_status:
                self._raw_return_data = self._io.read_bytes(4)
                _io__raw_return_data = KaitaiStream(BytesIO(self._raw_return_data))
                self.return_data = SmsdLan.Response.EventsStatus(_io__raw_return_data, self, self._root)
                self.return_data._read()
            elif _on == SmsdLan.Response.Code.instruction_pointer:
                self._raw_return_data = self._io.read_bytes(4)
                _io__raw_return_data = KaitaiStream(BytesIO(self._raw_return_data))
                self.return_data = SmsdLan.Response.DecodeFromInt(self.code, _io__raw_return_data, self, self._root)
                self.return_data._read()
            elif _on == SmsdLan.Response.Code.speed_current:
                self._raw_return_data = self._io.read_bytes(4)
                _io__raw_return_data = KaitaiStream(BytesIO(self._raw_return_data))
                self.return_data = SmsdLan.Response.DecodeFromInt(self.code, _io__raw_return_data, self, self._root)
                self.return_data._read()
            elif _on == SmsdLan.Response.Code.position_microstepping_electrical:
                self._raw_return_data = self._io.read_bytes(4)
                _io__raw_return_data = KaitaiStream(BytesIO(self._raw_return_data))
                self.return_data = SmsdLan.Response.CurrentElectricalStepMicrostep(_io__raw_return_data, self, self._root)
                self.return_data._read()
            else:
                self.return_data = self._io.read_bytes(4)

        class CurrentElectricalStepMicrostep(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.raw = self._io.read_u4le()

            @property
            def full_step(self):
                if hasattr(self, '_m_full_step'):
                    return self._m_full_step if hasattr(self, '_m_full_step') else None
                self._m_full_step = self.raw >> 7 & 3
                return self._m_full_step if hasattr(self, '_m_full_step') else None

            @property
            def microstep(self):
                """current microstep inside the current full step (measured as 1/128 of the full step)."""
                if hasattr(self, '_m_microstep'):
                    return self._m_microstep if hasattr(self, '_m_microstep') else None
                self._m_microstep = self.raw & 127
                return self._m_microstep if hasattr(self, '_m_microstep') else None

        class EventsStatus(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.has_happenned = self._io.read_u1()
                self.is_masking_raw = self._io.read_u1()
                self.is_waiting = self._io.read_u1()

            @property
            def is_masking(self):
                if hasattr(self, '_m_is_masking'):
                    return self._m_is_masking if hasattr(self, '_m_is_masking') else None
                _pos = self._io.pos()
                self._io.seek(0)
                self._raw__m_is_masking = self._io.read_bytes(0)
                _io__raw__m_is_masking = KaitaiStream(BytesIO(self._raw__m_is_masking))
                self._m_is_masking = SmsdLan.EventMaskFromInt(self.is_masking_raw, _io__raw__m_is_masking, self, self._root)
                self._m_is_masking._read()
                self._io.seek(_pos)
                return self._m_is_masking if hasattr(self, '_m_is_masking') else None

        class DecodeFromInt(KaitaiStruct):

            def __init__(self, code, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.code = code

            def _read(self):
                self.raw = self._io.read_u4le()

            @property
            def value(self):
                if hasattr(self, '_m_value'):
                    return self._m_value if hasattr(self, '_m_value') else None
                _pos = self._io.pos()
                self._io.seek(0)
                _on = self.code
                if _on == SmsdLan.Response.Code.speed_max:
                    self._raw__m_value = self._io.read_bytes(0)
                    _io__raw__m_value = KaitaiStream(BytesIO(self._raw__m_value))
                    self._m_value = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit, self._root.limits.speed_max_max_limit, _io__raw__m_value, self, self._root)
                    self._m_value._read()
                elif _on == SmsdLan.Response.Code.speed_min:
                    self._raw__m_value = self._io.read_bytes(0)
                    _io__raw__m_value = KaitaiStream(BytesIO(self._raw__m_value))
                    self._m_value = SmsdLan.SpeedVerifyRange(self.raw, 0, self._root.limits.speed_min_max_limit, _io__raw__m_value, self, self._root)
                    self._m_value._read()
                elif _on == SmsdLan.Response.Code.current_speed:
                    self._raw__m_value = self._io.read_bytes(0)
                    _io__raw__m_value = KaitaiStream(BytesIO(self._raw__m_value))
                    self._m_value = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_value, self, self._root)
                    self._m_value._read()
                elif _on == SmsdLan.Response.Code.instruction_pointer:
                    self._raw__m_value = self._io.read_bytes(0)
                    _io__raw__m_value = KaitaiStream(BytesIO(self._raw__m_value))
                    self._m_value = SmsdLan.InstructionPointer(self.raw, _io__raw__m_value, self, self._root)
                    self._m_value._read()
                else:
                    self._m_value = self._io.read_bytes(0)
                self._io.seek(_pos)
                return self._m_value if hasattr(self, '_m_value') else None

    class EventMaskFromInt(KaitaiStruct):

        def __init__(self, raw, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.raw = raw

        def _read(self):
            pass

        class Bit(KaitaiStruct):

            def __init__(self, idx, raw, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.idx = idx
                self.raw = raw

            def _read(self):
                pass

            @property
            def value(self):
                if hasattr(self, '_m_value'):
                    return self._m_value if hasattr(self, '_m_value') else None
                self._m_value = self.raw >> self.idx & 1 == 1
                return self._m_value if hasattr(self, '_m_value') else None

        @property
        def is_enabled(self):
            if hasattr(self, '_m_is_enabled'):
                return self._m_is_enabled if hasattr(self, '_m_is_enabled') else None
            _pos = self._io.pos()
            self._io.seek(0)
            self._raw__m_is_enabled = [None] * 8
            self._m_is_enabled = [None] * 8
            for i in range(8):
                self._raw__m_is_enabled[i] = self._io.read_bytes(0)
                _io__raw__m_is_enabled = KaitaiStream(BytesIO(self._raw__m_is_enabled[i]))
                _t__m_is_enabled = SmsdLan.EventMaskFromInt.Bit(i, self.raw, _io__raw__m_is_enabled, self, self._root)
                _t__m_is_enabled._read()
                self._m_is_enabled[i] = _t__m_is_enabled
            self._io.seek(_pos)
            return self._m_is_enabled if hasattr(self, '_m_is_enabled') else None

    class PowerstepStatus(KaitaiStruct):

        class AccelerationStatus(IntEnum):
            stop = 0
            accelerates = 1
            decelerates = 2
            constant_speed = 3

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.is_deenergized = self._io.read_bits_int_le(1) != 0
            self.is_ready = self._io.read_bits_int_le(1) != 0
            self.is_sw_on = self._io.read_bits_int_le(1) != 0
            self.has_sw_event_happenned = self._io.read_bits_int_le(1) != 0
            self.is_rotating_direction_forward = self._io.read_bits_int_le(1) != 0
            self.acceleration_status = KaitaiStream.resolve_enum(SmsdLan.PowerstepStatus.AccelerationStatus, self._io.read_bits_int_le(2))
            self.is_command_error = self._io.read_bits_int_le(1) != 0
            self._io.align_to_byte()
            self.reserved = self._io.read_u1()

        def __repr__(self):
            return u'PowerStepStatus<' + (u'Z' if self.is_deenergized else u'⚡') + u', ' + (u'\ud83d\udca4' if self.is_ready else u'⏳') + u', ' + (u'SW on, ' if self.is_sw_on else u'') + (u'\ud83d\udd0a' if self.has_sw_event_happenned else u'\ud83d\udd07') + u', ' + (u'→' if self.is_rotating_direction_forward else u'←') + u', ' + (u'⏹' if self.acceleration_status == SmsdLan.PowerstepStatus.AccelerationStatus.stop else u'⏩' if self.acceleration_status == SmsdLan.PowerstepStatus.AccelerationStatus.accelerates else u'⏪' if self.acceleration_status == SmsdLan.PowerstepStatus.AccelerationStatus.decelerates else u'⏵') + u', ' + (u'\ud83d\uddd9' if self.is_command_error else u'\ud83d\uddf8') + u', ' + (str(self.reserved) if self.reserved != 0 else u'') + u'>'

    class Header(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.checksum = self._io.read_u1()
            self.version = self._io.read_u1()
            self.type = KaitaiStream.resolve_enum(SmsdLan.Type, self._io.read_u1())
            self.id = self._io.read_u1()
            self.len = self._io.read_u2le()
            if not self.len <= 1024:
                raise kaitaistruct.ValidationGreaterThanError(1024, self.len, self._io, u'/types/header/seq/4')

    class InstructionPointer(KaitaiStruct):

        def __init__(self, raw, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.raw = raw

        def _read(self):
            pass

        @property
        def program(self):
            if hasattr(self, '_m_program'):
                return self._m_program if hasattr(self, '_m_program') else None
            self._m_program = self.raw >> 8 & 3
            return self._m_program if hasattr(self, '_m_program') else None

        @property
        def command(self):
            if hasattr(self, '_m_command'):
                return self._m_command if hasattr(self, '_m_command') else None
            self._m_command = self.raw & 255
            return self._m_command if hasattr(self, '_m_command') else None

    class PowerstepCommand(KaitaiStruct):
        """The structure SMSD_CMD_Type is used in data transmission packets.
        """

        class Opcode(IntEnum):
            end = 0
            speed_current_get = 1
            events_status_get = 2
            motor_mode_set = 3
            motor_mode_get = 4
            speed_min_set = 5
            speed_max_set = 6
            acceleration_set = 7
            decelleration_set = 8
            speed_full_step_set = 9
            event_mask_set = 10
            position_absolute_get = 11
            position_microstepping_electrical_get = 12
            status_and_clear_errors_get = 13
            speed_forward = 14
            speed_reverse = 15
            move_steps_forward = 16
            move_steps_reverse = 17
            move_to_position_forward = 18
            move_to_position_reverse = 19
            move_untill_sw_forward = 20
            move_untill_sw_reverse = 21
            move_untill_zero_forward_set_zero = 22
            move_untill_zero_reverse_set_zero = 23
            move_untill_in1_forward_set_label = 24
            move_untill_in1_reverse_set_label = 25
            move_to_recorded_zero = 26
            move_to_recorded_label = 27
            move_to_position = 28
            zero_set = 29
            reset_powerstep01 = 30
            stop_soft_hold = 31
            stop_hard_hold = 32
            stop_soft_deenergize = 33
            stop_hard_deenergize = 34
            sleep = 35
            relay_on = 36
            relay_off = 37
            relay_get = 38
            wait_for_in0 = 39
            wait_for_in1 = 40
            jump = 41
            jump_if_in0 = 42
            jump_if_in1 = 43
            loop = 44
            call = 45
            ret = 46
            program_start_mem0 = 47
            program_start_mem1 = 48
            program_start_mem2 = 49
            program_start_mem3 = 50
            halt = 51
            control_mode_set_en_step_dir = 52
            usb_stop = 53
            speed_min_get = 54
            speed_max_get = 55
            instruction_pointer_get = 56
            jump_if_at_zero = 57
            jump_if_zero = 58
            wait_for_continue = 59
            sleep_interruptible = 60
            move_untill_in1_forward_set_mark = 61
            move_untill_in1_reverse_set_mark = 62

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.raw = self._io.read_u4le()

        class Loop(KaitaiStruct):

            def __init__(self, raw, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.raw = raw

            def _read(self):
                pass

            @property
            def cycles(self):
                if hasattr(self, '_m_cycles'):
                    return self._m_cycles if hasattr(self, '_m_cycles') else None
                self._m_cycles = self.raw >> 10 & (1 << 10) - 1
                return self._m_cycles if hasattr(self, '_m_cycles') else None

            @property
            def commands(self):
                if hasattr(self, '_m_commands'):
                    return self._m_commands if hasattr(self, '_m_commands') else None
                self._m_commands = self.raw & (1 << 10) - 1
                return self._m_commands if hasattr(self, '_m_commands') else None

        class ZeroInt(KaitaiStruct):

            def __init__(self, input, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.input = input

            def _read(self):
                self.hack = self._io.read_bytes(0)
                _ = self.hack
                if not (self.input == 0 and len(_) == 0):
                    raise kaitaistruct.ValidationExprError(self.hack, self._io, u'/types/powerstep_command/types/zero_int/seq/0')

        class Microsteps(KaitaiStruct):

            def __init__(self, raw, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.raw = raw

            def _read(self):
                pass

            @property
            def weird(self):
                if hasattr(self, '_m_weird'):
                    return self._m_weird if hasattr(self, '_m_weird') else None
                self._m_weird = 1 << 21
                return self._m_weird if hasattr(self, '_m_weird') else None

            @property
            def modulus_mask(self):
                if hasattr(self, '_m_modulus_mask'):
                    return self._m_modulus_mask if hasattr(self, '_m_modulus_mask') else None
                self._m_modulus_mask = self.weird - 1
                return self._m_modulus_mask if hasattr(self, '_m_modulus_mask') else None

            @property
            def microsteps(self):
                """The motion commands are always set as microstepping measured displacements."""
                if hasattr(self, '_m_microsteps'):
                    return self._m_microsteps if hasattr(self, '_m_microsteps') else None
                self._m_microsteps = (self.raw & self.modulus_mask) - self.weird if self.raw >= self.weird else self.raw
                return self._m_microsteps if hasattr(self, '_m_microsteps') else None

        class AccelerationVerifyRange(KaitaiStruct):

            def __init__(self, acceleration, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.acceleration = acceleration

            def _read(self):
                self.hack = self._io.read_bytes(0)
                _ = self.hack
                if not (15 <= self.acceleration and self.acceleration <= 59000 and (len(_) == 0)):
                    raise kaitaistruct.ValidationExprError(self.hack, self._io, u'/types/powerstep_command/types/acceleration_verify_range/seq/0')

        class SignalVerifyRange(KaitaiStruct):

            def __init__(self, signal, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.signal = signal

            def _read(self):
                self.hack = self._io.read_bytes(0)
                _ = self.hack
                if not (self.signal <= 7 and len(_) == 0):
                    raise kaitaistruct.ValidationExprError(self.hack, self._io, u'/types/powerstep_command/types/signal_verify_range/seq/0')

        class TimeVerifyRange(KaitaiStruct):

            def __init__(self, time, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.time = time

            def _read(self):
                self.hack = self._io.read_bytes(0)
                _ = self.hack
                if not (self.time <= 3600000 and len(_) == 0):
                    raise kaitaistruct.ValidationExprError(self.hack, self._io, u'/types/powerstep_command/types/time_verify_range/seq/0')

        @property
        def argument_raw(self):
            """Zero if not needed."""
            if hasattr(self, '_m_argument_raw'):
                return self._m_argument_raw if hasattr(self, '_m_argument_raw') else None
            self._m_argument_raw = self.raw >> 10
            return self._m_argument_raw if hasattr(self, '_m_argument_raw') else None

        @property
        def reserved(self):
            if hasattr(self, '_m_reserved'):
                return self._m_reserved if hasattr(self, '_m_reserved') else None
            self._m_reserved = self.raw & 7
            return self._m_reserved if hasattr(self, '_m_reserved') else None

        @property
        def action(self):
            """for internal use, send as 0."""
            if hasattr(self, '_m_action'):
                return self._m_action if hasattr(self, '_m_action') else None
            self._m_action = self.raw >> 3 & 1 == 1
            return self._m_action if hasattr(self, '_m_action') else None

        @property
        def argument(self):
            if hasattr(self, '_m_argument'):
                return self._m_argument if hasattr(self, '_m_argument') else None
            _pos = self._io.pos()
            self._io.seek(0)
            _on = self.operation
            if _on == SmsdLan.PowerstepCommand.Opcode.program_start_mem2:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_steps_forward:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.Microsteps(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.program_start_mem0:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.stop_hard_hold:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.stop_hard_deenergize:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_full_step_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.argument_raw, 15, 15600, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_min_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, 0, self._root.limits.speed_min_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.events_status_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.relay_off:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_in1_reverse_set_mark:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.jump:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.InstructionPointer(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.end:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_forward:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.argument_raw, 15, 15600, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_reverse:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.argument_raw, 15, 15600, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.usb_stop:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_to_position_reverse:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.Microsteps(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_in1_forward_set_mark:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.ret:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.reset_powerstep01:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.loop:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.Loop(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.motor_mode_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.MotorMode(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.stop_soft_hold:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.relay_on:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_in1_reverse_set_label:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.wait_for_in0:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.zero_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_max_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.wait_for_in1:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_sw_reverse:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.SignalVerifyRange(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.relay_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.jump_if_zero:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.InstructionPointer(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.instruction_pointer_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.event_mask_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.EventMaskFromInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_zero_reverse_set_zero:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.acceleration_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.AccelerationVerifyRange(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.call:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.InstructionPointer(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_to_position_forward:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.Microsteps(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_zero_forward_set_zero:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.position_absolute_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_to_recorded_label:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_to_position:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.Microsteps(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.sleep:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.TimeVerifyRange(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.wait_for_continue:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_steps_reverse:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.Microsteps(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_sw_forward:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.SignalVerifyRange(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.program_start_mem3:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.decelleration_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.AccelerationVerifyRange(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.stop_soft_deenergize:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_untill_in1_forward_set_label:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit - 1, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.sleep_interruptible:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.TimeVerifyRange(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.halt:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.jump_if_in0:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.InstructionPointer(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_current_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.program_start_mem1:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.control_mode_set_en_step_dir:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.jump_if_at_zero:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.InstructionPointer(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.position_microstepping_electrical_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.jump_if_in1:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.InstructionPointer(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.status_and_clear_errors_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.motor_mode_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_min_get:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.move_to_recorded_zero:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.PowerstepCommand.ZeroInt(self.argument_raw, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            elif _on == SmsdLan.PowerstepCommand.Opcode.speed_max_set:
                self._raw__m_argument = self._io.read_bytes(0)
                _io__raw__m_argument = KaitaiStream(BytesIO(self._raw__m_argument))
                self._m_argument = SmsdLan.SpeedVerifyRange(self.raw, self._root.limits.speed_max_min_limit, self._root.limits.speed_max_max_limit, _io__raw__m_argument, self, self._root)
                self._m_argument._read()
            else:
                self._m_argument = self._io.read_bytes(0)
            self._io.seek(_pos)
            return self._m_argument if hasattr(self, '_m_argument') else None

        @property
        def operation(self):
            """the executing command code."""
            if hasattr(self, '_m_operation'):
                return self._m_operation if hasattr(self, '_m_operation') else None
            self._m_operation = KaitaiStream.resolve_enum(SmsdLan.PowerstepCommand.Opcode, self.raw >> 4 & 63)
            return self._m_operation if hasattr(self, '_m_operation') else None

    class NetworkConfig(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.mac = SmsdLan.NetworkConfig.MacAddr(self._io, self, self._root)
            self.mac._read()
            self.my_ip = SmsdLan.NetworkConfig.Ipv4(self._io, self, self._root)
            self.my_ip._read()
            self.subnet_mask = SmsdLan.NetworkConfig.Ipv4(self._io, self, self._root)
            self.subnet_mask._read()
            self.gateway = SmsdLan.NetworkConfig.Ipv4(self._io, self, self._root)
            self.gateway._read()
            self.dns = SmsdLan.NetworkConfig.Ipv4(self._io, self, self._root)
            self.dns._read()
            self.port = self._io.read_u2le()
            self.dhcp_mode = self._io.read_u1()

        class MacAddr(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.mac = self._io.read_bytes(6)

        class Ipv4(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.ipv4 = self._io.read_bytes(4)

    @property
    def checksummed_bytes(self):
        if hasattr(self, '_m_checksummed_bytes'):
            return self._m_checksummed_bytes if hasattr(self, '_m_checksummed_bytes') else None
        _pos = self._io.pos()
        self._io.seek(1)
        self._m_checksummed_bytes = self._io.read_bytes(6 - 1 + self.header.len)
        self._io.seek(_pos)
        return self._m_checksummed_bytes if hasattr(self, '_m_checksummed_bytes') else None

    @property
    def recomputed_checksum(self):
        if hasattr(self, '_m_recomputed_checksum'):
            return self._m_recomputed_checksum if hasattr(self, '_m_recomputed_checksum') else None
        _pos = self._io.pos()
        self._io.seek(0)
        self._raw__m_recomputed_checksum = self._io.read_bytes(0)
        _io__raw__m_recomputed_checksum = KaitaiStream(BytesIO(self._raw__m_recomputed_checksum))
        self._m_recomputed_checksum = SmsdLan.SmsdChecksum(self.checksummed_bytes, _io__raw__m_recomputed_checksum, self, self._root)
        self._m_recomputed_checksum._read()
        self._io.seek(_pos)
        return self._m_recomputed_checksum if hasattr(self, '_m_recomputed_checksum') else None