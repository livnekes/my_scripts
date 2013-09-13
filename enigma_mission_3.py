#!/usr/bin/python
from my_connection import *
from BeautifulSoup import BeautifulSoup
from PIL import Image
import sys
import time

REFERER  	    = 	"http://www.enigmagroup.org/forums/index.php"
MISSION_URL 	=   "http://www.enigmagroup.org/missions/programming/3/image.php"
LOGIN 	 	    = 	"http://www.enigmagroup.org/forums/login2/"

def download_image(url_path,out_path, cookies):
    """ Download image from url to local disk """

    with open(out_path, 'wb') as f:
        req     =	send_http_post(cookies, url_path, REFERER)
        f.write(req.read())
    f.close()

def get_image_pixel(img):
    """ Get the first pixel of an image """

    pixdata = img.load()
    return pixdata[0,0]

def main():
    """ This is the Main function """

    username 	=	sys.argv[1]
    password 	=	sys.argv[2]

    login_load  =   {'user':username, 'passwrd':password, 'cookielength':'-1'}
    cookies 	=	get_url_cookies(LOGIN, REFERER, login_load)

    download_image(MISSION_URL, 'image.jpeg', cookies)

    img 	    = 	Image.open('image.jpeg')
    img 	    = 	img.convert("RGB")
    pixel 	    = 	get_image_pixel(img)
    color 	    = 	"{0};{1};{2}".format(pixel[0], pixel[1], pixel[2])
    payload     =   {'submit':1, 'color':color}
    req 	   	=	send_http_post(cookies, MISSION_URL, MISSION_URL, payload)
    print req.read()

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    if len(sys.argv) != 3:
        print "Usage: %s Username Password ", sys.argv[0]
        sys.exit(1)
    main()
    print "Time: ",time.time() - start," seconds"


