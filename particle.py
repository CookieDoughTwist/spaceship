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
		
		self.x = 100		# m
		self.y = 100		# m
		self.vel_x = 0.0		# m/s
		self.vel_y = 0.0		# m/s
		self.acc_x = 0.0		# m/s^2
		self.acc_y = 0.0		# m/s^2
		self.ori = 0.0		# rad
		self.vel_ori = 0.0	# rad/s	
		self.acc_ori = 0.0	# rad/s^2
		self.mass = 1.0		# kg
		self.mom_ine = 1.0	# kg*m^2
		
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
		# Reset accelerations
		self.acc_x = 0.0
		self.acc_y = 0.0
		self.acc_ori= 0.0
		
	def acc(self,ddx,ddy):
		""" accelerate """
		self.acc_x += ddx
		self.acc_y += ddy
		
	def rot_acc(self,ddori):
		""" rotationally accelerate """
		self.acc_ori += ddori
		
	def force_cog(self,force,ori):
		""" apply force at center of gravity with given orientation """
		a = force/self.mass
		self.acc(a * math.cos(ori),
				 a * math.sin(ori))
				 
	def torque(self,torque):
		self.rot_acc(torque/self.mom_ine)
				 		          
	def force_off(self,force,f_ang,p_ang,r):
		""" apply force not at center of gravity with given orientation """
		# f_ang = clockwise angle of force
		# p_ang = clockwise angle of contact point
		# http://physics.stackexchange.com/questions/43232/force-applied-off-center-on-an-object		
		self.force_cog(force,f_ang)
		off_ang = f_ang-p_ang
		force_t = force*math.sin(off_ang) # torsional force
		self.torque(r * force_t)

	def impulse(self,mom_mag,ori):
		""" imparts momentum """
		vel_mag = mom_mag/self.mass
		self.vel_x += vel_mag*math.cos(ori)
		self.vel_y += vel_mag*math.sin(ori)
		
baryonic_state.id = 0		
	
