import unittest
import main

class TestStarter1(unittest.TestCase): #カードをサプライから獲得した際の挙動を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
	
	def test_gain_copper(self): #銅貨を獲得する
		self._game.player[0].gaincard(2, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),1) #捨て札の枚数は1枚
		self.assertEqual(len(self._game.field.supnumber(2).pile), 43) #銅貨の残り枚数は43枚
		self.assertEqual(self._game.player[0].dispile[0].ename, "Copper") #捨て札にあるのは今獲得した銅貨
	
	def test_gain_estate(self): #屋敷を獲得する
		self._game.player[0].gaincard(5, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),1) #捨て札の枚数は1枚
		self.assertEqual(len(self._game.field.supnumber(5).pile), 11) #屋敷の残り枚数は11枚
		self.assertEqual(self._game.player[0].dispile[0].ename, "Estate") #捨て札にあるのは今獲得した屋敷	
	