import unittest
import main
import card
import play

class TestCouncilRoom(unittest.TestCase): #アクションフェイズで議事堂をプレイするときの挙動を確認する(す手札の6枚目にカードを追加してチェックします)
	def setUp(self):
		print('setUp')
		self._game = play.game_setup()

def test_play_councilroom(self):
		self._game.player[0].hand.append(card.CouncilRoom()) 
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right")
		self.assertEqual(len(self._game.player[0].playarea),1)
		self.assertEqual(len(self._game.player[0].hand), 9)
		self.assertEqual(len(self._game.player[1].hand), 6)
		self.assertEqual(len(self._game.player[2].hand), 6)
		self.assertEqual(self._game.player[0].restactions, 0) 
		self.assertEqual(self._game.player[0].coins, 0) 
		self.assertEqual(self._game.player[0].restbuys, 0)
		self.assertFalse(isinstance(self._game.player[0].phase, main.ActionPhase))