#!/usr/bin/python

from extractSkinFeature import *
import os
import matplotlib.image as mpimg

def get_image_dataset(Path):
	
	files = os.listdir(Path)
	for img in files:
		imgUrl = Path + '/' + img
		try:
			mpimg.imread(imgUrl)
		except:
			os.remove(imgUrl)
		try:
			extract = ExtractSkinFeatures(imgUrl)
			print img
			extract.skin_detect()
			extract.extract_skin_features()
			data = ''
			out = open('training-data7.csv' , 'a')
			for feature in extract.skinFeatures:
				data += str(feature) + ','
			data += '0\n'
			out.write(data)
			out.close()
		except:
			pass

def main():
	Path = '/home/zhouxc/image'
	print Path
	get_image_dataset(Path)


if __name__ == '__main__':
	print '-----------'
	main()
