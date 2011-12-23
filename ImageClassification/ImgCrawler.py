#!/usr/bin/python

from Queue import Queue
from urlparse import urlparse , urljoin
from urllib import urlretrieve , urlopen
from os import makedirs
from BeautifulSoup import BeautifulSoup
from os.path import exists , split
import time
import threading
import re


import cookielib
import urllib2 , urllib
from urllib2 import URLError,HTTPError


class Retrieve(object):
	def __init__(self , url):
		self.url = url
	
	def getLinks(self):
		try:
			soup = BeautifulSoup(urllib2.urlopen(self.url))
			links = soup.findAll('a' , href = re.compile('(read-htm-tid-[1-9]{7}\.html)|(thread-htm-fid-11(-page-|\.html))'))
			images = soup.findAll('img' , src = re.compile('http://farm8.*.jpg$'))
			for image in images:

				if image.has_key('width') and image.has_key('height'):
					if int(image['width']) < 400 or int(image['height']) < 400:
						continue
				img = image['src']
				print img
				ext = split(img)
				global cunt
				imgfile = 'AdImg/' + ext[1]
				if not exists(imgfile):
					urlretrieve(img , imgfile)
		except:
			self.getLinks()


class GetPageThread(threading.Thread):
	def __init__(self ,queIn , queOut , seen , dome):
		threading.Thread.__init__(self)
		self.queIn = queIn
		self.queOut = queOut
		self.seen = seen
		self.dome = dome

	def run(self):
		while True:
			url = self.queIn.get()
			r = Retrieve(url)
			try:
				links , rootUrl  = r.getLinks()
			except TypeError:
				pass

			for link in links:
				link = link['href']
				link = urljoin('http://69.46.75.21/thread-htm-fid-11.html', link)
				print link
				if link not in self.seen:
					self.seen.append(link)
					if self.dome == urlparse(link)[1]:
						print link
						self.queOut.put(link)
			print self.getName()
			self.queIn.task_done()


class PopQueThread(threading.Thread):
	def __init__(self , queIn ,queOut , seen):
		threading.Thread.__init__(self)
		self.queIn = queIn
		self.queOut = queOut
		self.seen = seen
	
	def run(self):
		while True:
			url = self.queOut.get()
			self.seen.append(url)
			print url
			self.queIn.put(url)
			print self.getName()
			self.queOut.task_done()



	

class Crawler(object):
	''' 
	A multithread crawler downloads large number of images from adult website 
	and normal website.
	'''
	def __init__(self , url):
		self.url = url
		self.numThread = 100
		self.queIn = Queue(self.numThread)
		self.queOut = Queue(self.numThread)
		self.queOut.put(url)
		self.seen = []
		self.dome = urlparse(url)[1]

	def walk(self):
		for i in range(self.numThread):
			t = PopQueThread(self.queIn , self.queOut , self.seen)
			t.setDaemon(True)
			t.start()
		
		for i in range(self.numThread):
			dt = GetPageThread(self.queIn , self.queOut , self.seen , self.dome)
			dt.setDaemon(True)
			dt.start()

		self.queIn.join()
		self.queOut.join()


def login():
	''' 
	Login some website need to authentication
	fetch the login HTTP message
	'''
	cookie_support= urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)
	postdata = urllib.urlencode({
									'jumpurl' : '/index.php',
									'step'	  :  2,
									'pwuser'  : 'sexyzhouxc',
									'pwpwd'	  : 'zhouxc2007',
									'lgt'     :  0
                                })
	req = urllib2.Request(
							url = 'http://69.46.75.21/login.php',
							data = postdata,
						 )

	conn = urllib2.urlopen(req)
	print conn.info()



def main():
	#url = "http://igirls.tuita.com/"
	#url = "http://jaychiu.tuita.com/"
	#url = "http://jonny.tuita.com/"
	#url = "http://natural.tuita.com/"
	#url = 'http://www.9city.tv/forum-153-1.html'
	login()
	url = 'http://69.46.75.21/thread-htm-fid-11.html'
	spider = Crawler(url)
	spider.walk()

if __name__ == '__main__':
	start = time.time()
	main()
	print "Elapsed Time: %s" % (time.time() - start)
