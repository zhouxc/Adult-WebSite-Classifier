#!/usr/bin/python

import struct


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import floor
import numpy
import re

''' 
The skin data has been provided by researchers
'''
trainedFile = open('skinmodel.bin')
skinData = numpy.array(struct.unpack('32768f' , trainedFile.read(32768 * 4)))


class SkinDetector(object):
	''' 
	Check every color pixel of the image whether it is skin pixel
	the RGB values of every pixel can be classified into the 
	skin or non-skin categories by classification method according to
	color histogram features
	'''
	def __init__(self, imageFile):
		'''
		Be careful of JPG images which need to some operation like reversal
		'''
		self.imageFile = imageFile
		if re.match('.*\.(jpg|JPG)$' , self.imageFile) is not  None:	
			self.image = numpy.flipud(mpimg.imread(self.imageFile))
		else:
			self.image = 255.0 * mpimg.imread(self.imageFile)

		self.imgHeight = len(self.image)
		self.imgWidth = len(self.image[0])
	
	def show_image(self):
		'''
		Show the orignal image and the detected skin sections
		'''
		plt.imshow(self.image / 255.0)
		plt.show()
		#self.image[: , : , 1] = (self.skinProb > 0) * 255
		plt.imshow(self.newImage  , cmap = 'gray')
		plt.show()
	
	def computer_skin_probability(self):
		'''
		Every pixel has a mess of probability of being a skin pixel 
		according to their RGB values
		'''
		r = 1.0 * self.image[: , : , 0]
		g = 1.0 * self.image[: , : , 1]
		b = 1.0 * self.image[: , : , 2]
		#print r , g , b
		im = numpy.intp(1 + floor(r / 8.0)+floor(g / 8.0)*32 + floor(b / 8.0)*32* 32)
		self.skinProb = skinData[im - 1]

	def detect(self):
		self.newImage = (self.skinProb > 0) * 64

def main():
	img = 'sexy.jpg'
	detector = SkinDetector(img)
	detector.computer_skin_probability()
	detector.detect()
	detector.show_image()



if __name__ == '__main__':
	main()
