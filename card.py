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

