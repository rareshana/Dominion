import random

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
		self.phase = 0 #現在のフェーズを格納する
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
		if self.coins >= boughtcard.cost and self.restbuys > 0:
			self.coins -= boughtcard.cost #そのカードのコストを購入者の残り金から減算
			self.restbuys -= 1 #購入権を1減らす
			self.gaincard(number, field)
			print(boughtcard.jname)
			
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
		

