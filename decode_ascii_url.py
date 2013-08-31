#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import urllib 
import sys,re
from pdb import set_trace
import time
import urllib2
import requests

URL = "https://www.hackthissite.org/missions/prog/11/"


def parse_str(arr,shift):
	return ''.join([chr(int(i)-shift) for i in arr])
	

def main():
	#res = requests.get(URL, auth=('username', 'password'))
	#cookies = res.cookies
	
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', 'PHPSESSID=rvqudg7obbfh8rhp8803a6cli2'))
	opener.addheaders.append(('Referer', 'https://www.hackthissite.org/'))
	f = opener.open(URL)
	source = f.read()

	soup = BeautifulSoup(source)
	for tb in soup.table:
		match = re.search('<br />Generated String:.*<br />',str(tb))
		if match:
			arr = match.group(0).split('<br />')
	
	for a in arr:
		if a == '':
			continue

		if re.search('Generated String',a):
			print a
			digits = re.findall(r'\d+', a)
		else:
			print a
			shift = int(re.findall(r'\d+', a)[0])
			if re.search('-',a):
				shift = 0-shift
					
	answer = parse_str(digits,shift)

	#cookie = {'PHPSESSID':'rvqudg7obbfh8rhp8803a6cli2'}
	payload = {'solution': answer}
	print payload
	#res = requests.post("https://www.hackthissite.org/missions/prog/11/index.php", cookies=cookie, data=payload)
	
	
	url = URL + '/index.php'
	
	data = urllib.urlencode(payload)
	req = urllib2.Request(url, data)
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', 'PHPSESSID=rvqudg7obbfh8rhp8803a6cli2'))
	opener.addheaders.append(('Referer', 'https://www.hackthissite.org/'))
	f = opener.open(req)
	source = f.read()
	print source
	

if __name__ == '__main__':

	start = time.time()
	if len(sys.argv) != 1:
	    print "Usage: %s ", sys.argv[0]
	    sys.exit(1)
	main()
	print "Time: ",time.time() - start," seconds"


