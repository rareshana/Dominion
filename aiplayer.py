import player

class AIPlayer1(player.Player): #お金プレイ
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
			
	def what_buy(self):
		if self.coins < 3:
			pass
		elif self.coins < 6:
			self.buycard(3)
		elif self.coins < 8:
			self.buycard(4)
		else:
			self.buycard(7)
			
	def what_action(self):
		pass

class AIPlayer2(player.Player): #鍛冶屋ステロ
	def __init__(self, game):
		super().__init__(game)
		self.isAI = 1
		self.smithycount = 0
		self.smithyindex = -1
		
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
				print("test")
				break
			i += 1
			
	def what_buy(self):
		if self.smithyindex == -1 and "Smithy" in [x.name for x in self.game.field.actionpile]:
			self.smithyindex = [x.name for x in self.game.field.actionpile].index("Smithy") + 8
		
		if self.coins < 3:
			pass
		elif self.coins == 3:
			self.buycard(3)
		elif self.coins < 6 and self.smithycount == 0 and self.smithyindex != -1:
			self.smithycount += 1
			self.buycard(self.smithyindex)
		elif self.coins < 6:
			self.buycard(3)
		elif self.coins < 8:
			self.buycard(4)
		else:
			self.buycard(7)
					