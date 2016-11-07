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
		//std::cout << "Type a coordinate to pick up object in format 'x:y:z' in mm" << std::endl;

		//Lecea's code below
		std::cout << "Type a block to pick up" << std::endl;
		//no more Lecea

		std::cout << ">>";
		std::string command1;
		std::cin >> command1;

		std::vector<std::string> strings;
		boost::split(strings, command1, boost::is_any_of(":"));
		
		if (command1 == "Exit") {
			std::cout << "Goodbye" << std::endl;
			break;
		}

		//COMMENT OUT EVERYTHING BELOW
		//if (strings.size() != 3) {
		//	std::cout << "ERROR: improper number of inputs" << std::endl;
		//	continue;
		//}
		//double x, y, z;
		//std::istringstream bufferX(strings.at(0));
		//std::istringstream bufferY(strings.at(1));
		//std::istringstream bufferZ(strings.at(2));
		//bufferX >> x;
		//bufferY >> y;
		//bufferZ >> z;
		//x = x / 1000.0;//convert from mm to m
		//y = y / 1000.0;
		//z = z / 1000.0;
		//std::cout << "X: " << x << " Y: " << y << " Z: " << z << std::endl;
		//runs->moveGripper(0.01);
		//runs->moveTo(x, y, z);//move to general position
		//Instead move above object, orient gripper, then lower to grab
		//runs->grabMode();
		//TODO: actually move to position and grasp object
		//runs->moveTo(x, y+0.040, z);
		//runs->moveTo(x, y, z);
		//runs->moveGripper(0.002);
		//runs->moveTo(0.3,0.3,0.2);
		//runs->moveGripper(0.01);
		//END OF COMMENTING

		if (command1 == "1") {
			std::cout << "***Going to block 1" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0, 0.4-0.04, 0.4,1);
			runs->moveTo(0, 0.4, 0.4,1);
			runs->moveGripper(0.002);
			runs->moveTo(0, 0.4 - 0.04, 0.4, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "2") {
			std::cout << "***Going to block 2" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.1, 0.4-0.04, 0.4, 1);
			runs->moveTo(0.1, 0.4, 0.4);
			runs->moveGripper(0.002);
			runs->moveTo(0.1, 0.4 - 0.04, 0.4, 1);
		
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "3") {
			std::cout << "***Going to block 3" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.2, 0.4-0.04, 0.4, 1);
			runs->moveTo(0.2, 0.4, 0.4, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.2, 0.4 - 0.04, 0.4, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "4") {
			std::cout << "***Going to block 4" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.25, 0.4-0.04, 0.4, 1);
			runs->moveTo(0.25, 0.4, 0.4, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.25, 0.4 - 0.04, 0.4, 1);
		
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		
		else if (command1 == "5") {
			std::cout << "***Going to block 5" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0, 0.4-0.04, 0.3, 1);
			runs->moveTo(0, 0.4, 0.22, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0, 0.4 - 0.04, 0.3, 1);	

			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "6") {
			std::cout << "***Going to block 6" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.1, 0.4-0.04, 0.3, 1);
			runs->moveTo(0.1, 0.4, 0.3, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.1, 0.4 - 0.04, 0.3, 1);
			
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "7") {
			std::cout << "***Going to block 6" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.2, 0.4-0.04, 0.3, 1);
			runs->moveTo(0.2, 0.4, 0.3, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.2, 0.4 - 0.04, 0.3, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
		    runs->moveGripper(0.01);
		}
		else if (command1 == "8") {
			std::cout << "***Going to block 8" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.3, 0.4-0.04, 0.3, 1);
			runs->moveTo(0.3, 0.4, 0.3, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.3, 0.4 - 0.04, 0.3, 1);
			
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "9") {
			std::cout << "***Going to block 9" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(0, 0.4, 0.14, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "10") {
			std::cout << "***Going to block 10" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.1, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(0.1, 0.4, 0.14, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.1, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "11") {
			std::cout << "***Going to block 11" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.2, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(0.2, 0.4, 0.14, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.2, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "12") {
			std::cout << "***Going to block 12" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.3, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(0.3, 0.4, 0.14, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.3, 0.4 - 0.04, 0.14, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "13") {
			std::cout << "***Going to block 13" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(0, 0.4, 0.06, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "14") {
			std::cout << "***Going to block 14" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.1, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(0.1, 0.4, 0.06, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.1, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "15") {
			std::cout << "***Going to block 13" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.2, 0.4 - 0.04, 0.06, 0);
			runs->moveTo(0.2, 0.4, 0.06, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.2, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else if (command1 == "16") {
			std::cout << "***Going to block 16" << std::endl;
			runs->moveGripper(0.01);
			runs->moveTo(0.3, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(0.3, 0.4, 0.1, 1);
			runs->moveGripper(0.002);
			runs->moveTo(0.3, 0.4 - 0.04, 0.06, 1);
			runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.01);
		}
		else  {
			std::cout << "WRONG!!!" << std::endl;
		
		}
	}
	runs->shutdown();

	std::cout << "Press Enter to Exit Program" << std::endl;
	std::cin.ignore();

	return 0;
}

