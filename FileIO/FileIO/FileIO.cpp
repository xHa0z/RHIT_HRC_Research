// FileIO.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <string>
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

		myInFile.close();
		if (line != "" && line != "DONE" && line != "WORKING") {
			std::cout << "Completing command: " << std::endl;
			std::cout << line << std::endl;
			std::cout << std::endl;
			completedCommand = true;
		}

		if (completedCommand) {
			ofstream myOutFile;
			myOutFile.open("test.txt");
			myOutFile << "DONE\n";
			myOutFile.close();
			completedCommand = false;
		}
	}
    return 0;
}

