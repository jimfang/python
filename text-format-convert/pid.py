#!/usr/bin/python

#from mmap import mmap,ACCESS_READ
import sys
import getopt
import fnmatch
import os
from xlrd import open_workbook

def istxt(n):
    if type(n) == unicode or type(n) == str:
        return True
    return False

def exit(n):
    sys.exit(n)
    return True

def usage():
    print 'Usage: ./pid.py -f filename [-s substitue_name] [-v variation_number]'
    return True

#parsing arguments
options, remainder = getopt.getopt(sys.argv[1:], 'hf:s:v:')
filename = ''
subname = ''
varn = 'XX'
for opt, arg in options:
    if opt in ('-f'):
        filename = arg
    elif opt in ('-s'):
        subname = arg
    elif opt in ('-v'):
        varn = arg
    else:
        usage()
        exit(0)
if filename == '':
    usage()
    exit(0)

#find file
matches = []
for root, dirnames, filenames in os.walk('.'):
    for fn in fnmatch.filter(filenames, filename):
        matches.append(os.path.join(root, fn))
if len(matches) == 0:
    print "File not found"
    exit(0)
if len(matches) > 1:
    print "More than 1 file found"
    exit(0)
filename = matches[0]
print 'File found:',filename

#open work book
wb = open_workbook(filename, on_demand = True)
s = wb.sheet_by_name('Summary');

#find base hit rate
base_hit_rate = -0.1
for row in range(s.nrows):
    for col in range(s.ncols):
        value = s.cell(row, col).value
        if not istxt(value):
            continue
        if value.find('Hit Rate') == -1 or value.find('Feature') != -1:
            continue
        value = s.cell(row, col + 1).value
        if type(value) == float:
            base_hit_rate = value
        if base_hit_rate <= 0:
            value = s.cell(row, col + 2).value
            if type(value) == float:
                base_hit_rate = float(value)
        if base_hit_rate <= 0:
            print 'Hit Rate formating not expected'
            exit(0)
        break
    if base_hit_rate > 0:
        break

#find PID
found = -1
for row in range(s.nrows):
    for col in range(s.ncols):
        value = s.cell(row, col).value
        if istxt(value):
            if value.find('PID') != -1:
                found = row
                break
    if found != -1:
        break
if found == -1:
    print 'PID not found'
    exit(0)
print 'PID found on row',found

#find 5 Highest
col_high = -1
row_high = -1
row = found
while row < s.nrows:
    for col in range(s.ncols):
        value = s.cell(row, col).value
        if istxt(value):
            if value.find('Highest') != -1 or value.find('Top 5') != -1:
                col_high = col
                row_high = row
                break
    if col_high != -1 and row_high != -1:
        break
    row = row + 1
if col_high == -1 or row_high == -1:
    print '5 Highest not found'
    exit(0)
print '5 Highest found on [',row_high,',',col_high,']'

#find 5 Lowest
col_low = -1
row_low = -1
row = found
while row < s.nrows:
    for col in range(s.ncols):
        value = s.cell(row, col).value
        if istxt(value):
            if value.find('Lowest') != -1 or value.find('Bottom 5') != -1:
                col_low = col
                row_low = row
                break
    if col_low != -1 and row_low != -1:
        break
    row = row + 1
if col_low == -1 or row_low == -1:
    print '5 Lowest not found'
    exit(0)
print '5 Lowest found on [',row_low,',',col_low,']'

#find 5 Highest and Lowest string
row = row_high
col = col_high
inc = -1
sym_high = []
sym_low = []
rate_high = []
rate_low = []
row_first = -1
row_second = -1
while row < s.nrows:
    value = s.cell(row, col).value
    if istxt(value):
        if value.find(' in ') != -1:
            if row_first == -1:
                row_first = row - 1
            elif row_second == -1:
                row_second = row - 1
                break
    elif type(value) == float:
        if row_first == -1:
            row_first = row - 1
        elif row_second == -1:
            row_second = row - 1
            break
    row = row + 1
inc = row_second - row_first
print '5 Highest/Lowest string found on ',row_first,'with inc',inc

#split string if applicable
i = 0
while i < 5:
    row = row_first + i * inc
    value = s.cell(row, col_high).value
    if not istxt(value):
        print '5 Highest formating not expected'
        exit(0)
    sym_high.append(s.cell(row, col_high).value)
    value = s.cell(row_first + i * inc + 1, col_high).value
    if (not istxt(value)) and type(value) != float:
        print '5 Highest formating not expected'
        exit(0)
    rate_high.append(s.cell(row + 1, col_high).value)
    value = s.cell(row, col_low).value
    if not istxt(value):
        print '5 Lowest formating not expected'
        exit(0)
    sym_low.append(value)
    value = s.cell(row + 1, col_low).value
    if (not istxt(value)) and type(value) != float:
        print '5 Lowest formating not expected'
        exit(0)
    rate_low.append(value)
    i = i + 1

#analyze 5 Highest and Lowest string
num_high = []
num_low = []
symbol_high = []
symbol_low = []
hit_high = []
hit_low = []
i = 0
while i < 5:
    values = sym_high[i].split()
    if len(values) < 2:
        print '5 Highest symbol formating not expected'
        exit(0)
    num_high.append(values[0])
    symbol_high.append(values[len(values) - 1].upper())
    if symbol_high[i].find('SYMBOL') == -1:
        symbol_high[i] = "SYMBOL_" + symbol_high[i]
    if istxt(rate_high[i]):
        values = rate_high[i].split(' in ')
        if len(values) != 2:
            print '5 Highest rate formating not expected'
            exit(0)
        values[1] = values[1].replace(',', '')
        hit_high.append(int(values[1]))
    else:
        if type(rate_high[i]) != float:
            print '5 Highest rate formating not expected'
            exit(0)
        hit_high.append(int(round(rate_high[i])))
    values = sym_low[i].split()
    if len(values) < 2:
        print '5 Lowest symbol formating not expected'
        exit(0)
    num_low.append(values[0])
    symbol_low.append(values[len(values) - 1].upper())
    if symbol_low[i].find('SYMBOL') == -1:
        symbol_low[i] = "SYMBOL_" + symbol_low[i]
    if istxt(rate_low[i]):
        values = rate_low[i].split(' in ')
        if len(values) != 2:
            print '5 Lowest rate formating not expected'
            exit(0)
        values[1] = values[1].replace(',', '')
        hit_low.append(int(values[1]))
    else:
        if type(rate_low[i]) != float:
            print '5 Lowest rate formating not expected'
            exit(0)
        hit_low.append(int(round(rate_low[i])))
    i = i + 1

#find substitue
sub_high = [ 0, 0, 0, 0, 0 ]
if subname != '':
    i = 0
    while i < 5:
        if symbol_high[i].find('_GOLD') == -1:
            continue
        sub_high[i] = 1
        symbol_high[i] = symbol_high[i].replace('_GOLD', '')
        i = i + 1

print '\n=================================================\n'
print 'const PIDInfo_s PIDInfo_v%s =' %varn
print '{'
print '    {'
i = 0
while i < 5:
    if sub_high[i] == 1:
        print '        {',symbol_high[i],',',num_high[i],',',hit_high[i],',',subname,'},'
    else:
        print '        {',symbol_high[i],',',num_high[i],',',hit_high[i],'},'
    i = i + 1
i = 0
while i < 5:
    print '        {',symbol_low[i],',',num_low[i],',',hit_low[i],'},'
    i = i + 1
print '    },'
print '    %3.2f' %base_hit_rate
print '};'
print '\n=================================================\n'

