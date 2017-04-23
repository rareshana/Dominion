import card


numofcopper = 60
numofsilver = 40
numofgold = 30
numofvict2 = 8
numofvict34 = 12
numofact = 10
numofcurse = 10  #参加者一人当たりの呪いの枚数
kindoftreasure = 3  #財宝カードの種類
kindofvictoryc = 3  #基本勝利点カードの種類
kindofaction = 10  #王国カードの種類


class Game():
	def __init__(self, number):
		self.number = number  #参加人数
		self.player = []  #参加プレイヤーはplay.pyで設定する
		self.field = Field()  #場を生成
		self.turnplayer = 0
		self.turncount = 1
		
	def starter(self, supply):
		for i in range(self.number):#各プレイヤーのデッキに銅貨を7枚、屋敷を3枚ずつ配る
		#その後、各々のデッキをシャッフルし、デッキから5枚引いて手札にする
			copper = [card.Copper() for i in range(7)]
			estate = [card.Estate() for i in range(3)]
			self.player[i].cards.deck.extend(copper)
			self.player[i].cards.deck.extend(estate)
			self.player[i].shuffle()
			self.player[i].draw(5)
			
		copperrest = numofcopper - self.number * 7
		self.makesupply(copperrest, 2, card.Copper())  #銅貨の山を作る
		self.makesupply(numofsilver, 3, card.Silver())  #銀貨の山を作る
		self.makesupply(numofgold, 4, card.Gold())  #金貨の山を作る
		
		numofvict = self.howmany_victorycards(self.number)#人数によって勝利点カードの枚数を制御
		
		self.makesupply(numofvict, 5, card.Estate())  #屋敷の山を作る
		self.makesupply(numofvict, 6, card.Duchy())  #公領の山を作る
		self.makesupply(numofvict, 7, card.Province())  #属州の山を作る
		
		self.makesupply((self.number-1)*numofcurse, 1, card.Curse())   #呪いの山を作る
		
		[self.makesupply(numofact, i, j()) for i, j in zip(range(8, 18), supply)]  
		
		print([self.field.supnumber.get(i).name for i in range(1,18)])
	
	def howmany_victorycards(self, number):
		if number == 2:
			return numofvict2
		if number== 3 or number == 4:
			return numofvict34
			
	def makesupply(self, number, placenum, cardclass):  #山札を作る(引数は、枚数、場所、カードを生成するコマンド)
		cards = [cardclass for i in range(number)]
		self.field.supnumber.get(placenum).pile.extend(cards)
		self.field.supnumber.get(placenum).name = self.field.supnumber.get(placenum).pile[0].ename
		self.field.supnumber.get(placenum).cost = self.field.supnumber.get(placenum).pile[0].cost
	
	def beginturn(self, playernum):  #numに対応するプレイヤーのターンを開始する
		print("")
		print(self.turncount)
		print("ターン開始")
		turn = iter(Turn(self.player[playernum], self.field))
		self.player[playernum].beginturn(turn)
		self.player[playernum].nextphase() #Start
		self.player[playernum].nextphase() #Action
		self.player[playernum].gameinfo.phase.start()  #Action
		self.player[playernum].gameinfo.phase.start()  #Treasure
		self.player[playernum].gameinfo.phase.start()  #Buy
		
	def changeturn(self):
		self.turnplayer = (self.turnplayer + 1) % self.number
		
	def begingame(self):
		gameflag = 1
		while gameflag: 
			self.beginturn(self.turnplayer)
			gameflag = self.is_game_set_or_continue()
		self.endgame()
		
	def is_game_set_or_continue(self):
		if self.field.is_game_set():
			return 0
		self.changeturn()
		self.turncount += 1
		return 1
	
		
	def endgame(self):
	#勝利点が同じであるときは、よりターン数が少なかったプレイヤーの勝ち。
		print("ゲーム終了です")
		VP = [self.player[i].victorycount() for i in range(self.number)]
		print(VP)
		
	def get_cardinfo(self, number):
		return self.field.get_cardinfo(number)

		

		
