  # -*- coding: utf-8 -*
  
import os

import sys;
reload(sys);
sys.setdefaultencoding("utf-8")

def merge_sort(ary):
    if len(ary) <= 1 : return ary
    num = int(len(ary)/2)      
	#divided 2 branches
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left,right)   

def merge(left,right):
    #'''merge
    #sorted left and right to one big sorted '''
    l,r = 0,0        
    result = []
    while l<len(left) and r<len(right) :
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
	print "l, r", l, r
	print result, "--", left[l:], "--", right[r:]
    result += left[l:]
    result += right[r:]
    print result
    print "=============="
    return result
	

mylist = [6, 5, 3, 1, 8, 7, 2, 4, 9, 0]

sortlist = merge_sort(mylist)
print sortlist