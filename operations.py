import pygame
import math

def vec2unit(arr):
    mag = (arr[0]**2 + arr[1]**2)**0.5
    return (arr[0]/mag,arr[1]/mag)

def vec2ori(arr):
    return math.atan2(arr[1],arr[0])

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
	
def rot_matrix(theta):
	""" clockwise angle rotation matrix """
	return (( math.cos(theta),math.sin(theta)),
		    (-math.sin(theta),math.cos(theta)))
					  
def matrix_op(matrix,arr):
	return (arr[0]*matrix[0][0]+arr[1]*matrix[0][1],\
			arr[0]*matrix[1][0]+arr[1]*matrix[1][1])
			
def arr_add(arr0,arr1):
	return (arr0[0]+arr1[0],arr0[1]+arr1[1])
	
def arr_sub(arr0,arr1):
	return (arr0[0]-arr1[0],arr0[1]-arr1[1])
	    
def cloud_matrix_op(matrix,cloud):
    cloud_out = []
    for i in range(len(cloud)):
        cloud_out.append(matrix_op(matrix,cloud[i]))
    return cloud_out

def cloud_add(cloud,arr):
    cloud_out = []
    for i in range(len(cloud)):
        cloud_out.append(arr_add(cloud[i],arr))
    return cloud_out
    
def vert_intercept(line,x):
    if line[1][0]-line[0][0] == 0:
        return None    
    slope = (line[1][1]-line[0][1])/(line[1][0]-line[0][0])
    return x*slope+line[1][1]-line[1][0]*slope

def in_bounds(bounds,point):
    intercepts = 0
    for i in range(len(bounds)):
        if i == len(bounds)-1:
            line = (bounds[i],bounds[0])
        else:
            line = (bounds[i],bounds[i+1])
        # check if point is outside x bounds
        if not((point[0] > line[0][0] and point[0] < line[1][0]) or \
            (point[0] < line[0][0] and point[0] > line[1][0])):
            continue
        y = vert_intercept(line,point[0])
        if y is not None and point[1] > y: # check if point_y is above the vertical intersect (y)
            #print 'check'
            #print line
            #print point            
            intercepts = intercepts + 1
    #print 'intercepts = %d' % intercepts
    return intercepts % 2 == 1 
        
    
    
    
    
    
