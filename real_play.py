import main
import random
import card
import player
import play
import aiplayer

game = play.game_setup(2, 1)

print(len(game.field.supnumber.get(7).pile))
game.begingame()
