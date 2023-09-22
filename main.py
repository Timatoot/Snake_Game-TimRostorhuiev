import pygame
import random
import time

pygame.init()

#initiallize colours as constants
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#declaring variables
boardX = 500
boardY = 500
width = 10
height = 10
vel = 10
sPos = [[40,40], [60, 40], [80, 40], [100, 40]]
score = len(sPos) - 1
foodNum = 0
headDir = "Right"
font = pygame.font.Font('freesansbold.ttf', 32)

#create game window
size = (boardX, boardY)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")

#Main game variables
carryOn = True
clock = pygame.time.Clock()

def foodCoords():
	#making food variables global
	global foodX
	global foodY
	#random coordinated for food spawn
	foodX = random.randint(10, boardX - width - 10)
	foodY = random.randint(10, boardY - height - 10)

	foodX = (round(foodX / vel) * vel) + 1
	foodY = (round(foodY / vel) * vel) + 1

def foodSpawn():
	global foodNum
	global score

	if foodNum == 0:
		foodCoords()
		foodNum += 1
	pygame.draw.rect(screen, RED, (foodX, foodY, width - 2, height - 2))
	foodCollision()

def foodCollision():
	global foodHitbox
	global score
	global foodNum

	if (sPos[0][0] + width >= foodX and sPos[0][0] + width <= foodX + width) or (sPos[0][0] >= foodX - 2 and sPos[0][0] <= foodX + width - 2):
		if (sPos[0][1] + height >= foodY and sPos[0][1] + height <= foodY + height) or (sPos[0][1] >= foodY - 2 and sPos[0][1] <= foodY + height - 2):
			score = int(score)
			score += 1
			time.sleep(0.01)
			foodNum -= 1 
			sPos.append([0, 0])
	
def Head():
	global carryOn
	global headDir
	
	keys = pygame.key.get_pressed()

	#movement keys +/- speed/velocity
	if (keys[pygame.K_LEFT] and headDir != "Right") or headDir == "Left":
		if sPos[0][0] - vel >= 0:
			headDir = "Left"
		else:
			carryOn = False

	if (keys[pygame.K_RIGHT] and headDir != "Left") or headDir == "Right":
		if sPos[0][0] + vel + width <= boardX:
			headDir = "Right"
		else:
			carryOn = False

	if (keys[pygame.K_UP] and headDir != "Down") or headDir == "Up":
		if sPos[0][1] - vel >= 0:
			headDir = "Up"
		else:
			carryOn = False

	if (keys[pygame.K_DOWN] and headDir != "Up") or headDir == "Down":
		if sPos[0][1] + vel + width <= boardY:
			headDir = "Down"
		else:
			carryOn = False


def move():
	Head()
	if headDir == "Left":
		sPos[0][0] -= vel
	elif headDir == "Right":
		sPos[0][0] += vel
	elif headDir == "Up":
		sPos[0][1] -= vel
	elif headDir == "Down":
		sPos[0][1] += vel
	DrawSegment()

def DrawSegment():
	prevPieceX = sPos[0][0]
	prevPieceY = sPos[0][1]

	for i in range(len(sPos)-1):

		nextPieceX = sPos[i+1][0]
		nextPieceY = sPos[i+1][1]

		pygame.draw.rect(screen, GREEN, (sPos[i][0], sPos[i][1], width, height)) 
		pygame.draw.rect(screen, BLACK, (sPos[i][0], sPos[i][1], width, height), 1) 

		sPos[i+1][0] = prevPieceX
		sPos[i+1][1] = prevPieceY

		pygame.draw.rect(screen, GREEN, (sPos[i+1][0], sPos[i+1][1], width, height)) 
		pygame.draw.rect(screen, BLACK, (sPos[i+1][0], sPos[i+1][1], width, height), 1) 

		prevPieceX = nextPieceX
		prevPieceY = nextPieceY


#Main loop
while carryOn:
	clock.tick(20)
	#set background
	screen.fill(BLUE)

	score = str(score)
	text = font.render('Score = ' + score, True, WHITE)
	textRect = text.get_rect()
	textRect.center = (boardX // 2, 50)
	screen.blit(text, textRect)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			carryOn = False


	#creates player and food
	move()
	foodSpawn()

	pygame.display.update()	
#exit game
pygame.quit() 