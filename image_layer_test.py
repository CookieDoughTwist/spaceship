import pygame

def main():
	pygame.init()
	screen = pygame.display.set_mode((1600,900))
	done = False
	clock = pygame.time.Clock()
	
	image = pygame.image.load('graphics/Space Pod Export.png')
	flame = pygame.image.load('graphics/Space Pod Flame1.png')
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

		
		screen.fill((30,30,30))
		x = 0
		y = 0
		new_image = image.copy()
		new_image.blit(flame,(43,62))
		screen.blit(new_image,(x,y))
		pygame.display.flip()
		clock.tick(60)
		
		
main()