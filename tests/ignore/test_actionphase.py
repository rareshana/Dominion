import unittest
import main
import card
import play

class TestActionPhase(unittest.TestCase): #アクションフェイズでカードをプレイするときの挙動を確認する(すべて手札の6枚目にカードを追加してチェックします)
	def setUp(self):
		print('setUp')
		self._game = play.game_setup(2)
		
	def test_end_actionphase(self): #何も持っていなければアクションフェイズが終了している
		self._game.beginturn(0)
		self.assertFalse(isinstance(self._game.player[0].phase, main.ActionPhase)) 
	
	def test_play_smithy(self):
		self._game.player[0].hand.append(card.Smithy()) #鍛冶屋を追加
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right") #鍛冶屋をプレイする
		self.assertEqual(len(self._game.player[0].playarea),1)#場の枚数は1枚
		self.assertEqual(len(self._game.player[0].hand), 8) #手札の残り枚数は5+3枚
		self.assertEqual(self._game.player[0].restactions, 0) #残りアクション権は0
		self.assertFalse(isinstance(self._game.player[0].phase, main.ActionPhase))
		
	def test_play_village(self):
		self._game.player[0].hand.append(card.Village()) #村を追加
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right")
		self.assertEqual(len(self._game.player[0].playarea),1)#場の枚数は1枚
		self.assertEqual(len(self._game.player[0].hand), 6) #手札の残り枚数は5+1枚
		self.assertEqual(self._game.player[0].restactions, 2) #残りアクション権は2
		self.assertTrue(isinstance(self._game.player[0].phase, main.ActionPhase))
		
	def test_play_woodcutter(self):
		self._game.player[0].hand.append(card.Woodcutter()) 
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right")
		self.assertEqual(len(self._game.player[0].playarea),1)
		self.assertEqual(len(self._game.player[0].hand), 5) 
		self.assertEqual(self._game.player[0].restactions, 0) 
		self.assertEqual(self._game.player[0].coins, 2) #金量は2
		self.assertEqual(self._game.player[0].restbuys, 2)#残り購入権は2 
		self.assertFalse(isinstance(self._game.player[0].phase, main.ActionPhase))
	
	def test_play_market(self):
		self._game.player[0].hand.append(card.Market()) 
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right")
		self.assertEqual(len(self._game.player[0].playarea),1)
		self.assertEqual(len(self._game.player[0].hand), 6) #手札の残り枚数は5+1枚
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
		self.assertEqual(self._game.player[0].coins, 1) #金量は1
		self.assertEqual(self._game.player[0].restbuys, 2)#残り購入権は2
		self.assertTrue(isinstance(self._game.player[0].phase, main.ActionPhase))
		
	def test_play_laboratory(self):
		self._game.player[0].hand.append(card.Laboratory()) 
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right")
		self.assertEqual(len(self._game.player[0].playarea),1)
		self.assertEqual(len(self._game.player[0].hand), 7) #手札の残り枚数は5+2枚
		self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
		self.assertEqual(self._game.player[0].coins, 0) 
		self.assertEqual(self._game.player[0].restbuys, 1)
		self.assertTrue(isinstance(self._game.player[0].phase, main.ActionPhase))
	
	def test_play_festival(self):
		self._game.player[0].hand.append(card.Festival()) 
		self._game.beginturn(0)
		self._game.player[0].playcard(5, "right")
		self.assertEqual(len(self._game.player[0].playarea),1)
		self.assertEqual(len(self._game.player[0].hand), 5)
		self.assertEqual(self._game.player[0].restactions, 2) #残りアクション権は2
		self.assertEqual(self._game.player[0].coins, 2) 
		self.assertEqual(self._game.player[0].restbuys, 2)
		self.assertTrue(isinstance(self._game.player[0].phase, main.ActionPhase))
	

	#def test_play_copper(self): #銅貨をプレイしようとする
		#self._game.player[0].hand.append(card.Copper()) #銅貨を追加
		#self._game.player[0].playcard(5, "right") #銅貨をプレイしようとする
		#self.assertEqual(len(self._game.player[0].playarea),0) #場の枚数は0枚
		#self.assertEqual(len(self._game.player[0].hand), 6) #手札の残り枚数は6枚
		#self.assertEqual(self._game.player[0].coins, 0) #残りは0金
		#self.assertEqual(self._game.player[0].restactions, 1) #残りアクション権は1
	
	