import player

class HumanPlayer(player.Player):
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
	
	def choose_discard_from_hand(self):
		print([i.jname for i in self.cards.hand])
		answer = int(input())
		if answer == -1:
			return -1
		discard = self.hand_pop(answer)
		return discard
		
			
			