import particle
import pygame

class engine(object):
	""" Game Engine """
	def __init__(self,init_tick,step_freq):
		self.entities = []
		self.init_tick = init_tick	# ms
		self.step_freq = step_freq	# Hz
		self.n_steps = 0
		self.load_images()
		self.ship = particle.flaming_falcon(self.n_steps,self.image_dict)
		self.entities.append(self.ship)
		self.focus = self.ship
		
	def load_images(self):
		image_dict = dict()
		image_dict['missile'] = pygame.image.load('graphics/projectiles/missiles/generic_missile.png')
		image_dict['flaming_falcon_body'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_body.png')
		image_dict['flaming_falcon_left_nose'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_left_nose.png')
		image_dict['flaming_falcon_right_nose'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_right_nose.png')
		#image_dict['flaming_falcon'] = pygame.image.load('graphics/shields/hex shield example.png')
		image_dict['flaming_falcon_gun'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_gun.png')		
		image_dict['flaming_falcon_flame_1'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_flame_1.png')
		image_dict['flaming_falcon_flame_2'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_flame_2.png')
		image_dict['flaming_falcon_flame_3'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_flame_3.png')
		image_dict['bullet'] = pygame.image.load('graphics/projectiles/bullets/tungsten_shell.png')
		image_dict['bullet_flare'] = pygame.image.load('graphics/projectiles/bullets/tungsten_shell_flare.png')
		image_dict['medium_rcs'] = pygame.image.load('graphics/thrusters/medium_grey_inverted_thrusters.png')
		image_dict['hyper_neutron'] = pygame.image.load('graphics/doodads/hyper_neutron.png')
		
		# UI
		image_dict['pause'] = pygame.image.load('graphics/UI/PAUSED.png')
		self.image_dict = image_dict
	
	def place_hyper_neutron(self,coor):
		new_neutron = particle.hyper_neutron(self.n_steps,self.image_dict)
		new_neutron.state.set_pos(coor[0],coor[1])
		self.entities.append(new_neutron)
	
	def step(self,cur_tick,pressed,event_list):
		# Propagate all entities
		for entity in self.entities:
			entity.prop(self.n_steps)
			
		# Process user input
		wasd = [False,False,False,False] # up,down,left,right
		rtfg = [False,False,False,False]
		e = False
		for event in event_list:
			# Key downs first so that if both down and up happen,
			# up can reset.
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					wasd[0] = True
				if event.key == pygame.K_s:
					wasd[1] = True				
				if event.key == pygame.K_a:
					wasd[2] = True
				if event.key == pygame.K_d:
					wasd[3] = True	
				if event.key == pygame.K_r:
					rtfg[0] = True
				if event.key == pygame.K_t:
					rtfg[1] = True				
				if event.key == pygame.K_f:
					rtfg[2] = True
				if event.key == pygame.K_g:
					rtfg[3] = True	
				if event.key == pygame.K_e:
					e = True
		shift = pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]
		self.ship.command(wasd,rtfg,shift,e)
		if pressed[pygame.K_SPACE]: 
			new_proj = self.ship.fire_main_gun()
			if new_proj is not None:
				self.entities.append(new_proj)
			
		self.n_steps += 1
			
			
			
			
			
			
			
			
			