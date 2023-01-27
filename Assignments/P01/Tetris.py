#TO DO: L piece, Z piece, FONTS, SCORE
from Grid import Grid
from T import T
from I import I
from O import O
from NextBox import NextBox
import pygame
import random

speed = 10
moveBuffer = 0
screen_Size = 800
maxBuffer = 1000

def getRandomPiece(screen, gameSpace):
    r = random.randint(0,2)
    if r == 0:
        return T(screen, gameSpace)
    elif r == 1:
        return I(screen, gameSpace)
    elif r == 2:
        return O(screen, gameSpace)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((screen_Size, screen_Size))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    running = True

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

        #gets the time since the last clock cycle call and limits frames to 60FPS
        #(dt makes frame rate independent if user computer cant handle 60FPS)
        dt = clock.tick(60)

        #fills the screen with a soft grey for the eye
        screen.fill((34, 40, 49))
        
        if not piece.gameOver(groundedShapes):
            nextBox.draw()
            gameSpace.checkClear(groundedShapes)

            if piece.isGrounded(groundedShapes):
                groundedShapes.append(piece)
                piece = nextPiece
                nextPiece = getRandomPiece(screen, gameSpace)
                nextBox.setPiece(nextPiece)
            
            for shapes in groundedShapes:
                shapes.draw()
            
            piece.draw()

            #draws the top layer
            gameSpace.draw()

            if moveBuffer >= maxBuffer:
                piece.move()
                moveBuffer = 0
            else:
                moveBuffer += speed * dt 

            #user controls(needs quit so user can quit while running)
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
        else:
            groundedShapes.append(piece)

            for shapes in groundedShapes:
                shapes.draw()

            gameSpace.draw()

            nextBox.draw()


        #updates the screen
        pygame.display.flip()