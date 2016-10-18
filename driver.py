import pygame
import math
import particle
import operations as op
import spaceship
	
class pygame_wrapper(object):
	""" Holds pygame engine and display parameters """
	def __init__(self):
		pygame.init()
		dis_info = pygame.display.Info()
		self.screen_dim = [dis_info.current_w, dis_info.current_h]
		self.screen_center = [self.screen_dim[0]/2,self.screen_dim[1]/2] # bits
		self.screen = pygame.display.set_mode(\
			self.screen_dim,pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		self.frame_rate = 60 # Hz
		self.screen_ori = 0 # radians
		self.bits_per_meter = 5
		
		self.scroll_spd = 10 # bits/frame
		self.lock_screen = False
		self.lock_ori = False
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
				if event.key == pygame.K_u:
					self.lock_ori = not self.lock_ori
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: # left click grows radius 
					print 'cheese'
				elif event.button == 3: # right click shrinks radius 
					print 'balls'
		
		if self.lock_ori:
			self.screen_ori = self.engine.focus.state.ori+math.pi/2
		else:
			if pressed[pygame.K_PAGEUP]:
				self.screen_ori -= math.pi/180
			if pressed[pygame.K_PAGEDOWN]:
				self.screen_ori += math.pi/180
			if pressed[pygame.K_HOME]:
				self.screen_ori = 0
				
		if self.lock_screen:
			x = int(self.engine.focus.state.x*self.bits_per_meter)
			y = int(self.engine.focus.state.y*self.bits_per_meter)
			self.screen_center = [x,y]
		else:
			mouse_pos = pygame.mouse.get_pos()
			if mouse_pos[1] <= 0 or pressed[pygame.K_UP]:
				dx = int(self.scroll_spd*math.sin(math.pi-self.screen_ori))
				dy = int(self.scroll_spd*math.cos(math.pi-self.screen_ori))				
				self.screen_center[0] += dx
				self.screen_center[1] += dy
			if mouse_pos[1] >= self.screen_dim[1]-1 or pressed[pygame.K_DOWN]:				
				dx = int(self.scroll_spd*math.sin(math.pi-self.screen_ori))
				dy = int(self.scroll_spd*math.cos(math.pi-self.screen_ori))				
				self.screen_center[0] -= dx
				self.screen_center[1] -= dy
			if mouse_pos[0] <= 0 or pressed[pygame.K_LEFT]:
				dx = int(self.scroll_spd*math.cos(self.screen_ori))
				dy = int(self.scroll_spd*math.sin(self.screen_ori))				
				self.screen_center[0] -= dx
				self.screen_center[1] -= dy
			if mouse_pos[0] >= self.screen_dim[0]-1 or pressed[pygame.K_RIGHT]:
				dx = int(self.scroll_spd*math.cos(self.screen_ori))
				dy = int(self.scroll_spd*math.sin(self.screen_ori))				
				self.screen_center[0] += dx
				self.screen_center[1] += dy
		
		self.engine.step(pygame.time.get_ticks(),pressed,event_list)
		
		self.screen.fill((30,30,30))
		self.paint_grid()
		#self.paint_dot((0,0))
		self.paint_engine()
		pygame.display.flip()
		self.clock.tick(self.frame_rate)
		
	def paint_grid(self):
		# TODO: double comuting happening between here and paint_engine; consider merge 10/17/16 -AW
		center_offset = (self.screen_dim[0]/2,self.screen_dim[1]/2)
		rot_mat = op.rot_matrix(self.screen_ori)
		
		bit_width = self.grid_width*self.bits_per_meter
		
		screen_origin = self.get_screen_origin()
		x_offset = -(screen_origin[0] % bit_width)+bit_width
		y_offset = -(screen_origin[1] % bit_width)+bit_width
		
		w = self.screen_dim[0]
		h = self.screen_dim[1]
		
		# TODO: Perhaps make the bounds more accurate to decrease number of required iterations in the for loops 10/17/16 -AW
		
		for x in range(x_offset-w,x_offset+2*w,bit_width):			
			p0 = (x-1,-h)
			p1 = (x-1,2*h)
			cen_p0 = op.arr_sub(p0,center_offset)
			rot_p0 = op.matrix_op(rot_mat,cen_p0)
			dis_p0 = op.arr_add(rot_p0,center_offset)
			cen_p1 = op.arr_sub(p1,center_offset)
			rot_p1 = op.matrix_op(rot_mat,cen_p1)
			dis_p1 = op.arr_add(rot_p1,center_offset)
			
			pygame.draw.aaline(self.screen,(0,255,0),dis_p0,dis_p1)
		for y in range(y_offset-h,y_offset+2*h,bit_width):
			p0 = (-w,y-1)
			p1 = (2*w,y-1)
			cen_p0 = op.arr_sub(p0,center_offset)
			rot_p0 = op.matrix_op(rot_mat,cen_p0)
			dis_p0 = op.arr_add(rot_p0,center_offset)
			cen_p1 = op.arr_sub(p1,center_offset)
			rot_p1 = op.matrix_op(rot_mat,cen_p1)
			dis_p1 = op.arr_add(rot_p1,center_offset)
			
			pygame.draw.aaline(self.screen,(0,255,0),dis_p0,dis_p1)
			
	def paint_engine(self):
		center_offset = (self.screen_dim[0]/2,self.screen_dim[1]/2)
		rot_mat = op.rot_matrix(self.screen_ori)
		for entity in self.engine.entities:
			state = entity.state			
			loc = (state.x*self.bits_per_meter,\
						 state.y*self.bits_per_meter)
							
			cen_loc = op.arr_sub(loc,self.screen_center)
			rot_loc = op.matrix_op(rot_mat,cen_loc)
							
			dis_loc = op.arr_add(rot_loc,center_offset)

			image = entity.get_image(-self.screen_ori)
			image_center_offset = image.get_rect().center
			dis_loc = op.arr_sub(dis_loc,image_center_offset)
			self.screen.blit(image,dis_loc)
			
	def paint_dot(self,pos):
		screen_origin = self.get_screen_origin()
		pygame.draw.circle(self.screen,(255,0,0),(pos[0]-screen_origin[0],pos[1]-screen_origin[1]),10)

	def get_screen_origin(self):
		return (self.screen_center[0]-self.screen_dim[0]/2,\
				self.screen_center[1]-self.screen_dim[1]/2)
	
	def get_screen_corners(self):
		rot_mat = op.rot_matrix(self.screen_ori)
		c0 = op.matrix_op(rot_mat,(self.screen_dim[0]/2,self.screen_dim[1]/2))
		c1 = op.matrix_op(rot_mat,(self.screen_dim[0]/2,-self.screen_dim[1]/2))
		c2 = op.matrix_op(rot_mat,(-self.screen_dim[0]/2,-self.screen_dim[1]/2))
		c3 = op.matrix_op(rot_mat,(-self.screen_dim[0]/2,self.screen_dim[1]/2))
		
		return (c0,c1,c2,c3)
	
def main():
	driver = pygame_wrapper()
	driver.engine.place_hyper_neutron((200,103))
	#driver.engine.place_hyper_neutron((0,0))	
	while not driver.stop:
		driver.step()		

main()