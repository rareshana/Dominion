class CardType():
	cardtype = {'action':'isaction', 'treasure':'istreasure', 'victory':'isvictory', 'curse':'iscurse'}
	
	@classmethod
	def get_cardtype(cls, type):
		return cls.cardtype.get(type)
		
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
	
	def trashed(self, user):  #カードが廃棄された時の挙動
		pass
		
	def is_type(self, type):
		typec = CardType.get_cardtype(type)
		return (hasattr(self, typec))
		
	def is_action(self):
		return self.is_type('action')
	
	def is_treasure(self):
		return self.is_type('treasure')
	
	def is_victory(self):
		return self.is_type('victory')
	
	def is_curse(self):
		return self.is_type('curse')
	
	def is_victory_or_curse(self):
		return self.is_victory() or self.is_curse()
		
class TreasureCard(Card): #財宝カード
	def __init__(self, ename, jname, cost, clas, type, set, value):
		super().__init__(ename, jname, cost, clas, type, set)
		self.coins = value
		self.istreasure = 1 #財宝カードなら1
		
	def played(self, user): #財宝カードがプレイされると使用者の残り金数が増える
		user.pluscoins(self.coins)

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
		
class Smithy(ActionCard): #鍛冶屋
	def __init__(self):
		super().__init__("Smithy", "鍛冶屋", 4, "王国", "アクション", "基本")
	
	def played(self, user):
		user.draw(3)
	
class Village(ActionCard): #村
	def __init__(self):
		super().__init__("Village", "村", 3, "王国", "アクション", "基本")
	
	def played(self, user):
		user.draw(1)
		user.plusactions(2)

class Woodcutter(ActionCard): #木こり
	def __init__(self):
		super().__init__("WoodCutter", "木こり", 3, "王国", "アクション", "基本")
		
	def played(self, user):
		user.plusbuys(1)
		user.pluscoins(2)

class Market(ActionCard): #市場
	def __init__(self):
		super().__init__("Market", "市場", 5, "王国", "アクション", "基本")
		
	def played(self, user):
		user.draw(1)
		user.plusactions(1)
		user.plusbuys(1)
		user.pluscoins(1)

class Laboratory(ActionCard): #研究所
	def __init__(self):
		super().__init__("Laboratory", "研究所", 5, "王国", "アクション", "基本")
		
	def played(self, user):
		user.draw(2)
		user.plusactions(1)

class Festival(ActionCard): #祝祭
	def __init__(self):
		super().__init__("Festival", "祝祭", 5, "王国", "アクション", "基本")
		
	def played(self, user):
		user.plusactions(2)
		user.plusbuys(1)
		user.pluscoins(2)
		
class CouncilRoom(ActionCard): #議事堂
	def __init__(self):
		super().__init__("Council Room", "議事堂", 5, "王国", "アクション", "基本")
	
	def played(self, user):
		user.draw(4)
		user.plusbuys(1)
		[x.draw(1) for x in user.other_players]

class Chancellor(ActionCard): #宰相
	def __init__(self):
		super().__init__("Chancellor", "宰相", 3, "王国", "アクション", "基本")
	
	def played(self, user):
		user.pluscoins(2)
		answer = user.chancellor_effect()
		if answer == 'y':
			user.dispile.extend(user.deck[::-1])
			user.deck.clear()
			return
		if answer == 'n':
			pass
			return

class Feast(ActionCard): #祝宴
	def __init__(self):
		super().__init__("Feast", "祝宴", 4, "王国", "アクション", "基本")
	
	def played(self, user):
		user.trashcard(self, user.cards.playarea)
		user.what_gain_undercost(5)


class Workshop(ActionCard): #工房
	def __init__(self):
		super().__init__("Workshop", "工房", 3, "王国", "アクション", "基本")
	
	def played(self, user):
		user.what_gain_undercost(4)


class Adventurer(ActionCard): #冒険者
	def __init__(self):
		super().__init__("Adventurer", "冒険者", 6, "王国", "アクション", "基本")
	
	def played(self, user):
		tmp_treasure = []
		tmp_not_treasure = []
		
		while len(tmp_treasure) < 2:
			if user.is_deck_empty() and user.is_dispile_empty():
				break
				
			tmp = user.reveal_from_deck()
			if tmp.is_treasure():
				tmp_treasure.append(tmp)
			else:
				tmp_not_treasure.append(tmp)
		
		print(tmp_treasure)
		print(tmp_not_treasure)
		user.add_hand(tmp_treasure)
		user.add_dispile(tmp_not_treasure)
		
			
class Cellar(ActionCard): #地下貯蔵庫
	def __init__(self):
		super().__init__("Cellar", "地下貯蔵庫", 2, "王国", "アクション", "基本")
	
	def played(self, user):
		user.plusactions(1)
		choices = []
		while True:
			print("捨て札にするカードを選んでください")
			discarded = user.pop_from_hand()
			if discarded == -1:
				break
			choices.append(discarded)
		number = len(choices)
		print(number)
		user.put_on_dispile(choices)
		user.draw(number)
		
class Chapel(ActionCard): #礼拝堂
	def __init__(self):
		super().__init__("Chapel", "礼拝堂", 2, "王国", "アクション", "基本")
	
	def played(self, user):
		choices = []
		for i in range(4):
			print("廃棄するカードを選んでください")
			trashed = user.pop_from_hand()
			if trashed == -1:
				break
			choices.append(trashed)
		user.trashcard(choices)