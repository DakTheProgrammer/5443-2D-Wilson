#######################################################################
#                  Mutiplayer Asteroids/SpaceBattle
#                  By: Dakota Wilson and Leslie Cook
#
#   A Pygame version of Asteroids using classes with OOP principles. A
#   class assignment to make a multiplayer game that has the following:
#  - 2 to N players playing at once
#  - a sprite spaceship that has obvious guns showing
#  - minimum of 10 different ships 
#  - Bullets striking another player reduces their health by 10%
#  - health regenerates by 10% for staying alive a set amount of time
#  - Bullet sprite can be any shape or color
#  - Ships movement determined by keyboard input
#  - Score kept in one upper corner of the game 
#
#######################################################################
import sys
from GameDriver import GameDriver
from Messenger import Messenger

#multiplayer needs: exchange(like a holder of the game), user, password = username + 2023!!!!!, port = 5672, host = terrywgriffin.com
if len(sys.argv) > 1:
    
    try:
        creds = {
            'exchange': sys.argv[1],
            'user': sys.argv[2],
            'password': sys.argv[2] + '2023!!!!!',
            'port': 5672,
            'host': 'terrywgriffin.com'
        }
    except:
        print('\n\nIncorrect arguments for multiplayer!!!')
        print('\n\nShould look like: `python main.py exchange username`')
        sys.exit()

    multiplayer = Messenger(creds)

    game = GameDriver('Game', multiplayer=multiplayer)
else:
    game = GameDriver('Game')

game.GameLoop()