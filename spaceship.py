import particle
import pygame

class engine(object):
	""" Game Engine """
	def __init__(self,init_tick):
		self.entities = []
		self.init_tick = init_tick
		self.load_images()
		self.ship = particle.ship(init_tick)
		self.ship.update_image(self.image_dict['rocket'])
		self.entities.append(self.ship)
		
	def load_images(self):
		image_dict = dict()
		image_dict['rocket'] = pygame.image.load('graphics/andrew_rocket.png')
		image_dict['missile'] = pygame.image.load('graphics/lucy_rocket_sleeping.png')
		image_dict['flame'] = pygame.image.load('graphics/lucy_flame.png')
		self.image_dict = image_dict
		
	def step(self,cur_tick,pressed):
		self.ship.maneuver((pressed[pygame.K_UP],
					   pressed[pygame.K_DOWN],
					   pressed[pygame.K_LEFT],
					   pressed[pygame.K_RIGHT],
					   pressed[pygame.K_RCTRL]))
		if pressed[pygame.K_SPACE]: 
			new_missile = self.ship.fire_missile(pygame.time.get_ticks())
			if new_missile is not None:
				new_missile.update_image(self.image_dict['missile'])
				self.entities.append(new_missile)
				
		for entity in self.entities:
			entity.prop()