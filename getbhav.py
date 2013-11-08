import urllib2
import httplib, StringIO, zipfile

#download data
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
		fil = open("data/%s" % (filename), 'w')
		fil.write(csv)
		fil.close()
 
#generate filename
years = ["2013"]
months = ["JAN","FEB","MAR","APR","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
days = ["01","02","03","04","05","06","07","08","09","10",
        "11","12","13","14","15","16","17","18","19","20",
        "21","22","23","24","25","26","27","28","29","30","31"]
#months = ["JAN"]
#days = ["01","02","03"]
for year in years:
	for mon in months:
		for dd in days:
			downloadCSV(year,mon,dd)



