#pragma once
class CytonEpsilonRunner
{
public:
	CytonEpsilonRunner();
	~CytonEpsilonRunner();

	bool connect();
	bool shutdown();
	bool goToJointHome();

private:
	EcRealVector startJointPosition;
	bool connected;
};

