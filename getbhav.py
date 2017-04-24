#Copyright (c) 2017 Chinmay Hundekari
#See the file license.txt for copying permission.

import urllib2
import datetime
from dateutil.relativedelta import relativedelta
import requests
import httplib, StringIO, zipfile
import os
import sys

class nseConnect:
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Accept':'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
               'Accept-Encoding':'gzip,deflate,sdch',
               'Referer':'http://www.nseindia.com/archives/archives.htm'}
    url = "www.nseindia.com"

    def connect(self):
        response = requests.head('http://' + self.url)
        if response.status_code == 302:
            self.url = response.headers["Location"]
        isHttps = self.url.find("https") > -1
        self.url = self.url[self.url.find("//")+2:self.url.rfind("/")]
        if isHttps:
            self.conn = httplib.HTTPSConnection(self.url)
        else:
            self.conn = httplib.HTTPConnection(self.url)

    def disconnect(self):
        self.conn.close()

    def getFilename(self, date):
        [y, m, d] = self.convertDate(date)
        return "cm%s%s%sbhav.csv" % (d, m, y)

    def convertDate(self, date):
        y = date.strftime("%Y")
        m = date.strftime("%b").upper()
        d = date.strftime("%d")
        return [y, m, d]

    def getReqStr(self, date):
        [y, m, d] = self.convertDate(date)
        return "/content/historical/EQUITIES/%s/%s/%s.zip" % (y, m, self.getFilename(date))

    def getResponse(self, reqstr):
        c = self.conn
        c.request("GET", reqstr, None, self.headers)
        response = c.getresponse()
        self.data = response.read()
        if response.status == 403:
            print "Response status is %s\tCould not download %s." % (response.status, reqstr)
            print "%s" % (self.data)
            return -1
        elif response.status == 404:
            print "File not found\tCould not download %s." % (reqstr)
            return -1
        elif response.status != 200:
            print "Response status is %s \tCould not download %s." % (response.status, reqstr)
            print "%s" % (self.data)
            return -1

def downloadCSV(c, d):
    filename = c.getFilename(d)
    reqstr = c.getReqStr(d)

    print "Downloading %s ..." % (filename)
    if c.getResponse(reqstr) == -1:
        return -1
    sdata = StringIO.StringIO(c.data)
    z = zipfile.ZipFile(sdata)
    try:
        csv = z.read(z.namelist()[0])
    except Exception as e:
        print "%s" % (format(e))
        return -1
    if not csv:
        print "Could not download %s." % (e.message)
        return -1
    else:
        if not os.path.exists("data"):
            os.makedirs("data")
        fil = open(os.path.join("data",filename), 'w')
        fil.write(csv)
        fil.close()
        return 1

def downloadCSVDate(c, date):
    [y, m, d] = convertDate(date)
    return downloadCSV(c, y, m, d)

def getUpdate(c):
    errContinous = 0
    d = datetime.date.today()
    decr = datetime.timedelta(days=1)
    while errContinous > -30 and (not os.path.exists(os.path.join("data",c.getFilename(d)))):
        if downloadCSV(c, d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def getAll(c):
    errContinous = 0
    d = datetime.date.today()
    decr = datetime.timedelta(days=1)
    while errContinous > -30:
        if downloadCSV(c, d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def getYear(c, year):
    errContinous = 0
    d = datetime.date(int(year), 12, 31)
    decr = datetime.timedelta(days=1)
    while (errContinous > -30 and d.strftime("%Y") == year):
        if downloadCSV(c, d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def getMonth(c, mon, year):
    errContinous = 0
    decr = datetime.timedelta(days=1)
    d = datetime.date(int(year), int(mon), 1) + relativedelta(months=+1) - decr
    while errContinous > -30 and d.strftime("%Y") == year and d.strftime("%m") == mon:
        if downloadCSV(c, d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def _printUsage():
    print "Usage:"
    print "python getbhav.py -update \n\tUpdates bhav copy till last date found"
    print "python getbhav.py -getAll \n\tDownloads bhav copy from 2016 onwards"
    print "python getbhav.py -getYear [year]\n\tDownloads bhav copy for one year"
    print "python getbhav.py -getMonth [month] [year]\n\tDownloads bhav copy for one month"
    print "\tExample:\n\t\tpython getbhav.py -getMonth 02 2013"

def main(args):
    c = nseConnect()
    c.connect()
    if args:
        if args[0] == "-update":
            getUpdate(c)
        elif args[0] == "-getAll":
            getAll(c)
        elif args[0] == "-getYear":
            getYear(c, args[1])
        elif args[0] == "-getMonth":
            getMonth(c, args[1], args[2])
        else:
            _printUsage()
    else:
        downloadCSVDate(c, datetime.date.today())
    c.disconnect()

if __name__ == "__main__":
    main(sys.argv[1:])
