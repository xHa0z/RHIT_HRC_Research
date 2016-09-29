// CytonTelleOp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "CytonEpsilonRunner.h"
#include <Windows.h>

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

	double step = 0.01;
	double deltaX, deltaY, deltaZ = 0;
	while (looping) {

		//get keys being pressed and update
		if (GetAsyncKeyState(VK_ESCAPE)) {
			looping = false;
		}
		if (GetAsyncKeyState(VK_LEFT)) {
			deltaX += step;
		}
		if (GetAsyncKeyState(VK_RIGHT)) {
			deltaX -= step;
		}
		if (GetAsyncKeyState(VK_UP)) {
			deltaY += step;
		}
		if (GetAsyncKeyState(VK_DOWN)) {
			deltaY -= step;
		}
		if (GetAsyncKeyState(VK_PRIOR)) {//page up
			deltaZ += step;
		}
		if (GetAsyncKeyState(VK_NEXT)) {//page down
			deltaZ -= step;
		}
		if ((deltaX > step || deltaX < -step)|| (deltaY > step || deltaY < -step) || (deltaZ > step || deltaZ < -step)) {//don't move if nothing changed
			runs->moveDelta(deltaX, deltaY, deltaZ);//tell the cyton to move
			deltaX = 0;
			deltaY = 0;
			deltaZ = 0;
		}
		Sleep(100);
	}
	runs->shutdown();

	std::cout << "Press Enter to Exit Program" << std::endl;
	std::cin.ignore();

	return 0;
}

