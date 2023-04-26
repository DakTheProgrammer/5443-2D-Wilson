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

    messenger = Messenger(creds)

    game = GameDriver('Game', messenger, width=1200, height=720, background=(33,33,33))
else:
    print('\n\nIncorrect arguments for multiplayer!!!')
    print('\n\nShould look like: `python main.py exchange username`')
    sys.exit()

game.GameLoop()