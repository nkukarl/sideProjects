import pygame, sys, random
from pygame.locals import *

pygame.mixer.pre_init(frequency = 22050, size = -16, channels = 2, buffer = 512)
pygame.init()

# <function>
def getMask(image):
	mask = []
	for x in range(image.get_width()):
		mask.append([])
		for y in range(image.get_height()):
			mask[x].append(bool(image.get_at((x, y))[3]))
	return mask

def checkCollide(birdMask, birdx, birdy, pipeMask, pipex, pipey):
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

def scoreDisp(score):
	scoreStr = str(score)
	numx = 20
	numy = 20
	numWidth = 24
	for num in scoreStr:
		DISPLAYSURF.blit(numImgs[int(num)], (numx, numy))
		numx += numWidth

def paraInit():
	global birdy, velocity, wingOrder, pipex1, pipey1, pipex2, pipey2, pipex1Passed, pipex2Passed, gameOver, score, collide
	birdy = 10
	velocity = 0
	wingOrder = 0
	pipex1 = 300
	pipey1 = random.randint(-225, -125)
	pipex2 = 470
	pipey2 = random.randint(-225, -125)
	pipex1Passed = 0
	pipex2Passed = 0
	gameOver = 0
	score = 0
	collide = False
# </function>

# <parameter>
FPS = 30
fpsClock = pygame.time.Clock()
WIDTH = 288
HEIGHT = 512
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Flappy Bird')

birdx = 50
birdWIDTH = 34
birdHEIGHT = 24
GRAVITY = 0.25

pipeGAP = 150
pipeWIDTH = 52
pipeHEIGHT = 320

baseHEIGHT = 112
basex = 0
basey = HEIGHT - baseHEIGHT
# </parameter>

# <image>
birdImgs = [pygame.image.load('sprites/bird_down.png').convert_alpha(), pygame.image.load('sprites/bird_mid.png').convert_alpha(), pygame.image.load('sprites/bird_up.png').convert_alpha()]

bgImg = pygame.image.load('sprites/bg.png').convert_alpha()

pipe_upImg = pygame.image.load('sprites/pipe_up.png').convert_alpha()
pipe_downImg = pygame.image.load('sprites/pipe_down.png').convert_alpha()
# masks: birdMask has to be defined inside the while loop since birdImg changes over time
pipe_upMask = getMask(pipe_upImg)
pipe_downMask = getMask(pipe_downImg)

baseImg = pygame.image.load('sprites/base.png').convert_alpha()

numImgs = [pygame.image.load('sprites/' + str(i) + '.png').convert_alpha() for i in range(10)]
# </image>

# <audio>
hitSound = pygame.mixer.Sound('audio/hit.wav')
dieSound = pygame.mixer.Sound('audio/die.wav')
wingSound = pygame.mixer.Sound('audio/wing.wav')
pointSound = pygame.mixer.Sound('audio/point.wav')
# </audio>

# <initialisation>
paraInit()
# </initialisation>

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

	collide = checkCollide(birdMask, birdx, birdy, pipe_upMask, pipex1, pipey1) or checkCollide(birdMask, birdx, birdy, pipe_downMask, pipex1, pipey1 + pipeHEIGHT + pipeGAP) or checkCollide(birdMask, birdx, birdy, pipe_upMask, pipex2, pipey2) or checkCollide(birdMask, birdx, birdy, pipe_downMask, pipex2, pipey2 + pipeHEIGHT + pipeGAP) or birdy <= 0 or birdy >= HEIGHT - baseHEIGHT - birdHEIGHT

	if collide:
		if gameOver == 0:
			hitSound.play()
			gameOver = 1

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE or event.key == K_UP:
					paraInit()
					
	else:
		
		wingOrder = (wingOrder + 1) % 3

		velocity += GRAVITY
		birdy += velocity

		# pipe location looping
		if pipex1 - 2 < -pipeWIDTH:
			pipex1 = WIDTH
			pipey1 = random.randint(-225, -125)
			pipex1Passed = 0
		else:
			pipex1 = pipex1 - 2
			if pipex1 + pipeWIDTH < birdx:
				pipex1Passed += 1
			if pipex1Passed == 1:
				score += 1
				pointSound.play()

		if pipex2 - 2 < -pipeWIDTH:
			pipex2 = WIDTH
			pipey2 = random.randint(-225, -125)
			pipex2Passed = 0
		else:
			pipex2 = pipex2 - 2
			if pipex2 + pipeWIDTH < birdx:
				pipex2Passed += 1
			if pipex2Passed == 1:
				score += 1
				pointSound.play()

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
					wingSound.play()

	scoreDisp(score)
	pygame.display.update()
	fpsClock.tick(FPS)