import pygame
import math
import particle
import operations


def load_images():
	image_dict = dict()
	image_dict['rocket'] = pygame.image.load('rocket_small_cute_lineart_neo.png')
	image_dict['missile'] = pygame.image.load('missile_square.png')
	return image_dict

def display_particle(screen,particle):
	state = particle.state
	image = operations.rot_center(particle.image,state.ori / (2*math.pi) * 360 - 90)		
	center = image.get_rect().center

	screen.blit(image,(state.x-center[0],state.y-center[1]))	
	
def main():
	pygame.init()
	screen = pygame.display.set_mode((1600,900))
	done = False
	clock = pygame.time.Clock()
	
	image_dict = load_images()
	ship = particle.ship()
	ship.update_image(image_dict['rocket'])
	
	entities = []
	entities.append(ship)
	
	while not done: 
	
		pressed = pygame.key.get_pressed()
	
		alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
		ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			# Closing Strokes
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w and ctrl_held:
					return
				if event.key == pygame.K_F4 and alt_held:
					return
				if event.key == pygame.K_ESCAPE:
					return			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: # left click grows radius 
					print 'cheese'
				elif event.button == 3: # right click shrinks radius 
					print 'balls'

		ship.maneuver((pressed[pygame.K_UP],
					   pressed[pygame.K_DOWN],
					   pressed[pygame.K_LEFT],
					   pressed[pygame.K_RIGHT],
					   pressed[pygame.K_RCTRL]))

		if pressed[pygame.K_SPACE]: 
			new_missile = ship.fire_missile()
			new_missile.update_image(image_dict['missile'])
			entities.append(new_missile)
		
		screen.fill((30,30,30))
		hor,ver = screen.get_size()
		for entity in entities:
			display_particle(screen,entity)
			entity.prop()
		pygame.display.flip()
		clock.tick(60)
		
		
main()