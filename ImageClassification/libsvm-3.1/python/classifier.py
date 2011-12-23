#!/usr/bin/python

import array
import numpy
import scipy
from numpy import sqrt , sum , divide
from svmutil import *

class Classifier(object):
	def __init__(self, trainingDataFile):
		self.trainingDataFile = trainingDataFile
		self.trainModel = None
		self.trainingDataSize = 0
		self.numFeatures = 0
		self.trainingData = []
		self.trainingLabel = []
	
	def read_data(self):
		data = open(self.trainingDataFile).readlines()
		self.trainingDataSize = len(data)
		print self.numFeatures
		#self.trainingData = numpy.zeros((self.trainingDataSize , self.numFeatures))
		for inst in data:
			nData = inst.split(',')
			if self.numFeatures == 0:
				self.numFeatures = len(nData) - 1
			temp = map(lambda r : float(r) , nData[:self.numFeatures])
			self.trainingData.append(temp)
			self.trainingLabel.append(int(nData[-1][0]))
	
	def normalize(self):
		self.trainingData = 1.0 *  scipy.array(self.trainingData)
		self.trainingData -= numpy.mean(self.trainingData , 0)
		self.trainingData /= numpy.std(self.trainingData , 0)
	
	def train(self):
		
		self.normalize()
		self.trainingLabel = scipy.array(self.trainingLabel)
		randIdx = numpy.array(range(self.trainingDataSize))
		numpy.random.shuffle(randIdx)
		self.trainingData = self.trainingData[randIdx]
		self.trainingLabel = self.trainingLabel[randIdx]

		x = self.trainingData[:6000].tolist()
		y = self.trainingLabel[:6000].tolist()
		prob = svm_problem(y , x)
		param = svm_parameter('-c 48 -b 1 -d 3 -r 0 -t 2 -h 0')
		self.trainModel = svm_train(prob , param)
	
	def predict(self):
		tx = self.trainingData[:6000].tolist()
		ty = self.trainingLabel[:6000].tolist()
		pLabels , pAcc , pVals = svm_predict(ty , tx , self.trainModel)
		
		print pAcc
		#print pLabels


def main():
	classifier = Classifier("training-data.csv")
	classifier.read_data()
	#print classifier.trainingData[1889]
	#classifier.normalize()

	#print classifier.trainingData[1889]
	#print classifier.trainingLabel[1889]
	#print len(classifier.trainingLabel)
	#classifier.trainingLabel = scipy.array(classifier.trainingLabel)
	#randIdx = numpy.array(range(classifier.trainingDataSize))
	#classifier.trainingData = classifier.trainingData[randIdx]
	#classifier.trainingLabel = classifier.trainingLabel[randIdx]
	
	#classifier.trainingLabel = classifier.trainingLabel.tolist()
	#classifier.trainingData = classifier.trainingData.tolist()
	#x = []
	#y = []
	#for i in range(10):
	#	x = x + classifier.trainingData[300*i : 300*(i + 1)]
	#	y = y + classifier.trainingLabel[300*i : 300 * (i + 1)]
	#	classifier.train(x , y)
	#	classifier.predict()
	#	print '----------------------------------------'

	classifier.train()
	classifier.predict()

if __name__ == '__main__':
		main()
