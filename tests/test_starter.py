import unittest
import main
import play

class TestStarter1(unittest.TestCase): #3人プレイ時のサプライに積まれている勝利点カード3種の枚数を確認＋呪い
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(3)
	
	def test_starter_estate(self): #屋敷の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[0].pile), 12)
	
	def test_starter_duchy(self): #公領の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[1].pile), 12)
	
	def test_starter_province(self): #属州の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[2].pile), 12)
	
	def test_starter_curse(self): #呪いの枚数チェック
		self.assertEqual(len(self._game.field.cursepile.pile), 20)

class TestStarter2(unittest.TestCase): #4人プレイ時のサプライに積まれている勝利点カード3種の枚数を確認＋呪い
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(4)
	
	def test_starter_estate(self): #屋敷の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[0].pile), 12)
	
	def test_starter_duchy(self): #公領の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[1].pile), 12)
	
	def test_starter_province(self): #属州の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[2].pile), 12)
	
	def test_starter_curse(self): #呪いの枚数チェック
		self.assertEqual(len(self._game.field.cursepile.pile), 30)