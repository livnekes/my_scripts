#!/usr/bin/python
import sys
from pdb import set_trace
import time

def read_file():
	f = open('wordlist.txt','r')
	words = []
	for line in f:
    		words.append(line.strip())

	f.close()
	return words

def find_word(i,words):
	arr1 = get_arr(i)
	for word in words:
		arr2 = get_arr(word)
		if are_eq(arr1,arr2):
			return word
	return 'not found'

def are_eq(a, b):
    return set(a) == set(b) and len(a) == len(b)

def get_arr(word):
	arr = []
	for l in word:
    		arr.append(l)	
	return arr

def read_scram_words():	
	f = open('scram_words.txt','r')
	words = []
	for line in f:
		if line.strip() == '':
			continue
    		words.append(line.strip())
	f.close()
	return words

def main():
	
	inputs = read_scram_words()
	words = read_file()
	result = []
	for i in inputs:
		result.append(find_word(i,words))
	print ','.join(result)
		
 
if __name__ == '__main__':

	if len(sys.argv) != 1:
	    print "Usage: %s ", sys.argv[0]
	    sys.exit(1)

	main()

