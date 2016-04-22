# -*- coding: utf-8 -*-
#the whole program

#(1) Imports:
import os
import copy
import shutil
import getopt
from xlrd import open_workbook

import sys;
reload(sys);
sys.setdefaultencoding("utf-8")

def sprintf(buf, fmt, *args):
    buf.write(fmt % args)
	
def usage():
    print 'Usage: rename-10-id.py -f filename -s src_folder -d dest_folder -k key_filter '
    return True

#parsing arguments
options, remainder = getopt.getopt(sys.argv[1:], 'hs:f:k:d:')
src_xls = ''
key_filter = ''
src_name = ''
dest_name =''

for opt, arg in options:
	if opt in ('-k'):
		key_filter = arg
	elif opt in ('-f'):
		src_xls = arg
	elif opt in ('-s'):
		src_name = arg
	elif opt in ('-d'):
		dest_name = arg
	else:
		usage()
		exit(0)
		
#if key_filter == '':
#    usage()
#    exit(0)
	
#(2) List files:
path = os.getcwd()
files = os.listdir(path)

if src_name != '':
	src_path = os.path.join(path, src_name)
	print src_path	
	files_src = os.listdir(src_path)

new_path = os.path.join(path, dest_name)
print new_path
directory = new_path
if not os.path.exists(directory):
    os.makedirs(directory)
	
#(3) Pick out 'src' files:
if files_src:
	files_jpg = [f for f in files_src if f[-3:] == 'jpg' or f[-3:] == 'JPG' or f[-3:] == 'png' or f[-3:] == 'PNG']
#print 'file number = ', len(files_jpg)

#(4) Pick out 'xls' files:
files_xls = [f for f in files if f[-3:] == 'xls']
#print files_xls

#(5) Loop over list of files to append to empty dataframe:
#for f in files_xls:
#    data = pd.read_excel(f, 'Sheet1')
#open work book
if src_xls != '':
	filename = src_xls
else:
	filename = files_xls[0]
	
wb = open_workbook(filename, on_demand = True)
s = wb.sheet_by_index(0); #sheet_by_name('Summary');

int_search_index = 1
offset = 1
int_col_code = 0 #transport code
int_col_be = 1+offset
int_col_aol = 2+offset # ao code
int_col_name = 7+offset # name
int_col_idcn = 8+offset

#total row numbers
int_rows_total = s.nrows
my_dict = {}
#minor title row 0
print 'total row = ', int_rows_total-1

value_be = []
value_aol = []
value_name = []
value_idcn = []

for row in range(int_search_index, s.nrows):
	str_cmp = ''
	code = str(s.cell(row, int_col_code).value)
	#value_aol = str(s.cell(row, int_col_aol).value)
	value_be = str(s.cell(row, int_col_be).value)
	value_name = (s.cell(row, int_col_name).value)
	value_idcn = str(s.cell(row, int_col_idcn).value)
	
	#print code_len
	str_cmp +=code +'-'+value_be+'-'+value_name+'-'+value_idcn
	#str_cmp +=code +'-'+ value_aol +'-'+value_name+'-'+value_idcn
	
	if key_filter in code:
		#ignore empty code 
		if code != '':
			my_dict[code] = str_cmp

number_uitem = len(my_dict)
		
files_tmp = copy.deepcopy(files_jpg)
newfile = ''

for key in (my_dict):  
	found = 0
	value_idcn = my_dict[key][-18:]
	
	code_len = len(key)
	#print code_len
	#print value_idcn
	#print 'key=%s, value=%s' % (key, my_dict[key])  
	#print 'key= %s -----' %(key)
	#print my_dict[key]
	#search in file jpg list
	for item in files_jpg:
		#print item[0:17]
		#if item.find(my_dict[key]):
		#if item[0:17] in my_dict[key][0:17]:
		#print item#[-24:]
		if value_idcn in item[-22:]:
			if key in item[:code_len]:
				#print '--found--'
				#print item
				#copy 
				if dest_name != '':				
					srcname = os.path.join(src_path, item)
					#newfile = my_dict[key]+item[-6:]
					newfile = '10_' + my_dict[key][code_len+1:code_len+14]+item[-4:]
					dest_name = os.path.join(new_path, newfile)
					#print srcname
					#print dest_name
					#shutil.copy2(srcname, new_path)
					shutil.copy(srcname, dest_name)
				
				files_tmp.remove(item)
				found += 1

	if found >= 1:
		my_dict[key] = ''

	
print '--Done IE ID --'
	
