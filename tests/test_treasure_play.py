import unittest
import main

class TestTreasurePlay1(unittest.TestCase): #3人プレイ時のサプライに積まれている勝利点カード3種の枚数を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
	
	def test_play_copper(self): #銅貨をプレイする
		copper=main.Copper()
		self._game.player[0].hand.append(copper)
		self._game.player[0].playcard(5)
		self.assertEqual(self._game.player[0].coins,1)
		
	def test_play_silver(self): #銀貨をプレイする
		silver = main.Silver()
		self._game.player[0].hand.append(silver)
		self._game.player[0].playcard(5)
		self.assertEqual(self._game.player[0].coins,2)
	
	def test_play_gold(self): #金貨をプレイする
		gold = main.Gold()
		self._game.player[0].hand.append(gold)
		self._game.player[0].playcard(5)
		self.assertEqual(self._game.player[0].coins,3)