class flaming_falcon(object):
	""" Holds ship data """
	def __init__(self,init_step,image_dict):		
		self.main_thrust = 1e6
		self.side_thrust = 1e5
		self.rcs_thrust = 1e5
		self.init_step = init_step
		self.current_step = init_step
		self.fire_cd = 0.5 # seconds
		self.fire_last = -float('inf')
		
		self.state = baryonic_state()
		
		# Main thrusters
		self.main = False
		self.retro = False
		self.left = False
		self.right = False
		
		# RCS thrusters
		self.bow_port = False
		self.bow_star = False
		self.stern_port = False
		self.stern_star = False	
		self.bow_port_fore = False
		self.bow_star_fore = False
		self.stern_port_aft = False
		self.stern_star_aft = False
		
		mass = 50000	# kg
		x_len = 100		# m
		y_len = 250		# m
				
		left_x = 250-365
		left_y = 216-250
		self.left_r = math.sqrt(math.pow(left_x,2)+math.pow(left_y,2))
		self.left_theta = math.atan2(left_y,left_x)
		
		right_x = 250-365
		right_y = 283-250
		self.right_r = math.sqrt(math.pow(right_x,2)+math.pow(right_y,2))
		self.right_theta = math.atan2(right_y,right_x)
		
		front_rcs_x = 250-175
		back_rcs_x = 250-325
		left_hull_y = 216-250
		right_hull_y = 283-250
		
		
		self.rcs_r = math.sqrt(front_rcs_x*front_rcs_x+right_hull_y*right_hull_y)
		self.bow_port_theta = math.atan2(left_hull_y,front_rcs_x)
		self.bow_star_theta = math.atan2(right_hull_y,front_rcs_x)
		self.stern_port_theta = math.atan2(left_hull_y,back_rcs_x)
		self.stern_star_theta = math.atan2(right_hull_y,back_rcs_x)
		
		self.state.set_mass(mass)
		self.state.set_mom_ine(mass*(x_len*x_len+y_len*y_len)/12)
		
		self.image_dict = image_dict
		
		# Save image pointers
		self.image = image_dict['flaming_falcon']
		self.gun_image = image_dict['flaming_falcon_gun']
		self.flame_image_1 = image_dict['flaming_falcon_flame_1']
		self.flame_image_2 = image_dict['flaming_falcon_flame_2']
		self.flame_image_3 = image_dict['flaming_falcon_flame_3']
		self.bullet_flare = image_dict['bullet_flare']
		rcs_exhaust_image = image_dict['medium_rcs']
		self.left_rcs_exhaust_image = \
			operations.rot_center(rcs_exhaust_image,-90)
		self.right_rcs_exhaust_image = \
			operations.rot_center(rcs_exhaust_image,90)
		self.fore_rcs_exhaust_image = \
			operations.rot_center(rcs_exhaust_image,180)
		self.aft_rcs_exhaust_image = rcs_exhaust_image
			
	def prop(self,current_step):
		self.current_step = current_step
		# Propagate object based on current state
		# Constant acceleration over interval assumed
		self.state.prop()
		# Change the acceleration
		# Does not affect kinematics of current step
		if self.main:
			self.state.force_cog(self.main_thrust,self.state.ori)
		if self.left:
			self.state.force_off(self.side_thrust,self.state.ori,\
			self.left_theta+self.state.ori,self.left_r)
		if self.right:			
			self.state.force_off(self.side_thrust,self.state.ori,\
			self.right_theta+self.state.ori,self.right_r)
		if self.bow_port:			
			thrust_ori = self.state.ori+math.pi/2
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.bow_port_theta+self.state.ori,self.rcs_r)
		if self.bow_star:
			thrust_ori = self.state.ori-math.pi/2
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.bow_star_theta+self.state.ori,self.rcs_r)
		if self.stern_port:
			thrust_ori = self.state.ori+math.pi/2
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.stern_port_theta+self.state.ori,self.rcs_r)
		if self.stern_star:
			thrust_ori = self.state.ori-math.pi/2
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.stern_star_theta+self.state.ori,self.rcs_r)
		# The following recycles the ratios of the main side thrusters
		# because lazy and they might be moved often
		# The fore left right is flipped to take advantage of symmetry.
		if self.bow_port_fore:
			thrust_ori = self.state.ori+math.pi
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.right_theta+self.state.ori+math.pi,self.left_r)
		if self.bow_star_fore:
			thrust_ori = self.state.ori+math.pi
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.left_theta+self.state.ori+math.pi,self.right_r)
		if self.stern_port_aft:
			thrust_ori = self.state.ori
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.left_theta+self.state.ori,self.left_r)
		if self.stern_star_aft:
			thrust_ori = self.state.ori
			self.state.force_off(self.rcs_thrust,thrust_ori,\
			self.right_theta+self.state.ori,self.right_r)
			
	def command(self,wasd,rtfg,shift):
		""" movement """
			
		# Main thrusters
		if wasd[0]:
			self.boost_pro()
		if wasd[1]:
			self.boost_retro()
		if wasd[2]:
			self.boost_left()
		if wasd[3]:
			self.boost_right()		
		
		# RCS thrusters
		if shift:
			if rtfg[0]:
				self.rcs_bow_port_fore()
			if rtfg[1]:
				self.rcs_bow_star_fore()
			if rtfg[2]:
				self.rcs_stern_port_aft()
			if rtfg[3]:
				self.rcs_stern_star_aft()
		else:		
			if rtfg[0]:
				self.rcs_bow_port()
			if rtfg[1]:
				self.rcs_bow_star()
			if rtfg[2]:
				self.rcs_stern_port()
			if rtfg[3]:
				self.rcs_stern_star()
								
	def boost_pro(self):
		self.main = not self.main
		
	def boost_left(self):
		self.left = not self.left		
		
	def boost_right(self):
		self.right = not self.right
		
	def boost_retro(self):
		# NO RETRO
		self.retro = not self.retro

	def rcs_bow_port(self):
		self.bow_port = not self.bow_port
		
	def rcs_bow_star(self):
		self.bow_star = not self.bow_star
		
	def rcs_stern_port(self):
		self.stern_port = not self.stern_port
		
	def rcs_stern_star(self):
		self.stern_star = not self.stern_star	
		
	def rcs_bow_port_fore(self):
		self.bow_port_fore = not self.bow_port_fore
		
	def rcs_bow_star_fore(self):
		self.bow_star_fore = not self.bow_star_fore
		
	def rcs_stern_port_aft(self):
		self.stern_port_aft = not self.stern_port_aft
	
	def rcs_stern_star_aft(self):
		self.stern_star_aft = not self.stern_star_aft

	def fire_main_gun(self):
		if self.current_step - self.fire_last >= self.fire_cd*60: # 60 step/second
			self.fire_last = self.current_step
			new_proj = bullet(self.current_step,self.image_dict)
			new_state = new_proj.state
			ori = self.state.ori
			aft = 27 # meters
			new_state.set_pos(aft*math.cos(ori)+self.state.x,\
			                  aft*math.sin(ori)+self.state.y)	
			new_state.set_ori(self.state.ori)
			muzzle_vel = 100
			new_state.set_vel(muzzle_vel*math.cos(ori)+self.state.vel_x,\
							  muzzle_vel*math.sin(ori)+self.state.vel_y)
			return new_proj
					
	def get_image(self):
		# Lower x is toward the left (port) side of the ship
		# Higher x is toward the right (starboard) side of the ship
		# Lower y is toward the front (bow) side of the ship
		# Higher y is toward the back (stern) side of the ship
		rect = self.image.get_rect()
		# Create a new surface for image
		image = pygame.Surface((rect[2],rect[3]),pygame.SRCALPHA)
		# Paint exhaust trails
		if self.main:
			image.blit(self.flame_image_1,(227,367))
		if self.left:
			image.blit(self.flame_image_3,(209,364))
		if self.right:
			image.blit(self.flame_image_3,(276,364))
		if self.bow_port:
			image.blit(self.left_rcs_exhaust_image,(176,150))
		if self.bow_star:
			image.blit(self.right_rcs_exhaust_image,(284,150))
		if self.stern_port:
			image.blit(self.left_rcs_exhaust_image,(176,300))
		if self.stern_star:
			image.blit(self.right_rcs_exhaust_image,(284,300))
		if self.bow_port_fore:
			image.blit(self.fore_rcs_exhaust_image,(205,100))
		if self.bow_star_fore:
			image.blit(self.fore_rcs_exhaust_image,(255,100))
		if self.stern_port_aft:
			image.blit(self.aft_rcs_exhaust_image,(205,345))
		if self.stern_star_aft:
			image.blit(self.aft_rcs_exhaust_image,(255,345))
		
		# Paint main gun
		fire_period = 0.25 # seconds
		fire_progress = min((self.current_step-self.fire_last)/(fire_period*60),1.0)
		if fire_progress <= .1:
			image.blit(self.bullet_flare,(241,93))
		recoil_coef = math.sin(fire_progress*math.pi)
		image.blit(self.gun_image,(247,115+15*recoil_coef)) # y = 115 is home position
		image.blit(self.image,(0,0))
		
		image = operations.rot_center(image,\
			-self.state.ori / (2*math.pi) * 360 - 90)		
	
		return image
		
class bullet(object):
	""" Holds bullet data """
	def __init__(self,init_step,image_dict):
		self.state = baryonic_state()
		self.image = image_dict['bullet']
		self.init_step = init_step
		self.current_step = init_step
		
	def prop(self,current_step):
		self.current_step = current_step
		self.state.prop()

	def get_image(self):		
		image = operations.rot_center(self.image,\
			-self.state.ori / (2*math.pi) * 360 - 90)
		return image
		
class missile(object):
	""" Holds missile data """
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

class hyper_neutron(object):
	""" Holds neutron data """
	def __init__(self,init_step,image_dict):
		self.state = baryonic_state()
		self.state.set_mass(400)
		self.image = image_dict['hyper_neutron']
		
	def prop(self,current_step):
		self.state.prop()
	
	def get_image(self):
		return self.image
		
		