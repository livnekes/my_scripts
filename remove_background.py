#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageChops, ImageFilter
from pdb import set_trace
import glob

white_rgb = (255,255,255)
min_dist = 500

##############################################################
#   returns the average pixel of a rectangle area
##############################################################
def get_mean_pixels_values_area(pix_map, l_x, l_y, r_x, r_y):
    global white_rgb

    # dims is the dimension of the pix format (RGB => 3)
    dims = [0] * len(pix_map[l_x, l_y])
    area_size = (r_x-l_x) * (r_y-l_y)

    total_samples = 0
    for i in range(r_x-l_x+1):
        for j in range(r_y-l_y+1):
            if pix_map[l_x+i, l_y+j] == white_rgb:
                continue
            total_samples += 1                        

            for d in range(len(dims)):
                dims[d] += pix_map[l_x+i, l_y+j][d]

    if total_samples < area_size / 2:
        return white_rgb
                
    for d in range(len(dims)):
        try:
            dims[d] /= total_samples
        except:
            dims = white_rgb
            
    return dims

#############################################
#   returns the distance between two pixels 
#############################################
def get_euclidean_dist(pix1, pix2):
    total_sum = 0.0 
    for i in range(len(pix1)):
        total_sum += (pix1[i]-pix2[i])**2
    return total_sum

##########################################
#   remove the background from an image
##########################################
def remove_background(im):    

    width,height = im.size
    pix_mat	= im.load()

    arr1 = range(height)
    arr2 = range(10,width - 1)
    clear_matrix_helper(pix_mat, arr1, arr2, 1)

    arr1 = range(height)
    arr2 = range(1,width - 10)
    arr2.reverse()
    clear_matrix_helper(pix_mat, arr1, arr2, -1)

    return im

##########################################
#   remove pixels in matrix
##########################################
def clear_matrix_helper(pix_mat, arr1, arr2, k):
    global min_dist
    skip = False
    for j in arr1:
        for i in arr2:
            pix = pix_mat[i,j]
            if skip or pix == white_rgb:
                continue
            next_pix = pix_mat[i+k,j]
            dist = get_euclidean_dist(pix, next_pix)
            if dist < min_dist:
                pix_mat[i,j] = white_rgb
            else:
                skip = True
        skip = False

####################
#   trim image
####################
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((10,10)))
    diff = ImageChops.difference(im, bg)
    #diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        # found no content
        raise ValueError("cannot trim; image was empty")

####################
#   test function
####################
def test():

    if len(sys.argv) < 2:
        sys.exit("Usage: %s fuzz_factor " % sys.argv[0])

    min_dist = int(sys.argv[1])

    images = glob.glob('test[0-9]*.jpg')
    print images
    for name in images:
        prefix = name.split('.')[0]
        sufix = name.split('.')[1]

        im = Image.open(name)
        
        im = im.filter(ImageFilter.FIND_EDGES)
        
        im.save("test_imgs/inverts/{}_test.{}".format(prefix, sufix))
    
####################
#   main function
####################
def main():
    global min_dist

    if len(sys.argv) < 2:
        sys.exit("Usage: %s fuzz_factor " % sys.argv[0])

    min_dist = int(sys.argv[1])

    images = glob.glob('test[0-9]*.jpg')
    print images
    for name in images:
        im = Image.open(name).convert("RGB")
        prefix = name.split('.')[0]
        sufix = name.split('.')[1]

        im = remove_background(im)
        width,height = im.size
        box = (10, 0, width-10, height)
        im = im.crop(box)
        im.save("test_imgs/{}_cropped".format(prefix), "PNG")

if __name__ == '__main__':
    main()
    test()

