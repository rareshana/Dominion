import main
import random
import card
import player
import aiplayer

def game_setup(number, nontest=None):
	game = main.Game(number)
	playerdecide(game, game.player, game.number, nontest)
	game.starter()
	return game

def playerdecide(game, playerr, people, nontest=None):
	if nontest == None:
		testplayer=[player.Player(game), player.Player(game), player.Player(game), player.Player(game)]
	else:
		testplayer=[aiplayer.AIPlayer(game), aiplayer.AIPlayer(game), aiplayer.AIPlayer(game), aiplayer.AIPlayer(game)]
	
	for i in range(people):
		playerr.append(testplayer[i])

	for i in range(people): #自分以外のプレイヤーのリストをothers に入れる
		tmp = playerr[:]
		tmp.remove(playerr[i])
		playerr[i].others = tmp
