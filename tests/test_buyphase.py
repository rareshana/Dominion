import unittest
import main
import card
import play

class TestBuyPhase(unittest.TestCase): #購入フェイズでカードをプレイするときの挙動を確認する 適当に何金か持っていると仮定します
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(2)
		self._game.beginturn(0)
	
	def test_buy_copper(self): #銅貨を購入する
		self._game.player[0].coins = 3 #3金持っていると仮定する 
		self._game.player[0].buycard(2) #銅貨を購入しようとする
		self.assertEqual(self._game.player[0].dispile[-1].ename, "Copper") #捨て札の一番上は銅貨
		self.assertEqual(self._game.player[0].coins, 3) #残りは3金
		self.assertEqual(self._game.player[0].restbuys, 0) #残り購入権は0
		
	def test_buy_estate(self): #屋敷を購入する
		self._game.player[0].coins = 3 #3金持っていると仮定する 
		self._game.player[0].buycard(5) #屋敷を購入しようとする
		self.assertEqual(self._game.player[0].dispile[-1].ename, "Estate") #捨て札の一番上は屋敷
		self.assertEqual(self._game.player[0].coins, 1) #残りは1金
		self.assertEqual(self._game.player[0].restbuys, 0) #残り購入権は0

	def test_buy_twocopper(self): #銅貨を2枚購入しようとする
		self._game.player[0].coins = 3 #3金持っていると仮定する 
		self._game.player[0].buycard(2) #銅貨を購入しようとする
		self.assertEqual(self._game.player[0].dispile[-1].ename, "Copper") #捨て札の一番上は銅貨
		self.assertEqual(self._game.player[0].coins, 3) #残りは3金
		self.assertEqual(self._game.player[0].restbuys, 0) #残り購入権は0
		
		self._game.player[0].buycard(5) #続けて屋敷を購入しようとする(買えない)
		self.assertEqual(self._game.player[0].dispile[-1].ename, "Copper") #捨て札の一番上は銅貨
		self.assertEqual(self._game.player[0].coins, 3) #残りは3金
		self.assertEqual(self._game.player[0].restbuys, 0) #残り購入権は0