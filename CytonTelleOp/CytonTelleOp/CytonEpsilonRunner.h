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

private:
	EcRealVector startJointPosition;
	bool connected;
};

