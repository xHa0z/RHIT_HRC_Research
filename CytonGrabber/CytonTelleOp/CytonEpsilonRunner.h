#pragma once
class CytonEpsilonRunner
{
public:
	CytonEpsilonRunner();
	~CytonEpsilonRunner();

	bool connect();
	bool shutdown();
	bool goToJointHome(double r0 , double r1 , double r2 , double r3 , double r4 , double r5 , double r6 );
	//bool moveDelta(double x, double y, double z);
	bool moveTo(double x, double y, double z, int method = 0);
	bool grabMode();
	bool moveGripper(EcReal);

private:
	EcRealVector startJointPosition;
	bool connected;
};

