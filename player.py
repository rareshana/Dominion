import random
import card
import main

class Player():
	def __init__(self, game):
		self.cards = PlayerCards() #手札、デッキ、巣手札、プレイエリア
		self.available = AvailablePerTurn() #残り金数、残りアクション権、残り購入権
		self.isAI = 0
		self.isHuman = 0
		self.other_players = []
		self.gameinfo = PlayerGameInfo(game)
	
	def draw(self, number):
		self.cards.draw(number)
	
	def playcard(self, number, when = None): #カードは手札からプレイされる　手札の何枚目かをnumberとして与える 正規のタイミング(財宝フェイズに出す財宝、アクションフェイズにアクション権を消費して出すアクションカード)でカードをプレイするとき、whenに'right'を与えることにする
		the_card = self.cards.hand_pickup(number)
		if (when is None) or (self.gameinfo.playable(the_card)):
			playedcard = self.cards.play_from_hands(number)
			self.gameinfo.rightplayed(when)
			playedcard.played(self)
			self.is_actionphase_end(when)  #処理終了後、アクションフェイズで残りアクション権が0ならばフェイズを自動的に終了する	
			return True
		return False
	
	def is_actionphase_end(self, when):
		if self.gameinfo.phase_judged(main.ActionPhase) and (when is 'right') and (not self.is_action_left()): 
			self.phaseend()
	
	def shuffle(self):
		self.cards.shuffle()
		
	def gaincard(self, number): #カードは原則サプライから獲得される　山札の番号をnumberとして与える。それだけだと情報が足りないので、fieldの情報も与えなければ……
		place = self.gameinfo.get_supply(number)
		if place.is_left(): #山札が切れていない場合のみ獲得できる
			gainedcard = place.pile.pop()
			self.put_on_dispile(gainedcard)
			gainedcard.gained(self)
			#place.zerocheck(self.gameinfo.game.field) #変更が必要……
			self.zerocheck_pile(place)
	
	def buycard(self, number):#カードは原則サプライから購入される　山札の番号をnumberとして与える。
		place = self.gameinfo.get_supply(number)
		if not place.is_left():
			return
		if self.available.coins >= place.cost and self.available.rest_buys > 0:
			self.available.coins -= place.cost #そのカードのコストを購入者の残り金から減算
			self.available.rest_buys -= 1 #購入権を1減らす
			print(self.available.rest_buys)
			self.gaincard(number)
			print(place.name)

	def trashcard(self, object, place): #廃棄時効果の発動のタイミングは？
		number = place.index(object)
		trashedcard = place.pop(number)
		self.put_on_trash(trashedcard)
		trashedcard.trashed(self)
		
	def phaseend(self): #現在のフェーズを終了し、次のフェーズへ移行する
		self.gameinfo.phaseend()
	
	def nextphase(self):
		self.gameinfo.phaseend()
	
	def victorycount(self):
		return self.cards.victorycount()
	
	def handcheck(self, type):
		typec = card.CardType.get_cardtype(type)
		return self.cards.handcheck(typec)
	
	def plusactions(self, number):
		self.available.plusactions(number)
	
	def plusbuys(self, number):
		self.available.plusbuys(number)
		
	def pluscoins(self, number):
		self.available.pluscoins(number)
	
	def what_action(self):
		self.phaseend()
		
	def what_buy(self):
		pass
		
	def chancellor_effect(self):
		return 'n'
	
	def what_gain(self, number):
		pass
		
	def beginturn(self, turn):
		self.gameinfo.beginturn(turn)
	
	def is_action_left(self):
		return self.available.is_action_left()
		
	def put_on_dispile(self, card):
		self.cards.put_on_dispile(card)
		
	def put_on_trash(self, card):
		self.gameinfo.put_on_trash(card)
		
	def zerocheck_pile(self, place):
		if place.zerocheck():
			self.gameinfo.add_zeropile()
			
	def phase_judged(self, phase):
		return self.gameinfo.phase_judged(phase)
	
	def turnstart(self):
		self.available.turnstart()
	
	def is_buys_left(self):
		return self.available.is_buys_left()
		
	def cleanup(self):
		self.cards.cleanup_cards()
		self.draw(5)
	
	def is_deck_empty(self):
		return self.cards.is_deck_empty()
		
	def is_dispile_empty(self):
		return self.cards.is_dispile_empty()

	def reveal_from_deck(self):
		return self.cards.reveal_from_deck()
	
	def add_hand(self, cards):
		self.cards.add_hand(cards)
	
	def add_dispile(self, cards):
		self.cards.add_dispile(cards)
	
