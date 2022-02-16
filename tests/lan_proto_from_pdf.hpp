#pragma once

#include <cstdint>

constexpr uint8_t xor_sum(uint8_t *data, uint16_t length) {
	uint8_t xor_temp = 0xFF;
	while(length--) {
		xor_temp += *data;
		data++;
	}
	return (xor_temp ^ 0xFF);
}


// modbus
enum class register_type_t : uint8_t {
	DISCRETE_INPUTS = 0,
	COILS = 1,
	INPUTS = 2,
	HOLDING_REGISTERS = 3
};

enum class command_t : uint8_t {
	STOP_PROGRAM = 0,
	REGISTER_SYSTEM_SET = 1,
	REGISTER_MODBUS_WRITE = 2,
	READ_REG_MODBUS = 3,
	DELAY = 4,
	JMP = 5,
	JEQ = 6,
	JNEQ = 7,
	JGT = 8,
	JLT = 9,
	CALL = 10,
	RETURN = 11,
	LOOP = 12,
	FULL_STOP_PROGRAM = 13
};

//lan

enum class CODE_CMD : uint8_t{
	REQUEST,
	RESPONSE,
	POWERSTEP01,
	POWERSTEP01_W_MEM0,
	POWERSTEP01_W_MEM1,
	POWERSTEP01_W_MEM2,
	POWERSTEP01_W_MEM3,
	POWERSTEP01_R_MEM0,
	POWERSTEP01_R_MEM1,
	POWERSTEP01_R_MEM2,
	POWERSTEP01_R_MEM3,
	CONFIG_SET,
	CONFIG_GET,
	PASSWORD_SET,
	ERROR_GET,

	// Undocumented codes:
	Unknown15 = 15,
	VersionData = 16,
};

enum class CMD_PowerSTEP01 : uint32_t{
	END = 0x00,
	GET_SPEED = 0x01,
	STATUS_IN_EVENT = 0x02,
	SET_MODE = 0x03,
	GET_MODE = 0x04,
	SET_MIN_SPEED = 0x05,
	SET_MAX_SPEED = 0x06,
	SET_ACC = 0x07,
	SET_DEC = 0x08,
	SET_FS_SPEED = 0x09,
	SET_MASK_EVENT = 0x0A,
	GET_ABS_POS = 0x0B,
	GET_EL_POS = 0x0C,
	GET_STATUS_AND_CLR = 0x0D,
	RUN_F = 0x0E,
	RUN_R = 0x0F,
	MOVE_F = 0x10,
	MOVE_R = 0x11,
	GO_TO_F = 0x12,
	GO_TO_R = 0x13,
	GO_UNTIL_F = 0x14,
	GO_UNTIL_R = 0x15,
	SCAN_ZERO_F = 0x16,
	SCAN_ZERO_R = 0x17,
	SCAN_LABEL_F = 0x18,
	SCAN_LABEL_R = 0x19,
	GO_ZERO = 0x1A,
	GO_LABEL = 0x1B,
	GO_TO = 0x1C,
	RESET_POS = 0x1D,
	RESET_POWERSTEP01 = 0x1E,
	SOFT_STOP = 0x1F,
	HARD_STOP = 0x20,
	SOFT_HI_Z = 0x21,
	HARD_HI_Z = 0x22,
	SET_WAIT = 0x23,
	SET_RELE = 0x24,
	CLR_RELE = 0x25,
	GET_RELE = 0x26,
	WAIT_IN0 = 0x27,
	WAIT_IN1 = 0x28,
	GOTO_PROGRAM = 0x29,
	GOTO_PROGRAM_IF_IN0 = 0x2A,
	GOTO_PROGRAM_IF_IN1 = 0x2B,
	LOOP_PROGRAM = 0x2C,
	CALL_PROGRAM = 0x2D,
	RETURN_PROGRAM = 0x2E,
	START_PROGRAM_MEM0 = 0x2F,
	START_PROGRAM_MEM1 = 0x30,
	START_PROGRAM_MEM2 = 0x31,
	START_PROGRAM_MEM3 = 0x32,
	STOP_PROGRAM_MEM = 0x33,
	STEP_CLOCK = 0x34,
	STOP_USB = 0x35,
	GET_MIN_SPEED = 0x36,
	GET_MAX_SPEED = 0x37,
	GET_STACK = 0x38,
	GOTO_PROGRAM_IF_ZERO = 0x39,
	GOTO_PROGRAM_IF_IN_ZERO = 0x3A,
	WAIT_CONTINUE = 0x3B,
	SET_WAIT_2 = 0x3C,
	SCAN_MARK2_F = 0x3D,
	SCAN_MARK2_R = 0x3E,
	
