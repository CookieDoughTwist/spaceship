import pygame
import math
import particle


def main():
	pygame.init()
	screen = pygame.display.set_mode((1600,900))
	done = False
	clock = pygame.time.Clock()
	
	ship = particle.baryon()
	ship_image = pygame.image.load('rocket_small_cute_lineart_neo.png')
	missile_image = pygame.image.load('missile_square.png')
	ship.update_image(ship_image,8)
	#ship = particle.baryon('rocket_small_cute_lineart.png')
	ship.move(0,0)
	
	entities = []
	entities.append(ship)
	
	while not done: 
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

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_UP]: particle.boost(ship)
		if pressed[pygame.K_LEFT]: particle.torque_boost_left(ship) #ship.rot_left()
		if pressed[pygame.K_RIGHT]: particle.torque_boost_right(ship) #ship.rot_right()
		if pressed[pygame.K_SPACE]: 
			missile = particle.fire(ship,missile_image)
			entities.append(missile)
		
		screen.fill((30,30,30))
		hor,ver = screen.get_size()
		for entity in entities:
			particle.display(screen,entity)
			entity.prop()
			if entity.id == 1:
				particle.boost(entity)
		pygame.display.flip()
		clock.tick(60)
		
		
main()