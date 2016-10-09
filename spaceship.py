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
		self.image_dict = image_dict
		
	def step(self,cur_tick,pressed):
		# Propagate all entities
		for entity in self.entities:
				entity.prop()
			
		# Process user input
		self.ship.command((pressed[pygame.K_UP],
					   pressed[pygame.K_DOWN],
					   pressed[pygame.K_LEFT],
					   pressed[pygame.K_RIGHT],
					   pressed[pygame.K_RCTRL]))
		if pressed[pygame.K_SPACE]: 
			new_missile = self.ship.fire_missile(pygame.time.get_ticks())
			if new_missile is not None:
				self.entities.append(new_missile)
			
		self.n_steps += 1
			
			
			
			
			
			
			
			
			