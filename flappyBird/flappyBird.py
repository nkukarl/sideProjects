import pygame, sys, random
from pygame.locals import *

# sound delay on ubuntu
# pygame.mixer.pre_init(frequency = 22050, size = -16, channels = 2, buffer = 512)
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
	numx = 10
	numy = 40
	for num in scoreStr:
		DISPLAYSURF.blit(digitImgs[int(num)], (numx, numy))
		if num == '1':
			numx += 25
		else:
			numx += 28

def starDisp(starCount):
	starx = 10
	stary = 10
	for _ in range(starCount):
		DISPLAYSURF.blit(starImg, (starx, stary))
		starx += 24

def paraInit():
	global birdy, velocity, wingOrder, pipeGapDecr, starCount, pipe1Gap, pipex1, pipey1, pipe2Gap, pipex2, pipey2, pipex1Passed, pipex2Passed, gameOver, score, collided, paused
	birdy = 40
	velocity = 0
	wingOrder = 0

	DIFFICULTY = random.choice(pipeGapDecrMap.keys())
	pipeGapDecr = pipeGapDecrMap[DIFFICULTY][0]
	starCount = pipeGapDecrMap[DIFFICULTY][1]

	pipe1Gap = pipeGAP
	pipex1 = 300
	pipey1 = random.randint(-(pipe1Gap / 2 + 180), -100)
	pipe2Gap = pipeGAP
	pipex2 = 470
	pipey2 = random.randint(-(pipe2Gap / 2 + 180), -100)
	pipex1Passed = 0
	pipex2Passed = 0
	gameOver = 0
	score = 0
	collided = False
	paused = 0

# </function>

# <parameter>
FPS = 30
fpsClock = pygame.time.Clock()
WIDTH = 288
HEIGHT = 512
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Flappy Bird')

birdx = 40
birdWIDTH = 34
birdHEIGHT = 24
GRAVITY = 0.25

pipeGAP = 140

# pipeGapDecrMap: each entry --> difficulty: (pipeGapDecrStep, starCount)
pipeGapDecrMap = {'EASY': (0, 1), 'MEDIUM': (4, 2), 'HARD': (8, 3), 'INSANE': (16, 4)}
pipeWIDTH = 52
pipeHEIGHT = 320

baseHEIGHT = 112
basex = 0
basey = HEIGHT - baseHEIGHT

pauseWIDTH = 64
pauseHEIGHT = 64
# </parameter>

# <image>

starImg = pygame.image.load('sprites/star.png').convert_alpha()

birdImgs = [pygame.image.load('sprites/bird_down.png').convert_alpha(), pygame.image.load('sprites/bird_mid.png').convert_alpha(), pygame.image.load('sprites/bird_up.png').convert_alpha()]

bgImg = pygame.image.load('sprites/bg.png').convert_alpha()

pipe_upImg = pygame.image.load('sprites/pipe_up.png').convert_alpha()
pipe_downImg = pygame.image.load('sprites/pipe_down.png').convert_alpha()
# masks: birdMask has to be defined inside the while loop since birdImg changes over time
pipe_upMask = getMask(pipe_upImg)
pipe_downMask = getMask(pipe_downImg)

baseImg = pygame.image.load('sprites/base.png').convert_alpha()

digitImgs = [pygame.image.load('sprites/' + str(i) + '.png').convert_alpha() for i in range(10)]
pauseImg = pygame.image.load('sprites/pause.png').convert_alpha()

# message generation using http://fontmeme.com/pixel-fonts/

continueMsgImg = pygame.image.load('sprites/continueMsg.png').convert_alpha()
restartMsgImg = pygame.image.load('sprites/restartMsg.png').convert_alpha()
pauseMsgImg = pygame.image.load('sprites/pauseMsg.png').convert_alpha()
upMsgImg = pygame.image.load('sprites/upMsg.png').convert_alpha()

overMsgImg = pygame.image.load('sprites/overMsg.png').convert_alpha()

# </image>

# <audio>
startSound = pygame.mixer.Sound('audio/start.wav')
collideSound = pygame.mixer.Sound('audio/collide.wav')
flySound = pygame.mixer.Sound('audio/fly.wav')
pointSound = pygame.mixer.Sound('audio/point.wav')
pauseSound = pygame.mixer.Sound('audio/pause.wav')
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
	DISPLAYSURF.blit(pipe_downImg, (pipex1, pipey1 + pipeHEIGHT + pipe1Gap))

	DISPLAYSURF.blit(pipe_upImg, (pipex2, pipey2))
	DISPLAYSURF.blit(pipe_downImg, (pipex2, pipey2 + pipeHEIGHT + pipe2Gap))

	DISPLAYSURF.blit(baseImg, (basex, basey))

	starDisp(starCount)
	

	collided = checkCollide(birdMask, birdx, birdy, pipe_upMask, pipex1, pipey1) or checkCollide(birdMask, birdx, birdy, pipe_downMask, pipex1, pipey1 + pipeHEIGHT + pipe1Gap) or checkCollide(birdMask, birdx, birdy, pipe_upMask, pipex2, pipey2) or checkCollide(birdMask, birdx, birdy, pipe_downMask, pipex2, pipey2 + pipeHEIGHT + pipe2Gap) or birdy <= 0 or birdy >= HEIGHT - baseHEIGHT - birdHEIGHT

	if collided:

		DISPLAYSURF.blit(restartMsgImg, (0, 440))
		DISPLAYSURF.blit(overMsgImg, (18, 200))

		if gameOver == 0:
			collideSound.play()
			gameOver = 1

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					paraInit()
					
	else:
		
		if not paused:
			'''
			pause
			play
			'''
			DISPLAYSURF.blit(upMsgImg, (0, 440))
			DISPLAYSURF.blit(pauseMsgImg, (0, 465))
			

			wingOrder = (wingOrder + 1) % 3

			velocity += GRAVITY
			birdy += velocity

			# pipe location looping
			if pipex1 - 2 < -pipeWIDTH:
				pipex1 = WIDTH
				pipey1 = random.randint(-(pipe1Gap / 2 + 180), -100)
				pipe1Gap -= pipeGapDecr
				pipex1Passed = 0
			else:
				pipex1 = pipex1 - 2
				if pipex1 + pipeWIDTH < birdx:
					pipex1Passed += 1
				if pipex1Passed == 1:
					score += 15 - int(pipe1Gap / 10)
					pointSound.play()

			if pipex2 - 2 < -pipeWIDTH:
				pipex2 = WIDTH
				pipey2 = random.randint(-(pipe2Gap / 2 + 180), -100)
				pipe2Gap -= pipeGapDecr
				pipex2Passed = 0
			else:
				pipex2 = pipex2 - 2
				if pipex2 + pipeWIDTH < birdx:
					pipex2Passed += 1
				if pipex2Passed == 1:
					score += 15 - int(pipe2Gap / 10)
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
					if event.key == K_UP:
						velocity = -3
						flySound.play()
					if event.key == K_ESCAPE:
						paused = 1
						pauseSound.play()

		else:
			DISPLAYSURF.blit(pauseImg, ((WIDTH - pauseWIDTH) / 2, (HEIGHT - pauseHEIGHT) / 2))
			DISPLAYSURF.blit(continueMsgImg, (0, 440))
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_UP:
					paused = 0
					



	scoreDisp(score)
	pygame.display.update()
	fpsClock.tick(FPS)