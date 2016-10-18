import pygame
import math

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
	
def vert_intercept(line,x):	
	if line[1][0]-line[0][0] == 0:
		return None
	slope = (line[1][1]-line[0][1])/(line[1][0]-line[0][0])
	return x*slope+line[1][1]-line[1][0]*slope