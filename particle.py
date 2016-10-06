import pygame
import math
import operations
import copy

class baryonic_state(object):
	""" Holds Baryonic Data """
	def __init__(self,parent_id=-1):
		self.id = baryonic_state.id
		baryonic_state.id += 1
		self.x = 0
		self.y = 0
		self.vel_x = 0
		self.vel_y = 0
		self.ori = 0
		self.vel_ori = 0
		self.mass = 1		
	
	def move(self,x,y):
		self.x = x
		self.y = y
	
	def set_ori(self,ori):
		self.ori = ori
	
	def prop(self):
		self.x += self.vel_x
		self.y += self.vel_y
		self.ori += self.vel_ori
		
	def acc(self,ddx,ddy):
		self.vel_x += ddx
		self.vel_y += ddy
		
	def rot_acc(self,ddori):
		self.vel_ori += ddori
		

baryonic_state.id = 0		
	
class ship(object):
	""" Holds ship data """
	def __init__(self,init_ticks,image_dict):		
		self.thrust = .1
		self.init_ticks = init_ticks
		self.fire_cd = 1000 # miliseconds
		self.last_fire = -float('inf')
		
		self.state = baryonic_state()		
		self.left = False
		self.right = False
		
		self.image_dict = image_dict
		
		rocket_image = image_dict['rocket']
		rec = rocket_image.get_rect().size
		self.image = pygame.transform.scale(rocket_image,(rec[0],rec[1]))
		flame_image = image_dict['flame']
		rec = flame_image.get_rect().size
		self.flame_image = pygame.transform.scale(flame_image,(rec[0],rec[1]))
		

	def prop(self):
		self.state.prop()
		
	def maneuver(self,commands):
		""" commands = (up,down,left,right,ctrl) """
		#  (1,-1)  (1,0)  (1,1)
		#  (0,-1)  (0,0)  (0,1)
		# (-1,-1) (-1,0) (-1,1)
		direction = (commands[0] - commands[1], commands[3] - commands[2])
		self.left = False
		self.right = False
		if (0,0) == direction:
			return
			
			
		if commands[4]:
			# Ion thrusters
			if (1,-1) == direction:
				self.rcs_pro()
			elif (1,0) == direction:
				self.rcs_pro()
			elif (1,1) == direction:
				self.rcs_pro()
			elif (0,-1) == direction:
				self.rcs_left()
			elif (0,1) == direction:
				self.rcs_right()
			elif (-1,-1) == direction:
				self.rcs_retro()
			elif (-1,0) == direction:
				self.rcs_retro()
			elif (-1,1) == direction:
				self.rcs_retro()
			
		else:
			# Main thrusters
			if (1,-1) == direction:
				self.boost_pro()
			elif (1,0) == direction:
				self.boost_pro()
			elif (1,1) == direction:
				self.boost_pro()
			elif (0,-1) == direction:
				self.boost_left()
			elif (0,1) == direction:
				self.boost_right()
			elif (-1,-1) == direction:
				self.boost_retro()
			elif (-1,0) == direction:
				self.boost_retro()
			elif (-1,1) == direction:
				self.boost_retro()
				
		
	def boost_pro(self):
		self.boost_left()
		self.boost_right()
		
	def boost_left(self):
		self.state.acc(self.thrust * math.cos(self.state.ori),
					 - self.thrust * math.sin(self.state.ori))
		self.state.rot_acc(.00005)
		self.right = True		
		
	def boost_right(self):
		self.state.acc(self.thrust * math.cos(self.state.ori),
					 - self.thrust * math.sin(self.state.ori))
		self.state.rot_acc(-.00005)
		self.left = True
		
	def boost_retro(self):
		self.state.acc(- self.thrust/2 * math.cos(self.state.ori),
					     self.thrust/2 * math.sin(self.state.ori))
		
	def rcs_pro(self):
		self.state.acc(self.thrust/10 * math.cos(self.state.ori),
					 - self.thrust/10 * math.sin(self.state.ori))
		
	def rcs_left(self):
		self.state.rot_acc(.0001)
		
	def rcs_right(self):
		self.state.rot_acc(-.0001)
		
	def rcs_retro(self):
		self.state.acc(- self.thrust/10 * math.cos(self.state.ori),
					     self.thrust/10 * math.sin(self.state.ori))
		
	def fire_missile(self,current_ticks):
		if current_ticks-self.last_fire >= self.fire_cd:
			self.last_fire = current_ticks
			new_missile = missile(self.image_dict)
			new_missile.set_state(copy.copy(self.state))
			return new_missile
			
	def get_image(self):
		if self.left or self.right:
			image = self.image.copy()
			if self.left:
				image.blit(self.flame_image,(27,62))
			if self.right:
				image.blit(self.flame_image,(42,62))
			image = operations.rot_center(image,self.state.ori / (2*math.pi) * 360 - 90)		
		else:
			image = operations.rot_center(self.image,self.state.ori / (2*math.pi) * 360 - 90)		
		return image
		
class missile(object):
	"""Holds missile data """
	def __init__(self,image_dict):
		self.thrust = .5
		self.state = baryonic_state()	
		image = image_dict['rocket']
		rec = image.get_rect().size
		self.image = pygame.transform.scale(image,(rec[0]/50,rec[1]/50))		
		
	def prop(self):
		self.state.prop()
		self.boost()
		
	def set_state(self,state):
		self.state = state
		
	def boost(self):
		self.state.vel_x += self.thrust * math.cos(self.state.ori)
		self.state.vel_y -= self.thrust * math.sin(self.state.ori)
		
	def get_image(self):
		image = operations.rot_center(self.image,self.state.ori / (2*math.pi) * 360 - 90)
		return image

	