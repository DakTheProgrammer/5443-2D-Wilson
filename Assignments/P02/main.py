#######################################################################
#                           Battle of the Hill
#                           By: Dakota Wilson
#
#   A turn based tank shooter written in pygame. This game involves
#   projectile motion on projectiles with given power shot out of a
#   tank. The goal is to destroy your opponent using specific strategy
#   of cratering a hill to find a shot to take out the enemy.
#
#   NOTE: PIL is used to trim transparency off of all PNGS to try
#   and get more consistent rectangles
#
#######################################################################
from GameDriver import GameDriver

#loop is used so that the game can easily be reset
while True:
    Game = GameDriver(background=(135, 206, 235), name="Battle of the Hill")
    Game.gameLoop()

    if Game.CheckExit():
        break