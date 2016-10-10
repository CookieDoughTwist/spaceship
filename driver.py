import pygame
import math
import particle
import operations
import spaceship


def display_particle(screen,screen_origin,particle):
	state = particle.state
	x_m = state.x # meters
	y_m = state.y # meters
	x = x_m*5
	y = y_m*5
	image = particle.get_image()
	center = image.get_rect().center

	screen.blit(image,(x-center[0]-screen_origin[0],y-center[1]-screen_origin[1]))	
	
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
	screen_origin = [-27,-23]
	lock_screen = False
	grid_width = 500 # bits	
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
		
		event_list = pygame.event.get()	
		for event in event_list:
			if event.type == pygame.QUIT:
				done = True
			# Closing Strokes
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w and ctrl_held:
					return
				if event.key == pygame.K_F4 and alt_held:
					return	
				if event.key == pygame.K_y:
					lock_screen = not lock_screen								
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: # left click grows radius 
					print 'cheese'
				elif event.button == 3: # right click shrinks radius 
					print 'balls'
		
		if lock_screen:
			w = screen.get_width()
			h = screen.get_height()
			x_m = engine.focus.state.x
			y_m = engine.focus.state.y
			x = int(x_m*5-w/2)
			y = int(y_m*5-h/2)
			screen_origin = [x,y]
		else:
			if pressed[pygame.K_UP]:
				screen_origin[1] -= 10
			if pressed[pygame.K_DOWN]:
				screen_origin[1] += 10
			if pressed[pygame.K_LEFT]:
				screen_origin[0] -= 10
			if pressed[pygame.K_RIGHT]:
				screen_origin[0] += 10
		

		
		engine.step(pygame.time.get_ticks(),pressed,event_list)
		
		screen.fill((30,30,30))
		paint_grid(screen,screen_origin,grid_width)
		paint_dot(screen,screen_origin,(0,0))
		paint_engine(screen,screen_origin,engine)
		pygame.display.flip()
		clock.tick(frame_rate)
		
		
main()