import random

numofcopper = 60
numofsilver = 40
numofgold = 30

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
		copper = [Copper() for i in range(copperrest)]
		self.field.treasurepile.append(copper)#銅貨の山を作る
		silver = [Silver() for i in range(numofsilver)]
		self.field.treasurepile.append(silver)#銀貨の山を作る
		gold = [Gold() for i in range(numofgold)]
		self.field.treasurepile.append(gold)#金貨の山を作る
	
	
class Field():
	def __init__(self):
		self.trash = [] #廃棄置き場
		self.cursepile = [] #呪い置き場
		self.treasurepile = [] #財宝置き場
		self.victorypile = [] #勝利点カード置き場
		self.actionpile = [] #アクションカード置き場

class Player():
	def __init__(self):
		self.deck = [] #デッキ
		self.hand = [] #手札
		self.dispile = [] #捨て札の山
		self.playarea = [] #各プレイヤーの場
	
	def draw(self, number): #デッキからカードをnumber枚引く
		if (number > len(self.deck)) and len(self.deck) > 0: #デッキの枚数が足りず、かつ捨て札があるとき
			number = number - len(self.deck)
			self.hand.extend(self.deck)
			self.deck.clear()
			self.deck = self.deck + self.dispile
			self.dispile.clear()
			self.shuffle
		drawcard = self.deck[:number]
		self.deck = self.deck[number:]
		self.hand.extend(drawcard)
	
	def shuffle(self): #デッキをシャッフルする
		random.shuffle(self.deck)

class Card(): #カード
	def __init__(self, ename, jname, cost, clas, type, set):
		self.ename = ename #カードの名称(英語)
		self.jname = jname #カードの名称(日本語)
		self.cost = cost #コスト
		self.clas = clas #カードの分類(基本カードとか王国カードとか)
		self.type = type #カードの種類
		self.set = set #拡張セット

class TreasureCard(Card): #財宝カード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.coins = value

class VictoryCard(Card): #勝利点カード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.vicpts = value
		
class CurseCard(Card): #呪いカード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.vicpts = value

class ActionCard(Card): #アクションカード
	def __init__(self, ename, jname, cost, clas, type, set):
		super().__init__(ename, jname, cost, clas, type, set)
		self.vicpts = value
		
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
		super().__init__("Estate", "屋敷", 2, "基本", "勝利点", "基本", 2)


