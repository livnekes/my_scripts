#!/usr/bin/python
import sys,re
from pdb import set_trace
from hashlib import md5
import time

##############
## Globals  ##
##############
# chars is all digit and all lowercase chars
chars = [chr(i) for i in range(97,123)]
chars.extend([str(i) for i in range(10)])
debug = True
debug = False

def calc_md5(string):
	""" Calc md5 - 32 hexa digits"""
	return md5(string).hexdigest()

def brute_force_rec(string, md5_pass):
    """ Decyper md5 hash """
    if len(string) > 6:
        return False
    if calc_md5(string) == md5_pass:
        return string
    for char in chars:
        if len(string) and string[-1] == char:
            continue
        res = brute_force_rec(string+char, md5_pass)
        if res:
            return res
    return False

def main():
    """ Brute force md5 hash """
    md5_pass = sys.argv[1]
    print brute_force_rec('f', md5_pass)

if __name__ == '__main__':

	start = time.time()
	if len(sys.argv) != 2:
	    print "Usage: %s pass 2 crack", sys.argv[0]
	    sys.exit(1)
	main()
	print "Time: ",time.time() - start," seconds"

