#pragma once
class CytonEpsilonRunner
{
public:
	CytonEpsilonRunner();
	~CytonEpsilonRunner();

	bool connect();
	bool shutdown();
	bool goToJointHome();
	bool moveDelta(double x, double y, double z);
	bool moveTo(double x, double y, double z);
	bool grabMode();
	bool moveGripper(EcReal);

private:
	EcRealVector startJointPosition;
	bool connected;
};

