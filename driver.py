import pygame
import math
import particle
import operations
import spaceship


def display_particle(screen,screen_origin,particle):
	state = particle.state
	image = particle.get_image()
	center = image.get_rect().center

	screen.blit(image,(state.x-center[0]-screen_origin[0],state.y-center[1]-screen_origin[1]))	
	
def paint_engine(screen,screen_origin,engine):
	for entity in engine.entities:
		display_particle(screen,screen_origin,entity)
	
def paint_grid(screen,screen_origin,grid_width):
	w = screen.get_width()
	h = screen.get_height()
	x_offset = -(screen_origin[0] % grid_width)+grid_width
	y_offset = -(screen_origin[1] % grid_width)+grid_width
	for x in range(x_offset,w+x_offset,grid_width):
		vertical_line = pygame.Surface((1, h), pygame.SRCALPHA)
		vertical_line.fill((0, 255, 0, 30))
		screen.blit(vertical_line, (x - 1, 0))
	for y in range(y_offset,h+y_offset,grid_width):
		horizontal_line = pygame.Surface((w, 1), pygame.SRCALPHA)
		horizontal_line.fill((0, 255, 0, 30))
		screen.blit(horizontal_line, (0, y - 1))

def paint_dot(screen,screen_origin,pos):
	pygame.draw.circle(screen,(255,0,0),(pos[0]-screen_origin[0],pos[1]-screen_origin[1]),10)
	
def main():
	pygame.init()
	screen_origin = (-27,-23)
	grid_width = 50 # bits	
	dis_info = pygame.display.Info()	
	#screen = pygame.display.set_mode((dis_info.current_w, dis_info.current_h))
	screen = pygame.display.set_mode((dis_info.current_w, dis_info.current_h),pygame.FULLSCREEN)
	done = False
	clock = pygame.time.Clock()
	frame_rate = 60 # Hz
	
	engine = spaceship.engine(pygame.time.get_ticks(),frame_rate)
		
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
		
		engine.step(pygame.time.get_ticks(),pressed)
		
		screen.fill((30,30,30))
		paint_grid(screen,screen_origin,grid_width)
		paint_dot(screen,screen_origin,(0,0))
		paint_engine(screen,screen_origin,engine)
		pygame.display.flip()
		clock.tick(frame_rate)
		
		
main()