NSEDatabase
===========

A tool to download historical quotes from NSE india, store quotes in a database and provide the data as pandas dataframe.

getbhav.py
==========

Usage:

    python getbhav.py -getAll 

Downloads bhav copy from 2016 onwards

    python getbhav.py -getYear [year]
    
Downloads bhav copy for one year

    python getbhav.py -getMonth [month] [year]

Downloads bhav copy for one month

Example:

    python getbhav.py -getMonth 02 2017


csvtodb.py
==========

Usage:

    python csvtodb.py -add [filename]

Adds file data to database
    
    python csvtodb.py -addDir [filename]

Adds all files in directory to database
    
    python csvtodb.py -getMany [Symbol1,[Symbol2,[Symbol3...]]]

Get data for Symbols
    
    python csvtodb.py -get [Symbol]

Get data for Symbol

report.py
=========

Usage:

    python report.py -posGain 5 20

Generates a sorted report of all scripts which have moved positively in last 5 days and also provides movement over last 20 days    
