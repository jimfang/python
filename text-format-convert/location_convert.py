#!/usr/bin/python

import random
import sys
import string


def istxt(n):
    if type(n) == unicode or type(n) == str:
        return True
    return False

def exit(n):
    sys.exit(n)
    return True
    
    
def main(argv):
  file_input_name = input('Enter input file name: ')
  #'test_src.h'
  #file_output = input('Enter output file name: ')
  #create_random_number_file(name, file_length)
  #count, total = read_random_number_file(name)
  
  #data_array = read_number_from_file(file_input_name) 
  #print data_array
  #write_array_to_file('out2.txt', data_array)
  convert_file(file_input_name, 'out3.txt')
  print()
  pass

def convert_file(file_in, file_out):
  fo = open(file_out, "w")
  with open(file_in) as f:
      data = f. readlines()
      for line in data:
        if line.strip() and line.count(",")==1 : # lines (ie skip them)
    	  #for x in line.split():
	      #  print x.replace(",", "")
	        nums = [int(x.replace(",", "")) for x in line.split()]
	        fo.write("    {%s," % nums[0])
	        fo.write(" %s, MESSAGE_Z},\n" % nums[1])
        else:
            fo.write(line)

  fo.close()



def read_number_from_file(filename):
    data_ar = []
    with open(filename) as f:
      data = f. readlines()
      for line in data:
	if line.strip() and line.count(",")==2 : # lines (ie skip them)
	  #for x in line.split():
	  #  print x.replace(",", "")
	  
	  nums = [int(x.replace(",", "")) for x in line.split()]
	  data_ar.append(nums)
	    
    return data_ar
  
def write_array_to_file(filename, data_array):
  # Open a file
  fo = open(filename, "w")

  # Write sequence of lines at the end of the file.
  for item in data_array:
    #fo.writelines(",".join(map(str,item)))
    fo.write("(640%s" % '{0:+}'.format(int(item[0]-640)))
    fo.write('), ')
    fo.write("(102%s" % '{0:+}'.format(int(item[0]-102)))    
    fo.write('),\n')

  # Close opend file
  fo.close()

def create_random_number_file(filename, length):
    bottom_of_random_range = 1
    top_of_random_range = 100
    file = open(filename, 'w')
    for number in range(length):
        file.write(str(random.randint(bottom_of_random_range, top_of_random_range)) + '\n')
    file.close()


def read_random_number_file(filename):
    file = open(filename, 'r')
    line = file.readline()
    read_count = 0
    random_total = 0
    while line != '':
        print(line.rstrip('\n'))
        random_total += int(line.rstrip('\n'))
        read_count += 1
        line = file.readline()

    return read_count, random_total

if __name__ == "__main__":
  main(sys.argv)
