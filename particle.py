import pygame
import math
import operations
import copy

class baryonic_state(object):
	""" Holds Baryonic Data """
	def __init__(self,parent_id=-1,step_freq=60.0):
		self.id = baryonic_state.id
		baryonic_state.id += 1
		self.parent_id = parent_id
		
		self.x = 200		# m
		self.y = 200		# m
		self.vel_x = 0		# m/s
		self.vel_y = 0		# m/s
		self.acc_x = 0		# m/s^2
		self.acc_y = 0		# m/s^2
		self.ori = 0		# rad
		self.vel_ori = 0	# rad/s	
		self.acc_ori = 0	# rad/s^2
		self.mass = 1		# kg
		self.mom_ine = 1	# kg*m^2
		
		self.step_dur = 1/step_freq # s
	
	def set_pos(self,x,y):
		self.x = x
		self.y = y
	
	def set_vel(self,vel_x,vel_y):
		self.vel_x = vel_x
		self.vel_y = vel_y
	
	def set_ori(self,ori):
		self.ori = ori
	
	def set_vel_ori(self,vel_ori):
		self.vel_ori = vel_ori
		
	def set_mass(self,mass):
		self.mass = mass
		
	def set_mom_ine(self,mom_ine):
		self.mom_ine = mom_ine
	
	def prop(self):
		# Constant acceleration assumption
		# Propagate position
		self.x += self.vel_x*self.step_dur + \
			0.5*self.acc_x*self.step_dur*self.step_dur
		self.y += self.vel_y*self.step_dur + \
			0.5*self.acc_y*self.step_dur*self.step_dur
		self.ori += self.vel_ori*self.step_dur + \
			0.5*self.acc_ori*self.step_dur*self.step_dur
		# Propagate velocity
		self.vel_x += self.acc_x*self.step_dur
		self.vel_y += self.acc_y*self.step_dur
		self.vel_ori += self.acc_ori*self.step_dur
		
		
	def acc(self,ddx,ddy):
		""" accelerate """
		self.vel_x += ddx
		self.vel_y += ddy
		
	def rot_acc(self,ddori):
		""" rotationally accelerate """
		self.vel_ori += ddori
		
	def force_cog(self,force,ori):
		""" apply force at center of gravity with given orientation """
		a = force/self.mass
		self.acc(a * math.cos(ori),
				 a * math.sin(ori))
				 
	def force_off(self,force,ori,r_sin_theta):
		force_x = force * math.cos(ori)
		force_y = force * math.sin(ori)
		self.acc(force_x/self.mass,force_y/self.mass)
		print r_sin_theta
		torque = r_sin_theta * force
		self.rot_acc(torque/self.mom_ine)
	
		

baryonic_state.id = 0		
	
class flaming_falcon(object):
	""" Holds ship data """
	def __init__(self,init_ticks,image_dict):		
		self.main_thrust = 50000
		self.side_thrust = 10000
		self.rcs_thrust = .01
		self.init_ticks = init_ticks
		self.fire_cd = 1000 # miliseconds
		self.last_fire = -float('inf')
		
		self.state = baryonic_state()
		self.main = False
		self.left = False
		self.right = False
		
		mass = 50000
		x_len = 100
		y_len = 250
		
		left_x = 216-250
		left_y = 365-250
		left_r = math.sqrt(math.pow(left_x,2)+math.pow(left_y,2))
		self.left_r_sin_theta = left_x/left_r
		
		right_x = 283-250
		right_y = 365-250
		right_r = math.sqrt(math.pow(right_x,2)+math.pow(right_y,2))
		self.right_r_sin_theta = right_x/right_r
				
		self.state.set_mass(mass)
		self.state.set_mom_ine(mass*(x_len*x_len+y_len*y_len)/12)
		
		self.image_dict = image_dict
		
		# Resize Images
		self.image = image_dict['flaming_falcon']
		
		self.flame_image_1 = image_dict['flaming_falcon_flame_1']
		self.flame_image_2 = image_dict['flaming_falcon_flame_2']
		self.flame_image_3 = image_dict['flaming_falcon_flame_3']

	def prop(self):
		# Propagate object based on current state
		# Constant acceleration over interval assumed
		self.state.prop()
		# Change the acceleration
		# Does not affect kinematics of current step
		if self.main:
			self.state.force_cog(self.main_thrust,self.state.ori)
		if self.left:
			self.state.force_off(self.side_thrust,self.state.ori,self.left_r_sin_theta)
		if self.right:
			self.state.force_off(self.side_thrust,self.state.ori,self.right_r_sin_theta)
		
		
		
	def command(self,commands):
		""" commands = (up,down,left,right,ctrl) """
		#  (1,-1)  (1,0)  (1,1)
		#  (0,-1)  (0,0)  (0,1)
		# (-1,-1) (-1,0) (-1,1)
		direction = (commands[0] - commands[1], commands[3] - commands[2])
		self.main = False
		self.left = False
		self.right = False
		
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
			if commands[0]:
				self.boost_pro();
			if commands[1]:
				self.boost_retro();
			if commands[2]:
				self.boost_left();
			if commands[3]:
				self.boost_right();
				
		
	def boost_pro(self):
		#self.state.force_cog(self.main_thrust,self.state.ori)
		self.main = True
		
	def boost_left(self):
		# thrust = self.side_thrust/self.state.mass
		# self.state.acc(self.side_thrust * math.cos(self.state.ori),
					 # - self.side_thrust * math.sin(self.state.ori))
		# self.state.rot_acc(.00005)
		self.right = True		
		
	def boost_right(self):
		# self.state.acc(self.side_thrust * math.cos(self.state.ori),
					 # - self.side_thrust * math.sin(self.state.ori))
		# self.state.rot_acc(-.00005)
		self.left = True
		
	def boost_retro(self):
		self.state.acc(- self.rcs_thrust/2 * math.cos(self.state.ori),
					     self.rcs_thrust/2 * math.sin(self.state.ori))
		
	def rcs_pro(self):
		self.state.acc(self.rcs_thrust/10 * math.cos(self.state.ori),
					 - self.rcs_thrust/10 * math.sin(self.state.ori))
		
	def rcs_left(self):
		self.state.rot_acc(.0001)
		
	def rcs_right(self):
		self.state.rot_acc(-.0001)
		
	def rcs_retro(self):
		self.state.acc(- self.rcs_thrust/10 * math.cos(self.state.ori),
					     self.rcs_thrust/10 * math.sin(self.state.ori))
		
	def fire_missile(self,current_ticks):
		if current_ticks-self.last_fire >= self.fire_cd:
			self.last_fire = current_ticks
			new_missile = missile(self.image_dict)
			new_missile.set_state(copy.copy(self.state))
			return new_missile
			
	def get_image(self):
		if self.main or self.left or self.right:
			image = self.image.copy()
			if self.main:
				image.blit(self.flame_image_1,(227,367))
			if self.left:
				image.blit(self.flame_image_3,(209,364))
			if self.right:
				image.blit(self.flame_image_3,(276,364))
			image = operations.rot_center(image,self.state.ori / (2*math.pi) * 360 - 90)		
		else:
			image = operations.rot_center(self.image,self.state.ori / (2*math.pi) * 360 - 90)		
		return image

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

	