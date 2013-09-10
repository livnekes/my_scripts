#!/usr/bin/python
from my_connection import *
import sys
import time

REFERER  	    = 	"http://www.enigmagroup.org/forums/index.php"
SITE 	 	    = 	"http://www.enigmagroup.org/"
MISSION_URL 	=   "http://www.enigmagroup.org/missions/programming/1/"
LOGIN 	 	    = 	"http://www.enigmagroup.org/forums/login2/"

def main():
    """ This is the Main function """

    username 	=	 sys.argv[1]
    password 	=	 sys.argv[2]
    ip          =    sys.argv[3]

    login_payload = {
        'user'		    : username,
        'passwrd'		: password,
        'cookielength'	: '-1',
    }

    cookies 	=	 get_url_cookies(LOGIN, REFERER, login_payload)

    payload = {
        'ip'		    : ip,
        'username'		: username,
    }

    cookie      =    makeCookie('mission', 'yes', '.enigmagroup.org')
    cookies.set_cookie(cookie)
    req 	    =	 send_http_post(cookies, MISSION_URL, REFERER, payload)
    #print req.read()

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    if len(sys.argv) != 4:
        print "Usage: %s Username Password IP", sys.argv[0]
        sys.exit(1)
    main()
    print "Time: ",time.time() - start," seconds"


