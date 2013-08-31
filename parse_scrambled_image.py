#!/usr/bin/python
import sys
from pdb import set_trace
import time
from PIL import Image,ImageDraw
from random import randint as rint
import os

WHITE_RGB = (255,255,255)

def draw_image(lines,im,pix):
	width,hight = im.size
	for y,line in enumerate(lines):
		for x,pixel in enumerate(line):
			pix[x,y] = pixel
	return	pix

def split_to_lines(pix,width,hight):
	lines = []
	for y in range(hight):
		line = []
		for x in range(width):
			line.append(pix[x,y])
		lines.append(line)
	return lines

def find_nearest_line(line1, lines):
	smallest_dist = float("inf")
	index = 0
	for i,line in enumerate(lines):
		dist = calc_dist_lines(line1,line)
		if dist < smallest_dist:
			smallest_dist = dist
			index = i
	return lines[index]

def calc_dist_lines(l1,l2):
	dist = 0.0
	for i,p1 in enumerate(l1):
		dist += calc_dist_points(p1,l2[i])
	return dist		

def calc_dist_points(p1,p2):
	sum_dist = 0.0
	for i in range(3):
		sum_dist += (p1[i] - p2[i])*(p1[i] - p2[i])
	return sum_dist

def get_sorted_lines(lines,r):
	sorted_lines = []
	l1 = lines[r]
	sorted_lines.append(l1)
	for i in range(len(lines)):
		lines.remove(l1)
		if lines:
			l2 = find_nearest_line(l1,lines)
			l1 = l2
			sorted_lines.append(l2)
	return sorted_lines

def copy_lines(lines):
	n_lines = []
	for line in lines:
		cline = []
		for tup in line:
			cline.append(tup)
		n_lines.append(cline)
	return n_lines

def remove_colors(lines,colors):
	for line in lines:
		for i,tup in enumerate(line):
			if tup not in colors:
				line[i] = WHITE_RGB

def remove_line(lines,index):
	for i,tup in enumerate(lines[index]):
		lines[index][i] = WHITE_RGB

def tup2str(tup):
	arr = []
	for i in tup:
		arr.append(str(i))
	return ','.join(arr)

def str2tup(string):
	arr = string.split(',')
	for i,val in enumerate(arr):
		arr[i] = int(val)
	return tuple(arr)

def count_colors(lines):
	colors = {}
	for line in lines:
		for tup in line:
			str_tup = tup2str(tup)
			if str_tup not in colors:
				colors[str_tup] = 1	
			else:
				colors[str_tup] += 1	
	return colors

def get_color_line_numbers(lines):
	nums = []
	for i,line in enumerate(lines):
		for tup in line:
			if tup != WHITE_RGB:
				nums.append(i)
	return list(set(nums))	

def get_main_colors(lines):
	colors = []
	col = count_colors(lines)
	for co in col:
		rgb = str2tup(co)
		if col[co] > 50 and rgb != (255,255,255):
			colors.append(rgb)
			continue
	return colors	

def clear_images():
	os.system("rm *test*.png")	

def check_all_distances(lines):
	dist = 0
	for i in range(len(lines) - 1):
		dist += calc_dist_lines(lines[i],lines[i+1])
		
	return dist

def iterate_all_color_lines(lines,nums):
	min_dist = float("inf")
	for i in nums:
		l1 = copy_lines(lines)
		new_lines = get_sorted_lines(l1,i)
		dist = check_all_distances(new_lines)
		if dist < min_dist:
			min_dist = dist
			sorted_lines = new_lines
	return sorted_lines	

def main():

	clear_images()
	img_path = sys.argv[1]
	im = Image.open(img_path)
	width,hight = im.size
	pix = im.load()
	lines = split_to_lines(pix,width,hight)	
	
	colors = get_main_colors(lines)	
	remove_colors(lines,colors)
	pix = draw_image(lines,im,pix)
	
	im.save('test.png')
	im = Image.open('test.png')
	width,hight = im.size
	pix = im.load()
	lines = split_to_lines(pix,width,hight)
	fname = 'test'	

	lines2 = copy_lines(lines)
	col1 = colors[0]
	col2 = colors[1]
	remove_colors(lines,[col1])
	nums = get_color_line_numbers(lines)

	new_lines = iterate_all_color_lines(lines,nums)
	pix = draw_image(new_lines,im,pix)
	im.save("sorted_color1_{0}.png".format(fname))

	remove_colors(lines2,[col2])
	nums = get_color_line_numbers(lines2)

	new_lines = iterate_all_color_lines(lines2,nums)
	pix = draw_image(new_lines,im,pix)
	im.save("sorted_color2_{0}.png".format(fname))


if __name__ == '__main__':

	if len(sys.argv) != 2:
	    print "Usage: %s file", sys.argv[0]
	    sys.exit(1)
	start_time = time.time()
	main()
	print time.time() - start_time, "seconds"

