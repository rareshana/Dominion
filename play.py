import main
import random
import card

game = main.Game(2,2) #２人プレイの設定
print(len(game.field.supnumber.get(7).pile))
game.begingame()

