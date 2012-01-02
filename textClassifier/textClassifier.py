#!/usr/bin/python

import os
import math

'''
pornDict is the dictionary of chinese pron words
I use a python open source tool called smallseg in chinese sentences segmentation.
'''
pornDict = open('porn.dic').read().split()
dic =[x.rstrip() for x in file("porn.dic")]
from smallseg import SEG


class NavieBayes(object):
	'''
	Polynomial Navie Bayes classifier for text classification.
	Firstly , train a wordmodel on the training datasets and store 
	parameters into .csv files.
	In Classification , load the trained wordmode and get the parameters,
	then do classification in navie bayes ways.
	'''
	def __init__(self , trainingData = None , testData = None):
		self.posTotal = 0.0
		self.negTotal = 0.0
		self.negative = {}
		self.positive = {}
		self.trainingData = trainingData
		self.testData = testData
		for word in pornDict:
			self.positive[word] = 0.0
			self.negative[word] = 0.0
	
	def train(self):
		'''
		Train a navie bayes model on training datasets , then store the
		parameters into local files
		'''
		for data in self.trainingData:
			c += 1
			text = data[0]
			label = data[1]
			for word in text:
				if label == 'Positive':
					#print word
					self.positive[word] += 1.0
					self.posTotal += 1
				else:
					self.negative[word] += 1.0
					self.negTotal += 1.0
		
		#out = open('WordModel.csv' , 'a')
		#for word in pornDict:
		#	temp = word + ' ' + str(self.positive[word]) + ' ' + str(self.negative[word]) + '\n'
		#	out.write(temp)
		#out.close()
	
	def get_train_model(self):
		model = open('WordModel.csv').readlines()
		data = map(lambda s : s.split() , model)
		for temp in data:
			self.positive[temp[0]] = float(temp[1])
			self.negative[temp[0]] = float(temp[2])
			self.posTotal += self.positive[temp[0]]
			self.negTotal += self.negative[temp[0]]

	def classfy(self):
		'''
		Get the trained model to do classification on the test datasets
		Use log to replace multiplication with plus method to avoid underflow
		And return the performance on the test dataset.
		'''
		hit = 0
		self.get_train_model()
		for data in self.testData:
			text = data[0]
			label = data[1]
			gd = 0.0
			bd = 0.0
			for word in text:
				gd += math.log(float(self.positive[word] + 1.0) / (self.posTotal + len(pornDict)))
				bd += math.log(float(self.negative[word] + 1.0) / (self.negTotal + len(pornDict)))
				
			p_gd = math.log(float(self.posTotal + 1.0) / (self.posTotal + self.negTotal + 2.0))
			p_bd = math.log(float(self.negTotal + 1.0) / (self.posTotal + self.negTotal + 2.0))

			predictLabel = 'Negative'
			if gd + p_gd > bd + p_bd:
				predictLabel = 'Positive'
			else:
				pass
	
			if predictLabel == label:
				hit += 1
			
		print hit
		print hit * 1.0 / len(self.testData)

def get_data():
	'''
	Get the training and text datasets from local folds
	Positive and negative datasets were stored in different folds
	When loading the datasets , do sentences segmentation with smallseg tool
	'''
	posPath = '/home/zhouxc/skindetector/AdultWebsiteText/'
	negPath = '/home/zhouxc/skindetector/NormalWebsiteText/'
	posFiles = os.listdir(posPath)
	negFiles = os.listdir(negPath)

	trainingData = []
	seg = SEG()
	seg.set(dic)
	c = 0
	print '---------------------Read Positive DataSet-----------------'
	for fileName in posFiles:
		#if c > 100: break
		c += 1
		print "PositiveData" + str(c)
		path = posPath + fileName
		data = seg.cut(open(path).read())
		text = [word.encode('utf-8') for word in data if word.encode('utf-8') in pornDict]
		trainingData.append((text , 'Positive'))
	print '---------------------Positive DataSet done-----------------'
	c = 0
	
	print '---------------------Read Negative DataSet-----------------'
	for fileName in negFiles:
		#if c > 100:	break
		c += 1
		print "NegativeData" + str(c)
		path = negPath + fileName
		data = seg.cut(open(path).read())
		text = [word.encode('utf-8') for word in data if word.encode('utf-8')  in pornDict]
		trainingData.append((text , 'Negative'))
	print '--------Negative DataSet  done-----------------------------------'
	
	return trainingData  , trainingData

def main():
	
	trainingData , textData = get_data()
	bayes = NavieBayes(trainingData , textData)
	#bayes.train()
	#bayes = NavieBayes(textData)
	bayes.classfy()

if __name__ == "__main__":
	main()
