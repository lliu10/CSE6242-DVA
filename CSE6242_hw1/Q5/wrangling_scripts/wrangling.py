"""
cse6242 s21
wrangling.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table. """
import csv
from operator import itemgetter

def username():
    return 'eperalta6'

def data_wrangling():
    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = list()
        
        ...
        
        # Read in the header
        for header in reader:
            break
        
        # Read in each row
        for row in reader:
            # Only read first 100 data rows - [2 points] Q5.a
            if len(table) == 100: 
                break

            else:
                row[2] = float(row[2])
                table.append(row)
        
        # Order table by the last column - [3 points] Q5.b
        table.sort(key= lambda x: x[2], reverse= True)

        for i in range(len(table)):
            table[i][2] = str(table[i][2])

    
    return header, table

