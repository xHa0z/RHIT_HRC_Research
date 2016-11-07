// FileIO.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <string>
#include <Windows.h>
using namespace std;


int main()
{
	int i = 0;
	bool completedCommand = false;
	while (true) {
		string line = "";
		ifstream myInFile;
		myInFile.open("test.txt");

		getline(myInFile, line);
		i++;

		myInFile.close();
		if (line == "DONE") {
			std::cout << "Recieved DONE" << std::endl;
			std::cout << "Sending command: com:" << i << std::endl;
			std::cout << std::endl;
			completedCommand = true;
		}

		if (completedCommand) {
			ofstream myOutFile;
			myOutFile.open("test.txt");
			myOutFile << "com:" << i;
			myOutFile.close();
			completedCommand = false;
		}

		Sleep(1000);
	}
	return 0;
}

