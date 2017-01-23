// CytonTelleOp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "CytonEpsilonRunner.h"
#include <Windows.h>
#include <boost/algorithm/string.hpp>

//file reading includes
#include <iostream>
#include <fstream>
#include <string>
//#include <foundCore/ecApplication.h>
//#include <foundCore/ecMacros.h>
#include <foundCommon/ecCoordSysXForm.h>

#include <boost/assign/list_of.hpp>
#include <boost/filesystem.hpp>
#include <boost/program_options/options_description.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/variables_map.hpp>
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

	std::cout << "Run in debug mode? y/n" << std::endl;
	char temp = std::cin.get();
	bool debugMode = false;
	if (temp == 'n') {
		debugMode = false;
	}
	else if (temp == 'y') {
		debugMode = true;
	}
	else {
		std::cout << "command not recognized, defaulting to normal mode" << std::endl;
	}
	std::cout << "hi" << std::endl;

	bool looping = true;
	std::cout << "Press Escape to disconnect" << std::endl;

	while (looping) {
		std::string command1;
		if (debugMode) {
			std::cout << "Type 'Exit' to stop" << std::endl;
			//std::cout << "Type a coordinate to pick up object in format 'x:y:z' in mm" << std::endl;

			//Lecea's code below
			std::cout << "Type a block to pick up" << std::endl;
			//no more Lecea

			std::cout << ">>";
			std::cin >> command1;

			std::vector<std::string> strings;
			boost::split(strings, command1, boost::is_any_of(":"));

		}
		else {
			std::ifstream myInFile;
			myInFile.open("test.txt");

			std::getline(myInFile, command1);
			myInFile.close();
		}
		
		if (command1 == "Exit") {
			std::cout << "Goodbye" << std::endl;
			break;
		}

		if (command1 == "" || command1 == "DONE" || command1 == "WORKING") {
			//do nothing
			continue;
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

		else if (command1 == "1") {
			std::cout << "***Going to block 1" << std::endl;
			//runs->moveGripper(0.01);
			//runs->moveTo(0, 0.4-0.04, 0.4,1);
			//runs->moveTo(0, 0.4, 0.4,1);
			//runs->moveGripper(0.002);
			//runs->moveTo(0, 0.4 - 0.04, 0.4, 1);
			//runs->moveTo(-0.1, 0.3, 0.15);
			runs->moveGripper(0.010);
			runs -> goToJointHome(-0.436144,0.103779,1.497224,-1.509429,0.145293,0.430562,1.328925);
			runs-> goToJointHome(-0.608486,-0.034184,1.363483,-1.263482,0.124052,0.392361,1.328925);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.536157, 0.319435, 1.463605, -1.470364, 0.370870, 0.470375, 1.324251);
			runs->goToJointHome(-0.004435,0.180997,1.210828,-1.343153,1.22991,-0.309694,1.724626);
			runs->moveGripper(0.010);

			



		}
		else if (command1 == "2") {
			std::cout << "***Going to block 2" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-0.951140, -0.000458, 0.922159, -1.368966, 0.787627, 0.595992, 0.797665);
			runs->goToJointHome(-0.864756, -0.158007, 0.923604, -1.245293, 0.593964, 0.496533, 0.835978);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.985745, 0.190394, 1.126053, -1.525368, 0.864976, 0.822488, 0.915433);
			runs->goToJointHome(-1.031035, -0.0497, 0.365213, -1.2345, 1.425788, -0.4683, 0.528178);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "3") {
			std::cout << "***Going to block 3" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-1.096092,0.000291,0.963400,-1.357477,0.713974,0.547328,0.810284);
			runs->goToJointHome(-1.036027, -0.188038, 0.967827, -1.187935, 0.515767, 0.429763, 0.840993);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.384326, 0.196094, 0.831783, -1.392970, 1.144997, 0.601747, 0.653090);
			runs->goToJointHome(-1.031035,-0.0215,0.431566,-1.232923,1.425788,-0.865725,0.531781);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "4") {
			std::cout << "***Going to block 4" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-1.173, -0.476, -0.0234, -1.2116, 1.4334, -0.1932, -0.09938);
			runs->goToJointHome(-1.099480, -0.516700, 0.218541, -1.325465, 1.026560, 0.302881, -0.169663);
			runs->goToJointHome(-0.996461,-0.627262,0.212854,-1.161756,0.892117,0.327777,-0.169663);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.099480, -0.516700, 0.218541, -1.325465, 1.026560, 0.302881, -0.169663);
			runs->goToJointHome(-1.524971,-0.347380,0.272449,-1.453503,1.438154,-0.507657,-0.241518);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		
		else if (command1 == "5") {
			std::cout << "***Going to block 5" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-0.193898,-0.345596,1.733568,-1.8147,-0.329878,0.492749,1.747917);
			runs->goToJointHome(-0.304173,-0.338805,1.586819,-1.618073,-0.256283,0.448194,1.521256);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.180899,-0.074373,1.644651,-1.856905,-0.006224,0.570831,1.582260);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "6") {
			std::cout << "***Going to block 6" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-0.389703,-0.096549,1.673022,-1.694086,0.078940,0.268315,1.524653);
			runs->goToJointHome(-0.557076,-0.223317,1.499618,-1.510136,0.004991,0.364868,1.320658);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.457330,0.406464,1.648365,-1.700486,0.612650,0.505513,1.391287);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
			
		}
		else if (command1 == "7") {
			std::cout << "***Going to block 6" << std::endl;
			runs->goToJointHome(-0.885164,-0.018224,1.469991,-1.484022,0.323858,0.555646,1.230244);
			runs->goToJointHome(-0.969105,-0.168469,1.421369,-1.265781,0.223863,0.421013,1.176900);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.953720,0.242870,1.472074,-1.489307,0.582989,0.612867,1.240220);
			//this one needs to check
			//runs->goToJointHome(-1.084107,0.184478,0.779407,-1.557055,1.564801,0,0.594135);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "8") {
			std::cout << "***Going to block 8" << std::endl;
			runs->goToJointHome(-1.0835, -0.683, 0.1739, -1.429, 1.0564, 0.3338, -0.457808);
			runs->goToJointHome(-0.956542,-0.737367,0.175210,-1.323550,0.905058,0.347709,-0.360793);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.570870, -0.420680, 0.426269, -1.439009, 1.440784, 0.031831, -0.382473);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "9") {
			std::cout << "***Going to block 9" << std::endl;
			runs->goToJointHome(-0.277343,-0.196774,1.606540,-1.619746,0.249761,0.269587,1.406216);
			runs->goToJointHome(-0.323171,-0.405008,1.514512,-1.521797,0.007396,0.198650,1.307037);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.159780,0.055808,1.676317,-1.682108,0.440175,0.244551,1.47540);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "10") {
			std::cout << "***Going to block 10" << std::endl;
			runs->goToJointHome(-0.851678,-0.169595,1.405392,-1.310158,0.711384,0.415535,1.300128);
			runs->goToJointHome(-0.911190,-0.345115,1.363692,-1.169007,0.527138,0.398685,0.990952);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.859289,0.124167,1.434976,-1.439089,0.962618,0.396875,0.990952);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "11") {
			std::cout << "***Going to block 11" << std::endl;
			runs->goToJointHome(-1.066267,-0.101326,1.432554,-1.311852,0.711125,0.365255,0.990952);
			runs->goToJointHome(-1.114857,-0.312916,1.390735,-1.116032,0.493673,0.359659,0.990952);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.062748,0.182863,1.429702,-1.439672,0.887120,0.341686,0.990952);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "12") {
			std::cout << "***Going to block 12" << std::endl;
			runs->goToJointHome(-1.313928,-0.461585,1.289621,-1.207069,0.452590,0.767524,0.683815);
			runs->goToJointHome(-1.297058,-0.652186,1.234327,-1.069188,0.323517,0.694200,0.683815);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.306145,-0.145909,1.373220,-1.443878,0.703985,0.878165,0.683815);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "13") {
			std::cout << "***Going to block 13" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-0.469208, -0.468382, 1.449460, -1.454684, 0.407734, 0.231322, 1.571725);
			runs->goToJointHome(-0.590853,-0.691487,1.327786,-1.229677,0.189394,0.235292,1.241576);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.485499,-0.329018,1.446525,-1.450751,0.541825,0.199152,1.241576);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "14") {
			std::cout << "***Going to block 14" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-0.991339, -0.378192, 1.433883, -1.210976, 0.818012, 0.326138, 0.990952);
			runs->goToJointHome(-1.013779,-0.631612,1.376613,-1.039002,0.520247,0.312049,0.834486);
			runs->moveGripper(0.004);
			runs->goToJointHome(-0.951836,-0.054214,1.360871,-1.379939,1.081523,0.335173,0.75915);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else if (command1 == "15") {
			std::cout << "***Going to block 15" << std::endl;
			runs->goToJointHome(-1.010838,-0.874208,0.790079,-1.492243,0.770900,0.919271,-0.124148);
			runs->goToJointHome(-0.926983,-1.055401,0.689399,-1.350464,0.638688,0.852968,-0.148323);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.197229,-0.813594,0.867981,-1.579644,1.099263,0.954778,-0.369024);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		
		}
		else if (command1 == "16") {
			std::cout << "***Going to block 16" << std::endl;
			runs->moveGripper(0.010);
			runs->goToJointHome(-1.487264,-0.641145,1.426211,-1.001752,0.476813,0.542310,0.533144);
			runs->goToJointHome(-1.412282,-0.984733,1.315186,-0.880356,0.227297,0.494892,0.382473);
			runs->moveGripper(0.004);
			runs->goToJointHome(-1.5035,-0.436651,1.417697,-1.0994337,0.628128,0.606963,0.382473);
			runs->goToJointHome(-1.313653,0.162255,1.289856,-1.382314,1.122259,0.024025,0.382473);
			runs->goToJointHome(-0.004435, 0.180997, 1.210828, -1.343153, 1.22991, -0.309694, 1.724626);
			runs->moveGripper(0.010);
		}
		else  {
			std::cout << "WRONG!!!" << std::endl;
		}

		//send back that we are done
		std::ofstream myOutFile;
		myOutFile.open("test.txt");
		myOutFile << "DONE\n";
		myOutFile.close();
	}
	runs->shutdown();

	std::cout << "Press Enter to Exit Program" << std::endl;
	std::cin.ignore();

	return 0;
}

