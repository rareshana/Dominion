import main

game = main.Game(2) #２人プレイの設定


for i in range(5):
	game.player[0].gaincard(5, game.field)
del game.player[0].deck[2:]

print(len(game.player[0].deck), len(game.player[0].hand), len(game.player[0].dispile))

game.player[0].draw(3)

print(len(game.player[0].deck), len(game.player[0].hand), len(game.player[0].dispile))
