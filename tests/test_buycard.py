import unittest
import main

class TestBuyCard1(unittest.TestCase): #カードをサプライから購入した際の挙動を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
		self._game.player[0].coins = 3 #場に3金出したとする
	
	def test_gain_copper(self): #銅貨を購入する
		self._game.player[0].buycard(2, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),1) #捨て札の枚数は1枚
		self.assertEqual(len(self._game.field.supnumber.get(2).pile), 45) #銅貨の残り枚数は45枚
		self.assertEqual(self._game.player[0].dispile[0].ename, "Copper") #捨て札にあるのは今獲得した銅貨
		self.assertEqual(self._game.player[0].coins, 3) #残りは3金
		self.assertEqual(self._game.player[0].restbuys, 0) #残り購入権は0
	
	def test_gain_estate(self): #屋敷を購入する
		self._game.player[0].buycard(5, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),1) #捨て札の枚数は1枚
		self.assertEqual(len(self._game.field.supnumber.get(5).pile), 7) #屋敷の残り枚数は7枚
		self.assertEqual(self._game.player[0].dispile[0].ename, "Estate") #捨て札にあるのは今獲得した屋敷	
		self.assertEqual(self._game.player[0].coins, 1) #残りは3金
		self.assertEqual(self._game.player[0].restbuys, 0) #残り購入権は0