class PlayerCards():
	def __init__(self):
		self.deck = [] #デッキ 下から上へ
		self.hand = [] #手札 左から右へ
		self.dispile = [] #捨て札の山 下から上へ
		self.playarea = [] #各プレイヤーの場 左から右へ
	
	def draw(self, number):
		if (number > len(self.deck)) and len(self.deck) >= 0: #デッキの枚数が足りず、かつ捨て札があるとき
			number = self.dispile_to_deck(number)
			#number -= len(self.deck)
			#self.hand.extend(self.deck[::-1])
			#self.deck.clear()
			#self.deck.extend(self.dispile)
			#self.dispile.clear()
			#self.shuffle()
		drawcard = self.deck[-number:]
		self.deck = self.deck[:-number]
		self.hand.extend(drawcard[::-1])
	
	def shuffle(self):
		random.shuffle(self.deck)
	
	def dispile_to_deck(self, number):
		number -= len(self.deck)
		self.hand.extend(self.deck[::-1])
		self.deck.clear()
		self.deck.extend(self.dispile)
		self.dispile.clear()
		self.shuffle()
		return number

	def victorycount(self):
		vp = 0
		self.deck.extend(self.dispile)
		self.deck.extend(self.hand)
		self.deck.extend(self.playarea)
		vp = sum([i.vicpts for i in self.deck if i.is_victory_or_curse()])
		return vp	
	
	def handcheck(self, type):
		type_cards = [x for x in self.hand if hasattr(x, type)]
		number = len(type_cards)
		return number
		
	def play_from_hands(self, number):
		playedcard = self.hand.pop(number)
		self.playarea.append(playedcard)
		return playedcard
	
	def hand_pickup(self, number):
		return self.hand[number]
		
	def put_on_dispile(self, card):
		self.dispile.append(card)
	
	def cleanup_cards(self):
		self.dispile.extend(self.playarea)
		self.playarea.clear()
		self.dispile.extend(self.hand)
		self.hand.clear()
		
	def is_deck_empty(self):
		if self.deck == []:
			return True
		return False
		
	def is_dispile_empty(self):
		if self.dispile == []:
			return True
		return False
	
	def reveal_from_deck(self):
		if len(self.deck) == 0 and len(self.deck) >= 0: #デッキの枚数が足りず、かつ捨て札があるとき
			self.dispile_to_deck(1)
		revealed_card = self.deck[-1:][0]
		self.deck = self.deck[:-1]
		return revealed_card
	
	def add_hand(self, cards):
		self.hand.extend(cards)
	
	def add_dispile(self, cards):
		self.dispile.extend(cards)
		
		
class AvailablePerTurn():
	def __init__(self):
		self.rest_actions = 1
		self.rest_buys = 1
		self.coins = 0
	
	def turnstart(self):
		self.__init__()
	
	def plusactions(self, number):
		self.rest_actions += number
	
	def plusbuys(self, number):
		self.rest_buys += number
		
	def pluscoins(self, number):
		self.coins += number
	
	def is_action_left(self):
		return (self.rest_actions > 0)
	
	def is_buys_left(self):
		return (self.rest_buys > 0)
		
class PlayerGameInfo():
	def __init__(self, game):
		self.turn = 0
		self.phase = 0
		self.game = game
	
	def get_cardinfo(self, number):
		return self.game.get_cardinfo(number)

	def phaseend(self):
		self.phase = next(self.turn)
		
	def beginturn(self, turn):
		self.turn = turn
	
	def phase_judged(self, phase):
		return isinstance(self.phase, phase)
		
	def get_supply(self, number):
		return self.game.get_supply(number)
	
	def rightplayed(self, when):
		self.phase.rightplayed(when)
		
	def playable(self, card):
		return self.phase.playable(card)
	
	def put_on_trash(self, card):
		self.game.put_on_trash(card)
	
	def get_cardtype(self, type):
		return CardType.get_cardtype(type)
	
	def add_zeropile(self):
		self.game.add_zeropile()
		
class HumanPlayer(Player):
	def __init__(self, game):
		super().__init__(game)
		self.isHuman = 1
		
	def what_coin_play(self):
		number = int(input())
		if number == -1:
			return -1
		self.playcard(number, 'right')
		return False
			
	def what_action(self):
		number = int(input())
		if number == -1:
			self.phaseend()
			return
		self.playcard(number, 'right')
			
	def what_buy(self):
		number = int(input())
		if number == -1:
			self.phaseend()
			return
		self.buycard(number)
		
	def chancellor_effect(self):
		print("山札をすべて捨て札にしますか y/n")
		flag = 1
		while flag:
			answer = input()
			flag = self.input_y_or_n(answer)
		return answer
		
	def input_y_or_n(self, answer):
		if answer == 'y' or answer == 'n':
			return 0
		print("yまたはnで答えてください")
		return 1
				
	def what_gain_undercost(self, number):
		print("{0}コスト以下のカードを獲得します".format(number))
		flag = 1
		while flag:
			answer = int(input())
			place = self.gameinfo.get_supply(answer)
			flag = self.is_gainable(answer, place, number)
				
	def is_gainable(self, answer, place, number):
		if place.cost <= number:
			self.gaincard(answer)
			return 0
		print("コストが高すぎます")
		return 1


#任意のプレイヤーは捨て札の一番上のカードをいつでも見ることができる
#プレイヤーはデッキの残り枚数を数えることができる
#廃棄置き場のカードを確認することができる
#サプライに残っているカードの枚数を確認できる


