import pygame
import numpy as np
import matplotlib.pyplot as plt

pygame.init()

# pygame screen
win = pygame.display.set_mode((352, 352))
pygame.display.set_caption("Real-Time NO. Recognition")

run = True
mouse_down = True
canvas = []
pixel_canvas = np.zeros((32, 32), dtype=int)
marker_size = 10
mouse_state = ()
mouse_pos = ()


def draw_window():
	win.fill((255, 255, 255))  # white bg

	# draw each point in canvas list
	for point in canvas:
		pygame.draw.circle(win, (0, 0, 0), point[:2], marker_size)

	pygame.display.update()


# mainloop
while run:
	for event in pygame.event.get():  # close window
		if event.type == pygame.QUIT:
			run = False

	# get mouse state
	mouse_state = pygame.mouse.get_pressed(num_buttons=3)
	mouse_pos = list(pygame.mouse.get_pos())
	mouse_down = True if mouse_state[0] else mouse_down

	# draw
	if mouse_state[0]:
		if mouse_pos not in canvas:  # add mouse position and to canvas
			canvas.append(mouse_pos)

	# detect mouse up
	if (not mouse_state[0]) and mouse_down:
		for spot in canvas:
			pixel_canvas[int(spot[1] / 11)][int(spot[0] / 11)] = 1

			mouse_down = False

	# redraw window
	draw_window()


pygame.quit()
