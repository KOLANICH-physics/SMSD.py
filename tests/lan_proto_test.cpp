#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <iostream>
#include <sstream>
#include <string>

#include <fstream>

#include <nameof.hpp>
#include <magic_enum.hpp>

#include "lan_proto_from_pdf.hpp"
#include "lan_proto_undocumented.hpp"


const std::filesystem::path prefix = "./testData/";

template <typename T>
void dumpStructures(T *b, T *e) {
	std::ofstream f;
	uint16_t i = 0;
	for(; b < e; ++b) {
		auto &el = *b;
		auto parentDir = prefix / nameof::nameof_short_type<T>();
		std::filesystem::create_directories(parentDir);
		std::stringstream s;
		s << i << ".dat";
		std::filesystem::path fn = s.str();
		auto fpn = parentDir / fn;
		std::cout << fpn << std::endl;
		f.open(fpn);
		f.write((const char *) &el, sizeof(el));
		f.close();
		++i;
	}
}

void test_powerSTEP_STATUS_TypeDef() {
	powerSTEP_STATUS_TypeDef a[11];
	memset(a, 0, sizeof(a));

	a[0].HiZ = 1;		 // 01 00
	a[1].BUSY = 1;		 // 02 00
	a[2].SW_F = 1;		 // 04 00
	a[3].SW_EVN = 1;	 // 08 00
	a[4].DIR = 1;		 // 10 00
	a[5].MOT_STATUS = 1; // 20 00
	a[6].MOT_STATUS = 2; // 40 00
	a[7].MOT_STATUS = 3; // 60 00
	a[8].CMD_ERROR = 1;	 // 80 00
	a[9].RESERVE = 1;	 // 00 01
	a[10].RESERVE = 0xFF;// 00 ff

	dumpStructures(std::begin(a), std::end(a));
}

void test_COMMANDS_RETURN_DATA_Type() {
	COMMANDS_RETURN_DATA_Type a[3];
	memset(a, 0, sizeof(a));

	a[0].STATUS_POWERSTEP01 = powerSTEP_STATUS_TypeDef {
		.HiZ = 1,
		.BUSY = 1,
		.SW_F = 1,
		.SW_EVN = 1,
		.DIR = 1,
		.MOT_STATUS = 2,
		.CMD_ERROR = 1,
		.RESERVE = 0x77,
	};												  // df 77 00 00 00 00 00
	a[1].ERROR_OR_COMMAND = static_cast<code_t>(0xAB);// 00 00 ab 00 00 00 00
	a[2].RETURN_DATA = 0xFFFFFFFF;					  // 00 00 00 ff ff ff ff

	dumpStructures(std::begin(a), std::end(a));
}

constexpr CMD_PowerSTEP01 speedCommands[]{
	CMD_PowerSTEP01::SET_MIN_SPEED,
	CMD_PowerSTEP01::SET_MAX_SPEED,
	CMD_PowerSTEP01::SET_FS_SPEED,
	CMD_PowerSTEP01::RUN_F,
	CMD_PowerSTEP01::RUN_R,
	CMD_PowerSTEP01::MOVE_F,
	CMD_PowerSTEP01::MOVE_R,
	CMD_PowerSTEP01::SCAN_ZERO_F,
	CMD_PowerSTEP01::SCAN_ZERO_R,
	CMD_PowerSTEP01::SCAN_LABEL_F,
	CMD_PowerSTEP01::SCAN_LABEL_R,
	CMD_PowerSTEP01::SCAN_MARK2_F,
	CMD_PowerSTEP01::SCAN_MARK2_R,
};

constexpr CMD_PowerSTEP01 accelerationCommands[]{
	CMD_PowerSTEP01::SET_ACC,
	CMD_PowerSTEP01::SET_DEC,
};

constexpr CMD_PowerSTEP01 waitCommands[]{
	CMD_PowerSTEP01::SET_WAIT,
	CMD_PowerSTEP01::SET_WAIT_2,
};

constexpr CMD_PowerSTEP01 positionCommands[]{
	CMD_PowerSTEP01::GO_TO_F,
	CMD_PowerSTEP01::GO_TO_R,
	CMD_PowerSTEP01::GO_TO,
};

