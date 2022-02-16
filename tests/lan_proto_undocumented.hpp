#pragma once

#include <cstdint>

#include "lan_proto_from_pdf.hpp"


struct [[gnu::packed]] VersionData{
	struct [[gnu::packed]] Version{
		uint16_t major = 0;
		uint16_t minor = 0;
	};

	Version hardware;
	Version firmware;
	uint8_t protocol = CURRENT_PROTOCOL_VERSION;
};

struct [[gnu::packed]] LAN_COMMAND_VersionDataGet{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::VersionData,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = 0,
	};
};

struct [[gnu::packed]] LAN_COMMAND_VersionDataResponse{
	LAN_COMMAND_Type_header header{
		.CMD_TYPE = CODE_CMD::VersionData,
		.CMD_IDENTIFICATION = 0xFF,
		.LENGTH_DATA = sizeof(VersionData),
	};
	VersionData payload;
};
