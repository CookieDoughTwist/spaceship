import pygame
import math
import particle
import operations
import spaceship


def display_particle(screen,particle):
	state = particle.state
	image = operations.rot_center(particle.image,state.ori / (2*math.pi) * 360 - 90)		
	center = image.get_rect().center

	screen.blit(image,(state.x-center[0],state.y-center[1]))	
	
def display_engine(screen,engine):
	for entity in engine.entities:
		display_particle(screen,entity)
	pygame.display.flip()
	
def main():
	pygame.init()
	screen = pygame.display.set_mode((1600,900))
	done = False
	clock = pygame.time.Clock()
	
	engine = spaceship.engine(pygame.time.get_ticks())
	
	while not done: 
	
		pressed = pygame.key.get_pressed()
		print pygame.K_w
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
		
		engine.step(pygame.time.get_ticks(),pressed)
		
		screen.fill((30,30,30))
		
		display_engine(screen,engine)

		clock.tick(60)
		
		
main()