import random

numofcopper = 60
numofsilver = 40
numofgold = 30
numofvict2 = 8
numofvict34 = 12
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
		copper = [Copper() for i in range(copperrest)]
		self.field.treasurepile[0].pile.extend(copper)#銅貨の山を作る
		silver = [Silver() for i in range(numofsilver)]
		self.field.treasurepile[1].pile.extend(silver)#銀貨の山を作る
		gold = [Gold() for i in range(numofgold)]
		self.field.treasurepile[2].pile.extend(gold)#金貨の山を作る
	
		if self.number == 2: #人数によって勝利点カードの枚数を制御
			numofvict = numofvict2
		elif self.number == 3 or self.number == 4:
			numofvict = numofvict34
			
		estate = [Estate() for i in range(numofvict)]
		self.field.victorypile[0].pile.extend(estate)#屋敷の山を作る
		duchy = [Duchy() for i in range(numofvict)]
		self.field.victorypile[1].pile.extend(duchy)#公領の山を作る
		province = [Province() for i in range(numofvict)]
		self.field.victorypile[2].pile.extend(province)#属州の山を作る

class Pile(): #サプライのカードの山
	def __init__(self):
		self.pile = [] #カードの山
		#self.kind = kind #置かれるカードの種類
	
class Field():
	zeropile = 0 #0枚になったサプライの個数
	def __init__(self):
		self.trash = Pile() #廃棄置き場(単独)
		self.cursepile = Pile() #呪い置き場(単独)
		self.treasurepile = [Pile() for i in range(kindoftreasure)] #財宝置き場
		self.victorypile = [Pile() for i in range(kindofvictoryc)] #勝利点カード置き場
		self.actionpile = [Pile() for i in range(kindofaction)] #王国カード置き場

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
			self.shuffle
		drawcard = self.deck[:number]
		self.deck = self.deck[number:]
		self.hand.extend(drawcard)
	
	def playcard(self, number): #カードは手札からプレイされる　手札の何枚目かをnumberとして与える
		playedcard = self.hand.pop(number)
		self.playarea.append(playedcard)#手札からカードを取り出して自分の場に出す
		playedcard.played(self)
		
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
		
	def played(self, user): #カードがプレイされた時の挙動
		pass

class TreasureCard(Card): #財宝カード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.coins = value
		
	def played(self, user): #財宝カードがプレイされると使用者の残り金数が増える
		user.coins += self.coins

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
		
		

