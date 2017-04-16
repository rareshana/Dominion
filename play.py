import main
import random
import card
import player
import aiplayer

def game_setup(number, nontest=None):
	game = main.Game(number)
	playerdecide(game, game.player, game.number, nontest)
	supply = supplydecide()
	game.starter(supply)
	return game

def playerdecide(game, playerr, people, nontest=None):
	if nontest == None:
		testplayer=[player.Player(game), player.Player(game), player.Player(game), player.Player(game)]
	else:
		testplayer=[aiplayer.AIPlayer1(game), player.HumanPlayer(game), aiplayer.AIPlayer1(game), aiplayer.AIPlayer1(game)]
		
	for i in range(people):
		playerr.append(testplayer[i])

	for i in range(people): #自分以外のプレイヤーのリストをothers に入れる
		tmp = playerr[:]
		tmp.remove(playerr[i])
		playerr[i].others = tmp

def supplydecide():
	return [card.Smithy, card.Village, card.Woodcutter, card.Market, card.Laboratory, card.Festival, card.CouncilRoom, card.Chancellor, card.Feast]