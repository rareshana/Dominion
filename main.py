import random

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
		self.player = [Player() for i in range(number)] #参加人数分のPlayerオブジェクトを生成
		self.field = Field()#場を生成
		self.starter()
	
	def starter(self):
		for i in range(self.number): #各プレイヤーのデッキに銅貨を7枚、屋敷を3枚ずつ配る
			copper = [Copper() for i in range(7)]
			estate = [Estate() for i in range(3)]
			self.player[i].deck.extend(copper)
			self.player[i].deck.extend(estate)
		
		copperrest = numofcopper - self.number * 7
		self.makesupply(copperrest, 2, Copper())#銅貨の山を作る
		self.makesupply(numofsilver, 3, Silver())#銀貨の山を作る
		self.makesupply(numofgold, 4, Gold())#金貨の山を作る
	
		if self.number == 2: #人数によって勝利点カードの枚数を制御
			numofvict = numofvict2
		elif self.number == 3 or self.number == 4:
			numofvict = numofvict34
		
		self.makesupply(numofvict, 5, Estate())#屋敷の山を作る
		self.makesupply(numofvict, 6, Duchy())#公領の山を作る
		self.makesupply(numofvict, 7, Province())#属州の山を作る
		
		self.makesupply((self.number-1)*numofcurse, 1, Curse()) #呪いの山を作る
		
	def makesupply(self, number, placenum, cardclass):
		cards = [cardclass for i in range(number)]
		self.field.supnumber.get(placenum).pile.extend(cards)
		self.field.supnumber.get(placenum).name = self.field.supnumber.get(placenum).pile[0].ename


class Pile(): #サプライのカードの山
	def __init__(self):
		self.pile = [] #カードの山
		self.name = "" #山札に置かれているカードの名前
	
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
		
		
class Player():
	def __init__(self):
		self.deck = [] #デッキ
		self.hand = [] #手札
		self.dispile = [] #捨て札の山
		self.playarea = [] #各プレイヤーの場
		self.coins = 0 #自分のターンに使える残り金数
		self.restactions = 1 #自分のターンに使えるアクションの残り回数
		self.restbuys = 1 #自分のターンで使用できる残り購入権
	
	def draw(self, number): #デッキからカードをnumber枚引く
		if (number > len(self.deck)) and len(self.deck) > 0: #デッキの枚数が足りず、かつ捨て札があるとき
			number = number - len(self.deck)
			self.hand.extend(self.deck)
			self.deck.clear()
			self.deck = self.deck + self.dispile
			self.dispile.clear()
			self.shuffle()
		drawcard = self.deck[:number]
		self.deck = self.deck[number:]
		self.hand.extend(drawcard)
	
	def playcard(self, number): #カードは手札からプレイされる　手札の何枚目かをnumberとして与える
		playedcard = self.hand.pop(number)
		self.playarea.append(playedcard)#手札からカードを取り出して自分の場に出す
		playedcard.played(self)
		
	def shuffle(self): #デッキをシャッフルする
		random.shuffle(self.deck)
	
	def gaincard(self): #カードを獲得するときの挙動#これから書く
		pass
	

class Card(): #カード
	def __init__(self, ename, jname, cost, clas, type, set):
		self.ename = ename #カードの名称(英語)
		self.jname = jname #カードの名称(日本語)
		self.cost = cost #コスト
		self.clas = clas #カードの分類(基本カードとか王国カードとか)
		self.type = type #カードの種類
		self.set = set #拡張セット
		
	def played(self, user): #カードがプレイされた時の挙動
		pass
	
	def gained(self, user): #カードが獲得された時の挙動
		pass

class TreasureCard(Card): #財宝カード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.coins = value
		self.istreasure = 1 #財宝カードなら1
		
	def played(self, user): #財宝カードがプレイされると使用者の残り金数が増える
		user.coins += self.coins

class VictoryCard(Card): #勝利点カード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.vicpts = value
		self.isvictory = 1 #勝利点カードなら1
		
class CurseCard(Card): #呪いカード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.vicpts = value
		self.iscurse = 1 #呪いカードなら1
		
class ActionCard(Card): #アクションカード
	def __init__(self, ename, jname, cost, clas, type, set):
		super().__init__(ename, jname, cost, clas, type, set)
		self.isaction = 1 #アクションカードなら1
		
class Copper(TreasureCard): #銅貨
	def __init__(self):
		super().__init__("Copper", "銅貨", 0, "基本", "財宝", "基本", 1)

class Silver(TreasureCard): #銀貨
	def __init__(self):
		super().__init__("Silver", "銀貨", 3, "基本", "財宝", "基本", 2)

class Gold(TreasureCard): #金貨
	def __init__(self):
		super().__init__("Gold", "金貨", 6, "基本", "財宝", "基本", 3)
		
class Estate(VictoryCard): #屋敷
	def __init__(self):
		super().__init__("Estate", "屋敷", 2, "基本", "勝利点", "基本", 1)
		
class Duchy(VictoryCard): #公領
	def __init__(self):
		super().__init__("Duchy", "公領", 5, "基本", "勝利点", "基本", 3)

class Province(VictoryCard): #属州
	def __init__(self):
		super().__init__("Province", "属州", 8, "基本", "勝利点", "基本", 6)
		
class Curse(CurseCard): #呪い
	def __init__(self):
		super().__init__("Curse", "呪い", 0, "基本", "呪い", "基本", -1)

