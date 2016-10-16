import pygame
import math
import particle
import operations
import spaceship
	
class pygame_wrapper(object):
	""" Holds pygame engine and display parameters """
	def __init__(self):
		pygame.init()
		dis_info = pygame.display.Info()
		self.screen_dim = [dis_info.current_w, dis_info.current_h]
		self.screen_center = [self.screen_dim[0]/2,self.screen_dim[1]/2]
		self.screen = pygame.display.set_mode(\
			self.screen_dim,pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		self.frame_rate = 60 # Hz
		self.bits_per_meter = 5
		self.lock_screen = False
		self.grid_width = 100 # meters
		
		self.engine = spaceship.engine(\
			pygame.time.get_ticks(),self.frame_rate)
			
		self.stop = False
		
	def step(self):
		pressed = pygame.key.get_pressed()
		alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
		ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
		
		event_list = pygame.event.get()	
		
		for event in event_list:
			if event.type == pygame.QUIT:
				self.stop = True
				return
			# Closing Strokes
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w and ctrl_held:
					self.stop = True
					return
				if event.key == pygame.K_F4 and alt_held:
					self.stop = True
					return
				if event.key == pygame.K_y:
					self.lock_screen = not self.lock_screen								
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: # left click grows radius 
					print 'cheese'
				elif event.button == 3: # right click shrinks radius 
					print 'balls'
		
		if self.lock_screen:
			x_m = self.engine.focus.state.x
			y_m = self.engine.focus.state.y
			x = int(x_m*self.bits_per_meter)
			y = int(y_m*self.bits_per_meter)
			self.screen_center = [x,y]
		else:
			if pressed[pygame.K_UP]:
				self.screen_center[1] -= 10
			if pressed[pygame.K_DOWN]:
				self.screen_center[1] += 10
			if pressed[pygame.K_LEFT]:
				self.screen_center[0] -= 10
			if pressed[pygame.K_RIGHT]:
				self.screen_center[0] += 10
		

		
		self.engine.step(pygame.time.get_ticks(),pressed,event_list)
		
		self.screen.fill((30,30,30))
		self.paint_grid()
		self.paint_dot((0,0))
		self.paint_engine()
		pygame.display.flip()
		self.clock.tick(self.frame_rate)
		
	def paint_grid(self):
		bit_width = self.grid_width*self.bits_per_meter
		
		screen_origin = self.get_screen_origin()
		x_offset = -(screen_origin[0] % bit_width)+bit_width
		y_offset = -(screen_origin[1] % bit_width)+bit_width
		
		w = self.screen_dim[0]
		h = self.screen_dim[1]
		
		for x in range(x_offset,w+x_offset,bit_width):			
			vertical_line = pygame.Surface((1, h), pygame.SRCALPHA)
			vertical_line.fill((0, 255, 0, 30))
			self.screen.blit(vertical_line, (x - 1, 0))
		for y in range(y_offset,h+y_offset,bit_width):
			horizontal_line = pygame.Surface((w, 1), pygame.SRCALPHA)
			horizontal_line.fill((0, 255, 0, 30))
			self.screen.blit(horizontal_line, (0, y - 1))
			
	def paint_engine(self):
		screen_origin = self.get_screen_origin()
		for entity in self.engine.entities:
			state = entity.state			
			x = state.x*self.bits_per_meter
			y = state.y*self.bits_per_meter
			image = entity.get_image()
			center = image.get_rect().center
			x_bit = x-center[0]-screen_origin[0]
			y_bit = y-center[1]-screen_origin[1]	
			rect = image.get_rect()	
			
			# Do not paint things out of bounds
			if x_bit+rect[2] >= 0 and \
			   x_bit <= self.screen.get_width() and \
			   y_bit+rect[3] >= 0 and \
			   y_bit <= self.screen.get_height():
				self.screen.blit(image,(x_bit,y_bit))
			
	def paint_dot(self,pos):
		screen_origin = self.get_screen_origin()
		pygame.draw.circle(self.screen,(255,0,0),(pos[0]-screen_origin[0],pos[1]-screen_origin[1]),10)

	def get_screen_origin(self):
		return (self.screen_center[0]-self.screen_dim[0]/2,\
				self.screen_center[1]-self.screen_dim[1]/2)
	
def main():
	driver = pygame_wrapper()
	driver.engine.place_hyper_neutron((310,103))
	while not driver.stop:
		driver.step()

main()