import unittest
import main
import card
import play

class TestCleanUpPhase(unittest.TestCase): #クリーンアップフェイズの挙動を確認する
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(2)
		self._game.beginturn(0)
		self._game.player[0].phaseend()
		self._game.player[0].phaseend()
		
		
	def test_cleanup(self): 
		self._game.player[0].phaseend()
		self.assertEqual(len(self._game.player[0].dispile), 5) 
		self.assertEqual(len(self._game.player[0].hand), 5)
		self.assertEqual(len(self._game.player[0].deck), 0)
	