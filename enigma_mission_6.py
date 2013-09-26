#!/usr/bin/python
import sys
import time
from pdb import set_trace
from BeautifulSoup import BeautifulSoup
from my_connection import *

REFERER 	=   "http://www.enigmagroup.org/forums/index.php"
MISSION_URL 	=   "http://www.enigmagroup.org/missions/programming/6/"
LOGIN 		=   "http://www.enigmagroup.org/forums/login2/"

def read_dict_words():
	""" Read a dictionary file with words """
	f = open('keywords.txt','r')
	words = []
	for line in f:
    		words.append(line.strip())

	f.close()
	return words

def unscramble_word(scram_word, words):
	""" Find the unscramble word in the dictionary """ 
	for word in words:
		if are_eq(list(scram_word),list(word)):
			return word
	print scram_word
	return 'not found'

def unscramble_words(scram_words, words):
	""" Find the unscramble words """ 

	unscram_words = []
	for word in scram_words:
		unscram_words.append(unscramble_word(word, words))
	return unscram_words

def are_eq(a, b):
	""" Check if two arrays have the same chars """
	return set(a) == set(b) and len(a) == len(b)

def get_scram_words(cookies):	
	req 	=	 send_http_post(cookies, MISSION_URL, REFERER)
	soup 	=	 BeautifulSoup(req.read())
	scram_words = []
	inputs 	=	 soup.findAll('p')[0]
	for word in inputs:
		if word.string:
			scram_words.append(word[1:])
	return scram_words[:-1]
	

def main():
	""" This is the Main function """

	username 	=	sys.argv[1]
	password 	=	sys.argv[2]

	login_load  	= 	{'user':username, 'passwrd':password, 'cookielength':'-1'}
	cookies 	=	get_url_cookies(LOGIN, REFERER, login_load)

	dict_words	= 	read_dict_words()
	scram_words 	= 	get_scram_words(cookies)
	words 		= 	unscramble_words(scram_words, dict_words)

	payload 	=   	{'anagram':','.join(words), 'submit':'true'}
	req   		=	send_http_post(cookies, MISSION_URL+'submit.php', MISSION_URL, payload)
	print req.read()
 
if __name__ == '__main__':

	if len(sys.argv) != 3:
	    print "Usage: %s username password", sys.argv[0]
	    sys.exit(1)

	main()