	UNKNOWN = 0x3F,
};

enum class code_t : uint8_t{
	OK, //< command accepted without errors
	OK_ACCESS, //< successful authentication (the User has got access to the Controller control)
	ERROR_ACCESS, //< authentication error (the User has not got access to the Controller control)
	ERROR_ACCESS_TIMEOUT, //< authentication timeout is not elapsed (authentication timeout is 1 sec)
	ERROR_XOR, //< checksum error
	ERROR_NO_COMMAND, //< the command does not exist
	ERROR_LEN, //< the packet length error
	ERROR_RANGE, //< exceeding values limits
	ERROR_WRITE, //< writing error
	ERROR_READ, //< reading error
	ERROR_PROGRAMS, //< program error
	ERROR_WRITE_SETUP,
	NO_NEXT, //< no next command
	END_PROGRAMS, //< end of program
	COMMAND_GET_STATUS_IN_EVENT, //< the field RETURN_DATA contains the bit map of input signals
	COMMAND_GET_MODE, //< the field RETURN_DATA contains the bit map of the Controller parameters
	COMMAND_GET_ABS_POS, //< the field RETURN_DATA contains the current position of the stepper motor (measured as steps)
	COMMAND_GET_EL_POS, //< the field RETURN_DATA contains the current electrical position of the rotor
	COMMAND_GET_SPEED, //< the field RETURN_DATA contains the current motor speed
	COMMAND_GET_MIN_SPEED, //< the field RETURN_DATA contains the current set minimum motor speed
	COMMAND_GET_MAX_SPEED, //< the field RETURN_DATA contains the current set maximum motor speed
	COMMAND_GET_STACK, //< the field RETURN_DATA contains information about executing program number and command number
	STATUS_RELE_SET, //< relay is turned ON
	STATUS_RELE_CLR, //< relay is turned OFF
};

struct [[gnu::packed]] powerSTEP_STATUS_TypeDef {
	bool HiZ : 1 = false;
	bool BUSY : 1 = false;
	bool SW_F : 1 = false;
	bool SW_EVN : 1 = false;
	bool DIR : 1 = false;
	uint8_t MOT_STATUS : 2 = false;
	bool CMD_ERROR : 1 = false;
	uint8_t RESERVE : 8;
};

struct [[gnu::packed]] COMMANDS_RETURN_DATA_Type {
	powerSTEP_STATUS_TypeDef STATUS_POWERSTEP01;
	code_t ERROR_OR_COMMAND;
	uint32_t RETURN_DATA = 0;
};

struct [[gnu::packed]] SMSD_CMD_Type {
	uint8_t RESERVE : 3 = 0;
	bool ACTION : 1 = 0;
	CMD_PowerSTEP01 COMMAND : 6 = CMD_PowerSTEP01::UNKNOWN;
	uint32_t DATA : 22 = 0;
};

struct [[gnu::packed]] ErrorCounters {
	uint32_t
	N_STARTS=0, //< counter of stepper motor phases energizing
	ERROR_XT=0, //< quantity of internal errors of clock enables
	ERROR_TIME_OUT=0, //< quantity of timeout errors of the main process executing
	ERROR_INIT_POWERSTEP01=0, //<quantity of chip PowerSTEP01 initialization failures
	ERROR_INIT_WIZNET=0, //< quantity of chip W5500 initialization failures
	ERROR_INIT_FRAM=0, //<quantity of memory chip FRAM initialization failures
	ERROR_SOCKET=0, //<quantity of LAN connection errors
	ERROR_FRAM=0, //<quantity of errors of data exchange with the memory chip FRAM.
	ERROR_INTERRUPT=0, //quantity of interrupt handling errors
	ERROR_EXTERN_5V=0, //< quantity of current overloads of the internal 5VDC power source
	ERROR_EXTERN_VDD=0, //< quantity of exceeding the limits of power supply voltage
	ERROR_THERMAL_POWERSTEP01=0, //< quantity of chip PowerSTEP01 overheatings
	ERROR_THERMAL_BRAKE=0, //< quantity of the brake resistor overheatings
	ERROR_COMMAND_POWERSTEP01=0, //< quantity of errors during commands transfer to the chip PowerSTEP01
	ERROR_UVLO_POWERSTEP01=0, //< for internal use
	ERROR_STALL_POWERSTEP01=0, //< for internal use
	ERROR_WORK_PROGRAM=0 //<quantity of program executing errors
	;
};

