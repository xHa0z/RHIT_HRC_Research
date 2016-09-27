//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//     Copyright (c) 2012-2013 Energid Technologies. All rights reserved.
//
// Filename:    labviewremoteCommand.h
//
// Description: Labview remote command header file
//              
//
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define LABVIEW_EXPORT

#ifdef LABVIEW_EXPORT

#define Labview_Remote_API __declspec(dllexport)
#else
#define Labview_Remote_API __declspec(dllimport)
#endif



///Actin Headers////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "ecRemoteComm.h"
#include <foundCore/ecApplication.h>
#include <foundCore/ecMacros.h>
#include <foundCommon/ecCoordSysXForm.h>
#include <foundCore/ecTypes.h>


#include <iomanip>
#include <iostream>
#include <algorithm>

using namespace std;



////Function Definitions///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

extern "C"
{

typedef struct EcRemoteComm EcRemoteComm; /* make the class opaque to the wrapper */

///
void handleInit(void);

///initialize the labview remote command client
Labview_Remote_API char* remoteCommandInit( char* ipAddress);

///set the eeset
Labview_Remote_API char* setEESet(int eeSet);

///set the control descriptor
Labview_Remote_API char* setControlDescriptor(int contDesc);

///place active EE
Labview_Remote_API char* moveEE(float x,float y,float z ,float roll,float pitch,float yaw);

///place active EE with quaternions
Labview_Remote_API char* moveEEQuaternions(float x,float y,float z ,float wAngle,float xAngle,float yAngle, float zAngle);

///place active EE with Tool Relative, using quaternions
Labview_Remote_API char* moveEEQuaternionsToolRelative(float x,float y,float z ,float wAngle,float xAngle,float yAngle, float zAngle);

///move EE Tool Relative
Labview_Remote_API char* moveEEToolRelative(float x,float y,float z ,float roll,float pitch,float yaw);

///move all joints
Labview_Remote_API char* moveJoints(float jointValues[ ], int numJoints);

///move a single joint
Labview_Remote_API char* moveJoint(int joint ,float jointValue);

///get the joints
Labview_Remote_API double getJointValue(int joint);

//get the Roll of the active EE guide frame
Labview_Remote_API double getEERoll(void);

//get the Pitch of the active EE guide frame
Labview_Remote_API double getEEPitch(void);

//get the Yaw of the active EE guide frame
Labview_Remote_API double getEEYaw(void);

//get the W Angle of the active EE guide frame
Labview_Remote_API double getEEWAngle(void);

//get the X Angle of the active EE guide frame
Labview_Remote_API double getEEXAngle(void);

//get the Y Angle of the active EE guide frame
Labview_Remote_API double getEEYAngle(void);

//get the Z Angle of the active EE guide frame
Labview_Remote_API double getEEZAngle(void);

//get the X position of the active EE guide frame
Labview_Remote_API double getXValue(void);

//get the Y position of the active EE guide frame
Labview_Remote_API double getYValue(void);

//get the Z position of the active EE guide frame
Labview_Remote_API double getZValue(void);

//get the actual roll of the simulated end effector
Labview_Remote_API double getActualEERoll(void);

//get the actual roll of the simulated end effector
Labview_Remote_API double getActualEEPitch(void);

//get the actual roll of the simulated end effector
Labview_Remote_API double getActualEEYaw(void);

//get the W Angle of the simulated end effector
Labview_Remote_API double getActualEEWAngle(void);

//get the X Angle of the simulated end effector
Labview_Remote_API double getActualEEXAngle(void);

//get the Y Angle of the simulated end effector
Labview_Remote_API double getActualEEYAngle(void);

//get the Z Angle of the simulated end effector
Labview_Remote_API double getActualEEZAngle(void);

//get the Actual X position of the active EE
Labview_Remote_API double getActualXValue(void);

//get the Actual Y position of the active EE
Labview_Remote_API double getActualYValue(void);

//get the Actual Z position of the active EE
Labview_Remote_API double getActualZValue(void);

//get if the actual position of the active EE has acheived the desired position
Labview_Remote_API int achievedDesired(float positionTolerance, float angularTolerance);

//get if the actual position of the active EE has acheived the desired position, for free spin in z ees
Labview_Remote_API int achievedDesiredFreeSpinZ(float positionTolerance, float angularTolerance);

//get if the actual joint angles have acheived the desired joint angles
Labview_Remote_API int achievedDesiredJoints(float angleTolerance,float jointValues[ ], int numJoints);

///call manipulation action
Labview_Remote_API char* runManipulationAction(char* actionManagerFilePath,char* actionName, int timeInMilliSeconds);

///shut down interface
Labview_Remote_API char* remoteCommandShutdown( void );

}