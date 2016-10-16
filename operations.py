import pygame
import math
import numpy as np

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
	return np.matrix((( math.cos(theta),math.sin(theta)),
			          (-math.sin(theta),math.cos(theta))))