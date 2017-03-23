import unittest
import main

class TestGaincard1(unittest.TestCase): #カードをサプライから獲得した際の挙動を確認
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
	
	def test_gain_copper(self): #銅貨を獲得する
		self._game.player[0].gaincard(2, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),1) #捨て札の枚数は1枚
		self.assertEqual(len(self._game.field.supnumber.get(2).pile), 45) #銅貨の残り枚数は45枚
		self.assertEqual(self._game.player[0].dispile[0].ename, "Copper") #捨て札にあるのは今獲得した銅貨
	
	def test_gain_estate(self): #屋敷を獲得する
		self._game.player[0].gaincard(5, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),1) #捨て札の枚数は1枚
		self.assertEqual(len(self._game.field.supnumber.get(5).pile), 7) #屋敷の残り枚数は7枚
		self.assertEqual(self._game.player[0].dispile[0].ename, "Estate") #捨て札にあるのは今獲得した屋敷	
	
class TestGaincard2(unittest.TestCase): #既にサプライにカードがないのにカードを獲得しようとした場合の挙動
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
		self._game.field.supnumber.get(2).pile.clear()
		self._game.field.supnumber.get(5).pile.clear()#銅貨と屋敷のサプライの山を消す
	
	def test_gain_copper(self): #銅貨を獲得しようとする
		self._game.player[0].gaincard(2, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),0) #捨て札の枚数は0枚
		self.assertEqual(len(self._game.field.supnumber.get(2).pile), 0) #銅貨の残り枚数は0枚
		self.assertEqual(self._game.player[0].dispile, []) #捨て札には何もない
		
	def test_gain_estate(self): #屋敷を獲得しようとする
		self._game.player[0].gaincard(5, self._game.field)
		self.assertEqual(len(self._game.player[0].dispile),0) #捨て札の枚数は0枚
		self.assertEqual(len(self._game.field.supnumber.get(5).pile), 0) #屋敷の残り枚数は0枚
		self.assertEqual(self._game.player[0].dispile, []) #捨て札には何もない