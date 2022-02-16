meta:
  id: smsd_lan
  title: Smart Motor Devices SMSD-4.2LAN and SMSD-8.0LAN protocol v04
  endian: le
  bit-endian: le
  imports:
   - ./smsd_limits
   - ./checksum_simple_additive_u1

doc-ref:
   - https://smd.ee/manuals/smsd-lan-communication-protocol.pdf
   - https://electroprivod.ru/pdf/smsd-4.2lan-communication-protocol.pdf

doc: |
  It is possible to connect to devices either via TCP or via a virtual COM port through USB.
  It is required to transfer data as whole information packets, every packet conforms the structure, described in this manual. Every packet contains only one data transmission command. It is not possible to transfer more than one data transmission command inside one information packet. Every information packet should be continuously transferred, without interruptions. After receiving an information packet, the controller handles it and sends a response, the response is sent the same physical line as the command was received. A sequence of bytes in the information packets is inverted – “little-endian”, (Intel).
  These parameters can be changed afterwards by commands sent through a USB or Ethernet connection.
  RS-232 parameters (USB connection):
  · Baud rate - 115200
  · Data bits - 8
  · Parity – none
  · Stop bits – 1

-orig-id: LAN_COMMAND_Type

params:
  - id: limits
    type: smsd_limits

seq:
  - id: header
    type: header
  - id: check_checksum
    size: 0
    valid:
      expr: _.size == 0 and recomputed_checksum.value == header.checksum
  - id: data
    -orig-id: DATA
    size: header.len
    type:
      switch-on: header.type
      cases:
        type::response: response
        #type::password: bytes
        #type::password_set: bytes
        type::power_step: powerstep_command
        type::powerstem_write_mem_0: powerstep_commands
        type::powerstem_write_mem_1: powerstep_commands
        type::powerstem_write_mem_2: powerstep_commands
        type::powerstem_write_mem_3: powerstep_commands
        type::powerstem_read_mem_0: empty
        type::powerstem_read_mem_1: empty
        type::powerstem_read_mem_2: empty
        type::powerstem_read_mem_3: empty
        type::network_config_set: network_config
        type::network_config_get: empty
        type::error_counters: error_counters
        type::version_data: version_data
    if: header.len
    doc: the data portion of the packet, length of the data portion is LENGTH_DATA bytes.
instances:
  checksummed_bytes:
    pos: header.checksum._sizeof
    size: sizeof<header> - header.checksum._sizeof + header.len
  recomputed_checksum:
    pos: 0
    size: 0
    type: smsd_checksum(checksummed_bytes)

