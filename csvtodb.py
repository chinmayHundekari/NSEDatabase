#Copyright (c) 2013 Chinmay Hundekari
#See the file license.txt for copying permission.

import sqlite3
import csv
import sys
import os
import datetime as dt
import pandas as pd

def convertDate(date):
    monthdict = {"JAN" : 1,
                "FEB" : 2,
                "MAR" : 3,
                "APR" : 4,
                "MAY" : 5,
                "JUN" : 6,
                "JUL" : 7,
                "AUG" : 8,
                "SEP" : 9,
                "OCT" : 10,
                "NOV" : 11,
                "DEC" : 12,
                }
    date = date.split('-')
    day = int(date[0])
    mon = monthdict[date[1]]
    year = int(date[2])
    return dt.datetime(year, mon, day, 16)

def importcsvtoDB(filename):
    con = sqlite3.connect("test.db")

    with con:
        cur = con.cursor()

        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            rownum = 0
            for row in reader:
                if rownum == 0:
                    header = row
                else:
                    colnum = 0
                    for col in row:
                        if colnum == 0:
                            Symbol = col
                            print 'Inserting %s...' % (col)
                        if colnum == 2:
                            Open = col
                        if colnum == 3:
                            High = col
                        if colnum == 4:
                            Low = col
                        if colnum == 5:
                            Close = col
                        if colnum == 8:
                            Volume = col
                        if colnum == 9:
                            Tottrdval = col
                        if colnum == 10:
                            Date = col

                        colnum += 1
                    query = "INSERT INTO Quotes VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" %(Symbol, Date,Open, High, Low, Close, Volume , Tottrdval )
                    try:
                        cur.execute(query)
                    except :
                        print "Error on " + query
                        pass
                    #print query
                rownum += 1

def initDBQuotes():
    if not os.path.exists("test.db"):
        con = sqlite3.connect("test.db")
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE Quotes(Symbol    TEXT,Date DATE, Open TEXT, High TEXT, Low TEXT, Close TEXT, Volume TEXT, Tottrdval TEXT,PRIMARY KEY (Symbol, Date))")

def getLastDayScripts():
    con = sqlite3.connect("test.db")
    with con:
        cur = con.cursor()
        cur.execute(" SELECT DISTINCT DATE FROM Quotes")
        rows = cur.fetchall()
        dates = [ convertDate(str(row[0])) for row in rows]
        d = max(dates)
        cur = con.cursor()
        query = (" SELECT Symbol FROM Quotes WHERE DATE=\"%s\"") % (d.strftime("%d-%b-%Y").upper())
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    return -1

def obtainQuotes(Symbol):
    con = sqlite3.connect("test.db")

    with con:
        cur = con.cursor()
        cur.execute(" SELECT * FROM Quotes WHERE Symbol=\"%s\"" %(Symbol))
        rows = cur.fetchall()
        nprow = {}
        for row in rows:
            colnum = 0
            for col in row:
                if colnum == 1:
                    date = convertDate(col)
                if colnum == 2:
                    Open = float(col)
                if colnum == 3:
                    High = float(col)
                if colnum == 4:
                    Low = float(col)
                if colnum == 5:
                    Close = float(col)
                if colnum == 6:
                    Volume = float(col)
                if colnum == 7:
                    Tottrdval = float(col)
                    #print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (date, Open, High, Low, Close, Volume, Tottrdval),
                    nprow[date] = {'Open':Open,'High':High,'Low': Low,'Close': Close,'Volume': Volume,'Tottrdval': Tottrdval}
                colnum += 1
        datframe1 = pd.DataFrame.from_dict(nprow, orient="index")
        return datframe1

def obtainQuotesList(Symbols):
    con = sqlite3.connect("test.db")

    with con:
        cur = con.cursor()
        stock_data = {}
        for Symbol in Symbols:
            print "Getting data for %s" % (Symbol)
            cur.execute(" SELECT * FROM Quotes WHERE Symbol=\"%s\"" %(Symbol))
            rows = cur.fetchall()
            nprow = {}
            for row in rows:
                colnum = 0
                for col in row:
                    if colnum == 1:
                        date = convertDate(col)
                    if colnum == 2:
                        Open = float(col)
                    if colnum == 3:
                        High = float(col)
                    if colnum == 4:
                        Low = float(col)
                    if colnum == 5:
                        Close = float(col)
                    if colnum == 6:
                        Volume = float(col)
                    if colnum == 7:
                        Tottrdval = float(col)
                        nprow[date] = {'Open':Open,'High':High,'Low': Low,'Close': Close,'Volume': Volume,'Tottrdval': Tottrdval}
                    colnum += 1
            datframe1 = pd.DataFrame.from_dict(nprow, orient="index")
            stock_data[Symbol] = pd.DataFrame.from_dict(nprow, orient="index")
        return stock_data

def importdirtoDB(directory):
    for csvFile in os.listdir(directory):
        importcsvtoDB(os.path.join(directory,csvFile))

def _printUsage():
    print "Usage:"
    print "python csvtodb.py -add [filename]\n\tAdds file data to database"
    print "python csvtodb.py -addDir [filename]\n\tAdds all files in directory to database"
    print "python csvtodb.py -getMany [Symbol1,[Symbol2,[Symbol3...]]]\n\tGet data for Symbols"
    print "python csvtodb.py -get [Symbol]\n\tGet data for Symbol"

def main(args):
    if args:
        if args[0] == "-get":
            Datframe = obtainQuotes(args[1])
            print Datframe[:]
        elif args[0] == "-getMany":
            Datframe = obtainQuotesList(args[1:])
            print Datframe[args[1]][:10]
        elif args[0] == "-add":
            initDBQuotes()
            importcsvtoDB(args[1])
        elif args[0] ==    "-addDir":
            initDBQuotes()
            importdirtoDB(args[1])
        else:
            _printUsage()
    else:
        _printUsage()

if __name__ == "__main__":
    main(sys.argv[1:])