class Field():
	zeropile = 0  #0枚になったサプライの個数
	def __init__(self):
		self.trash = [] #廃棄置き場(単独)
		self.cursepile = Pile()  #呪い置き場(単独)
		self.treasurepile = [Pile() for i in range(kindoftreasure)]  #財宝置き場
		self.victorypile = [Pile() for i in range(kindofvictoryc)]  #勝利点カード置き場
		self.actionpile = [Pile() for i in range(kindofaction)]  #王国カード置き場
		
		self.supnumber = {1:self.cursepile}
		suptrenum = {(i+2):self.treasurepile[i] for i in range(3)}
		supvicnum = {(i+5):self.victorypile[i] for i in range(3)}
		supactnum = {(i+8):self.actionpile[i] for i in range(10)}
		self.supnumber.update(suptrenum)
		self.supnumber.update(supvicnum)
		self.supnumber.update(supactnum)  #サプライの場に番号を対応付けた
	
	def is_game_set(self):
		if self.zeropile >= 3 or len(self.supnumber.get(7).pile) == 0:
			return True
		return False
	
	def get_cardinfo(self, number):
		return self.supnumber.get(number).pile[0]
		
		
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
		self.player.available.rest_actions = 1
		self.player.available.rest_buys = 1
		self.player.available.coins = 0
		
		
class ActionPhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		print("アクションフェイズです")
	
	def start(self):
		while (isinstance(self.player.gameinfo.phase, ActionPhase)):
			self.what_do()
	
	def what_do(self):
		if not self.player.handcheck('action'):
			self.player.phaseend()
			return
			
		if self.player.isAI == 1 or self.player.isHuman == 1:  #AIまたは人間用
			print([i.jname for i in self.player.cards.hand])
			print("どのアクションカードを使用しますか")
			self.player.what_action()
		#分けられそう		
		
	def playable(self, card):
		return hasattr(card, 'isaction')
		
	def rightplayed(self, when):
		if when == 'right':
			self.player.available.rest_actions -= 1  #カードがプレイされたらアクション権を1減らす
			
class TreasurePhase(Phase):
	def __init__(self, player):
		super().__init__(player)
		print("財宝フェイズです")
		print([i.jname for i in self.player.cards.hand])
		
	def start(self):
		if self.player.isAI == 1:  #AI用
			self.player.play_coins()
			print(self.player.available.coins)
			self.player.phaseend()
			return
			
		if self.player.isHuman == 1:
			isbreak = 0
			self.treasure_playable_time(isbreak)
			print(self.player.available.coins)
			self.player.phaseend()
			return
		
		if self.player.isAI == 0:  #プレイヤ用
			pass
	#Strategyパターン？
	
	def treasure_playable_time(self, flag):
		while flag != -1:
			print([i.jname for i in self.player.cards.hand])
			print("使用する財宝カードの番号を入力してください")
			flag = self.player.what_coin_play()
			
	def playable(self, card):
		return hasattr(card, 'istreasure')
		
class BuyPhase(Phase):
	def __init__(self, player, field):
		super().__init__(player)
		print("購入フェイズです")
		self.field = field
		
	def start(self):
		while (isinstance(self.player.gameinfo.phase, BuyPhase)):
			self.is_ai_or_human()
				
	def is_ai_or_human(self):
		if self.player.isAI == 1:  #AI用
			self.is_continue_ai()
			return
			
		if self.player.isHuman == 1:
			self.is_continue_human()
			return
			
	def is_continue_ai(self):
		if self.player.available.rest_buys > 0:
			self.player.what_buy()
			return
		self.player.phaseend()
	
	def is_continue_human(self):
		if self.player.available.rest_buys > 0:
			print("購入するカードの番号を入力してください")
			self.player.what_buy()
			return
		self.player.phaseend()
					
class CleanUpPhase(Phase):
	def __init__(self, player, field):
		super().__init__(player)
		print("クリーンアップフェイズです")
		self.cleanup()
		
	def cleanup(self):
		self.player.cards.dispile.extend(self.player.cards.playarea)
		self.player.cards.playarea.clear()
		self.player.cards.dispile.extend(self.player.cards.hand)
		self.player.cards.hand.clear()
		self.player.draw(5)
		
class Pile():  #サプライのカードの山
	def __init__(self):
		self.pile = []  #カードの山 下から上へ
		self.name = ""  #山札に置かれているカードの名前
		self.cost = -1  #山札に置かれているカードのコスト
		
	def zerocheck(self, field):  #山をチェックし、それが残り0枚ならzeropileをインクリメントする
		if len(self.pile) == 0:
			field.zeropile += 1