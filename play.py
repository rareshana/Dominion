import main

game = main.Game(2) #２人プレイの設定
print(game.player[0].deck)
exec("game.player[0].shuffle()")
print(game.player[0].deck)