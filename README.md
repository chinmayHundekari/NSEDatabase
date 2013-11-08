NSEDatabase
===========

A tool to download historical quotes from NSE india, store quotes in a database and provide the data as pandas dataframe.

getbhav.py
==========

Usage:

    python getbhav.py


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
