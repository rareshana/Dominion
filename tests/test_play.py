import unittest
import main
import card
import play

class Testplay(unittest.TestCase): #アクションフェイズでカードをプレイするときの挙動を確認する(すべて手札の6枚目にカードを追加してチェックします)
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(3)
		
	def test_end_actionphase(self): #何も持っていなければアクションフェイズが終了している
		self.assertEqual(self._game.player[0].others, [self._game.player[1], self._game.player[2]]) 
	

	
	