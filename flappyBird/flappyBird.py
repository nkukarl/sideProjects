import pygame, sys, random
from pygame.locals import *

pygame.init()

# function definition
def getMask(image):
	mask = []
	for x in range(image.get_width()):
		mask.append([])
		for y in range(image.get_height()):
			mask[x].append(bool(image.get_at((x, y))[3]))
	return mask

def checkCrash(birdMask, birdx, birdy, pipeMask, pipex, pipey):

	birdx = int(birdx)
	birdy = int(birdy)

	raw = [[False] * HEIGHT for _ in range(WIDTH)]
	for i in range(birdx, birdx + birdWIDTH):
		for j in range(birdy, birdy + birdHEIGHT):
			if i >= 0 and i <= WIDTH and j >= 0 and j <= HEIGHT - baseHEIGHT:
				raw[i][j] = birdMask[i - birdx][j - birdy]

	for i in range(pipex, pipex + pipeWIDTH):
		for j in range(pipey, pipey + pipeHEIGHT):
			if i >= 0 and i < WIDTH and j >= 0 and j < HEIGHT - baseHEIGHT:
				if pipeMask[i - pipex][j - pipey] and raw[i][j]:
					return True

	return False

FPS = 30
fpsClock = pygame.time.Clock()
WIDTH = 288
HEIGHT = 512
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Flappy Bird')

WHITE = (255, 255, 255)
birdWIDTH = 34
birdHEIGHT = 24
birdx = 50
birdy = 10
GRAVITY = 0.25
velocity = 0

birdImgs = [pygame.image.load('bird_down.png').convert_alpha(), pygame.image.load('bird_mid.png').convert_alpha(), pygame.image.load('bird_up.png').convert_alpha()]
wingOrder = 0

bgImg = pygame.image.load('bg.png').convert_alpha()

pipe_upImg = pygame.image.load('pipe_up.png').convert_alpha()
pipe_downImg = pygame.image.load('pipe_down.png').convert_alpha()

pipex1 = 300
pipey1 = random.randint(-225, -125)
pipex2 = 470
pipey2 = random.randint(-225, -125)
pipex1Flag = 0
pipex2Flag = 0
pipeGAP = 150
pipeWIDTH = 52
pipeHEIGHT = 320

baseImg = pygame.image.load('base.png').convert_alpha()
baseHEIGHT = 112
basex = 0
basey = HEIGHT - baseHEIGHT

# masks: birdMask has to be defined inside the while loop since birdImg changes over time

pipe_upMask = getMask(pipe_upImg)
pipe_downMask = getMask(pipe_downImg)


hitSound = pygame.mixer.Sound('hit.wav')
dieSound = pygame.mixer.Sound('die.wav')
wingSound = pygame.mixer.Sound('wing.wav')
pointSound = pygame.mixer.Sound('point.wav')

notHit = 1

score = 0

numImgs = [pygame.image.load(str(i) + '.png').convert_alpha() for i in range(10)]

while True:

	birdImg = birdImgs[wingOrder]
	birdMask = getMask(birdImg)

	DISPLAYSURF.blit(bgImg, (0, 0))
	DISPLAYSURF.blit(birdImg, (birdx, birdy))
	
	DISPLAYSURF.blit(pipe_upImg, (pipex1, pipey1))
	DISPLAYSURF.blit(pipe_downImg, (pipex1, pipey1 + pipeHEIGHT + pipeGAP))

	DISPLAYSURF.blit(pipe_upImg, (pipex2, pipey2))
	DISPLAYSURF.blit(pipe_downImg, (pipex2, pipey2 + pipeHEIGHT + pipeGAP))

	DISPLAYSURF.blit(baseImg, (basex, basey))

	crash = checkCrash(birdMask, birdx, birdy, pipe_upMask, pipex1, pipey1) or checkCrash(birdMask, birdx, birdy, pipe_downMask, pipex1, pipey1 + pipeHEIGHT + pipeGAP) or checkCrash(birdMask, birdx, birdy, pipe_upMask, pipex2, pipey2) or checkCrash(birdMask, birdx, birdy, pipe_downMask, pipex2, pipey2 + pipeHEIGHT + pipeGAP) or birdy < 0 or birdy >= HEIGHT - baseHEIGHT - birdHEIGHT

	if crash:
		if notHit:
			# hitSound.play()
			notHit = 0

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

	else:

		wingOrder = (wingOrder + 1) % 3

		velocity += GRAVITY
		birdy += velocity

		# pipe location looping
		if pipex1 - 2 < -pipeWIDTH:
			pipex1 = WIDTH
			pipey1 = random.randint(-225, -125)
			pipex1Flag = 0
		else:
			pipex1 = pipex1 - 2
			if pipex1 + pipeWIDTH < birdx:
				pipex1Flag += 1
			if pipex1Flag == 1:
				score += 1
				# pointSound.play()

		if pipex2 - 2 < -pipeWIDTH:
			pipex2 = WIDTH
			pipey2 = random.randint(-225, -125)
			pipex2Flag = 0
		else:
			pipex2 = pipex2 - 2
			if pipex2 + pipeWIDTH < birdx:
				pipex2Flag += 1
			if pipex2Flag == 1:
				score += 1
				# pointSound.play()

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
					velocity = -5
					# wingSound.play()

	scoreStr = str(score)
	numx = 20
	numy = 20
	numWidth = 24
	for num in scoreStr:
		DISPLAYSURF.blit(numImgs[int(num)], (numx, numy))
		numx += numWidth

	pygame.display.update()
	fpsClock.tick(FPS)