#include "stdafx.h"
#include "CytonEpsilonRunner.h"

#include <control/ecEndEffectorSet.h>
#include <controlCore/ecFrameEndEffector.h>
#include <control/ecManipEndEffectorPlace.h>
#include <foundCore/ecApplication.h>
#include <foundCore/ecMacros.h>
#include <manipulation/ecManipulationActionManager.h>
#include <manipulationDirector/ecManipulationScript.h>
#include <manipulationDirector/ecManipulationDirector.h>
#include <math.h>
#include <remoteCommand/ecRemoteCommand.h>
#include <xmlReaderWriter/ecXmlObjectReaderWriter.h>
#include <iostream>
#include <boost/bind.hpp>
#include "CytonEpsilonRunner.h"
#include <foundCommon/ecCoordSysXForm.h>

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

	size_t size = currentJoints.size();  // Make sure the robot does not go off limit
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
bool CytonEpsilonRunner::moveDelta(double dx, double dy, double dz) {
	
	EcManipulatorEndEffectorPlacement actualEEPlacement;
	EcCoordinateSystemTransformation actualCoord;
	getActualPlacement(actualEEPlacement);
	actualCoord = actualEEPlacement.offsetTransformations()[0].coordSysXForm();

	EcVector trans = actualCoord.translation();
	double x = trans.x();
	double y = trans.y();
	double z = trans.z();


	x += dx;
	y += dy;
	z += dz;

	std::cout << "move to X:" << x << " Y:" << y << " Z:" << z << std::endl;

	EcCoordinateSystemTransformation pose;
	pose.setTranslationX(x);
	pose.setTranslationY(y);
	pose.setTranslationZ(z);


	EcOrientation orientation;
	orientation.setFrom123Euler(0, 0, 0);
	pose.setOrientation(orientation);
	setEndEffectorSet(0); //point end effector set

	EcEndEffectorPlacement desiredPlacement(pose);

	setDesiredPlacement(desiredPlacement, 0, 0);


	return true;
}

//Tells the robot to move in the specified direction
bool CytonEpsilonRunner::moveTo(double x, double y, double z, int method) {

	std::cout << "move to X:" << x << " Y:" << y << " Z:" << z << std::endl;

	EcManipulatorEndEffectorPlacement actualEEPlacement;
	EcCoordinateSystemTransformation pose;
	EcCoordinateSystemTransformation offset, zero, actualCoord;
	zero.setTranslation(EcVector(0, 0, 0));

	pose.setTranslationX(x);
	pose.setTranslationY(y);
	pose.setTranslationZ(z);


	EcOrientation orientation;
	orientation.setFrom123Euler(1.5, 0, 0);
	pose.setOrientation(orientation);
	setEndEffectorSet(method); //point end effector set

	EcEndEffectorPlacement desiredPlacement(pose);

	setDesiredPlacement(desiredPlacement, 0, 0);

	//EcU32 timeout = 5000;
	EcU32 timeout = 3000;
	EcU32 interval = 10;
	EcU32 count = 0;
	EcBoolean achieved = EcFalse;
	while (!achieved && !(count >= timeout / interval))
	{
		EcSLEEPMS(interval);
		count++;

		getActualPlacement(actualEEPlacement);
		if (actualEEPlacement.offsetTransformations().size() < 1)
		{
			return EcFalse;
		}
		actualCoord = actualEEPlacement.offsetTransformations()[0].coordSysXForm();

		//get the transformation between the actual and desired 
		offset = (actualCoord.inverse()) * pose;
		

		if (offset.approxEq(zero, .00001))
		{
			achieved = EcTrue;
		}

	}


	return true;
}




bool CytonEpsilonRunner::grabMode() {

	EcOrientation orientation; 
	EcCoordinateSystemTransformation pose;
	EcManipulatorEndEffectorPlacement actualEEPlacement;

	//roll about x-axis, pitch about y-axis,Yaw about z-axis
	orientation.setFrom123Euler(1.5, 0, 0);

	pose.setOrientation(orientation);
	EcEndEffectorPlacement desiredPlacement(pose);

	//setDesiredPlacement(desiredPlacement, 100, 100);
	EcU32 timeout = 3000;
	EcU32 interval = 10;
	EcU32 count = 0;
	EcBoolean achieved = EcFalse;
	while (!achieved && !(count >= timeout / interval))
	{
		EcSLEEPMS(interval);
		count++;

		//std::cout << "Moving " << std::endl;
		//getActualPlacement(actualEEPlacement);
	}

	return true;
}





bool CytonEpsilonRunner::moveGripper(const EcReal gripperPos) {

	EcManipulatorEndEffectorPlacement actualEEPlacement, desiredEEPlacement;
	//switch to frame ee set, so the link doesnt move when we try and grip

	setEndEffectorSet(FRAME_EE_SET);
	EcSLEEPMS(100);
	//get the current placement of the end effectors
	getActualPlacement(actualEEPlacement);

	//0 is the Wrist roll link (point or frame end effector), 
	//1 is the first gripper finger link (linear constraint end effector)
	EcEndEffectorPlacementVector state = actualEEPlacement.offsetTransformations();

	if (state.size() < 2)
	{
		return EcFalse;
	}

	//set the translation of the driving gripper finger
	EcCoordinateSystemTransformation gripperfinger1trans = state[1].coordSysXForm();
	gripperfinger1trans.setTranslation(EcVector(0, 0, gripperPos));
	EcEndEffectorPlacement finger1placement = state[1];
	finger1placement.setCoordSysXForm(gripperfinger1trans);
	state[1] = finger1placement;

	desiredEEPlacement.setOffsetTransformations(state);

	//set the desired placement
	setDesiredPlacement(desiredEEPlacement, 0);

	// if it hasnt been achieved after 2 sec, return false
	EcU32 timeout = 2000;
	EcU32 interval = 10;
	EcU32 count = 0;
	EcBoolean achieved = EcFalse;
	while (!achieved && !(count >= timeout / interval))
	{
		EcSLEEPMS(interval);
		count++;

		//std::cout << "Moving " << std::endl;

		getActualPlacement(actualEEPlacement);
		EcEndEffectorPlacementVector currentState = actualEEPlacement.offsetTransformations();
		EcCoordinateSystemTransformation gripperfinger1trans = currentState[1].coordSysXForm();
		EcReal difference = std::abs(gripperPos - gripperfinger1trans.translation().z());
		//std::cout << "distance between actual and desired: " << difference << std::endl;

		if (difference < .000001)
		{
			achieved = EcTrue;
		}
	}
	std::cout << (achieved ? "Achieved Gripper Position" : "Failed to Achieve Gripper Position") << std::endl;
	return achieved;


	//return false;

}