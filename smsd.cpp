#include "../ctre.hpp"
#include <iostream>

auto matcher = ctre::match<"^(LD)(\\d+)$">;

void parseCommand(std::string cmdStr){
	auto [whole, command, num] = matcher(cmdStr);
	/*Serial.print("whole ");
	Serial.println(whole.data());
	Serial.print("command ");
	Serial.println(command.data());
	Serial.print("num ");
	Serial.println(num.data());*/
	std::cout << "whole " << whole << " command " << command << " num " << num.data() << std::endl;
}

int main(){
	parseCommand("LD1");
}
