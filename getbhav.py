#Copyright (c) 2013 Chinmay Hundekari
#See the file license.txt for copying permission.

import urllib2
import httplib, StringIO, zipfile
import os
import sys

def downloadCSV(year="2013",mon="NOV",dd="06"):
	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7',
			   'Accept':'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
			   'Accept-Encoding':'gzip,deflate,sdch',
			   'Referer':'http://www.nseindia.com/archives/archives.htm'}
	filename = "cm%s%s%sbhav.csv" % (dd,mon,year)
	url = "www.nseindia.com"
	reqstr = "/content/historical/EQUITIES/%s/%s/%s.zip" % (year, mon, filename)

	conn = httplib.HTTPConnection(url)
	print "Downloading %s ..." % (filename)
	conn.request("GET", reqstr, None, headers)
	response = conn.getresponse()
	if response.status != 200:
		print "Response status != 200 \nCould not download %s." % (filename)
		return
	data = response.read()
	sdata = StringIO.StringIO(data)
	z = zipfile.ZipFile(sdata)
	csv = z.read(z.namelist()[0])
	if not csv:
		print "Could not download %s." % (filename)
		return
	else:
		if not os.path.exists("data"):
			os.makedirs("data")
		fil = open(os.path.join("data",filename), 'w')
		fil.write(csv)
		fil.close()
 
def getAll():
	years = ["2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013"]
	months = ["JAN","FEB","MAR","APR","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
	days = ["01","02","03","04","05","06","07","08","09","10",
			"11","12","13","14","15","16","17","18","19","20",
			"21","22","23","24","25","26","27","28","29","30","31"]
	for year in years:
		for mon in months:
			for dd in days:
				downloadCSV(year,mon,dd)

def getYear(year):
	months = ["JAN","FEB","MAR","APR","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
	days = ["01","02","03","04","05","06","07","08","09","10",
			"11","12","13","14","15","16","17","18","19","20",
			"21","22","23","24","25","26","27","28","29","30","31"]
	for mon in months:
		for dd in days:
			downloadCSV(year,mon,dd)

def getMonth(mon, year):
	days = ["01","02","03","04","05","06","07","08","09","10",
			"11","12","13","14","15","16","17","18","19","20",
			"21","22","23","24","25","26","27","28","29","30","31"]
	for dd in days:
		downloadCSV(year,mon,dd)

def _printUsage():
	print "Usage:"
	print "python getbhav.py -getAll \n\tDownloads bhav copy from 2001 to 2013"
	print "python getbhav.py -getYear [year]\n\tDownloads bhav copy for one year"
	print "python getbhav.py -getMonth [month] [year]\n\tDownloads bhav copy for one month"
	print "\tExample:\n\t\tpython getbhav.py -getMonth JAN 2013"
	
def main(args):
	if args:
		if args[0] == "-getAll":
			getAll()
		elif args[0] == "-getYear":
			getYear(args[1])
		elif args[0] == "-getMonth":
			getMonth(args[1], args[2])
		else:
			_printUsage()
	else:
		_printUsage()

if __name__ == "__main__":
	main(sys.argv[1:])
