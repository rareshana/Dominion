import main
import random
import card
import player
import aiplayer
import humanplayer

def game_setup(number, nontest=None):
	game = main.Game(number)
	player_entry(game, game.player, game.number, nontest)
	supply = supply_decide()
	game.starter(supply)
	return game

def player_entry(game, playerr, people, nontest=None):
	testplayer = player_decide(game, nontest)
	
	for i in range(people):
		playerr.append(testplayer[i])

	for i in range(people): #自分以外のプレイヤーのリストをothers に入れる
		tmp = playerr[:]
		tmp.remove(playerr[i])
		playerr[i].other_players = tmp

def player_decide(game, nontest):
	if nontest == None:
		testplayer=[player.Player(game), player.Player(game), player.Player(game), player.Player(game)]
		return testplayer
	testplayer=[aiplayer.AIPlayer1(game), aiplayer.AIPlayer2(game), humanplayer.HumanPlayer(game), aiplayer.AIPlayer1(game)]
	return testplayer
	
def supply_decide():
	return [card.Smithy, card.Feast, card.Library, card.Market, card.Laboratory, card.Festival, card.CouncilRoom, card.Cellar, card.Adventurer, card.Workshop]