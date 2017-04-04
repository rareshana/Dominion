import unittest
import main
import card

class TestActionPhase(unittest.TestCase): #アクションフェイズでカードをプレイするときの挙動を確認する(すべて手札の6枚目にカードを追加してチェックします)
	def setUp(self):
		print('setUp')
		self._game = main.Game(2)
		self._game.beginturn(0)
	
	def test_play_copper(self): #銅貨をプレイしようとする
		self._game.player[0].hand.append(card.Copper()) #銅貨を追加
		self._game.player[0].playcard(5, "right") #銅貨をプレイしようとする
		self.assertEqual(len(self._game.player[0].playarea),0) #場の枚数は0枚
		self.assertEqual(len(self._game.player[0].hand), 6) #手札の残り枚数は6枚
		self.assertEqual(self._game.player[0].coins, 0) #残りは0金
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
	
	