import sys
from GameDriver import GameDriver

try:
    player = int(sys.argv[1])
except:
    print("Invalid argument")
    sys.exit()

Game = GameDriver(player,background=(135, 206, 235))

Game.gameLoop()