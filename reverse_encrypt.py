#!/usr/bin/python

import sys,re
from pdb import set_trace
from hashlib import md5
import time

##############
## Globals  ##
##############
chars = [chr(i) for i in range(32,127)]

def calc_md5(string):
	""" Calc md5 - 32 hexa digits"""
	return md5(string).hexdigest()

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
		#value 		= ord(char) + int('0x0' + str_password_md5[j:j+1], 16) - int_md5_total
		value 		= ord(char) - int_md5_total		
		md1 		= calc_md5(string[:i+1])[:16]    
		md2 		= calc_md5(str(int_md5_total))[:16]
		# int_md5_total always bigger than 115
		int_md5_total	= eval_cross_total(md1+md2)
		arr_encrypted.append(str(value))
		
	return ' '.join(arr_encrypted)

def decrypt_string(int_arr):
	""" Decrypt int array into string"""
	#chars 		= [ i for i in 'tqpwlie vkstnm']
	j  		= 0
	len_chars	= len(chars)
	len_arr 	= len(int_arr)
	str_pass 	= [None]*32
	loop 		= True
	while loop:
		string 	= ''
		# guess char value
		char 	= chars[j % len_chars]
		k 	= 0
		# m is the guess value of str_password_md5[k]
		m 	= 0
		while str_pass[31]:			
			# guess the int_md5_total value
			int_md5_total 	= ord(char) - int_arr[0] + m
			if int_md5_total < 115:	
				j 	+= 1	
				break
			
			while m < 16:

				str_pass[k] 	= m
				string 		+= char
				k 		+= 1
	
				md1 			= calc_md5(string[:i+1])[:16]    
				md2 			= calc_md5(str(int_md5_total))[:16]
				int_md5_total		= eval_cross_total(md1+md2)
			
				int_char 		= int_md5_total + int_arr[i+1] - m
	
				if int_char not in range(32,127) or int_md5_total < 115:
					m 		+= 1 
					
				char 			= chr(int_char)
				string 			+= char
				set_trace()
	
		# found the right string
		set_trace()
		if encrypt_string(string,'key',str_pass) == int_arr[:32]:
			loop = False
			break
		else:	
			m 	= m + 1 % 16
			string 	= string[:-1]
		j += 1 		
		
	return string		
			
		
	
def main():

	data = "99Z-KH5-OEM-240-1.1QGG-V33-OEM-0B1-1.1Z93-Z29-OEM-BNX-1.1IQ0-PZI-OEM-PK0-1.1UM4-VDL-OEM-B9O-1.1L0S-4R2-OEM-UQL-1.1JBL-EYQ-OEM-ABB-1.1NL1-3V3-OEM-L4C-1.17CQ-1ZR-OEM-U3I-1.1XX0-IHL-OEM-5XK-1.1KJQ-RXG-OEM-TW8-1.1 OZR-LW1-OEM-5EM-1.10B8-6K5-OEM-EFN-1.1OE2-20L-OEM-SSI-1.10ME-HAE-OEM-9XB-1.1"

	data = 'livne kestin age 29 kibbutz gaash'
	a = encrypt_string(data,'pass')
	int_arr = [int(l) for l in a.split(' ')]
	print decrypt_string(int_arr) 
	

if __name__ == '__main__':

	start = time.time()
	if len(sys.argv) != 1:
	    print "Usage: %s ", sys.argv[0]
	    sys.exit(1)
	main()
	print "Time: ",time.time() - start," seconds"

