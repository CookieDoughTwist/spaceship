import pygame
import math
import operations
import copy

class baryon(object):
	""" Holds Baryonic Data """
	def __init__(self,parent_id=-1):
		self.id = baryon.id
		self.parent_id = parent_id
		baryon.id += 1
		self.x = 0
		self.y = 0
		self.vel_x = 0
		self.vel_y = 0
		self.ori = 0
		self.vel_ori = 0
		self.mass = 1		
		self.thrust = .1
		
	def update_image(self,image_load,image_frac):
		rec = image_load.get_rect().size
		self.image = pygame.transform.scale(image_load,(rec[0]/image_frac,rec[1]/image_frac))
		
	def move(self,x,y):
		self.x = x
		self.y = y
	
	def set_ori(self,ori):
		self.ori = ori
	
	def prop(self):
		self.x += self.vel_x
		self.y += self.vel_y
		self.ori += self.vel_ori
		
	def rot_left(self):
		self.ori += .1
		
	def rot_right(self):
		self.ori -= .1
	
	def get_image(self):
		return operations.rot_center(self.image,self.ori / (2*math.pi) * 360 - 90)		

baryon.id = 0		
	
def display(screen,baryon):
	image = baryon.get_image()
	center = image.get_rect().center
	screen.blit(image,(baryon.x-center[0],baryon.y-center[1]))		
	
	
def boost(baryon):
	baryon.vel_x += (baryon.thrust / baryon.mass) * math.cos(baryon.ori)
	baryon.vel_y -= (baryon.thrust / baryon.mass) * math.sin(baryon.ori)
	
def torque_boost_left(baryon):
	baryon.vel_ori += .001
	
def torque_boost_right(baryon):
	baryon.vel_ori -= .001
	
def fire(baryon,image):
	missile = copy.copy(baryon)
	missile.update_image(image,50)
	missile.id = 1
	missile.thrust = .5
	return missile
	
	