void testSMSD_CMD_Type() {
	SMSD_CMD_Type a[14];
	memset(a, 0, sizeof(a));

	a[0].RESERVE = 1;								//01 00 00 00
	a[1].RESERVE = 2;								//02 00 00 00
	a[2].RESERVE = 4;								//04 00 00 00
	a[3].ACTION = 1;								//08 00 00 00
	a[4].COMMAND = static_cast<CMD_PowerSTEP01>(1); //10 00 00 00
	a[5].COMMAND = static_cast<CMD_PowerSTEP01>(2); //20 00 00 00
	a[6].COMMAND = static_cast<CMD_PowerSTEP01>(4); //40 00 00 00
	a[7].COMMAND = static_cast<CMD_PowerSTEP01>(8); //80 00 00 00
	a[8].COMMAND = static_cast<CMD_PowerSTEP01>(16);//00 01 00 00
	a[9].COMMAND = static_cast<CMD_PowerSTEP01>(32);//00 02 00 00

	a[10].COMMAND = speedCommands[1];
	a[10].DATA = 0x0000FF;							//60 fc 03 00
	a[11].COMMAND = a[12].COMMAND = a[13].COMMAND = positionCommands[0];
	a[11].DATA = 0x00FF00;							//20 01 fc 03
	a[12].DATA = 0x0F0000;							//00 00 00 3C
	a[13].DATA = 0x300000;							//00 00 00 C0

	dumpStructures(std::begin(a), std::end(a));
}

void testSMSD_LAN_Config_Type() {
	static_assert(sizeof(SMSD_LAN_Config_Type) == 4 * 4 + 6 + 2 + 1);
	SMSD_LAN_Config_Type a[1];
	memset(a, 0, sizeof(a));

	a[0] = defaultLanConfig;
	/*
	00000000  00 f8 dc 3f 00 00 c0 a8  01 02 ff ff 00 00 c0 a8  |...?............|
	00000010  01 01 00 00 00 00 88 13  01                       |.........|
	*/

	dumpStructures(std::begin(a), std::end(a));
}

uint8_t calculateChecksum(LAN_COMMAND_Type_header &h){
	return xor_sum((uint8_t*) &(h.Ver), sizeof(LAN_COMMAND_Type_header) - sizeof(h.XOR_SUM) + h.LENGTH_DATA);
}

void recalculateChecksum(LAN_COMMAND_Type_header &h){
	h.XOR_SUM = calculateChecksum(h);
}

void testLAN_COMMAND_Type_header() {
	LAN_COMMAND_Type_header a[1];
	memset(a, 0, sizeof(a));
	a[0] = LAN_COMMAND_Type_header {
		.XOR_SUM = 0xf3,
		.Ver = 0x02,
		.CMD_TYPE = CODE_CMD::CONFIG_GET,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = 0,
	};
	recalculateChecksum(a[0]);
	//f3 02 0c ff 00 00

	dumpStructures(std::begin(a), std::end(a));
}


void dumpCommands(LAN_COMMAND_Type_header** b, LAN_COMMAND_Type_header** e) {
	std::ofstream f;
	uint16_t i = 0;
	for(; b < e; ++b) {
		auto &el = **b;
		recalculateChecksum(el);

		auto parentDir = prefix / "commands";
		std::filesystem::create_directories(parentDir);
		std::stringstream s;
		
		s << i << "_" << magic_enum::enum_name(el.CMD_TYPE);

		if(el.LENGTH_DATA){
			switch(el.CMD_TYPE){
				case CODE_CMD::RESPONSE:
				{
					auto &r = *reinterpret_cast<LAN_COMMAND_RESPONSE*>(&el);
					s << "_" << magic_enum::enum_name(r.payload.ERROR_OR_COMMAND);
				}
				break;
				case CODE_CMD::POWERSTEP01:
				{
					auto &c = *reinterpret_cast<LAN_COMMAND_POWERSTEP01*>(&el);
					s << "_" << magic_enum::enum_name(c.payload.COMMAND);
				}
				break;
				case CODE_CMD::POWERSTEP01_R_MEM0:
				case CODE_CMD::POWERSTEP01_W_MEM0:
				case CODE_CMD::POWERSTEP01_R_MEM1:
				case CODE_CMD::POWERSTEP01_W_MEM1:
				case CODE_CMD::POWERSTEP01_R_MEM2:
				case CODE_CMD::POWERSTEP01_W_MEM2:
				case CODE_CMD::POWERSTEP01_R_MEM3:
				case CODE_CMD::POWERSTEP01_W_MEM3:
				{
					//auto &c = *reinterpret_cast<LAN_COMMAND_POWERSTEP01_MEM*>(&el);
					s << "_" << el.LENGTH_DATA / sizeof(SMSD_CMD_Type);
				}
				break;
			}
		}

		s << ".dat";
		std::filesystem::path fn = s.str();
		auto fpn = parentDir / fn;
		std::cout << fpn << std::endl;
		f.open(fpn);
		f.write((const char *) &el, sizeof(el) + el.LENGTH_DATA);
		f.close();
		++i;
	}
}

