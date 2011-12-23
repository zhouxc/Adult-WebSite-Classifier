#!/usr/bin/python

import numpy
import sys
from scipy.stats import entropy
from SkinDetector import SkinDetector
import matplotlib.pyplot as plt
from scipy.sparse import cs_graph_components

from math import sqrt

dir = [(0 , 1) , (1 , 0), (0 , -1) , (-1 , 0)]

class ExtractSkinFeatures(SkinDetector):
	'''
	ExtractSkinFeatures Class inherited from Class SkinDetector is 
	used to extract skin features from skin color pixels. There are
	sixteen skin features including:
	1.percentage of pixels detected as skin
	2.number of connected components of skin and the maxinum component
	3.average probability of the skin pixels
	4.the mean and deviation of R,G,B color value of skin pixels
	5.the entropy of R,G,B color value of skin pixels
	6.the hight and width of the image
	7.the maxinum area of the skin section
	'''
	def __init__(self , imageFile):
		
		SkinDetector.__init__(self , imageFile)
		self.count = 0
		self.connectedComponents = 0
		self.maxComponent = 0
		self.visited = numpy.zeros((5000 , 5000))
		self.componentPixes = []
		self.maxComponentPixes = []
		self.maxSkinArea = 0.0
		self.skinFeatures = []

	def skin_detect(self):
		'''
		This method gets skin pixels as the input of 
		feature extraction
		'''
		self.computer_skin_probability()
		self.detect()
		#self.show_image()

	def extract_skin_features(self):
		''' 
		Extract sixteen features from skin color pixels , features are:
		self.meanRGB 				: the mean of R,G,B color value of skin pixels 
		self.stdRGB  				: the deviation of R,G,B color value of skin pixels
		self.avgSkinProb 			: average probability of the skin pixels
		self.skinPixesPercentage	: percentage of pixels detected as skin
		self.rgbEntropy			    : the entropy of R,G,B color value of skin pixels
		self.imgHeight:				: the hight of the image
		self.imgWidth:				: the width of the image
		self.maxComponent:			: the maxinum connected components of skins
		self.connectedComponents	: number of connected components of skins
		self.maxSkinArea			: the maxinum area of skin section
		'''
		self.skins = numpy.where(self.skinProb > 0)
		self.skinPixes = self.image[self.skins]
		
		self.meanRGB = numpy.mean(self.skinPixes ,0)
		self.stdRGB = numpy.std(self.skinPixes , 0)
		self.avgSkinProb = numpy.mean(self.skinProb[self.skins])
		self.skinPixesPercentage = 1.0*len(self.skinPixes) / (self.imgHeight*self.imgWidth)

		self.rHistogram = numpy.histogram(self.skinPixes[:,0], range = (0,255), bins = 32)
		self.gHistogram = numpy.histogram(self.skinPixes[:,1], range = (0,255), bins = 32)
		self.bHistogram = numpy.histogram(self.skinPixes[:,2], range = (0,255), bins = 32)
		
		self.rEntropy = entropy(self.rHistogram[0] + 0.00001)
		self.gEntropy = entropy(self.gHistogram[0] + 0.00001)
		self.bEntropy = entropy(self.bHistogram[0] + 0.00001)
		
		#print self.rEntropy
		self.compute_connected_components()

		self.skinFeatures += self.meanRGB.tolist()
		self.skinFeatures += self.stdRGB.tolist()
		self.skinFeatures += [self.avgSkinProb , self.skinPixesPercentage]
		self.skinFeatures += [self.rEntropy , self.gEntropy , self.bEntropy]
		self.skinFeatures += [self.imgHeight , self.imgWidth]
		self.skinFeatures += [self.maxComponent , self.connectedComponents]
		self.skinFeatures += [self.maxSkinArea]

	
	def compute_connected_components(self):
		'''
		Call the flood_fill method compute the number of connected components
		and the maxinum connected component of skins
		'''
		skinSize = len(self.skins[0])
		for i in range(skinSize):
			x , y = self.skins[0][i] , self.skins[1][i]
			if self.visited[x][y] == 0:
				self.flood_fill(x , y)
				#print self.count , len(self.componentPixes)
				self.connectedComponents += 1
				if self.maxComponent < self.count:
					self.maxComponent = self.count
					self.maxComponentPixes = self.componentPixes
				self.componentPixes = []
				self.count = 1

		self.compute_max_skinArea()

	def compute_max_skinArea(self):
		'''
		Find the most left , most right , most up , most down pixel of
		the maxinum component pixels and then computer the area of the quadrangle
		if it doss not exisit , the area is zero
		'''
		try:
			left = min(self.maxComponentPixes , key = lambda tup : tup[1])
			right = max(self.maxComponentPixes , key = lambda tup : tup[1])
			up = min(self.maxComponentPixes)
			down = max(self.maxComponentPixes)

			a = sqrt(1.0 * pow(up[0]- left[0] , 2) + pow(up[1] - left[1] , 2))
			b = sqrt(1.0 * pow(right[0]- up[0] , 2) + pow(right[1] - up[1] , 2))
			c = sqrt(1.0 * pow(down[0]- right[0] , 2) + pow(down[1] - right[1] , 2))
			d = sqrt(1.0 * pow(left[0]- down[0] , 2) + pow(left[1] - down[1] , 2))

			e = sqrt(1.0 * pow(left[0] - right[0] , 2) + pow(left[1] - right[1] , 2))

			L = a + b + e
			area1 = sqrt(0.5 * L * (0.5 * L - a) * (0.5 * L - b) * (0.5 * L - e))
			L = c + d + e
			area2 = sqrt(0.5 * L * (0.5 * L - c) * (0.5 * L - d) * (0.5 * L - e))
		
			self.maxSkinArea = area1 + area2
		except ValueError:
			self.maxSkinArea = 0.0

		#print self.maxSkinArea
		#print len(self.maxComponentPixes)

		
	def flood_fill(self , x , y):
		''' 
		Run BFS algorithm to search the graph represented by matrix
		find the maxinum component and the number of components
		'''
		queue = [(x , y)]
		self.visited[x][y] = 1
		self.componentPixes.append((x , y))
		while len(queue) != 0:
			curPos = queue.pop()
			nextPos = ()
			for i in range(4):
				rx = curPos[0] + dir[i][0]
				ry = curPos[1] + dir[i][1]
				if rx < 0 or rx >= self.imgHeight or ry < 0 or ry >= self.imgWidth:
					continue
				if self.skinProb[rx][ry] <= 0 or self.visited[rx][ry] == 1:
					continue
				self.count += 1
				self.componentPixes.append((rx , ry))
				queue.append((rx , ry))
				self.visited[rx][ry] = 1
		
def main():
	f = ExtractSkinFeatures('sexy.jpg')
	f.skin_detect()
	f.show_image()
	f.extract_skin_features()
	print
	print '--------------Features Result------------------------'
	print
	print '%s features extracted' % len(f.skinFeatures)
	
	print
	print
	print 'The features are:'
	print
	print f.skinFeatures



if __name__ == '__main__':
	main()







