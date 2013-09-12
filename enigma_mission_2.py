#!/usr/bin/python
from my_connection import *
from BeautifulSoup import BeautifulSoup
import sys
import time

REFERER  	    = 	"http://www.enigmagroup.org/forums/index.php"
MISSION_URL 	=   "http://www.enigmagroup.org/missions/programming/2/"
LOGIN 	 	    = 	"http://www.enigmagroup.org/forums/login2/"

def main():
    """ This is the Main function """

    username 	=	 sys.argv[1]
    password 	=	 sys.argv[2]

    login_payload = {
        'user'		    : username,
        'passwrd'		: password,
        'cookielength'	: '-1',
    }

    cookies 	=	 get_url_cookies(LOGIN, REFERER, login_payload)


    req 	   	=		 send_http_post(cookies, MISSION_URL, REFERER)
    soup 	    =	 BeautifulSoup(req.read())
    inputs 	    =	 soup.findAll('input')
    enumber     =	 int(inputs[1]['value'])
    etime 	    =	 inputs[2]['value']
    ehash 	    =	 inputs[3]['value']
    answer 	    =	 enumber * 4

    payload = {
        'answer'	    : answer,
        'E[number]'		: enumber,
        'E[time]'       : etime,
        'hash'          : ehash,
        'submit'        : 'Submit Answer'
    }

    req 	    =	 send_http_post(cookies, MISSION_URL+"index.php", REFERER, payload)
    print req.read()

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    if len(sys.argv) != 3:
        print "Usage: %s Username Password ", sys.argv[0]
        sys.exit(1)
    main()
    print "Time: ",time.time() - start," seconds"