void testLAN_COMMAND_Type() {
	LAN_COMMAND_REQUEST<0> noPass{}; // ff 02 00 ff 00 00

	LAN_COMMAND_REQUEST<8> defaultPass{
		.password{0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF}
	}; // 37 02 00 ff 08 00 01 23  45 67 89 ab cd ef

	LAN_COMMAND_PASSWORD_SET<8> setDefaultPass{
		.password{0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF}
	}; // 2a 02 0d ff 08 00 01 23  45 67 89 ab cd ef

	LAN_COMMAND_RESPONSE resp{
		.payload{
			.STATUS_POWERSTEP01{
				.HiZ = 1,
				.BUSY = 1,
				.SW_F = 1,
				.SW_EVN = 1,
				.DIR = 1,
				.MOT_STATUS = 2,
				.CMD_ERROR = 1,
				.RESERVE = 0x77,
			},
			.ERROR_OR_COMMAND = static_cast<code_t>(0xAB),
			.RETURN_DATA = 0x0
		}
	}; // f6 02 01 ff 07 00 df 77  ab 00 00 00 00

	LAN_COMMAND_POWERSTEP01 moveFInstr{
		.payload{
			.COMMAND = CMD_PowerSTEP01::MOVE_F,
			.DATA = 0x000000,
		}
	}; // f8 02 02 ff 04 00 00 01  00 00

	LAN_COMMAND_POWERSTEP01 getSpeedInstr{
		.payload{
			.COMMAND = CMD_PowerSTEP01::GET_SPEED,
			.DATA = 0x000000
		}
	}; // ea 02 02 ff 04 00 10 fc  03 00

	LAN_COMMAND_RESPONSE resp1{
		.payload{
			.STATUS_POWERSTEP01 = powerSTEP_STATUS_TypeDef {
				.HiZ = 1,
				.BUSY = 1,
				.SW_F = 1,
				.SW_EVN = 1,
				.DIR = 1,
				.MOT_STATUS = 2,
				.CMD_ERROR = 1,
				.RESERVE = 0x00,
			},
			.ERROR_OR_COMMAND = code_t::COMMAND_GET_SPEED,
			.RETURN_DATA = 0x1234,
		}
	}; // c0 02 01 ff 07 00 df 00  12 34 12 00 00

	LAN_COMMAND_POWERSTEP01_W_MEM<1> writeSingle{
		.payload{
			{
				.RESERVE = 1,
				.ACTION = 1,
				.COMMAND = static_cast<CMD_PowerSTEP01>(1),
				.DATA = 0x0000FF,
			}
		},
	}; // e0 02 03 ff 04 00 19 fc  03 00

	LAN_COMMAND_POWERSTEP01_R_MEM<0> readRequest{}; // f8 02 07 ff 00 00


	LAN_COMMAND_POWERSTEP01_R_MEM<1> readResponse{
		.payload{
			{
				.RESERVE = 1,
				.ACTION = 1,
				.COMMAND = static_cast<CMD_PowerSTEP01>(1),
				.DATA = 0x0000FF,
			}
		}
	}; // dc 02 07 ff 04 00 19 fc  03 00

	LAN_COMMAND_CONFIG_SET setLanConfig;
	/*
	00000000  59 02 0b ff 19 00 00 f8  dc 3f 00 00 c0 a8 01 02  |Y........?......|
	00000010  ff ff 00 00 c0 a8 01 01  00 00 00 00 88 13 01     |...............|
	0000001f
	*/
	
	LAN_COMMAND_CONFIG_GET getLanConfig; // f3 02 0c ff 00 00
	LAN_COMMAND_CONFIG_GET_RESPONSE getLanConfigResponse;
	/*00000000  58 02 0c ff 19 00 00 f8  dc 3f 00 00 c0 a8 01 02  |X........?......|
	00000010  ff ff 00 00 c0 a8 01 01  00 00 00 00 88 13 01     |...............|
	0000001f*/

	LAN_COMMAND_ERROR_GET getError; // f1 02 0e ff 00 00

	LAN_COMMAND_ERROR_GET_RESPONSE getErrorResponse;
	/*00000000  ad 02 0e ff 44 00 00 00  00 00 00 00 00 00 00 00  |....D...........|
	00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
	*
	00000040  00 00 00 00 00 00 00 00  00 00                    |..........|
	0000004a*/

	LAN_COMMAND_VersionDataGet getVerData;
	LAN_COMMAND_VersionDataResponse getVerDataResponse{
		.payload{
			Version hardware{
				.major=0x1234,
				.minor=0x5678,
			},
			firmware{
				.major=0xABCD,
				.minor=0xEF01,
			},
		}
	};

	LAN_COMMAND_Type_header* commandsPtrs[]{
		reinterpret_cast<LAN_COMMAND_Type_header*>(&noPass),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&defaultPass),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&setDefaultPass),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&resp),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&moveFInstr),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getSpeedInstr),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&resp1),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&writeSingle),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&readRequest),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&readResponse),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&setLanConfig),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getLanConfig),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getLanConfigResponse),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getError),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getErrorResponse)
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getVerData),
		reinterpret_cast<LAN_COMMAND_Type_header*>(&getVerDataResponse)
	};

	dumpCommands(std::begin(commandsPtrs), std::end(commandsPtrs));
}

