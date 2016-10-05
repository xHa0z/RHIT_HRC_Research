// CytonTelleOp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "CytonEpsilonRunner.h"
#include <Windows.h>
#include <boost/algorithm/string.hpp>

int main()
{
	CytonEpsilonRunner *runs = new CytonEpsilonRunner();

	std::cout << "Press Enter to Connect to CytonViewer" << std::endl;
	std::cin.ignore();
	if (!runs->connect()) {
		std::cout << "Press Enter to Exit" << std::endl;
		std::cin.ignore();
		return 0;
	}

	bool looping = true;
	std::cout << "Press Escape to disconnect" << std::endl;

	while (looping) {
		std::cout << "Type 'Exit' to stop" << std::endl;
		std::cout << "Type a coordinate to pick up object in format 'x:y:z' in mm" << std::endl;
		std::cout << ">>";
		std::string command1;
		std::cin >> command1;

		std::vector<std::string> strings;
		boost::split(strings, command1, boost::is_any_of(":"));
		
		if (command1 == "Exit") {
			std::cout << "Goodbye" << std::endl;
			break;
		}

		if (strings.size() != 3) {
			std::cout << "ERROR: improper number of inputs" << std::endl;
			continue;
		}
		
		double x, y, z;
		std::istringstream bufferX(strings.at(0));
		std::istringstream bufferY(strings.at(1));
		std::istringstream bufferZ(strings.at(2));

		bufferX >> x;
		bufferY >> y;
		bufferZ >> z;

		x = x / 1000.0;//convert from mm to m
		y = y / 1000.0;
		z = z / 1000.0;

		std::cout << "X: " << x << " Y: " << y << " Z: " << z << std::endl;


		runs->moveGripper(0.01);
		runs->moveTo(x, y, z+0.040);//move to general position
		//Instead move above object, orient gripper, then lower to grab
		runs->grabMode();
		//TODO: actually move to position and grasp object
		runs->moveTo(x, y, z);
		runs->moveGripper(0.007);
		//TODO: decide what to do with object after grabbing
		runs->moveTo(0.3,0,0.1);
		runs->moveGripper(0.01);

	}
	runs->shutdown();

	std::cout << "Press Enter to Exit Program" << std::endl;
	std::cin.ignore();

	return 0;
}

