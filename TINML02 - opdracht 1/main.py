import math
import random
import time

from data import trainingSet,outputDict, maxCost, testSet

class Node:
    def __init__(self, value = 0):
        self.links = []  # list of link objects
        self.value = value

    def getValue(self):
        if self.links:
            sum = 0
            for link in self.links:
                sum += link.getValue()
            return sum
        return self.value


class Link:
    def __init__(self,inNode,outNode):
        self.weight = 0 #random.randint(1,10)
        self.inNode = inNode
        outNode.links.append(self)

    def getValue(self):
        return self.weight * self.inNode.getValue()

class Network:
    def __init__(self):
        self.inNodes = []
        self.outNodes = []
        self.links = []
        self.averageCost = 0
        self.finalCost = 0
    
    def initLinks(self):
        for inRow in self.inNodes:
            for inNode in inRow:
                for outNode in self.outNodes:
                    self.links.append(Link(inNode,outNode))
    
    def insertWeights(self,listOfWeights):
        for weight,link in zip(listOfWeights,self.links):
            link.weight = weight

    def printWeights(self):
        for iLink in range(len(self.links)):
            print(iLink,"\t",self.links[iLink].weight)

    def softmax(self):
        div = sum([math.exp(outNode.getValue()) for outNode in self.outNodes])
        return [math.exp(outNode.getValue())/div for outNode in self.outNodes]  # vector of softmaxed output

    def calcCost(self,symbol):
        cost = 0
        outputVector = self.softmax()
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

    def train(self,trainingrate):
        startTime = time.time()
        self.averageCost = self.finalCost = self.computeAverageCost()
        while self.finalCost > maxCost:
            for link in self.links:
                link.weight += trainingrate
                cost = self.computeAverageCost()
                # print(cost)
                if cost < self.finalCost:
                    self.finalCost = cost
                    bestLink = link
                link.weight -= trainingrate
            bestLink.weight +=trainingrate

        print("training time: \t")
        print(round(time.time()-startTime,3))
        print("final cost: \t")
        print(self.finalCost)
        print("weights: ")
        for iLink in range(len(self.links)):
            print(iLink , "\t" , self.links[iLink].weight)

    def test(self):
        for testItem in testSet:
            nrOfRows = len(testItem[0])
            for iRow in range(nrOfRows):
                nrOfColumns = len(testItem[0][iRow])
                for iColumn in range(nrOfColumns):
                    self.inNodes[iRow][iColumn].value = testItem[0][iRow][iColumn] 
            outputVector = self.softmax()
            print("estimate of O:",round(100*outputVector[0],2),"%", "\t estimate of X:",round(100*outputVector[1],2),"%")
        pass

if __name__ == "__main__":

    network = Network()

    # create each node
    network.inNodes = [[Node() for column in range(3)] for row in range(3)]  # 3x3pixels = 9 Nodes
    network.outNodes = [Node() for column in range(2)] # X or O

    # initialize the links between each input and output node
    network.initLinks()

    # train with passed learning rate
    network.train(0.01)

    #test network with testset
    network.test()

