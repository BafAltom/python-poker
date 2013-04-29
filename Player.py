import random

class Player(object):
	currentId = 0

	@staticmethod
	def getNextId():
		Player.currentId += 1
		return Player.currentId

	def __init__(self, name, money):
		self.playerID = Player.getNextId()
		self.name = name
		self.money = money
		self.cards = []
		self.folded = False
		self.currentBet = 0

	def initTurn(self):
		assert len(self.cards) == 0, "Player still has cards at the start of a turn"
		assert self.money > 0, "Player " + str(self) + " does not have any money at the start of a turn"
		self.folded = False

	def chooseAction(self, currentBet):
		raise Exception("Player.chooseAction is an Abstract method!")

	def giveCard(self, card):
		assert len(self.cards) < 2, "Player already has 2 cards or more"
		self.cards.append(card)

	def takeAllCards(self):
		buff = []
		while len(self.cards) > 0:
			buff.append(self.cards.pop())
		return buff

	def __str__(self):
		return self.name + "($" + str(self.money) + ")"

	def bet(self, amount):
		tmp = min(amount, self.money)
		self.money -= tmp
		return tmp

class AI(Player):
	def __init__(self, name, money, alwaysFollow=False):
		Player.__init__(self, name, money)
		self.alwaysFollow = alwaysFollow

	def chooseAction(self, currentBet):
		if (self.alwaysFollow):
			return currentBet
		if (currentBet > self.money):
			return "F"  # TODO : able to do all-in
		return random.choice(["F", random.randint(currentBet, self.money)])

class Human(Player):
	def __init__(self, name, money):
		Player.__init__(self, name, money)

	def giveCard(self, card):
		print("Received : ", str(card))
		super(Human, self).giveCard(card)

	def chooseAction(self, currentBet):
		decision = input("What is " + str(self) + " going to do?")
		if (decision == "F"):
			return decision
		else:
			# TODO : try/catch
			decision = int(decision)
			return decision
