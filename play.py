import main

game = main.Game(2) #２人プレイの設定

game.player[0].draw(5)
print(game.player[0].hand)
game.player[0].playcard(2)
print(game.player[0].hand)
print(game.player[0].playarea)
game.player[0].playcard(2)
print(game.player[0].hand)
print(game.player[0].playarea)