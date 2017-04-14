import main
import random
import card
import player

def game_setup(number, nontest=None):
	game = main.Game(number)
	playerdecide(game.player, game.number, nontest)
	game.starter()
	return game

def playerdecide(playerr, people, nontest=None):
	if nontest == None:
		testplayer=[player.Player(), player.Player(), player.Player(), player.Player()]
	else:
		testplayer=[player.AIPlayer(), player.AIPlayer(), player.AIPlayer(), player.AIPlayer()]
	
	for i in range(people):
		playerr.append(testplayer[i])

	for i in range(people): #自分以外のプレイヤーのリストをothers に入れる
		tmp = playerr[:]
		tmp.remove(playerr[i])
		playerr[i].others = tmp
		
	print(playerr)
