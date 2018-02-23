import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
from card import *
from field import *
from player import *

class Game:
    def __init__(self, user1, user2):
        self.field = Field()
        self.player1 = Player(user1)
        self.player2 = Player(user2)
        self.endGame = False
    def ready(self):
        pass
        
    def start(self):
        pass

def initgame():
    player = User(money = 1000000)
    computer = User(money = 1000000)
    replay = True
    while replay:
        game = Game(player, computer)
        game.start()
        if game.winner == player:
            player.money += game.result
            computer.money -= game.result
        else:
            player.money -= game.result
            computer.money += game.result
        replay = askforReplay(None)
    sys.exit(0)
