#Copyright (c) 2017 Chinmay Hundekari
#See the file license.txt for copying permission.

import urllib2
import datetime
from dateutil.relativedelta import relativedelta
import requests
import httplib, StringIO, zipfile
import os
import sys

def check_redirect(url):
    response = requests.head(url)
    if response.status_code == 302:
        url = response.headers["Location"]
    return url

def downloadCSV(year="2013",mon="NOV",dd="06"):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Accept':'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
               'Accept-Encoding':'gzip,deflate,sdch',
               'Referer':'http://www.nseindia.com/archives/archives.htm'}
    filename = "cm%s%s%sbhav.csv" % (dd,mon,year)
    url = "www.nseindia.com"
    reqstr = "/content/historical/EQUITIES/%s/%s/%s.zip" % (year, mon, filename)

    url = check_redirect('http://' + url)
    isHttps = url.find("https") > -1
    url = url[url.find("//")+2:url.rfind("/")]
    print url
    if isHttps:
        conn = httplib.HTTPSConnection(url)
    else:
        conn = httplib.HTTPConnection(url)
    print "Downloading %s ..." % (filename)
    conn.request("GET", reqstr, None, headers)
    response = conn.getresponse()
    data = response.read()
    if response.status == 403:
        print "Response status is %s\tCould not download %s." % (response.status, filename)
        print "%s" % (data)
        return -1
    elif response.status == 404:
        print "File not found\tCould not download %s." % (filename)
        return -1
    elif response.status != 200:
        print "Response status is %s \tCould not download %s." % (response.status, filename)
        print "%s" % (data)
        return -1
    sdata = StringIO.StringIO(data)
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

def downloadCSVDate(date):
    year = date.strftime("%Y")
    mon = date.strftime("%b").upper()
    d = date.strftime("%d")
    return downloadCSV(year,mon,d)

def getAll():
    errContinous = 0
    d = datetime.date.today()
    decr = datetime.timedelta(days=1)
    while errContinous > -30:
        if downloadCSVDate(d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def getYear(year):
    errContinous = 0
    d = datetime.date(int(year), 12, 31)
    decr = datetime.timedelta(days=1)
    while (errContinous > -30 and d.strftime("%Y") == year):
        if downloadCSVDate(d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def getMonth(mon, year):
    errContinous = 0
    decr = datetime.timedelta(days=1)
    d = datetime.date(int(year), int(mon), 1) + relativedelta(months=+1) - decr
    while errContinous > -30 and d.strftime("%Y") == year and d.strftime("%m") == mon:
        if downloadCSVDate(d) > -1:
            errContinous = 0
        else:
            errContinous -= 1
        d -= decr

def _printUsage():
    print "Usage:"
    print "python getbhav.py -getAll \n\tDownloads bhav copy from 2001 to 2013"
    print "python getbhav.py -getYear [year]\n\tDownloads bhav copy for one year"
    print "python getbhav.py -getMonth [month] [year]\n\tDownloads bhav copy for one month"
    print "\tExample:\n\t\tpython getbhav.py -getMonth 02 2013"

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
        downloadCSVDate(datetime.date.today())

if __name__ == "__main__":
    main(sys.argv[1:])
