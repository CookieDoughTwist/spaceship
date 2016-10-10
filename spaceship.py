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
		self.ship = particle.flaming_falcon(init_tick,self.image_dict)
		self.entities.append(self.ship)
		self.focus = self.ship
		
	def load_images(self):
		image_dict = dict()
		image_dict['rocket'] = pygame.image.load('graphics/andrew_rocket.png')
		image_dict['missile'] = pygame.image.load('graphics/lucy_rocket_sleeping.png')
		image_dict['flame'] = pygame.image.load('graphics/lucy_flame.png')
		image_dict['flaming_falcon'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon.png')
		#image_dict['missile'] = pygame.image.load('graphics/lucy_rocket_sleeping.png')
		image_dict['flaming_falcon_flame_1'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_flame_1.png')
		image_dict['flaming_falcon_flame_2'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_flame_2.png')
		image_dict['flaming_falcon_flame_3'] = pygame.image.load('graphics/ships/flaming_falcon/flaming_falcon_flame_3.png')
		image_dict['bullet'] = pygame.image.load('graphics/projectiles/bullets/tungsten_shell.png')
		image_dict['medium_rcs'] = pygame.image.load('graphics/thrusters/medium_grey_inverted_thrusters.png')
		self.image_dict = image_dict
		
	def step(self,cur_tick,pressed,event_list):
		# Propagate all entities
		for entity in self.entities:
				entity.prop()
			
		# Process user input
		wasd = [False,False,False,False] # up,down,left,right
		rtfg = [False,False,False,False]
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
		
		self.ship.command(wasd,rtfg)
		if pressed[pygame.K_SPACE]: 
			new_missile = self.ship.fire_missile(pygame.time.get_ticks())
			if new_missile is not None:
				self.entities.append(new_missile)
			
		self.n_steps += 1
			
			
			
			
			
			
			
			
			