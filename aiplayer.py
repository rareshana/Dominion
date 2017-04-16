import player

class AIPlayer1(player.Player):#お金プレイ
	def __init__(self, game):
		super().__init__(game)
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
			
	def what_action(self):
		pass

class AIPlayer2(player.Player): #鍛冶屋ステロ
	def __init__(self, game):
		super().__init__(game)
		self.isAI = 1
		
	def play_coins(self):
		i = 0
		while i < len(self.hand):
			if self.playcard(i, 'right'):
				i -= 1
			if i+1 >= len(self.hand):
				break
			i += 1
			
	def play_action(self):
		i = 0
		while i < len(self.hand):
			if self.playcard(i, 'right'):
				break
			i += 1
			
	def what_buy(self, field, turncount):
		if self.coins < 3:
			pass
		elif self.coins < 6:
			self.buycard(3, field)
		elif self.coins < 8:
			self.buycard(4, field)
		else:
			self.buycard(7, field)
					