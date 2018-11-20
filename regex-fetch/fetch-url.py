#Import moudles
import re, sys, getopt, glob, os

# Getopt Parameters
usage = "Usage: filter.py -i html-source-file-name"
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:h', ['ifile=', 'help'])
except getopt.GetoptError:
    print(usage)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(usage)
        sys.exit(2)
    elif opt in ('-i', '--ifile'):
        inf_file = arg
    else:
        print(usage)
        sys.exit(2)


with open(inf_file, 'r', encoding="ascii", errors="surrogateescape") as fp:
   content = fp.read()
   tuples = re.findall(r'client-journal-view-action\" data-url=\"(.*)\">', content)
   #print(tuples)
   for tup in tuples:
      print(tup)