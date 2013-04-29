from Card import Card
import random

class Deck:
	def __init__(self, shuffle=False):
		self.cards = []
		for rank in Card.rankDict:
			for suit in Card.suitList:
				self.cards.append(Card(rank, suit))
		if (shuffle):
			self.shuffle()

	def pop(self):
		return self.cards.pop()

	def push(self, card):
		return self.cards.append(card)

	def __len__(self):
		return len(self.cards)

	def shuffle(self):
		c1, c2 = -1, -1
		for i in range(100*len(self)):
			c1 = random.randint(0, len(self) - 1)
			c2 = random.randint(0, len(self) - 1)
			#print("switched ", c1, " and ", c2)
			self.cards[c1], self.cards[c2] = self.cards[c2], self.cards[c1]

	def __repr__(self):
		reprStr = ""
		reprStr += "Card Deck ("
		reprStr += str(len(self))
		reprStr += ")\n"
		for card in self.cards:
			reprStr += str(card) + "\n"
		return reprStr

if __name__ == "__main__":
	deck = Deck(True)
	print(deck)
