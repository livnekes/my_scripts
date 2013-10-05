#!/usr/bin/python
from my_connection import *
from BeautifulSoup import BeautifulSoup
from PIL import Image
import sys
import time
from pdb import set_trace

REFERER  	    = 	"http://www.enigmagroup.org/forums/index.php"
MISSION_URL 	=   "http://www.enigmagroup.org/missions/programming/7/"
LOGIN 	 	    = 	"http://www.enigmagroup.org/forums/login2/"

def clean_array(arr):
    """ Remove the unnecessary words from array """

    return [x for x in arr if x not in ('Department:','Monthly','Budget:')]

def parse_string(line):
    """ Parse String to Dictionary """

    arr     =   clean_array(line.split(' '))
    data    =   {}
    for word in arr:
        if word[0] == '$':
            amount = int(word[1:])
            if depart in data:
                data[depart] += amount
            else:
                data[depart] = amount
        else:
            depart = word

    return data

def main():
    """ This is the Main function """

    username 	=	sys.argv[1]
    password 	=	sys.argv[2]

    login_load  =   {'user':username, 'passwrd':password, 'cookielength':'-1'}
    cookies 	=	get_url_cookies(LOGIN, REFERER, login_load)

    req 	   	=	send_http_post(cookies, MISSION_URL, MISSION_URL)
    soup 	    =	BeautifulSoup(req.read())
    p           =   soup.find("p", { "class" : "style7" })
    department  =   soup.find("div", { "class" : "style6" }).next.split(' ')[-2]
    company     =   None
    for line in p:
        if not company:
            company = line.split(' ')[-1]
        if len(line) > 1000:
            data = parse_string(line)

    total       =   data[department]
    payload     =   { 'company' : company, 'department' : department, 'total' : total } 
    req 	   	=	send_http_post(cookies, MISSION_URL + "submit.php", MISSION_URL, payload)
    print req.read()
        

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    if len(sys.argv) != 3:
        print "Usage: %s Username Password ", sys.argv[0]
        sys.exit(1)
    main()
    print "Time: ",time.time() - start," seconds"


