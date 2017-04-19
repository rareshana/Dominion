import random
import card
import main

class Player():
	def __init__(self, game):
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
		self.isHuman = 0
		self.others = []
		self.game = game
	
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
	
	def playcard(self, number, when = None): #カードは手札からプレイされる　手札の何枚目かをnumberとして与える 正規のタイミング(財宝フェイズに出す財宝、アクションフェイズにアクション権を消費して出すアクションカード)でカードをプレイするとき、whenに'right'を与えることにする
		if (when is None) or (self.phase.playable(self.hand[number])):
			playedcard = self.hand.pop(number)
			self.playarea.append(playedcard)#手札からカードを取り出して自分の場に出す
			self.phase.rightplayed(when)
			playedcard.played(self)
			self.is_phaseend(when)  #処理終了後、アクションフェイズで残りアクション権が0ならばフェイズを自動的に終了する	
			return True
		else:
			return False
	
	def is_phaseend(self, when):
		if isinstance(self.phase, main.ActionPhase) and when is 'right' and self.restactions == 0: 
			self.phaseend()
		
	def shuffle(self): #デッキをシャッフルする
		random.shuffle(self.deck)
	
	def gaincard(self, number): #カードは原則サプライから獲得される　山札の番号をnumberとして与える。それだけだと情報が足りないので、fieldの情報も与えなければ……
		place = self.game.field.supnumber.get(number)
		if place.pile: #山札が切れていない場合のみ獲得できる
			gainedcard = place.pile.pop()
			self.dispile.append(gainedcard)
			gainedcard.gained(self)
			place.zerocheck(self.game.field)
	
	def buycard(self, number):#カードは原則サプライから購入される　山札の番号をnumberとして与える。
		boughtcard = self.game.field.supnumber.get(number).pile[0] #購入したいカードを変数に取得
		if self.coins >= boughtcard.cost and self.restbuys > 0:
			self.coins -= boughtcard.cost #そのカードのコストを購入者の残り金から減算
			self.restbuys -= 1 #購入権を1減らす
			self.gaincard(number)
			print(boughtcard.jname)
	
	def trashcard(self, object, place):
		number = place.index(object)
		trashedcard = place.pop(number)
		self.game.field.trash.append(trashedcard)
		trashedcard.trashed(self)
		
	def phaseend(self): #現在のフェーズを終了し、次のフェーズへ移行する
		self.phase = next(self.turn)
		
	def victorycount(self): #ゲーム終了後の勝利点計算
		vp = 0
		self.deck.extend(self.dispile)
		self.deck.extend(self.hand)
		self.deck.extend(self.playarea)
		vp = sum([i.vicpts for i in self.deck if i.is_victory_or_curse()])
		return vp	
		
	def handcheck(self, type):
		typec = card.cardtype.get(type)
		type_cards = [x for x in self.hand if hasattr(x, typec)]
		number = len(type_cards)
		return number
		#for i in range(number):
			#if hasattr(self.hand[i], typec):
				#return True
		#return False
	
	def plusactions(self, number):
		self.restactions += number
	
	def plusbuys(self, number):
		self.restbuys += number
		
	def pluscoins(self, number):
		self.coins += number
		
	def what_action(self):
		self.phaseend()
		
	def what_buy(self):
		pass
		
	def chancellor_effect(self):
		return 'n'
	
	def what_gain(self, number):
		pass
	
class HumanPlayer(Player):
	def __init__(self, game):
		super().__init__(game)
		self.isHuman = 1
		
	def what_coin_play(self):
		number = int(input())
		if number == -1:
			return -1
		else:
			self.playcard(number, 'right')
			return False
			
	def what_action(self):
		number = int(input())
		if number == -1:
			self.phaseend()
		else:
			self.playcard(number, 'right')
			
	def what_buy(self):
		number = int(input())
		if number == -1:
			self.phaseend()
		else:
			self.buycard(number)
		
	def chancellor(self):
		print("山札をすべて捨て札にしますか y/n")
		flag = 1
		while flag:
		#while True:
			answer = input()
			flag = self.input_y_or_n(answer)
			#if answer == 'y' or answer == 'n':
				#break
			#else:
				#print("yまたはnで答えてください")
		return answer
		
	def input_y_or_n(self, answer):
		if answer == 'y' or answer == 'n':
			return 0
		else:
			print("yまたはnで答えてください")
			return 1
				
	def what_gain(self, number):
		print("{0}コスト以下のカードを獲得します".format(number))
		while True:
			answer = int(input())
			place = self.game.field.supnumber.get(answer)
			if place.cost <= number:
				self.gaincard(answer)
				break
			else:
				print("コストが高すぎます")
			

#任意のプレイヤーは捨て札の一番上のカードをいつでも見ることができる
#プレイヤーはデッキの残り枚数を数えることができる
#廃棄置き場のカードを確認することができる
#サプライに残っているカードの枚数を確認できる


