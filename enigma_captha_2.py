#!/usr/bin/python
from my_connection import *
import subprocess
from PIL import Image
import sys
import time
from pdb import set_trace

REFERER 	=   "http://www.enigmagroup.org/forums/index.php"
MISSION_URL 	=   " http://www.enigmagroup.org/missions/captcha/2/image.php"
LOGIN 		=   "http://www.enigmagroup.org/forums/login2/"
WHITE_RGB 	=   (255, 255, 255)

def download_image(url_path,out_path, cookies):
    """ Download image from url to local disk """

    with open(out_path, 'wb') as f:
        req     =	send_http_post(cookies, url_path, REFERER)
        f.write(req.read())
    f.close()

def readText():
    """ Read txt from file """

    with open('image.txt','r') as f:
        text = f.read()
    f.close()
    return text

def cleanImage():
    """ Remove distracting colors from image """

    img 	    = 	Image.open('image.png')
    img 	    = 	img.convert("RGB")
    width,height    =   img.size
    print width, height
    px 	            =   img.load()

    colors 	    =   {}

    for y in range(height):
        for x in range(width):
       	    col = px[x,y]
	    str_col = '{0}{1}{2}'.format(col[0], col[1], col[2])
	    if col == WHITE_RGB:
		continue
            if col != (41,36,33):
		px[x,y] = WHITE_RGB
	    if str_col not in colors:
	   	colors[str_col] = 1
	    else:
	   	colors[str_col] += 1
    img.save('image2.png')



def main():
    """ This is the Main function """

    username 	=	sys.argv[1]
    password 	=	sys.argv[2]

    login_load  = 	{'user':username, 'passwrd':password, 'cookielength':'-1'}
    cookies 	=	get_url_cookies(LOGIN, REFERER, login_load)

    download_image(MISSION_URL, 'image.png', cookies)
    cleanImage()
    cmd 	=   	"tesseract image2.png image && cat image.txt"
    process 	=  	subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    text 	= 	readText()
    print text

    payload 	=   	{'submit':True, 'answer':text}
    req   	=	send_http_post(cookies, MISSION_URL, MISSION_URL, payload)
    print req.read()

if __name__ == '__main__':
    """ Start main """

    start = time.time()
    if len(sys.argv) != 3:
        print "Usage: %s Username Password ", sys.argv[0]
        sys.exit(1)
    main()
    print "Time: ",time.time() - start," seconds"


