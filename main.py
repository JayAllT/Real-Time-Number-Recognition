import pygame
import numpy as np
from tensorflow import keras
import cv2

pygame.init()
pygame.font.init()

# pygame screen
win = pygame.display.set_mode((352, 352))
pygame.display.set_caption("Real-Time NO. Recognition")

global predicted_num

run = True
mouse_down = True
canvas = []
pixel_canvas = np.full((32, 32), 255, dtype=int)
marker_size = 10
mouse_state = ()
mouse_pos = ()
predicted_num = 0
font = pygame.font.SysFont("Arial", 14)

# load number recognition model
model = keras.models.load_model("model/model.h5")


def draw_window():
	global predicted_num

	win.fill((255, 255, 255))  # white bg

	# draw each point in canvas list
	for point in canvas:
		pygame.draw.circle(win, (0, 0, 0), point[:2], marker_size)

	# display predicted number
	text = font.render(f"Predicted Number: {predicted_num}", False, (0, 0, 0))
	win.blit(text, (10, 10))

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

	# clear screen
	keys = pygame.key.get_pressed()
	if keys[pygame.K_c]:
		canvas.clear()
		predicted_num = 0

	# detect mouse up
	if (not mouse_state[0]) and mouse_down:
		pixel_canvas = np.full((32, 32), 255, dtype=int)
		pixel_canvas = np.full((32, 32), 255, dtype=int)

		for spot in canvas:  # create pixelated canvas array
			pixel_canvas[int(spot[1] / 11)][int(spot[0] / 11)] = 0

		pixel_canvas = pixel_canvas / 255.0
		predicted_num = np.argmax(model.predict(np.array([pixel_canvas]))) + 1

		mouse_down = False

	# redraw window
	draw_window()


pygame.quit()
