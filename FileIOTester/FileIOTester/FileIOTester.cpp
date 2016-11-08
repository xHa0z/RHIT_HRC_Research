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
		myInFile.close();


		if (line == "DONE") {
			std::cout << "Recieved DONE" << std::endl;
			ofstream myOutFile;
			myOutFile.open("test.txt");
			std::string temp;
			temp = std::cin.get();
			myOutFile << temp;
			myOutFile.close();
			std::cout << "sent: " << temp <<std::endl;
		}


		Sleep(1000);
	}
	return 0;
}

