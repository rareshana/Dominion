import unittest
import main

class TestStarter1(unittest.TestCase): #3人プレイ時のサプライに積まれている勝利点カード3種の枚数を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(3)
	
	def test_starter_estate(self): #屋敷の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[0]), 12)
	
	def test_starter_duchy(self): #公領の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[1]), 12)
	
	def test_starter_province(self): #属州の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[2]), 12)

class TestStarter2(unittest.TestCase): #4人プレイ時のサプライに積まれている勝利点カード3種の枚数を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(4)
	
	def test_starter_estate(self): #屋敷の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[0]), 12)
	
	def test_starter_duchy(self): #公領の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[1]), 12)
	
	def test_starter_province(self): #属州の枚数チェック
		self.assertEqual(len(self._game.field.victorypile[2]), 12)