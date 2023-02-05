#######################################################################
#                           Hipster Tetris
#                         By: Dakota Wilson
#
#   A Pygame version of Tetris using classes with OOP principles. A
# class assignment to make a tile based game that has collisions.
#
#######################################################################
from Grid import Grid
from T import T
from I import I
from O import O
from S import S
from L import L
from NextBox import NextBox
import pygame
import random

pygame.init()
speed = 1
#buffer to balance movement speed
moveBuffer = 0
screen_Size = 800
maxBuffer = 1000

score = 0

#fonts:
font = pygame.font.Font("Fonts/Lora-Bold.ttf", 35)
subFont = pygame.font.Font("Fonts/Lora-Bold.ttf", 27)
title = font.render("HIPSTER TETRIS", True, ((208, 220, 216)))
subtitle = subFont.render("By: Dakota Wilson", True, ((208, 220, 216)))
instruction = font.render("Instructions:", True, ((208, 220, 216)))
instructions_Space = subFont.render("SPACE: Rotate", True, ((208, 220, 216)))
instructions_Left = subFont.render("A: Left", True, ((208, 220, 216)))
instructions_Right = subFont.render("D: Right", True, ((208, 220, 216)))
instructions_Place = subFont.render("S: Place", True, ((208, 220, 216)))
instructions_Restart = subFont.render("R: Restart", True, ((208, 220, 216)))
gameOver = font.render("GAME OVER!", True, ((255, 0, 0)))

#background music:
pygame.mixer.init()
pygame.mixer.music.load('Audio/Tetris.mp3')
pygame.mixer.music.play(-1)

#gets a random new Tetris piece
def getRandomPiece(screen, gameSpace):
    r = random.randint(0,4)
    if r == 0:
        return T(screen, gameSpace)
    elif r == 1:
        return I(screen, gameSpace)
    elif r == 2:
        return O(screen, gameSpace)
    elif r == 3:
        return S(screen, gameSpace)
    elif r == 4:
        return L(screen, gameSpace)

if __name__ == '__main__':
    screen = pygame.display.set_mode((screen_Size, screen_Size))
    pygame.display.set_caption("Tetris")

    #Used to get game clock used for frame rate
    clock = pygame.time.Clock()

    running = True
    #when game over used to display game over text
    over = False
    #used to know when to make game faster holds old score
    oldScore = 0

    #creates starting items
    gameSpace = Grid(screen)
    piece = getRandomPiece(screen, gameSpace)
    nextPiece = getRandomPiece(screen, gameSpace)
    nextBox = NextBox(screen, nextPiece)

    groundedShapes = []

    while running:
        #buttons available when the game isn't being played
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    over = False

                    piece = getRandomPiece(screen, gameSpace)
                    nextPiece = getRandomPiece(screen, gameSpace)
                    nextBox = NextBox(screen, nextPiece)

                    groundedShapes = []

                    score = 0
                    oldScore = 0
                    speed = 1


        #gets the time since the last clock cycle call and limits frames to 60FPS
        #(dt makes frame rate independent if user computer cant handle 60FPS)
        dt = clock.tick(60)

        #fills the screen with a soft grey for the eye
        screen.fill((34, 40, 49))
        
        #real game logic
        if not piece.gameOver(groundedShapes):
            score += gameSpace.checkClear(groundedShapes)

            #when the score hasn't just been updated and 10 lines have been cleared increase speed
            if oldScore < score:
                if score % 1000 == 0:
                    speed += 1
                    oldScore = score

            #logic for when the pice gets placed 
            if piece.isGrounded(groundedShapes):
                groundedShapes.append(piece)
                piece = nextPiece
                nextPiece = getRandomPiece(screen, gameSpace)
                nextBox.setPiece(nextPiece)
            
            #draws the piece
            piece.draw()

            #used to make sure piece is moving too fast
            #skips move in that case to slow it down
            #used to allow that classic tetris look when moving
            if moveBuffer >= maxBuffer:
                piece.move()
                moveBuffer = 0
            else:
                moveBuffer += speed * dt

            #user controls(needs quit so user can quit while running)
            #run game to see what each are used for specifically
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        piece.rotate(groundedShapes)
                    if event.key == pygame.K_d:
                        piece.right(groundedShapes)
                    if event.key == pygame.K_a:
                        piece.left(groundedShapes)
                    if event.key == pygame.K_s:
                        while not piece.isGrounded(groundedShapes):
                            piece.move()
                    if event.key == pygame.K_r:
                        over = False
                        piece = getRandomPiece(screen, gameSpace)
                        nextPiece = getRandomPiece(screen, gameSpace)
                        nextBox = NextBox(screen, nextPiece)

                        groundedShapes = []

                        score = 0
                        oldScore = 0
                        speed = 1
        else:
            #makes the piece that ended the game red
            piece.badPiece()
            groundedShapes.append(piece)

            over = True            

        #always draws these
        for shapes in groundedShapes:
                shapes.draw()

        gameSpace.draw()

        nextBox.draw()

        scoreLabel = font.render("SCORE: " + str(score), True, ((208, 220, 216)))
        speedLabel = font.render("SPEED: " + str(speed), True, ((208, 220, 216)))

        screen.blit(scoreLabel, (screen.get_width() * .66,screen.get_height() * .375))
        screen.blit(speedLabel, (screen.get_width() * .6625,screen.get_height() * .475))
        screen.blit(title, (screen.get_width() * .575,screen.get_height() * .6))
        screen.blit(subtitle, (screen.get_width() * .6,screen.get_height() * .65))
        screen.blit(instruction, (screen.get_width() * .625,screen.get_height() * .75))
        screen.blit(instructions_Space, (screen.get_width() * .64,screen.get_height() * .8))
        screen.blit(instructions_Right, (screen.get_width() * .695,screen.get_height() * .835))
        screen.blit(instructions_Left, (screen.get_width() * .705,screen.get_height() * .865))
        screen.blit(instructions_Place, (screen.get_width() * .695,screen.get_height() * .895))
        screen.blit(instructions_Restart, (screen.get_width() * .67,screen.get_height() * .925))

        #display game over
        if over:
            screen.blit(gameOver, (screen.get_width() / 8,screen.get_height() / 2))

        #updates the screen
        pygame.display.flip()