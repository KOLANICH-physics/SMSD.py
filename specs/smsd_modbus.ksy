meta:
  id: smsd_modbus
  title: Modbus instruction for Smart Motor Devices BLSD-20Modbus controllers
  endian: le
  bit-endian: le

doc-ref: 
  - https://smd.ee/manuals/BLSD-20Modbus_PS.pdf
  - https://electroprivod.ru/pdf/drivers/BLSD-20Modbus_PS_2020_10_08.pdf

types:
  # the real layout is not clear for me from the docs
  instruction:
    seq:
      - id: raw0
        type: u1
      - id: raw1
        type: u1
      - id: data
        -orig-id: uData
        size: 2
        type:
          switch-on: command
          cases:
            command::register_system_set: register_system
            command::register_modbus_write: register_modbus
            command::delay: delay
            command::jmp: jump(is_relative)
            command::jeq: jump(is_relative)
            command::jneq: jump(is_relative)
            command::jgt: jump(is_relative)
            command::jlt: jump(is_relative)
            command::call: jump(false)
            command::loop: loop

    instances:
      command:
        -orig-id: uCmd
        value: raw0 & 0b1111111
        enum: command
      is_relative:
        -orig-id: bTypeJmp
        value: (raw0 >> 7) & 0b1 == 1
        doc: displacement type for movement commands
      register_address:
        -orig-id: uAdrSysReg
        value: raw1 & 0xF
        doc: address of the system register AX_REG ... FX_REG with numbers 0 ... 5
      register_type:
        -orig-id: uTypeModbusReg
        value: (raw1 >> 4) & 0xF
        doc: type of a Modbus register
        enum: register_type

    enums:
      register_type:
        0: discrete_inputs
        1: coils
        2: inputs
        3: holding_registers
      command:
        0x00:
          id: stop_program
          -orig-id: CMD_STOP_PROGRAM
          doc: |
            stop executing of a user program, without exiting the user program execution mode. At the end of the program execution, all registers and state of the motor remain as they were before the command was executed (the motor continues to rotate if it was rotating before the command was executed). Before the next start of the program, you must send the CMD_FULL_STOP_PROGRAM command.
            Important: when the execution of a user program is stopped by the command CMD_STOP_PROGRAM, the state of the motor and all registers remain the same as they were set during the program. For this reason, if the motor was rotating at the moment the CMD_STOP_PROGRAM command was executed, it will continue executing the last task, i.e. movement will continue when the program has finished. After the program has finished the drive rotation can be stopped by writing a register via Modbus (Coils 2001h or Coils 2002h). To prevent uncontrolled rotation, a motor stop command can be set before the program end command.
        0x01:
          id: register_system_set
          -orig-id: CMD_SET_SYSTEM_REG
          doc: writing to the system register with the uAdrSysReg address, values from the uData data field.
        0x02:
          id: register_modbus_write
          -orig-id: CMD_WRITE_REG_MODBUS
          doc: writing the contents from the uAdrSysReg system register to the ModBUS register space defined by the TypeModbusReg field and its address in the uData field.
        0x03:
          id: read_reg_modbus
          -orig-id: CMD_READ_REG_MODBUS
          doc: reading the content from the ModBUS register space determined by the TypeModbusReg field and its address in the uData field into one of the uAdrSysReg system registers.
        0x04:
          id: delay
          -orig-id: CMD_DELAY
          doc: pause, ms.
        0x05:
          id: jmp
          -orig-id: CMD_JMP
          doc: jump to the address specified in the uData field.
        0x06:
          id: jeq
          -orig-id: CMD_JMP_AX_PARI_BX
          doc: jump to the address specified in the uData field, if the value in the system register AX_REG is equal to the value in BX_REG.
        0x07:
          id: jneq
          -orig-id: CMD_JMP_AX_NOPARI_BX
          doc: jump to the address specified in the uData field if the value in the system register AX_REG is not equal to the value in BX_REG.
        0x08:
          id: jgt
          -orig-id: CMD_JMP_AX_MORE_BX
          doc: jump to the address specified in the uData field, if the value in the system register AX_REG is greater than the value in BX_REG.
        0x09:
          id: jlt
          -orig-id: CMD_JMP_AX_LESS_BX
          doc: jump to the address specified in the uData field, if the value in the system register AX_REG is less than the value in BX_REG.
        0x0A:
          id: call
          -orig-id: CMD_CALL
          doc: call a subroutine starting at the address specified in the uData field.
        0x0B:
          id: ret
          -orig-id: CMD_RETURN
          doc: return from the subroutine.
        0x0C:
          id: loop
          -orig-id: CMD_FOR
          doc: cyclic execution of a sequence of commands.
        0x0D:
          id: full_stop_program
          -orig-id: CMD_FULL_STOP_PROGRAM
          doc: stopping the execution of the user program and exiting the program operation mode. At the end of the program execution, all registers and the state of the motor return to their original values, the motor stops.
    types:
      register_system:
        seq:
          - id: value
            type: u2
      register_modbus:
        seq:
          - id: reg
            type: u2
      delay:
        seq:
          - id: delay
            type: u2
            doc: in milliseconds
            -unit: ms
      jump:
        params:
          - id: is_relative
            type: bool
        seq:
          - id: addr
            type:
              switch-on: is_relative
              cases:
                true: relative
                false: absolute
        types:
          relative:
            seq:
              - id: addr
                type: s2
                valid:
                  min: -1024
                  max: 1024
          absolute:
            seq:
              - id: addr
                type: u2
                valid:
                  min: 0
                  max: 1024
      loop:
        seq:
          - id: repeats
            type: u1
            doc: The least significant byte of the uData field contains the number of repetitions.
          - id: commands
            type: u1
            doc: The high byte of the uData field contains the number of commands located after the CMD_FOR command that will be repeated in a cycle.

  error:
    doc: |
      5023h register of modbus.
      errors that occur during controller operation
    seq:
      - id: voltage_out_of_range
        type: b1
        doc: out of the supply voltage range
      - id: short_circuit_winding
        type: b1
        doc: short circuit of the motor windings
      - id: overheat_brake
        type: b1
        doc: overheating of the brake circuit
      - id: overheat_power
        type: b1
        doc: overheating of the power circuit
      - id: not_connected_hall
        type: b1
        doc: Hall sensors connecting error
      - id: emergency_stop
        type: b1
      - id: overheat_mcu
        type: b1
        doc: MCU overheating
      - id: test_control_program
        type: b1
      - id: runtime
        type: b1
        doc: user program execution error
      - id: io_settings
        type: b1
        doc: error reading or writing settings
      - id: output_analog
        type: b1
        doc: error in the operation of the output transistor switches
      - id: warning_breakpoint
        type: b1
        doc: warning about the impossibility of calculating the breakpoint
      - id: register_out_of_range
        type: b1
        doc: warning about an attempt to write to the register a value that is out of range
      - id: parity
        type: b1
        doc: RS-485 transmitting parity error

