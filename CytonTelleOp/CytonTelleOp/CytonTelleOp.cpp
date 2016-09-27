// CytonTelleOp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "CytonEpsilonRunner.h"

int main()
{
	CytonEpsilonRunner *runs = new CytonEpsilonRunner();

	std::cout << "Press Enter to Connect to CytonViewer" << std::endl;
	std::cin.ignore();
	runs->connect();
	std::cout << "Press Enter to Disconnect from CytonViewer" << std::endl;
	std::cin.ignore();
	runs->shutdown();

	std::cout << "Press Enter to Exit Program" << std::endl;
	std::cin.ignore();

	return 0;
}

