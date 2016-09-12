import csv
import random
import math
import operator

def loadDataset(filename, split, trainingSet=[], testSet=[]):
		with open(filename, 'rb') as csvfile:
				lines= csv.reader(csvfile)
				#reads the csv file into lines
				dataset = list(lines)
				#dataset is an array of the data rows in the csv
				for x in range(len(dataset)-1):
				#loops through the array of data rows
					for y in range(4):
					#loops through the data cells in each row
						dataset[x][y] = float(dataset[x][y])
						#stores each row of data from the original csv 
						#as an array within the new dataset array
					
					if random.random() < split:
						trainingSet.append(dataset[x])
					else:
						testSet.append(dataset[x])
					#splits the data so that some of the data is to use 
					#for prediction and the other data is set aside to check our predictions for accuracy

def euclideanDistance(instance1, instance2, length):
		distance= 0
		for x in range(length):
			distance += pow((instance1[x]-instance2[x]),2)
		return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
	#loops through each array in the training set
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		#gets the euclidean distance between each array in the training set and the test instance
		distances.append((trainingSet[x], dist))
		#adds each training set and their respective distance to the distances array
	distances.sort(key=operator.itemgetter(1))
	#sorts distances by the first column
	neighbors =[]
	for x in range(k):
		neighbors.append(distances[x][0])
	print neighbors
	return neighbors

def getResponse(neighbors):
	classVotes={}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		#get the species name for each flower
		if response in classVotes:
			classVotes[response] += 1
		else: 
			classVotes[response] = 1
		#gives each species instance a vote
		sortedVotes= sorted(classVotes.iteritems(), key= operator.itemgetter(1), reverse=True)
		return sortedVotes[0][0]
		#returns the name of the species with the most votes which is out prediction

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] is predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

	#returns the ratio of correct predictions out of total test set 

def main():
	trainingSet=[]
	testSet=[]
	split=0.67
	loadDataset('iris.csv', split, trainingSet, testSet)
	print 'Training set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	predictions=[]
	k=3
	for x in range(len(testSet)):
		neighbors=getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + 'actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')


main()