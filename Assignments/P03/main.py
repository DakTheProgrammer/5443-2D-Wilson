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

    Messenger(creds)

    game = GameDriver('Game')
    print('Multi')
else:
    game = GameDriver('Game')

game.GameLoop()