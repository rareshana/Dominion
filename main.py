import random
import card

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
	def __init__(self, number, AInum=0):
		self.number = number #参加人数
		self.player = [Player() for i in range(number-AInum)] #参加人数分のPlayerオブジェクトを生成
		player2 = [AIPlayer() for i in range(AInum)]
		self.player.extend(player2)
		self.field = Field()#場を生成
		self.turnplayer = 0
		self.turncount = 1
		self.starter()
	
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
		while True: #最終的にはWhile Trueにするよ
			self.beginturn(self.turnplayer)
			if self.field.is_game_set():
				break
			self.changeturn()
			self.turncount += 1
		self.endgame()
		
	def endgame(self):
		print("ゲーム終了です")
		VP = [self.player[i].victorycount() for i in range(self.number)]
		print(VP)
		
		
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

class StartPhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		self.player.restactions = 1
		self.player.restbuys = 1
		self.player.coins = 0
		

class ActionPhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		print("test 今はアクションフェイズです")
	
	def start(self): 
		if self.player.isAI == 1: #AI用
			self.player.phaseend() 
	
	def playable(self, card):
		return hasattr(card, 'isaction')
	
class TreasurePhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		print("test 今は財宝フェイズです")
		prints = [print(i.jname) for i in self.player.hand]
	
	def start(self):
		if self.player.isAI == 1: #AI用
			self.player.play_coins()
			print(self.player.coins)
		self.player.phaseend()
	
	def playable(self, card):
		return hasattr(card, 'istreasure')
	
class BuyPhase(Phase):
	def __init__(self, player, field):
		super().__init__(player)
		print("test 今は購入フェイズです")
		self.field = field
	
	def start(self):
		if self.player.isAI == 1: #AI用
			self.player.what_buy(self.field)
		self.player.phaseend()
	
class CleanUpPhase(Phase):
	def __init__(self, player, field):
		super().__init__(player)
		print("test 今はクリーンアップフェイズです")
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
	
		
class Player():
	def __init__(self):
		self.deck = [] #デッキ 下から上へ
		self.hand = [] #手札 左から右へ
		self.dispile = [] #捨て札の山 下から上へ
		self.playarea = [] #各プレイヤーの場 左から右へ
		self.coins = 0 #自分のターンに使える残り金数
		self.restactions = 1 #自分のターンに使えるアクションの残り回数
		self.restbuys = 1 #自分のターンで使用できる残り購入権
		self.turn = 0 #各ターンを格納する
		self.phase = Phase(self) #現在のフェーズを格納する
		self.isAI = 0
	
	def draw(self, number): #デッキからカードをnumber枚引く
		if (number > len(self.deck)) and len(self.deck) >= 0: #デッキの枚数が足りず、かつ捨て札があるとき
			number -= len(self.deck)
			self.hand.extend(self.deck[::-1])
			self.deck.clear()
			self.deck.extend(self.dispile)
			self.dispile.clear()
			self.shuffle()
		drawcard = self.deck[-number:]
		self.deck = self.deck[:-number]
		self.hand.extend(drawcard[::-1])
	
	def playcard(self, number, when = None): #カードは手札からプレイされる　手札の何枚目かをnumberとして与える 正規のタイミングでカードをプレイするとき、whenに'right'を与えることにする
		if (when is None) or (self.phase.playable(self.hand[number])):
			playedcard = self.hand.pop(number)
			self.playarea.append(playedcard)#手札からカードを取り出して自分の場に出す
			playedcard.played(self)
			return True
		else:
			return False
		
	def shuffle(self): #デッキをシャッフルする
		random.shuffle(self.deck)
	
	def gaincard(self, number, field): #カードは原則サプライから獲得される　山札の番号をnumberとして与える。それだけだと情報が足りないので、fieldの情報も与えなければ……
		place = field.supnumber.get(number)
		if place.pile: #山札が切れていない場合のみ獲得できる
			gainedcard = place.pile.pop()
			self.dispile.append(gainedcard)
			gainedcard.gained(self)
			place.zerocheck(field)
	
	def buycard(self, number, field):#カードは原則サプライから購入される　山札の番号をnumberとして与える。fieldの情報も与える。
		boughtcard = field.supnumber.get(number).pile[0] #購入したいカードを変数に取得
		if self.coins > boughtcard.cost and self.restbuys > 0:
			self.coins -= boughtcard.cost #そのカードのコストを購入者の残り金から減算
			self.restbuys -= 1 #購入権を1減らす
			self.gaincard(number, field)
			
	def phaseend(self): #現在のフェーズを終了し、次のフェーズへ移行する
		self.phase = next(self.turn)
		
	def victorycount(self): #ゲーム終了後の勝利点計算
		vp = 0
		self.deck.extend(self.dispile)
		self.deck.extend(self.hand)
		self.deck.extend(self.playarea)
		for i in range(len(self.deck)):
			if hasattr(self.deck[i], 'isvictory') or hasattr(self.deck[i], 'iscurse'):
				vp += self.deck[i].vicpts
		
		return vp
	
		
		
class AIPlayer(Player):
	def __init__(self):
		super().__init__()
		self.isAI = 1
		
	def play_coins(self):
		i = 0
		while i < len(self.hand):
			if self.playcard(i, 'right'):
				i -= 1
			if i+1 >= len(self.hand):
				break
			i += 1
			
	def what_buy(self, field):
		if self.coins < 3:
			pass
		elif self.coins < 6:
			self.buycard(3, field)
		elif self.coins < 8:
			self.buycard(4, field)
		else:
			self.buycard(7, field)
		

