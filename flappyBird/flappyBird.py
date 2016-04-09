import pygame, sys, random
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()
WIDTH = 288
HEIGHT = 512
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
birdWidth = 34
birdHeight = 24
# birdx = (WIDTH - birdWidth) / 2
birdx = 50
birdy = 10
GRAVITY = 2
gravity = GRAVITY
JUMP = 20

birdImgs = [pygame.image.load('bird_down.png').convert_alpha(), pygame.image.load('bird_mid.png').convert_alpha(), pygame.image.load('bird_up.png').convert_alpha()]
wingOrder = 0
birdImg = pygame.image.load('bird.png').convert_alpha()

bgImg = pygame.image.load('bg.png').convert_alpha()

pipe_upImg = pygame.image.load('pipe_up.png').convert_alpha()
pipe_downImg = pygame.image.load('pipe_down.png').convert_alpha()

pipex1 = 300
pipey1 = random.randint(-200, -100)
pipex2 = 470
pipey2 = random.randint(-200, -100)
pipeGap = 100
pipeWIDTH = 52
pipeHEIGHT = 320

baseImg = pygame.image.load('base.png').convert_alpha()
baseHEIGHT = 112
basex = 0
basey = HEIGHT - baseHEIGHT

while True:

	gravity += 0.05
	birdy += gravity

	birdImg = birdImgs[wingOrder]
	wingOrder = (wingOrder + 1) % 3

	DISPLAYSURF.blit(bgImg, (0, 0))
	DISPLAYSURF.blit(birdImg, (birdx, birdy))
	

	DISPLAYSURF.blit(pipe_upImg, (pipex1, pipey1))
	DISPLAYSURF.blit(pipe_downImg, (pipex1, pipey1 + pipeHEIGHT + pipeGap))

	DISPLAYSURF.blit(pipe_upImg, (pipex2, pipey2))
	DISPLAYSURF.blit(pipe_downImg, (pipex2, pipey2 + pipeHEIGHT + pipeGap))

	DISPLAYSURF.blit(baseImg, (basex, basey))

	
	# pipe location looping
	if pipex1 - 2 < -52:
		# pipex1 = (pipex1 - 2) % WIDTH
		pipex1 = WIDTH
		pipey1 = random.randint(-200, -100)
	else:
		pipex1 = pipex1 - 2

	if pipex2 - 2 < -52:
		# pipex2 = (pipex2 - 2) % WIDTH
		pipex2 = WIDTH
		pipey2 = random.randint(-200, -100)
	else:
		pipex2 = pipex2 - 2

	# base location looping
	basex -= 2
	if basex < -20:
		basex = 0

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_SPACE or event.key == K_UP:
				birdy -= JUMP
				gravity = GRAVITY

	pygame.display.update()
	fpsClock.tick(FPS)