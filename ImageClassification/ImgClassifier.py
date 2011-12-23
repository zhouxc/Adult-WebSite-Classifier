#!/usr/bin/python

import array
import numpy
import scipy
from numpy import sqrt , sum , divide
from svmutil import *

class Classifier(object):
	''' 
	Image classification in svm provided by libsvm package
	read training data and test data from file , normalize the data , 
	then put them into svm model.
	there are about 2500 postive(adult) images data and 5500 negative samples
	each sample has sixteen features
	use cross validation to choose the parameters of svm model
	the training error is about 95% and the test error is about 93%
	'''
	def __init__(self, trainingDataFile):
		self.trainingDataFile = trainingDataFile
		self.trainModel = None
		self.trainingDataSize = 0
		self.numFeatures = 0
		self.trainingData = []
		self.trainingLabel = []
	
	def read_data(self):
		'''
		Read dataset from files and do some operation
		'''
		data = open(self.trainingDataFile).readlines()
		self.trainingDataSize = len(data)
		print self.numFeatures
		for inst in data:
			nData = inst.split(',')
			if self.numFeatures == 0:
				self.numFeatures = len(nData) - 1
			temp = map(lambda r : float(r) , nData[:self.numFeatures])
			self.trainingData.append(temp)
			self.trainingLabel.append(int(nData[-1][0]))
	
	def normalize(self):
		'''
		Normalize the data to make sure the features are in the same scale
		'''
		self.trainingData = 1.0 *  scipy.array(self.trainingData)
		self.trainingData -= numpy.mean(self.trainingData , 0)
		self.trainingData /= numpy.std(self.trainingData , 0)
	
	def train(self):
		''' 
		Split the data randomly. Chose 6000 samples as training data.
		others are test data
		'''
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
		''' 
		Test the performence of the trained model on test data set
		'''
		tx = self.trainingData[:6000].tolist()
		ty = self.trainingLabel[:6000].tolist()
		pLabels , pAcc , pVals = svm_predict(ty , tx , self.trainModel)
		
		print pAcc


def main():
	classifier = Classifier("training-data.csv")
	classifier.read_data()
	classifier.train()
	classifier.predict()

if __name__ == '__main__':
		main()
