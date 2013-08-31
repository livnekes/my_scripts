#!/usr/bin/python

import sys,re
from pdb import set_trace
from hashlib import md5
import time
from threading import Thread, Lock

##############
## Globals  ##
##############
chars = [chr(i) for i in range(65,91)]
chars.extend([str(i) for i in range(10)])
debug = True 
debug = False
spacing_chars = ['.','-','\n']
known_chars = [i for i in chars]
known_chars.extend(spacing_chars)
decrypt_str_password_md5 = None
max_threads = 10
lock = Lock()


def calc_md5(string):
	""" Calc md5 - 32 hexa digits"""
	return md5(string).hexdigest()

def to_string(int_arr):
	""" turn int array into string""" 
	return ' '.join([str(i) for i in int_arr])

def get_new_int_md5_total(string, int_md5_total):
	"""" helper method for calc int_md5_total"""
	md1 	= calc_md5(string)[:16]    
	md2 	= calc_md5(str(int_md5_total))[:16]
	return eval_cross_total(md1+md2)

def eval_cross_total(str_md5):
	""" Calc the sum of all hexa digits in the md5 string.
	The sum is between 0 and 32*15 =480 """
	int_total = 0
	for char in str_md5:
		int_total += int('0x0' + char, 16)
	return int_total

def encrypt_string(string, password,str_password_md5=False):
	""" Encrypt string with password """
	if not str_password_md5:
		str_password_md5 	= calc_md5(password)
        int_md5_total	 	= eval_cross_total(str_password_md5)
        arr_encrypted 	 	= []
        for i,char in enumerate(string):
		j 		= i%32
		value 		= ord(char) + int('0x0' + str_password_md5[j:j+1], 16) - int_md5_total
		md1 		= calc_md5(string[:i+1])[:16]    
		md2 		= calc_md5(str(int_md5_total))[:16]
		if debug:
			print 'string[i],md1,md2 are: ', string[:i+1],md1,md2
			print 'ord(char) is: ' , ord(char)
			print 'int_md5_total is: ' , int_md5_total
			print 'str_password_md5[j:j+1] is: ' +  str_password_md5[j:j+1]
		# int_md5_total always bigger than 115
		int_md5_total	= eval_cross_total(md1+md2)
		arr_encrypted.append(str(value))
		
	return ' '.join(arr_encrypted)

def decrypt_int_array(int_arr, str_password_md5):
	""" Decrypt the int_array into string 
	    when the str_password_md5 is known """
	string 	 		= ''
	int_md5_total	 	= eval_cross_total(str_password_md5)
	for i,value in enumerate(int_arr):
		j 		= i%32
		string 		+= chr(value - int('0x0' + str_password_md5[j], 16) + int_md5_total)
		md1 		= calc_md5(string)[:16]    
		md2 		= calc_md5(str(int_md5_total))[:16]
		int_md5_total	= eval_cross_total(md1+md2)
		
	return string
			
def decrypt_string(int_arr):
	""" Decrypt int array into string"""
	for int_md5_total in range(115,481):
		for char in chars:
			str_md5_pass 	= [None]*40
			j 		= int_arr[0] - ord(char) + int_md5_total
			if j not in range(16):
				continue
			str_md5_pass[0] = hex(j)[-1]
			thread = Thread(target = decrypt_recursive, args = (char, int_md5_total, int_arr, 0, str_md5_pass))
    			thread.start()
			thread.join()
 
def decrypt_recursive(string, int_md5_total, int_arr, pos, str_md5_pass):	
	""" Decrypt recursive int array into string"""
	global decrypt_str_password_md5
	if pos in (3,7,11,15,23,27,31,35) and string[pos] != '-':
		return False
	elif pos in (8,28) and string[pos] != 'O':
		return False
	elif pos in (9,29) and string[pos] != 'E':
		return False
	elif pos in (10,30) and string[pos] != 'M':
		return False
	elif pos in (16,18,36,38) and string[pos] != '1':
		return False
	elif pos in (17,37) and string[pos] != '.':
		return False
	elif pos in [19] and string[pos] != '\n':
		return False
	elif pos == 39 and string[pos] == '\n':	
		str_md5_test = ''.join(str_md5_pass[:32])
		print string
		if decrypt_int_array(int_arr[:40], str_md5_test) == string:
			lock.acquire()
			decrypt_str_password_md5 = str_md5_test
			lock.release()
			return True
		return False

	elif pos in (0,1,2,4,5,6,12,13,14,20,21,22,24,25,26,32,33,34) and string[pos] in spacing_chars:
		return False

	int_md5_total	  = get_new_int_md5_total(string, int_md5_total)
	int_char 	  = int_md5_total + int_arr[pos+1] 
	for i in range(16):
		try:
			char 	= chr(int_char - i)
			if char not in known_chars:
				continue
			str_md5_pass[pos+1] = hex(i)[-1]
			res 	= decrypt_recursive(string + char, int_md5_total, int_arr, pos+1, str_md5_pass)
			if res:
				return res
		except:
			continue
	return False

	
def main():
	global decrypt_str_password_md5
	data_example = "99Z-KH5-OEM-240-1.1\nQGG-V33-OEM-0B1-1.1\nZ93-Z29-OEM-BNX-1.1\nIQ0-PZI-OEM-PK0-1.1\nUM4-VDL-OEM-B9O-1.1\
\nL0S-4R2-OEM-UQL-1.1\nJBL-EYQ-OEM-ABB-1.1\nNL1-3V3-OEM-L4C-1.1\n7CQ-1ZR-OEM-U3I-1.1\nXX0-IHL-OEM-5XK-1.1\nKJQ-RXG-OEM-TW8-1.1\
\nOZR-LW1-OEM-5EM-1.1\n0B8-6K5-OEM-EFN-1.1\nOE2-20L-OEM-SSI-1.1\n0ME-HAE-OEM-9XB-1.1\n"
	
	# each serial number has 20 digits
	a = encrypt_string(data_example,'pass')
	a = '-152 -205 -158 -178 -163 -179 -129 -154 -156 -166 -161 -200 -135 -182 -192 -195 -160 -159 -213 -211 -109 -181 -138 -191 -139 -133 -167 -160 -132 -193 -143 -236 -163 -186 -198 -191 -185 -198 -223 -163 -172 -160 -186 -227 -119 -146 -177 -180 -96 -151 -157 -146 -182 -161 -126 -153 -203 -159 -162 -258 -145 -191 -181 -197 -178 -120 -128 -195 -197 -153 -128 -212 -176 -148 -157 -194 -171 -216 -143 -236 -154 -224 -154 -189 -129 -167 -220 -202 -167 -133 -173 -196 -122 -174 -237 -201 -212 -186 -204 -233'
	int_arr = [int(l) for l in a.split(' ')]
	
	decrypt_string(int_arr) 
	if decrypt_str_password_md5:
		print decrypt_int_array(int_arr, decrypt_str_password_md5)
	

if __name__ == '__main__':
	
	start = time.time()
	if len(sys.argv) != 1:
	    print "Usage: %s ", sys.argv[0]
	    sys.exit(1)
	main()
	print "Time: ",time.time() - start," seconds"

