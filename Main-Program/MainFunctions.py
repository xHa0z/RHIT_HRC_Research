# This file contains all of the functions for the Main file.
# Created by: Chris Collinsworth
# Date: 10/29/2016

def getMatrixFromFile(fileName):
    """
    This function obtains the matrix from the specified text file
    and returns it as a 2D array.
    """
    matrixArray = []
    fileText = open(fileName + ".txt", "r+")
    for line in fileText.readlines():
        matrixArray.append([])
        for i in line.split(','):
            matrixArray[-1].append(int(i))
    fileText.close()
    return matrixArray

def multiplyMatrices(matrix1, matrix2):
    """
    This function multiplies two matrices by one another and
    returns the resulting matrix and the index of the resulting
    matrix's maximum number in an array.
    """
    matrixArray = []
    maxNumber = 0
    for row1, row2 in zip(matrix1, matrix2):
        matrixArray.append([])
        for number1, number2 in zip(row1, row2):
            matrixArray[-1].append(int(number1*number2))
            if ((number1*number2) > maxNumber):
                maxNumber = number1*number2
    for row, i in enumerate(matrixArray):
        try:
            column = i.index(maxNumber)
        except ValueError:
            continue
        return [matrixArray, [row,column]]
    return -1

def checkMatrix(matrix):
    """
    This function checks whether the values in the specified matrix
    are all -1.
    """
    if (matrix[0][0] == -1):
        return False
    return True

def resetTextFile(fileName, initialText):
    """
    This function removes the contents of the specified
    text file and then writes the new specified text to it.
    """
    fileText = open(fileName + ".txt", "r+")
    fileText.seek(0)
    fileText.truncate()
    fileText.write(initialText)
    fileText.close()
