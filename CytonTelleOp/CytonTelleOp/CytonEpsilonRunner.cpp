#include "stdafx.h"
#include "CytonEpsilonRunner.h"


#include "CytonEpsilonRunner.h"

#define FRAME_EE_SET 1
#define JOINT_CONTROL_EE_SET 0xFFFFFFFF
#define POINT_EE_SET 0
#define M_PI 3.141592653
#define TIMEOUT 5000  //5 seconds

using namespace Ec;


CytonEpsilonRunner::CytonEpsilonRunner()
{
	connected = false;
}


CytonEpsilonRunner::~CytonEpsilonRunner()
{
}


//connects to the robot itself and returns success
bool CytonEpsilonRunner::connect() {
	if (init()) {
		printf("established connection to Cyton\n");
		connected = true;
		return true;
	}
	else {
		printf("failed to connect to Cyton\n");
		connected = false;
		return false;
	}
}


//puts the robot into a safe position and closes everything.
bool CytonEpsilonRunner::shutdown() {
	std::cout << "Please clear all space around the robot" << std::endl << "press 'y' to continue shutting down, 'n' to exit" << std::endl;
	char resp;
	while (true) {
		std::cin >> resp;
		if (resp == 'n') {
			return false;
		}
		else if (resp == 'y') {
			break;
		}
	}
	if (goToJointHome()) {
		Ec::shutdown();
		connected = false;
		return true;
	}
	return false;
}


//Sets all joints to zero (except gripper) and returns true if successful.
bool CytonEpsilonRunner::goToJointHome() {
	//sets all joints to 0;
	EcRealVector jointPosition(7);

	const EcReal angletolerance = .000001;

	EcBoolean retVal = EcTrue;
	setEndEffectorSet(JOINT_CONTROL_EE_SET);
	//setEndEffectorSet(FRAME_EE_SET);
	EcSLEEPMS(500);

	//vector of EcReals that holds the set of joint angles
	EcRealVector currentJoints;
	retVal &= getJointValues(currentJoints);

	size_t size = currentJoints.size();
	if (size < jointPosition.size()) {
		size = currentJoints.size();
	}
	else if (size >= jointPosition.size()) {
		size = jointPosition.size();
	}

	for (size_t ii = 0; ii < size; ++ii) {
		currentJoints[ii] = jointPosition[ii];
	}
	//currentJoints[size - 1] = 0.003;

	retVal &= setJointValues(currentJoints);

	//Check if achieved
	EcBooleanVector jointAchieved;
	jointAchieved.resize(size);
	EcBoolean positionAchieved = EcFalse;

	// if it hasnt been achieved after 5 sec, return false

	EcU32 interval = 10;
	EcU32 count = 0;

	while (!positionAchieved && !(count >= TIMEOUT / interval)) {
		EcSLEEPMS(interval);
		count++;
		getJointValues(currentJoints);
		for (size_t ii = 0; ii < size; ++ii) {
			if (std::abs(jointPosition[ii] - currentJoints[ii]) < angletolerance) {
				jointAchieved[ii] = EcTrue;
			}
		}
		for (size_t ii = 0; ii < size; ++ii) {
			if (!jointAchieved[ii]) {
				positionAchieved = EcFalse;
				break;
			}
			else {
				positionAchieved = EcTrue;
			}
		}
	}
	return positionAchieved;
}

//Tells the robot to move in the specified direction
bool CytonEpsilonRunner::moveDelta(double x, double y, double z) {
	//TODO:Fill this out

	//TODO: Find current Cyton Position

	//TODO: Tell Cyton to move to current position + deltas

	//return true if successfull, false otherwise
	return false;
}