types:
  smsd_checksum:
    params:
      - id: data
        type: bytes
    seq:
      - id: original_checksum
        type: checksum_simple_additive_u1(0xFF, data)
    instances:
      value:
        value: (original_checksum.value ^ 0xFF) & 0xFF
  header:
    seq:
      - id: checksum
        -orig-id: XOR_SUM
        type: u1
      - id: version
        -orig-id: Ver
        type: u1
        doc: |
          communication protocol version.
          The current version of the data communication protocol - 0x02 (applicable for controllers since 19/04/2018).
      - id: type
        -orig-id: CMD_TYPE
        type: u1
        enum: type
        doc: type of the data transmission command
      - id: id
        -orig-id: CMD_IDENTIFICATION
        type: u1
        doc: unique identifier of the data transfer packet. The same identifier is sent inside the response information packet from the controller. The identifier uniquely associates a transferred command and received response.
      - id: len
        -orig-id: LENGTH_DATA
        type: u2
        valid:
          max: 1024
  empty:
    seq:
      - id: must_have_zero_size
        -affected-by: |
          self._unnamed0 = self._io.read_bytes_full()
          _ = self.unnamed_0
        size-eos: true
        valid:
          expr: _.size == 0

  instruction_pointer:
    params:
      - id: raw
        type: u2
    instances:
      program:
        value: (raw >> 8) & 0b11
      command:
        value: raw & 0xFF

  event_mask_from_int:
    params:
      - id: raw
        type: u2
    instances:
      is_enabled:
        pos: 0
        size: 0
        type: bit(_index, raw)
        #value: (raw >> _index) & 1 == 1
        repeat: expr
        repeat-expr: 8
    types:
      bit:
        params:
          - id: idx
            type: u1
          - id: raw
            type: u1
        instances:
          value:
            value: (raw >> idx) & 1 == 1

  speed_verify_range:
    params:
      - id: speed
        type: u2
        doc: always set as full steps per second!
        -unit: full step / second
      - id: min_allowed
        type: u2
        -unit: full step / second
      - id: max_allowed
        type: u2
        -unit: full step / second
    seq:
      - id: hack
        size: 0
        valid:
          expr: min_allowed <= speed and speed <= max_allowed and _.size == 0

  response:
    -orig-id: COMMANDS_RETURN_DATA_Type
    #to-string: |
    #  "PowerStep.Response(" +
    #    powerstep_status.to_s + ", " +
    #    code.to_s + ", " +
    #  ")"
    seq:
      - id: powerstep_status
        -orig-id: STATUS_POWERSTEP01
        type: powerstep_status
      - id: code
        -orig-id: ERROR_OR_COMMAND
        type: u1
        enum: code
      - id: return_data
        -orig-id: RETURN_DATA
        size: 4
        type:
          switch-on: code
          cases:
            code::position_microstepping_electrical: current_electrical_step_microstep
            code::events_status: events_status

            code::speed_min: decode_from_int(code)
            code::speed_max: decode_from_int(code)
            code::speed_current: decode_from_int(code)
            code::instruction_pointer: decode_from_int(code)

    enums:
      code:
        0:
          id: success
          -orig-id: OK
          doc: command accepted without errors
        1:
          id: auth_success
          -orig-id: OK_ACCESS
          doc: correct password
        2:
          id: auth_failure
          -orig-id: ERROR_ACCESS
          doc: incorrect password. You can retry in 1 second.
        3:
          id: rate_limited
          -orig-id: ERROR_ACCESS_TIMEOUT
          doc: to deter bruteforce
        4:
          id: wrong_checksum
          -orig-id: ERROR_XOR
        5:
          id: wrong_command
          -orig-id: ERROR_NO_COMMAND
          doc: the command does not exist
        6:
          id: wrong_length
          -orig-id: ERROR_LEN
          doc: the packet length error
        7:
          id: out_of_range
          -orig-id: ERROR_RANGE
          doc: exceeding values limits
        8:
          id: fail_write
          -orig-id: ERROR_WRITE
          doc: writing error
        9:
          id: fail_read
          -orig-id: ERROR_READ
          doc: reading error
        10:
          id: fail_program
          -orig-id: ERROR_PROGRAMS
          doc: program error
        11:
          id: fail_write_setup
          -orig-id: ERROR_WRITE_SETUP
        12:
          id: no_next
          -orig-id: NO_NEXT
          doc: no next command
        13:
          id: end_programs
          -orig-id: END_PROGRAMS
          doc: end of program
        14:
          id: events_status
          -orig-id: COMMAND_GET_STATUS_IN_EVENT
          -response-to: CMD_PowerSTEP01_STATUS_IN_EVENT
          doc: the field RETURN_DATA contains the bit map of input signals
        15:
          id: mode
          -orig-id: COMMAND_GET_MODE
          -response-to: CMD_PowerSTEP01_GET_MODE
          doc: the field RETURN_DATA contains the bit map of the Controller parameters
        16:
          id: position_absolute
          -orig-id: COMMAND_GET_ABS_POS
          -response-to: CMD_PowerSTEP01_GET_ABS_POS
          doc: the field RETURN_DATA contains the current position of the stepper motor (measured as steps)
        17:
          id: position_microstepping_electrical
          -orig-id: COMMAND_GET_EL_POS
          -response-to: CMD_PowerSTEP01_GET_EL_POS
          doc: the field RETURN_DATA contains the current electrical position of the rotor
        18:
          id: speed_current
          -orig-id: COMMAND_GET_SPEED
          -response-to: CMD_PowerSTEP01_GET_SPEED
          doc: the field RETURN_DATA contains the current motor speed
        19:
          id: speed_min
          -orig-id: COMMAND_GET_MIN_SPEED
          -response-to: CMD_PowerSTEP01_GET_MIN_SPEED
          doc: the field RETURN_DATA contains the current set minimum motor speed
        20:
          id: speed_max
          -orig-id: COMMAND_GET_MAX_SPEED
          -response-to: CMD_PowerSTEP01_GET_MAX_SPEED
          doc: the field RETURN_DATA contains the current set maximum motor speed
        21:
          id: instruction_pointer
          -orig-id: COMMAND_GET_STACK
          -response-to: CMD_PowerSTEP01_GET_STACK
          doc: the field RETURN_DATA contains information about executing program number and command number
        22:
          id: relay_set
          -orig-id: STATUS_RELE_SET
          -response-to:
            - CMD_PowerSTEP01_GET_RELE
            - CMD_PowerSTEP01_SET_RELE
          doc: relay is turned ON
        23:
          id: relay_clear
          -orig-id: STATUS_RELE_CLR
          -response-to:
            - CMD_PowerSTEP01_GET_RELE
            - CMD_PowerSTEP01_CLR_RELE
          doc: relay is turned OFF

    types:
      current_electrical_step_microstep:
        seq:
          - id: raw
            type: u4
        instances:
          full_step:
            value: (raw >> 7) & 0b11
          microstep:
            value: raw & 0b1111111
            -unit: 1/128 full step
            doc: current microstep inside the current full step (measured as 1/128 of the full step)

      events_status:
        seq:
          - id: has_happenned
            type: u1
          - id: is_masking_raw
            type: u1
          - id: is_waiting
            type: u1
        instances:
          is_masking:
            pos: 0
            size: 0
            type: event_mask_from_int(is_masking_raw)

      decode_from_int:
        params:
          - id: code
            type: u1
            enum: code
        seq:
          - id: raw
            type: u4
        instances:
          value:
            pos: 0
            size: 0
            type:
              switch-on: code
              cases:
                code::speed_min: speed_verify_range(raw, 0, _root.limits.speed_min_max_limit)
                code::speed_max: speed_verify_range(raw, _root.limits.speed_max_min_limit, _root.limits.speed_max_max_limit)
                code::current_speed: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit) # feels like bullshit
                code::instruction_pointer: instruction_pointer(raw)

  powerstep_commands:
    seq:
      - id: commands
        type: powerstep_command
        repeat: eos

  network_config:
    -orig-id: SMSD_LAN_Config_Type
    seq:
      - id: mac
        type: mac_addr
      - id: my_ip
        type: ipv4
      - id: subnet_mask
        type: ipv4
        doc: Why not prefix length instead?
      - id: gateway
        type: ipv4
      - id: dns
        type: ipv4
      - id: port
        type: u2
      - id: dhcp_mode
        type: u1
    types:
      mac_addr:
        seq:
          - id: mac
            size: 6
      ipv4:
        seq:
          - id: ipv4
            size: 4

  powerstep_status:
    -orig-id: powerSTEP_STATUS_TypeDef
    to-string: | #↺↻ ↠↞⇔⏯⏸⏴
      "PowerStepStatus<" +
        (is_deenergized ? "Z": "⚡") + ", " +
        (is_ready ? "💤": "⏳") + ", " +
        (is_sw_on ? "SW on, ": "") +
        (has_sw_event_happenned ? "🔊": "🔇") + ", " +
        (is_rotating_direction_forward ? "→": "←") + ", " +
        (acceleration_status == acceleration_status::stop?"⏹":(acceleration_status == acceleration_status::accelerates?"⏩":(acceleration_status == acceleration_status::decelerates?"⏪":"⏵"))) + ", " +
        (is_command_error ? "🗙": "🗸") + ", " +
        (reserved != 0x00 ? reserved.to_s : "") +
      + ">"
    seq:
      - id: is_deenergized
        -orig-id: HiZ 0x01
        type: b1
        doc: whether phases are in Z (disconnected, high-impedance) state
      - id: is_ready
        -orig-id: BUSY 0x02
        type: b1
      - id: is_sw_on
        -orig-id: SW_F 0x04
        type: b1
      - id: has_sw_event_happenned
        -orig-id: SW_EVN 0x08
        type: b1
      - id: is_rotating_direction_forward
        -orig-id: DIR 0x10
        type: b1
        doc: rotation direction
      - id: acceleration_status
        -orig-id: MOT_STATUS 0x20 0x40
        type: b2
        enum: acceleration_status
        doc: motor running state
      - id: is_command_error
        -orig-id: CMD_ERROR 0x80
        type: b1
        doc: command executing error
      - id: reserved
        -orig-id: RESERVE 0xFF
        type: u1
    enums:
      acceleration_status:
        0: stop
        1: accelerates
        2: decelerates
        3: constant_speed

  motor_mode:
    to-string: |
      "MotorMode<" +
        (is_in_current_mode?"A":"V") + ", " +
        "model=" + motor_model.to_i.to_s + ", " +
        "1/" + microstepping_denominator.to_s + ", " +
        (work_current_raw / 10).to_s + " A, " +
        (hold_current_percent).to_s + "%, " +
        program_n.to_s + ", " + 
        (reserved != 0?reserved.to_s:"") +
      ">"
    params:
      - id: raw
        type: u2
    seq:
      - id: hack
        size: 0
        valid:
          expr: |
            1 <= work_current_raw
            and
            work_current_raw <= 80
            and
            _.size == 0
    instances:
      reserved:
        value: raw >> 21
      program_n:
        -orig-id: PROGRAM_N
        value: (raw >> 19) & 0b11
      hold_current_raw:
        -orig-id: STOP_CURRENT
        value: (raw >> 17) & 0b11
      hold_current_percent:
        value: (hold_current_raw + 1) * 25
      hold_current:
        value: hold_current_percent / 100.
        doc: share of an operating current
      work_current_raw:
        -orig-id: WORK_CURRENT
        value: (raw >> 10) & 0b1111111
      work_current:
        value: work_current_raw / 10.
        -unit: Ampere
        doc: operating current for the current control mode.
      microstepping_nlog:
        -orig-id: MICROSTEPPING
        value: (raw >> 7) & 0b111
      microstepping_denominator:
        value: 1 << microstepping_nlog
      motor_model:
        -orig-id: MOTOR_TYPE
        value: (raw >> 1) & 0b111111
        enum: motor_model
        doc: motor type for the voltage control mode. See the table in the docs for the limitation values
      is_in_current_mode:
        -orig-id: CURRENT_OR_VOLTAGE
        value: raw & 0b1 == 1
        doc: |
          motor control mode
          false: voltage
          true: current
    enums:
      motor_model:
        7: sm4247
        25: sm5776
        33: sm8680_parallel
        34: sm8680_serial
        43: sm110201

  powerstep_command:
    -orig-id: SMSD_CMD_Type
    doc: |
      The structure SMSD_CMD_Type is used in data transmission packets.
    seq:
      - id: raw
        type: u4
    instances:
      reserved:
        -orig-id: RESERVE
        value: raw & 0b111
      action:
        -orig-id: ACTION
        value: (raw >> 3) & 0b1 == 1
        doc: for internal use, send as 0
      operation:
        -orig-id: COMMAND
        value: (raw >> 4) & 0b111111
        doc: the executing command code
        enum: opcode
      argument_raw:
        -orig-id: DATA
        value: raw >> 10
        doc: Zero if not needed.
      argument:
        # hack
        pos: 0
        size: 0
        type:
          switch-on: operation
          cases:
            opcode::move_to_recorded_zero: zero_int(argument_raw)
            opcode::move_to_recorded_label: zero_int(argument_raw)
            opcode::zero_set: zero_int(argument_raw)
            opcode::reset_powerstep01: zero_int(argument_raw)
            opcode::stop_soft_hold: zero_int(argument_raw)
            opcode::stop_hard_hold: zero_int(argument_raw)
            opcode::stop_soft_deenergize: zero_int(argument_raw)
            opcode::stop_hard_deenergize: zero_int(argument_raw)
            opcode::relay_on: zero_int(argument_raw)
            opcode::relay_off: zero_int(argument_raw)
            opcode::relay_get: zero_int(argument_raw)
            opcode::ret: zero_int(argument_raw)
            opcode::program_start_mem0: zero_int(argument_raw)
            opcode::program_start_mem1: zero_int(argument_raw)
            opcode::program_start_mem2: zero_int(argument_raw)
            opcode::program_start_mem3: zero_int(argument_raw)
            opcode::halt: zero_int(argument_raw)
            opcode::control_mode_set_en_step_dir: zero_int(argument_raw)
            opcode::usb_stop: zero_int(argument_raw)
            opcode::end: zero_int(argument_raw)
            opcode::wait_for_in0: zero_int(argument_raw)
            opcode::wait_for_in1: zero_int(argument_raw)
            opcode::wait_for_continue: zero_int(argument_raw)
            opcode::status_and_clear_errors_get: zero_int(argument_raw)

            opcode::position_absolute_get: zero_int(argument_raw) # -> current_electrical_step_microstep
            opcode::position_microstepping_electrical_get: zero_int(argument_raw) # -> current_electrical_step_microstep
            opcode::speed_current_get: zero_int(argument_raw) # -> speed_verify_range(argument_raw, 15, 15600)

            opcode::speed_min_set: speed_verify_range(raw, 0, _root.limits.speed_min_max_limit)
            opcode::speed_min_get: zero_int(argument_raw) # -> speed_verify_range(raw, 0, _root.limits.speed_min_max_limit)

            opcode::speed_max_set: speed_verify_range(raw, _root.limits.speed_max_min_limit, _root.limits.speed_max_max_limit)
            opcode::speed_max_get: zero_int(argument_raw) # -> speed_verify_range(raw, _root.limits.speed_max_min_limit, _root.limits.speed_max_max_limit)

            opcode::speed_full_step_set: speed_verify_range(argument_raw, 15, 15600)
            opcode::speed_forward: speed_verify_range(argument_raw, 15, 15600)
            opcode::speed_reverse: speed_verify_range(argument_raw, 15, 15600)

            # the ones for which limits are NOT documented, but we assume they are the same
            opcode::move_untill_zero_forward_set_zero: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit)
            opcode::move_untill_zero_reverse_set_zero: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit)
            opcode::move_untill_in1_forward_set_label: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit)
            opcode::move_untill_in1_reverse_set_label: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit)
            opcode::move_untill_in1_forward_set_mark: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit)
            opcode::move_untill_in1_reverse_set_mark: speed_verify_range(raw, _root.limits.speed_max_min_limit - 1, _root.limits.speed_max_max_limit)

            opcode::sleep: time_verify_range(argument_raw)
            opcode::sleep_interruptible: time_verify_range(argument_raw)

            opcode::acceleration_set: acceleration_verify_range(argument_raw)
            opcode::decelleration_set: acceleration_verify_range(argument_raw)

            # absolute positions
            opcode::move_to_position_forward: microsteps(argument_raw)
            opcode::move_to_position_reverse: microsteps(argument_raw)
            opcode::move_to_position: microsteps(argument_raw)

            # relative positions
            opcode::move_steps_forward: microsteps(argument_raw)
            opcode::move_steps_reverse: microsteps(argument_raw)

            opcode::move_untill_sw_forward: signal_verify_range(argument_raw)
            opcode::move_untill_sw_reverse: signal_verify_range(argument_raw)

            opcode::jump: instruction_pointer(argument_raw)
            opcode::jump_if_in0: instruction_pointer(argument_raw)
            opcode::jump_if_in1: instruction_pointer(argument_raw)
            opcode::call: instruction_pointer(argument_raw)
            opcode::jump_if_at_zero: instruction_pointer(argument_raw)
            opcode::jump_if_zero: instruction_pointer(argument_raw)
            opcode::instruction_pointer_get: zero_int(argument_raw) # -> instruction_pointer(argument_raw)

            opcode::loop: loop(argument_raw)

            opcode::motor_mode_set: motor_mode(argument_raw)
            opcode::motor_mode_get: zero_int(argument_raw) # -> motor_mode

            opcode::events_status_get: zero_int(argument_raw) # -> events_status
            opcode::event_mask_set: event_mask_from_int(argument_raw)

    types:
      zero_int:
        params:
          - id: input
            type: u2
        seq:
          - id: hack
            size: 0
            valid:
              expr: input == 0 and _.size == 0

      time_verify_range:
        params:
          - id: time
            type: u2
            -unit: millisecond
        seq:
          - id: hack
            size: 0
            valid:
              expr: time <= 3600000 and _.size == 0

      signal_verify_range:
        params:
          - id: signal
            type: u2
        seq:
          - id: hack
            size: 0
            valid:
              expr: signal <= 7 and _.size == 0

      acceleration_verify_range:
        params:
          - id: acceleration
            type: u2
            -unit: step/second^2
        seq:
          - id: hack
            size: 0
            valid:
              expr: 15 <= acceleration and acceleration <= 59000 and _.size == 0

      microsteps:
        params:
          - id: raw
            type: u2
        instances:
          weird:
            value: 1 << 21
          modulus_mask:
            value: weird - 1
          microsteps:
            value: 'raw >= weird ? (raw & modulus_mask) - weird : raw'
            -unit: microstep
            doc: The motion commands are always set as microstepping measured displacements.

      loop:
        params:
          - id: raw
            type: u2
        instances:
          cycles:
            value: (raw >> 10) & ((1 << 10) - 1)
          commands:
            value: raw & ((1 << 10) - 1)

    enums:
      opcode:
        0x00:
          id: end
          -orig-id: CMD_PowerSTEP01_END
          doc: marks the end of executing program
        0x01:
          id: speed_current_get
          -orig-id: CMD_PowerSTEP01_GET_SPEED
          doc: |
            reads the current motor speed.
            The important notice: for the correct response the minimum speed should be set to 0 by command `speed_min_set` before sending this command. Otherwise the result could be wrong for low speed movement and stops"
        0x02:
          id: events_status_get
          -orig-id: CMD_PowerSTEP01_STATUS_IN_EVENT
          doc: |
            reads information about current signals inputs state:
              * whether events happenned, 
              * if they are masked
              * if we are waiting for them
        0x03:
          id: motor_mode_set
          -orig-id: CMD_PowerSTEP01_SET_MODE
          doc: |
            sets motor and control parameters:
              * current or voltage
              * motor model (determines motor analog parameters: max. current per phase, resistance per phase, inductance per phase, Step angle)
              * microstepping mode
              * operating current
              * holding current
        0x04:
          id: motor_mode_get
          -orig-id: CMD_PowerSTEP01_GET_MODE
          doc: |
            reads motor control parameters (those ones that are in `motor_mode_set` + number of program, which is available to be started by external signals)
        0x05:
          id: speed_min_set
          -orig-id: CMD_PowerSTEP01_SET_MIN_SPEED
          doc: sets the motor minimum speed in full steps per second.
        0x06:
          id: speed_max_set
          -orig-id: CMD_PowerSTEP01_SET_MAX_SPEED
          doc: |
            sets the motor maximum speed in full steps per second.
        0x07:
          id: acceleration_set
          -orig-id: CMD_PowerSTEP01_SET_ACC
          doc: sets the motor acceleration in full steps/sec^2.
        0x08:
          id: decelleration_set
          -orig-id: CMD_PowerSTEP01_SET_DEC
          doc: sets the motor deceleration in full steps/sec^2.

        0x09:
          id: speed_full_step_set
          -orig-id: CMD_PowerSTEP01_SET_FS_SPEED
          doc: |
            sets the running speed in full steps per second, when the motor switches to a full step mode.
        0x0A:
          id: event_mask_set
          -orig-id: CMD_PowerSTEP01_SET_MASK_EVENT
          doc: masks input signals. Mask is ANDed to the signals.
        0x0B:
          id: position_absolute_get
          -orig-id: CMD_PowerSTEP01_GET_ABS_POS
          doc: reads the current motor position
        0x0C:
          id: position_microstepping_electrical_get
          -orig-id: CMD_PowerSTEP01_GET_EL_POS
          doc: reads the current motor electrical microstepping position
        0x0D:
          id: status_and_clear_errors_get
          -orig-id: CMD_PowerSTEP01_GET_STATUS_AND_CLR
          doc: reads the current state of the controller, and clears all error flags
        0x0E:
          id: speed_forward
          -orig-id: CMD_PowerSTEP01_RUN_F
          doc: starts motor rotation in forward direction at designated speed
        0x0F:
          id: speed_reverse
          -orig-id: CMD_PowerSTEP01_RUN_R
          doc: starts motor rotation in backward direction at designated speed.
        0x10:
          id: move_steps_forward
          -orig-id: CMD_PowerSTEP01_MOVE_F
          doc: |
            starts motor rotation in forward direction for specified displacement, accelerating and decelerating. The motor must be stopped before executing this command (field Mot_Status of the powerSTEP_STATUS_Type structure = 0).
        0x11:
          id: move_steps_reverse
          -orig-id: CMD_PowerSTEP01_MOVE_R
          doc: |
            starts motor rotation in backward direction for specified displacement, accelerating and decelerating. The motor must be stopped before executing this command (field Mot_Status of the powerSTEP_STATUS_Type structure = 0).

        # WTF?! Why do we have 2 commands to move to position?
        0x12:
          id: move_to_position_forward
          -orig-id: CMD_PowerSTEP01_GO_TO_F
          doc: |
            starts motor rotation in forward direction for specified position, accelerating and decelerating. The DATA field should contain the position value.
            .
        0x13:
          id: move_to_position_reverse
          -orig-id: CMD_PowerSTEP01_GO_TO_R
          doc: |
            starts motor rotation in backward direction for specified position, accelerating and decelerating. The DATA field should contain the position value.

        0x14:
          id: move_untill_sw_forward
          -orig-id: CMD_PowerSTEP01_GO_UNTIL_F
          doc: starts motor rotation in forward direction at the maximum speed until receiving a signal at the input SW (taking into account the signal masking, CMD_PowerSTEP01_SET_MASK_EVENT). After that the motor decelerates and stops.
        0x15:
          id: move_untill_sw_reverse
          -orig-id: CMD_PowerSTEP01_GO_UNTIL_R
          doc: starts motor rotation in backward direction at the maximum speed until receiving a signal at the input SW (taking into account the signal masking, CMD_PowerSTEP01_SET_MASK_EVENT). After that the motor decelerates and stops.

        0x16:
          id: move_untill_zero_forward_set_zero
          -orig-id: CMD_PowerSTEP01_SCAN_ZERO_F
          doc: starts motor rotation in forward direction at the set speed in full steps per second until receiving a signal at the input SET_ZERO and remembers that position as ZERO.
        0x17:
          id: move_untill_zero_reverse_set_zero
          -orig-id: CMD_PowerSTEP01_SCAN_ZERO_R
          doc: starts motor rotation in forward direction at the set speed in full steps per second until receiving a signal at the input SET_ZERO and remembers that position as ZERO.

        0x18:
          id: move_untill_in1_forward_set_label
          -orig-id: CMD_PowerSTEP01_SCAN_LABEL_F
          doc: |
            starts motor rotation in forward direction at the set speed in full steps per second until receiving a signal at the input IN1 and remembers that position as LABEL.

        0x19:
          id: move_untill_in1_reverse_set_label
          -orig-id: CMD_PowerSTEP01_SCAN_LABEL_R
          doc: |
            starts motor rotation in backward direction at the set speed in full steps per second until receiving a signal at the input IN1 and remembers that position as LABEL.

        0x1A:
          id: move_to_recorded_zero
          -orig-id: CMD_PowerSTEP01_GO_ZERO
          doc: movement to the ZERO position (remembered using move_untill_zero_*_set_zero)
        0x1B:
          id: move_to_recorded_label
          -orig-id: CMD_PowerSTEP01_GO_LABEL
          doc: movement to the LABEL position (remembered using move_untill_in1_*_set_label)

        0x1C:
          id: move_to_position
          -orig-id: CMD_PowerSTEP01_GO_TO
          doc: shortest movement to the specified position

        0x1D:
          id: zero_set
          -orig-id: CMD_PowerSTEP01_RESET_POS
          doc: sets ZERO position (to clear internal steps counter and specify a current position as a ZERO position)
        0x1E:
          id: reset_powerstep01
          -orig-id: CMD_PowerSTEP01_RESET_POWERSTEP01
          doc: hardware and software reset of the PowerSTEP01 stepper motor control module, but not of the whole Controller.
        0x1F:
          id: stop_soft_hold
          -orig-id: CMD_PowerSTEP01_SOFT_STOP
          doc: smooth decelerating of the stepper motor and stop. After that the motor holds the current position (with preset holding current).
        0x20:
          id: stop_hard_hold
          -orig-id: CMD_PowerSTEP01_HARD_STOP
          doc: sudden stop of the stepper motor and holding the current position (with preset holding current).
        0x21:
          id: stop_soft_deenergize
          -orig-id: CMD_PowerSTEP01_SOFT_HI_Z
          doc: smooth decelerating of the stepper motor and stop. After that the motor phases are deenergized
        0x22:
          id: stop_hard_deenergize
          -orig-id: CMD_PowerSTEP01_HARD_HI_Z
          doc: sudden stop of the stepper motor and deenergizing the stepper motor

        0x23:
          id: sleep
          -orig-id: CMD_PowerSTEP01_SET_WAIT
          doc: sets pause. The DATA field contains the waiting time measured as ms. Allowed value range 0 – 3600000 ms

        0x24:
          id: relay_on
          -orig-id: CMD_PowerSTEP01_SET_RELE
          doc: turn on the controller relay
        0x25:
          id: relay_off
          -orig-id: CMD_PowerSTEP01_CLR_RELE
          doc: turn off the controller relay
        0x26:
          id: relay_get
          -orig-id: CMD_PowerSTEP01_GET_RELE
          doc: read a current state of the controller relay

        0x27:
          id: wait_for_in0
          -orig-id: CMD_PowerSTEP01_WAIT_IN0
          doc: wait until receiving a signal to the input IN0
        0x28:
          id: wait_for_in1
          -orig-id: CMD_PowerSTEP01_WAIT_IN1
          doc: wait until receiving a signal to the input IN1

        0x29:
          id: jump
          -orig-id: CMD_PowerSTEP01_GOTO_PROGRAM
          doc: |
            unconditionally jumps to a specified command number in a specified program number. The DATA field contains the information about a program memory number and a command sequence number: 

        0x2A:
          id: jump_if_in0
          -orig-id: CMD_PowerSTEP01_GOTO_PROGRAM_IF_IN0
          doc: |
            conditionally jumps to a specified command number in a specified program number if there is a signal at the input IN0. The DATA field contains the information about a program memory number and a command sequence number: 
        0x2B:
          id: jump_if_in1
          -orig-id: CMD_PowerSTEP01_GOTO_PROGRAM_IF_IN1
          doc: |
            conditionally jumps to a specified command number in a specified program number if there is a signal at the input IN1. The DATA field contains the information about a program memory number and a command sequence number: 
        0x2C:
          id: loop
          -orig-id: CMD_PowerSTEP01_LOOP_PROGRAM
          doc: |
            loop – the Controller repeats specified times specified number of commands (start from the first command after this command. The DATA field contains the information about commands number and cycles number: bits 0..9 of the DATA field contain the commands number, bits 10..19 of the DATA field contain the cycles number.

        0x2D:
          id: call
          -orig-id: CMD_PowerSTEP01_CALL_PROGRAM
          doc: |
            calls a subprogram. The subprogram is executed until the `ret` and after that returns to the next command of the main program after `call`.
        0x2E:
          id: ret
          -orig-id: CMD_PowerSTEP01_RETURN_PROGRAM
          doc: specifies the end of a subprogram and to return back to the main program.

        0x2F:
          id: program_start_mem0
          -orig-id: CMD_PowerSTEP01_START_PROGRAM_MEM0
          doc: &program_start_mem_doc starts executing a program from the Controller memory area.
        0x30:
          id: program_start_mem1
          -orig-id: CMD_PowerSTEP01_START_PROGRAM_MEM1
          doc: *program_start_mem_doc
        0x31:
          id: program_start_mem2
          -orig-id: CMD_PowerSTEP01_START_PROGRAM_MEM2
          doc: *program_start_mem_doc
        0x32:
          id: program_start_mem3
          -orig-id: CMD_PowerSTEP01_START_PROGRAM_MEM3
          doc: *program_start_mem_doc

        0x33:
          id: halt
          -orig-id: CMD_PowerSTEP01_STOP_PROGRAM_MEM
          doc: stops executing a program

        0x34:
          id: control_mode_set_en_step_dir
          -orig-id: CMD_PowerSTEP01_STEP_CLOCK
          doc: changes the control mode to pulse control using external input signals EN, STEP, DIR.
        0x35:
          id: usb_stop
          -orig-id: CMD_PowerSTEP01_STOP_USB
          doc: stops data transfer via USB interface

        0x36:
          id: speed_min_get
          -orig-id: CMD_PowerSTEP01_GET_MIN_SPEED
          doc: reads the current set minimum motor speed
        0x37:
          id: speed_max_get
          -orig-id: CMD_PowerSTEP01_GET_MAX_SPEED
          doc: reads the current set maximum motor speed
        0x38:
          id: instruction_pointer_get
          -orig-id: CMD_PowerSTEP01_GET_STACK
          doc: reads information about current executing command number and program number from the controller.

        0x39:
          id: jump_if_at_zero
          -orig-id: CMD_PowerSTEP01_GOTO_PROGRAM_IF_ZERO
          doc: |
            conditionally jumps to a specified command number in a specified program number if the current position value is 0. The DATA field contains the information about a program memory number and a command sequence number: 
        0x3A:
          id: jump_if_zero
          -orig-id: CMD_PowerSTEP01_GOTO_PROGRAM_IF_IN_ZERO
          doc: |
            conditionally jumps to a specified command number in a specified program number if there is a signal at the input SET_ZERO. The DATA field contains the information about a program memory number and a command sequence number:  This command is valid for 2d version of communication protocol only.

        0x3B:
          id: wait_for_continue
          -orig-id: CMD_PowerSTEP01_WAIT_CONTINUE
          doc: waits for synchronization signal at the input CONTINUE, which is used for synchronization of executing programs in different controllers. This command is valid for 2d version of communication protocol only.
        0x3C:
          id: sleep_interruptible
          -orig-id: CMD_PowerSTEP01_SET_WAIT_2
          doc: sets a pause. The DATA field contains the waiting time measured as ms. Allowed value range 0 – 3600000 ms. Unlike with the similar command CMD_PowerSTEP01_SET_WAIT, executing of this command can be interrupted by input signals IN0, IN1 or SET_ZERO. This command is valid for 2d version of communication protocol only.
        0x3D:
          id: move_untill_in1_forward_set_mark
          -orig-id: CMD_PowerSTEP01_SCAN_MARK2_F
          doc: |
            starts motor rotation in forward direction at the set speed in full steps per second until receiving a signal at the input IN1 and remembers that position as `Mark`. The motor stops according the deceleration value.
            This command is valid for 2d version of communication protocol only.

        0x3E:
          id: move_untill_in1_reverse_set_mark
          -orig-id: CMD_PowerSTEP01_SCAN_MARK2_R
          doc: |
            starts motor rotation in backward direction at the set speed in full steps per second until receiving a signal at the input IN1 and remembers that position as `Mark`. The motor stops according the deceleration value.
            This command is valid for 2d version of communication protocol only.

  error_counters:
    seq:
      - id: starts
        -orig-id: N_STARTS
        type: u4
        doc: counter of stepper motor phases energizing
      - id: xt
        -orig-id: ERROR_XT
        type: u4
        doc: quantity of internal errors of clock enables
      - id: timeouts
        -orig-id: ERROR_TIME_OUT
        type: u4
        doc: quantity of timeout errors of the main process executing
      - id: chip_powerstep01_init
        -orig-id: ERROR_INIT_POWERSTEP01
        type: u4
        doc: quantity of chip PowerSTEP01 initialization failures
      - id: chip_w5500_init
        -orig-id: ERROR_INIT_WIZNET
        type: u4
        doc: quantity of chip W5500 initialization failures
      - id: fram_init
        -orig-id: ERROR_INIT_FRAM
        type: u4
        doc: quantity of memory chip FRAM initialization failures
      - id: lan
        -orig-id: ERROR_SOCKET
        type: u4
        doc: quantity of LAN connection errors
      - id: fram_exchange
        -orig-id: ERROR_FRAM
        type: u4
        doc: quantity of errors of data exchange with the memory chip FRAM.
      - id: interrupts
        -orig-id: ERROR_INTERRUPT
        type: u4
        doc: quantity of interrupt handling errors
      - id: overcurrents
        -orig-id: ERROR_EXTERN_5V
        type: u4
        doc: quantity of current overloads of the internal 5VDC power source
      - id: overvoltages
        -orig-id: ERROR_EXTERN_VDD
        type: u4
        doc: quantity of exceeding the limits of power supply voltage
      - id: overheatings_chip_powerstep01
        -orig-id: ERROR_THERMAL_POWERSTEP01
        type: u4
        doc: quantity of chip PowerSTEP01 overheatings
      - id: overheatings_brake
        -orig-id: ERROR_THERMAL_BRAKE
        type: u4
        doc: quantity of the brake resistor overheatings
      - id: chip_powerstep01_command_transfer
        -orig-id: ERROR_COMMAND_POWERSTEP01
        type: u4
        doc: quantity of errors during commands transfer to the chip PowerSTEP01
      - id: unkn_uvlo_powerstep
        -orig-id: ERROR_UVLO_POWERSTEP01
        type: u4
        doc: for internal use
      - id: unkn_stall_powerstep
        -orig-id: ERROR_STALL_POWERSTEP01
        type: u4
        doc: for internal use
      - id: program_errors
        -orig-id: ERROR_WORK_PROGRAM
        type: u4
        doc: quantity of program executing errors

  version_data:
    doc: undocumented type. But in the manual for another controller something is found.
    doc-ref: https://smd.ee/manuals/BLSD-20Modbus_PS.pdf 6.8. Identification registers
    seq:
      - id: hardware
        type: version
        doc: |
          major: Driver type
          minor: version
      - id: firmware
        type: version
        doc: |
          major: indentifier
          minor: version
      - id: protocol
        type: u1
    types:
      version:
        to-string: '"Version(" + major.to_s + ", " + minor.to_s + ")"'
        seq:
          - id: major
            type: u2
            -orig-id: HW_MAJOR, FW_MAJOR
          - id: minor
            -orig-id: HW_MINOR, FW_MINOR
            type: u2

enums:
  type:
    0:
      id: password
      -orig-id: CODE_CMD_REQUEST
      doc: |
        authentication (the DATA field of the packet contains authentification information)
        The data transmission command CODE_CMD_REQUEST is used for authorizing purpose. The data transfer packet with CODE_CMD_REQUEST code is sent from the controller to the user as a response to a LAN connection event (only for LAN connection, not used for USB connection).
        After receiving of the packet with CODE_CMD_REQUEST command, the User should send a data transfer packet, which contains authentication password (8 bytes).
        The default password is 0x01 0x23 0x45 0x67 0x89 0xAB 0xCD 0xEF.
        The controller doesn’t check version of the communication protocol (field VER) in this data packet.
        This password can be changed using data transmission command CODE_CMD_PASSWORD_SET.
        The controller checks received password and sends a response, which contains a result. CMD_TYPE of the response is CODE_CMD_RESPONSE, the data field of the response contains COMMANDS_RETURN_DATA structure. Please, learn the COMMANDS_RETURN_DATA structure below in this manual.
    1:
      id: response
      -orig-id: CODE_CMD_RESPONSE
      doc: |
        confirmation (the entry of the DATA field depends on a sent data transmission command)
        The data transfer packet with CODE_CMD_RESPONSE code is sent from the controller to the user as a response to some data transmission commands - CODE_CMD_POWERSTEP01, CODE_CMD_CONFIG_SET, CODE_CMD_ID_SET, CODE_CMD_POWERSTEP01_W_MEM, and in case of errors occur. The data field of the packet contains COMMANDS_RETURN_DATA structure. Please, learn the COMMANDS_RETURN_DATA structure below in this manual.
    2:
      id: power_step
      -orig-id: CODE_CMD_POWERSTEP01
      doc: motor control (the DATA field of the packet contains POWERSTEP01 commands - SMSD_CMD_Type type)
    3:
      id: powerstem_write_mem_0
      -orig-id: CODE_CMD_POWERSTEP01_W_MEM0
      doc: writing of an executing program into the controller memory
    4:
      id: powerstem_write_mem_1
      -orig-id: CODE_CMD_POWERSTEP01_W_MEM1
      doc: writing of an executing program into the controller memory
    5:
      id: powerstem_write_mem_2
      -orig-id: CODE_CMD_POWERSTEP01_W_MEM2
      doc: writing of an executing program into the controller memory
    6:
      id: powerstem_write_mem_3
      -orig-id: CODE_CMD_POWERSTEP01_W_MEM3
      doc: writing of an executing program into the controller memory
    7:
      id: powerstem_read_mem_0
      -orig-id: CODE_CMD_POWERSTEP01_R_MEM0
      doc: reading of an executing program from the controller memory
    8:
      id: powerstem_read_mem_1
      -orig-id: CODE_CMD_POWERSTEP01_R_MEM1
      doc: reading of an executing program from the controller memory
    9:
      id: powerstem_read_mem_2
      -orig-id: CODE_CMD_POWERSTEP01_R_MEM2
      doc: reading o an executing program from the controller memory
    10:
      id: powerstem_read_mem_3
      -orig-id: CODE_CMD_POWERSTEP01_R_MEM3
      doc: reading of an executing program from the controller memory

    11:
      id: network_config_set
      -orig-id: CODE_CMD_CONFIG_SET
      doc: writing of LAN parameters
    12:
      id: network_config_get
      -orig-id: CODE_CMD_CONFIG_GET
      doc: reading of LAN parameters
    13:
      id: password_set
      -orig-id: CODE_CMD_PASSWORD_SET
      doc: changing of authentication password
    14:
      id: error_counters
      -orig-id: CODE_CMD_ERROR_GET
      doc: reading of information about number of operation mode starts and error statistics.

    15:
      id: unknown_15
      doc: if 16 exists, it is likely 15 exists too

    16:
      id: version_data
      doc: |
        Sent by the SMC Program LAN 7.0.7 after authentication
        Seems to be we must respond with version_data
