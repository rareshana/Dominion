import unittest
import main

class TestDraw1(unittest.TestCase): #初期デッキから5枚引いた時の枚数を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
		
	def test_draw_handnumber(self): #手札の枚数チェック
		self.assertEqual(len(self._game.player[0].hand), 5)
	
	def test_draw_decknumber(self): #デッキの枚数チェック
		self.assertEqual(len(self._game.player[0].deck), 5)

class TestDraw2(unittest.TestCase): #初期デッキから15枚引こうとした時の枚数を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
		
	def test_draw_handnumber(self): #手札の枚数チェック
		self._game.player[0].draw(5)
		self._game.player[0].draw(5)
		self.assertEqual(len(self._game.player[0].hand), 10)
	
	def test_draw_decknumber(self): #デッキの枚数チェック
		self._game.player[0].draw(5)
		self._game.player[0].draw(5)
		self.assertEqual(len(self._game.player[0].deck), 0)
		
class TestDraw3(unittest.TestCase): #手札5枚、捨て札5枚、デッキ2枚の時に3枚ドローする時の枚数を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
		for i in range(5):
			self._game.player[0].gaincard(5, self._game.field)
		del self._game.player[0].deck[2:]
		
	def test_draw_handnumber(self): #手札の枚数チェック
		self._game.player[0].draw(3)
		self.assertEqual(len(self._game.player[0].hand), 8)
	
	def test_draw_decknumber(self): #デッキの枚数チェック
		self._game.player[0].draw(3)
		self.assertEqual(len(self._game.player[0].deck), 4)
	
	def test_draw_dispilenumber(self): #デッキの枚数チェック
		self._game.player[0].draw(3)
		self.assertEqual(len(self._game.player[0].dispile), 0)
		 
	
