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

'''
Regular expressions for crawling texts from urls of specific areas
'''
regex = re.compile(".*[\x80-\xff].*")
#regexUrl = re.compile('(read-htm-tid-[1-9]{7}\.html)|(thread-htm-fid-[0-9]*(-page-|\.html))')
#regexUrl = re.compile('(thread.php\?fid-.*)|(html/read.*html)')
regexUrl = re.compile('(http://66.96.246.115/forum-[0-9]*-[0-9]*.html)|(http://66.96.246.115/thread-.*.html)')

class Retrieve(object):
	def __init__(self , url):
		self.url = url
	
	'''
	Get raw text about chinese words from HTMLS parsed by BeautifulSoup
	'''
	def get_raw_text(self , soup):
		s = soup.string
		if s == None:
			contents = soup.contents
			text = ''
			for content in contents:
				subText = self.get_raw_text(content)
				text += subText
			return text
		else:
			s = s.strip()
			if regex.match(s.strip().encode('utf-8')) != None:
				return s.strip()
			return ''
			
	def getLinks(self):
		try:
			print self.url
			soup = BeautifulSoup(urllib2.urlopen(self.url) , fromEncoding='gb18030')
			ext = split(self.url)
			outfile = 'AdultWebsiteText/' +ext[1] + '.txt'
			if not exists(outfile):
				out = open(outfile , 'a')
				rawText = self.get_raw_text(soup)
				out.write(rawText.encode('utf-8'))
				out.close()

			links = soup.findAll('a' , href = regexUrl)
		
			return links
		except:
			print 'error'
			return None
			#self.getLinks()
		


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
			links = r.getLinks()
			
			if links == None : continue

			for link in links:
				link = link['href']
				#link = urljoin('http://184.164.141.66/', link)
				#link = urljoin('http://c1521.biz.tm/index.php' , link)
				if link not in self.seen:
					self.seen.append(link)
					if self.dome == urlparse(link)[1]:
						print link
						self.queOut.put(link)
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
			self.queIn.put(url)
			self.queOut.task_done()


class Crawler(object):
	''' 
	A multithread crawler downloads large number of texts from adult website 
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
	#login()
	#url = 'http://69.46.75.21/read-htm-tid-2591003.html'
	#url = 'http://69.46.75.21/index.php'
	#url = 'http://c1521.biz.tm/index.php'
	#url = 'http://69.46.75.21/thread-htm-fid-148.html'
	#url = 'http://70.85.48.252/bt/'
	#url = 'http://184.164.141.66/'
	#url = 'http://184.164.141.66/'
	#url = 'http://66.96.246.115/'
	#url = 'http://66.96.246.115/forum-108-1.html'
	url = 'http://66.96.246.115/forum.php'
	#url = 'http://184.164.141.66/thread.php?fid-75.html'
	spider = Crawler(url)
	spider.walk()

if __name__ == '__main__':
	start = time.time()
	main()
	print "Elapsed Time: %s" % (time.time() - start)
