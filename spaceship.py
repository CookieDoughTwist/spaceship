import particle
import pygame

class engine(object):
	""" Game Engine """
	def __init__(self,init_tick):
		self.entities = []
		self.init_tick = init_tick
		self.load_images()
		self.ship = particle.ship(init_tick,self.image_dict)
		self.entities.append(self.ship)
		
	def load_images(self):
		image_dict = dict()
		image_dict['rocket'] = pygame.image.load('graphics/space_pod_export.png')
		image_dict['missile'] = pygame.image.load('graphics/lucy_rocket_sleeping.png')
		image_dict['flame'] = pygame.image.load('graphics/space_pod_flame1.png')
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
				self.entities.append(new_missile)
				
		for entity in self.entities:
			entity.prop()