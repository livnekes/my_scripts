#!/usr/bin/python
from my_connection import *
from BeautifulSoup import BeautifulSoup
from PIL import Image
import sys
import time
from pdb import set_trace

FAKE_REFERER    = 	"admin.enigmagroup.org"
REFERER  	    = 	"http://www.enigmagroup.org/forums/index.php"
MISSION_URL 	=   "http://www.enigmagroup.org/missions/basics/spoof/3/"
LOGIN 	 	    = 	"http://www.enigmagroup.org/forums/login2/"

def main():
    """ This is the Main function """

    username 	=	sys.argv[1]
    password 	=	sys.argv[2]

    login_load  =   {'user':username, 'passwrd':password, 'cookielength':'-1'}
    cookies 	=	get_url_cookies(LOGIN, REFERER, login_load)

    req 	   	=	send_http_post(cookies, MISSION_URL, FAKE_REFERER)
    soup 	    =	BeautifulSoup(req.read())
    print soup
        

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    if len(sys.argv) != 3:
        print "Usage: %s Username Password ", sys.argv[0]
        sys.exit(1)
    main()
    print "Time: ",time.time() - start," seconds"


