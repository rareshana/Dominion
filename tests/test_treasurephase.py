import unittest
import main
import card
import play

class TestTreasurePhase(unittest.TestCase): #財宝フェイズでカードをプレイするときの挙動を確認する(すべて手札の6枚目にカードを追加してチェックします)
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(2)
		self._game.beginturn(0)
	
	def test_play_copper(self): #銅貨をプレイしようとする
		self._game.player[0].hand.append(card.Copper()) #銅貨を追加
		self._game.player[0].playcard(5, "right") #銅貨をプレイしようとする
		self.assertEqual(len(self._game.player[0].playarea),1) #場の枚数は1枚
		self.assertEqual(len(self._game.player[0].hand), 5) #手札の残り枚数は5枚
		self.assertEqual(self._game.player[0].coins, 1) #残りは1金
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
		
	def test_play_silver(self): #銀貨をプレイしようとする
		self._game.player[0].hand.append(card.Silver()) 
		self._game.player[0].playcard(5, "right") 
		self.assertEqual(len(self._game.player[0].playarea),1) #場の枚数は1枚
		self.assertEqual(len(self._game.player[0].hand), 5) #手札の残り枚数は5枚
		self.assertEqual(self._game.player[0].coins, 2) #残りは2金
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
	
	def test_play_gold(self): #金貨をプレイしようとする
		self._game.player[0].hand.append(card.Gold()) 
		self._game.player[0].playcard(5, "right") 
		self.assertEqual(len(self._game.player[0].playarea),1) #場の枚数は1枚
		self.assertEqual(len(self._game.player[0].hand), 5) #手札の残り枚数は5枚
		self.assertEqual(self._game.player[0].coins, 3) #残りは3金
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
		
	def test_play_estate(self): #屋敷をプレイしようとする
		self._game.player[0].hand.append(card.Estate()) #屋敷を追加
		self._game.player[0].playcard(5, "right") #屋敷をプレイしようとする
		self.assertEqual(len(self._game.player[0].playarea),0) #場の枚数は0枚
		self.assertEqual(len(self._game.player[0].hand), 6) #手札の残り枚数は6枚
		self.assertEqual(self._game.player[0].coins, 0) #残りは0金
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
	
	