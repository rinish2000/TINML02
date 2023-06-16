import math
import random
from data import trainingSet,outputDict, maxCost, testSet

class Data:
    # converts dataset to array
    
    def convert(dataItem):
        outputVector = []
        nrOfRows = len(dataItem[0])
        for iRow in range(nrOfRows):
            nrOfColumns = len(dataItem[0][iRow])
            for iColumn in range(nrOfColumns):
                outputVector.append(dataItem[0][iRow][iColumn])
        return outputVector

class Network:
    # def __init__(self):
    #     pass

    def multiply(inputVector,weightMatrix):
        outputVector = []
        for iweight in range(len(weightMatrix)):
            outputVector.append([])
            for iInput in range(len(inputVector)):
                outputVector[iweight].append(inputVector[iInput] * weightMatrix[iweight][iInput])

        # return outputVector
        return [sum(output) for output in outputVector]

    def softmax(inputVector):
        div = sum([math.exp(value) for value in inputVector])
        return [math.exp(value)/div for value in inputVector]
    
    def calcCost(symbol):
        cost = 0
        outputVector = Network.softmax()
        for iOutputValue in range(len(outputVector)):
            cost += (outputVector[iOutputValue] - outputDict[symbol][iOutputValue])**2
            cost = math.sqrt(cost)
        return cost
    
    def computeAverageCost(self):
        accummulatedCost = 0 
        for trainingsItem in trainingSet:
            # print(trainingsItem)                # (((1, 1, 1), (1, 0, 1), (1, 1, 1)), 'O')
            nrOfRows = len(trainingsItem[0])
            for iRow in range(nrOfRows):
                nrOfColumns = len(trainingsItem[0][iRow])
                # print("--------------")
                for iColumn in range(nrOfColumns):
                    self.inNodes[iRow][iColumn].value = trainingsItem[0][iRow][iColumn] 
                    # print(trainingsItem[0][iRow][iColumn])
            accummulatedCost += self.calcCost(trainingsItem[1])
            averageCost = accummulatedCost/len(trainingSet)
        return averageCost
        

# matrix = [[random.randint(1,2) for column in range(9)] for row in range(2)]
matrix =[[0 for column in range(9)] for row in range(2)]
input = Data.convert(trainingSet[0])

print(Network.softmax(Network.multiply(input,matrix)))