template <typename T>
void printSizeof(){
	std::cout << "sizeof(" << nameof::nameof_short_type<T>() << ") " << sizeof(T) << std::endl;
}

voif printSizeofs(){
	printSizeof<powerSTEP_STATUS_TypeDef>();
	printSizeof<COMMANDS_RETURN_DATA_Type>();
	printSizeof<SMSD_CMD_Type>();
	printSizeof<ErrorCounters>();
	printSizeof<SMSD_LAN_Config_Type>();
	printSizeof<LAN_COMMAND_Type_header>();
	printSizeof<LAN_COMMAND_RESPONSE>();
	printSizeof<LAN_COMMAND_POWERSTEP01>();
	printSizeof<LAN_COMMAND_CONFIG_SET>();
	printSizeof<LAN_COMMAND_CONFIG_GET_RESPONSE>();
	printSizeof<LAN_COMMAND_CONFIG_GET>();
	printSizeof<LAN_COMMAND_ERROR_GET>();
	printSizeof<LAN_COMMAND_ERROR_GET_RESPONSE>();
	printSizeof<LAN_COMMAND_VersionDataGet>();
	printSizeof<LAN_COMMAND_VersionDataResponse>();

	printSizeof<LAN_COMMAND_POWERSTEP01_W_MEM<0, 0>>();
	printSizeof<LAN_COMMAND_POWERSTEP01_R_MEM<0, 0>>();
	printSizeof<LAN_COMMAND_PASSWORD_SET<0>>();
	printSizeof<LAN_COMMAND_REQUEST<0>>();


}


int main() {
	printSizeofs();
	testSMSD_CMD_Type();
	test_powerSTEP_STATUS_TypeDef();
	test_COMMANDS_RETURN_DATA_Type();
	testSMSD_LAN_Config_Type();
	testLAN_COMMAND_Type_header();
	testLAN_COMMAND_Type();
	return 0;
}
