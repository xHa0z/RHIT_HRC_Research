# This is the main file for the project. It obtains input from the
# NLP and Leap Motion portions of the project and then writes output
# to the Cyton robot text file.
# Created by: Chris Collinsworth
# Date: 10/29/2016

from MainFunctions import getMatrixFromFile, \
                          multiplyMatrices, \
                          checkMatrix, \
                          resetTextFile

# stopStatement = false
NLPTextFileName = "NLPTextFile"
NLPMatrixInit = "0,0,0,0\n0,0,0,0\n0,0,0,0\n0,0,0,0"

# while stopStatement == false:
NLPMatrix = getMatrixFromFile(NLPTextFileName)
bool = checkMatrix(NLPMatrix)
if bool == False:
    return str("Didn't catch that.")
probabilityMatrix, maxNumberIndex = multiplyMatrices(NLPMatrix, NLPMatrix)
# resetTextFile(NLPTextFileName, NLPMatrixInit)
