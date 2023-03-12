from GameDriver import GameDriver

while True:
    Game = GameDriver(background=(135, 206, 235))
    Game.gameLoop()

    if Game.CheckExit():
        break