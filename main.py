import random
import card
import player

numofcopper = 60
numofsilver = 40
numofgold = 30
numofvict2 = 8
numofvict34 = 12
numofcurse = 10 #参加者一人当たりの呪いの枚数
kindoftreasure = 3 #財宝カードの種類
kindofvictoryc = 3 #基本勝利点カードの種類
kindofaction = 10 #王国カードの種類


class Game():
	def __init__(self, number):
		self.number = number #参加人数
		self.player = [] #参加プレイヤーはplay.pyで設定する
		self.field = Field()#場を生成
		self.turnplayer = 0
		self.turncount = 1
	
	def starter(self):
		for i in range(self.number): #各プレイヤーのデッキに銅貨を7枚、屋敷を3枚ずつ配る　その後、各々のデッキをシャッフルし、デッキから5枚引いて手札にする
			copper = [card.Copper() for i in range(7)]
			estate = [card.Estate() for i in range(3)]
			self.player[i].deck.extend(copper)
			self.player[i].deck.extend(estate)
			self.player[i].shuffle()
			self.player[i].draw(5)
			
		copperrest = numofcopper - self.number * 7
		self.makesupply(copperrest, 2, card.Copper())#銅貨の山を作る
		self.makesupply(numofsilver, 3, card.Silver())#銀貨の山を作る
		self.makesupply(numofgold, 4, card.Gold())#金貨の山を作る
	
		if self.number == 2: #人数によって勝利点カードの枚数を制御
			numofvict = numofvict2
		elif self.number == 3 or self.number == 4:
			numofvict = numofvict34
		
		self.makesupply(numofvict, 5, card.Estate())#屋敷の山を作る
		self.makesupply(numofvict, 6, card.Duchy())#公領の山を作る
		self.makesupply(numofvict, 7, card.Province())#属州の山を作る
		
		self.makesupply((self.number-1)*numofcurse, 1, card.Curse()) #呪いの山を作る
		
		
	def makesupply(self, number, placenum, cardclass): #山札を作る(引数は、枚数、場所、カードを生成するコマンド)
		cards = [cardclass for i in range(number)]
		self.field.supnumber.get(placenum).pile.extend(cards)
		self.field.supnumber.get(placenum).name = self.field.supnumber.get(placenum).pile[0].ename
	
	def beginturn(self, playernum): #numに対応するプレイヤーのターンを開始する
		print("ターン開始")
		print(self.turncount)
		turn = iter(Turn(self.player[playernum], self.field))
		self.player[playernum].turn = turn
		self.player[playernum].phase = next(self.player[playernum].turn) #Start
		
		self.player[playernum].phase = next(self.player[playernum].turn) #Action
		self.player[playernum].phase.start()#Action
		self.player[playernum].phase.start()#Treasure
		self.player[playernum].phase.start()#Buy
		
	def changeturn(self):
		self.turnplayer = (self.turnplayer + 1) % self.number
		
	def begingame(self):
		while True: 
			self.beginturn(self.turnplayer)
			if self.field.is_game_set():
				break
			self.changeturn()
			self.turncount += 1
		self.endgame()
		
	def endgame(self):#勝利点が同じであるときは、よりターン数が少なかったプレイヤーの勝ち。
		print("ゲーム終了です")
		VP = [self.player[i].victorycount() for i in range(self.number)]
		print(VP)

		

		
class Field():
	zeropile = 0 #0枚になったサプライの個数
	def __init__(self):
		self.trash = Pile() #廃棄置き場(単独)
		self.cursepile = Pile() #呪い置き場(単独)
		self.treasurepile = [Pile() for i in range(kindoftreasure)] #財宝置き場
		self.victorypile = [Pile() for i in range(kindofvictoryc)] #勝利点カード置き場
		self.actionpile = [Pile() for i in range(kindofaction)] #王国カード置き場
		
		self.supnumber = {0:self.trash, 1:self.cursepile}
		suptrenum = {(i+2):self.treasurepile[i] for i in range(3)}
		supvicnum = {(i+5):self.victorypile[i] for i in range(3)}
		supactnum = {(i+8):self.actionpile[i] for i in range(10)}
		self.supnumber.update(suptrenum)
		self.supnumber.update(supvicnum)
		self.supnumber.update(supactnum) #サプライの場に番号を対応付けた
	
	def is_game_set(self):
		if self.zeropile >= 3 or len(self.supnumber.get(7).pile) == 0:
			return True
		else:
			return False

		
		
class Turn():
	def __init__(self, player, field):
		self.player = player
		self.field = field
		
	def __iter__(self):
		yield StartPhase(self.player)
		yield ActionPhase(self.player)
		yield TreasurePhase(self.player)
		yield BuyPhase(self.player, self.field)
		yield CleanUpPhase(self.player, self.field)
		
		
		
class Phase():
	def __init__(self, player):
		self.player = player
		
	def playable(self, card):
		return False
		
	def start(self):
		pass
		
	def rightplayed(self, when):
		pass
		

class StartPhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		self.player.restactions = 1
		self.player.restbuys = 1
		self.player.coins = 0
		
class ActionPhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		print("アクションフェイズです")
	
	def start(self):
		if not self.player.handcheck('action'):
			self.player.phaseend()
		elif self.player.isAI == 1: #AI用
			self.player.phaseend() 
	
	def playable(self, card):
		return hasattr(card, 'isaction')
		
	def rightplayed(self, when):
		if when == 'right':
			self.player.restactions -= 1 #カードがプレイされたらアクション権を1減らす
	
class TreasurePhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		print("財宝フェイズです")
		prints = [print(i.jname) for i in self.player.hand]
	
	def start(self):
		if self.player.isAI == 1: #AI用
			self.player.play_coins()
			print(self.player.coins)
			self.player.phaseend()
		elif self.player.isAI == 0: #プレイヤ用
			pass
			
	def playable(self, card):
		return hasattr(card, 'istreasure')
	
class BuyPhase(Phase):
	def __init__(self, player, field):
		super().__init__(player)
		print("購入フェイズです")
		self.field = field
	
	def start(self):
		if self.player.isAI == 1: #AI用
			self.player.what_buy(self.field)
			self.player.phaseend()
	
class CleanUpPhase(Phase):
	def __init__(self, player, field):
		super().__init__(player)
		print("クリーンアップフェイズです")
		self.cleanup()
		
	def cleanup(self):
		self.player.dispile.extend(self.player.playarea)
		self.player.playarea.clear()
		self.player.dispile.extend(self.player.hand)
		self.player.hand.clear()
		self.player.draw(5)
		
class Pile(): #サプライのカードの山
	def __init__(self):
		self.pile = [] #カードの山 下から上へ
		self.name = "" #山札に置かれているカードの名前
		
	def zerocheck(self, field): #山をチェックし、それが残り0枚ならzeropileをインクリメントする
		if len(self.pile) == 0:
			field.zeropile += 1
	