struct [[gnu::packed]] SMSD_LAN_Config_Type{
	enum dhcp_mode: uint8_t{
		unkn = 1
	};

	struct [[gnu::packed]] MAC{
		uint8_t mac[6];
	};

	struct [[gnu::packed]] IPv4{
		uint8_t ipv4[4];
	};

	MAC mac;
	IPv4 ip;
	IPv4 sn;
	IPv4 gw;
	IPv4 dns;
	uint16_t Port;
	dhcp_mode dhcp;
};

constexpr SMSD_LAN_Config_Type defaultLanConfig{
	.mac = {0x00, 0xf8, 0xdc, 0x3f, 0x00, 0x00},
	.ip = {192, 168, 1, 2},
	.sn = {255, 255, 0, 0},
	.gw = {192, 168, 1, 1},
	.dns = {0, 0, 0, 0},
	.Port = 5000,
	.dhcp = static_cast<SMSD_LAN_Config_Type::dhcp_mode>(1),
};

constexpr uint8_t CURRENT_PROTOCOL_VERSION = 0x02;

struct [[gnu::packed]] LAN_COMMAND_Type_header {
	uint8_t XOR_SUM = 0;
	uint8_t Ver = CURRENT_PROTOCOL_VERSION;
	CODE_CMD CMD_TYPE;
	uint8_t CMD_IDENTIFICATION = 0x00;
	uint16_t LENGTH_DATA = 0x00;
};

template <uint8_t passwordLength, CODE_CMD type>
struct [[gnu::packed]] LAN_COMMAND_Password{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = type,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = passwordLength,
	};
	uint8_t password[passwordLength];
};

template <uint8_t passwordLength>
using LAN_COMMAND_REQUEST = LAN_COMMAND_Password<passwordLength, CODE_CMD::REQUEST>;

template <uint8_t passwordLength>
using LAN_COMMAND_PASSWORD_SET = LAN_COMMAND_Password<passwordLength, CODE_CMD::PASSWORD_SET>;

struct [[gnu::packed]] LAN_COMMAND_RESPONSE{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::RESPONSE,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = sizeof(COMMANDS_RETURN_DATA_Type),
	};
	COMMANDS_RETURN_DATA_Type payload;
};

struct [[gnu::packed]] LAN_COMMAND_POWERSTEP01{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::POWERSTEP01,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = sizeof(SMSD_CMD_Type),
	};
	SMSD_CMD_Type payload;
};

template <uint8_t count_of_commands, CODE_CMD type>
struct [[gnu::packed]] LAN_COMMAND_POWERSTEP01_MEM{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = type,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = sizeof(SMSD_CMD_Type) * count_of_commands,
	};
	SMSD_CMD_Type payload[count_of_commands];
};

template <uint8_t count_of_commands, uint8_t mem=0>
using LAN_COMMAND_POWERSTEP01_R_MEM = LAN_COMMAND_POWERSTEP01_MEM<count_of_commands, static_cast<CODE_CMD>(static_cast<uint8_t>(CODE_CMD::POWERSTEP01_R_MEM0) + mem)>;

template <uint8_t count_of_commands, uint8_t mem=0>
using LAN_COMMAND_POWERSTEP01_W_MEM = LAN_COMMAND_POWERSTEP01_MEM<count_of_commands, static_cast<CODE_CMD>(static_cast<uint8_t>(CODE_CMD::POWERSTEP01_W_MEM0) + mem)>;

template <CODE_CMD type>
struct [[gnu::packed]] LAN_COMMAND_Config{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = type,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = sizeof(SMSD_LAN_Config_Type),
	};
	SMSD_LAN_Config_Type payload = defaultLanConfig;
};

using LAN_COMMAND_CONFIG_SET = LAN_COMMAND_Config<CODE_CMD::CONFIG_SET>;
using LAN_COMMAND_CONFIG_GET_RESPONSE = LAN_COMMAND_Config<CODE_CMD::CONFIG_GET>;

struct [[gnu::packed]] LAN_COMMAND_CONFIG_GET{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::CONFIG_GET,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = 0,
	};
};

struct [[gnu::packed]] LAN_COMMAND_ERROR_GET{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::ERROR_GET,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = 0,
	};
};

struct [[gnu::packed]] LAN_COMMAND_ERROR_GET_RESPONSE{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::ERROR_GET,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = sizeof(ErrorCounters),
	};
	ErrorCounters errorCounters;
};

