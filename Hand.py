from Deck import Deck
from Card import Card
import copy


class Hand:
	handTypeDict = {"High": 1, "Pair": 2, "Two Pairs": 3, "Three of a kind": 4, "Straight": 5, "Flush": 6, "Full House": 7, "Four of a kind": 8, "Straight Flush": 9}

	def __init__(self, cards):
		assert len(cards) == 5, "Hand : cards does not have 5 cards " + str(self.cards)
		self.cards = copy.copy(cards)
		self.cards.sort()
		self.setHistogram()
		self.handType = self.getHandValue()

	def setHistogram(self):
		self.histogram = [0]*len(Card.rankDict)
		for card in self.cards:
			rank = card.rankValue - 2
			self.histogram[rank] += 1

	def getHandValue(self):
		if (4 in self.histogram) and (1 in self.histogram):
			return Hand.handTypeDict["Four of a kind"]
		elif (3 in self.histogram) and (2 in self.histogram):
			return Hand.handTypeDict["Full House"]
		elif (3 in self.histogram) and (self.histogram.count(1) == 2):
			return Hand.handTypeDict["Three of a kind"]
		elif (self.histogram.count(2) == 2) and (1 in self.histogram):
			return Hand.handTypeDict["Two Pairs"]
		elif (self.histogram.count(1) == 3) and (1 in self.histogram):
			return Hand.handTypeDict["Pair"]

		# Check for Flush
		isFlush = True
		firstSuit = self.cards[0].suit
		for card in self.cards:
			isFlush = isFlush and firstSuit == card.suit

		# Check for Straight
		isStraight = (self.cards[-1].rankValue - self.cards[0].rankValue == 4)
		# TODO : check for the wheel (A - 2 - 3 - 4 - 5)
		if (not isStraight):
			isStraight = (self.cards[-1].rank == "A" and self.cards[-2].rank == "5")

		if (isFlush and isStraight):
			return Hand.handTypeDict["Straight Flush"]
		elif (isFlush):
			return Hand.handTypeDict["Flush"]
		elif (isStraight):
			return Hand.handTypeDict["Straight"]

		return Hand.handTypeDict["High"]

	def __lt__(self, other):
		return self.compare(other) < 0

	def compare(self, other):
		"""
		Returns an int
			< 0 if self < other
			== 0 if self == other
			> 0 if self > other
		"""
		if (self.handType != other.handType):
			return self.handType - other.handType
		# Same hand type : check for type-specific cards
		if (self.handType == 2):  # Pair
			selfRank = self.histogram.index(2)
			otherRank = other.histogram.index(2)
			if (selfRank != otherRank):
				return selfRank - otherRank
		if (self.handType == 3):  # Two pairs
			# check the highest pair
			selfRank = 0
			for rank, count in enumerate(reversed(self.histogram)):
				if (count == 2):
					selfRank = rank
					break
			otherRank = 0
			for rank, count in enumerate(reversed(other.histogram)):
				if (count == 2):
					otherRank = rank
					break
			if (selfRank != otherRank):
				return otherRank - selfRank  # reversed again
			# highest pair was the same : check the second pair
			selfRank = self.histogram.index(2)
			otherRank = other.histogram.index(2)
			if (selfRank != otherRank):
				return selfRank - otherRank
		if (self.handType == 4):  # Three of kind
			selfRank = self.histogram.index(3)
			otherRank = other.histogram.index(3)
			if (selfRank != otherRank):
				return selfRank - otherRank
		if (self.handType == 7):  # Full House
			# Check the three of a kind
			selfRank = self.histogram.index(3)
			otherRank = other.histogram.index(3)
			if (selfRank != otherRank):
				return selfRank - otherRank
			# Check the pair
			selfRank = self.histogram.index(2)
			otherRank = other.histogram.index(2)
			if (selfRank != otherRank):
				return selfRank - otherRank
		if (self.handType == 8):  # Four of a kind
			selfRank = self.histogram.index(4)
			otherRank = other.histogram.index(4)
			if (selfRank != otherRank):
				return selfRank - otherRank

		# The winning hand will be determined by the rest of the cards
		for i in reversed(range(len(self.cards))):
			if (self.cards[i].rankValue != other.cards[i].rankValue):
				return self.cards[i].rankValue - other.cards[i].rankValue
		return 0

	def __repr__(self):
		reprStr = ""
		for name, value in Hand.handTypeDict.items():
			if (self.handType == value):
				reprStr += name
		reprStr += " ("
		for card in self.cards:
			reprStr += str(card) + " "
		reprStr += ")"
		return reprStr

	@staticmethod
	def findBestHandIn7(cards):
		assert len(cards) == 7, "findBestHandIn : need 7 cards, not " + str(len(cards))
		# brute force !!!!
		currentMax = Hand([cards[0], cards[1], cards[2], cards[3], cards[4]])
		for removedCard1 in cards:
			tmpCards = copy.copy(cards)
			tmpCards.pop(tmpCards.index(removedCard1))
			for removedCard2 in tmpCards:
				fiveCards = copy.copy(tmpCards)
				fiveCards.pop(fiveCards.index(removedCard2))
				hand = Hand(fiveCards)
				if (hand > currentMax):
					currentMax = hand
		return currentMax

if __name__ == "__main__":
	cards = []
	cards.append(Card("A", "H"))
	cards.append(Card("K", "H"))
	cards.append(Card("Q", "H"))
	cards.append(Card("J", "H"))
	cards.append(Card("10", "H"))
	hand1 = Hand(cards)
	assert hand1.handType == 9, "Unit Test Failed : Straight Flush"

	cards = []
	cards.append(Card("A", "H"))
	cards.append(Card("2", "D"))
	cards.append(Card("3", "C"))
	cards.append(Card("4", "D"))
	cards.append(Card("5", "H"))
	hand2 = Hand(cards)
	assert hand2.handType == 5, "Unit Test Failed : Straight (wheel) was " + str(hand2)

	cards = []
	cards.append(Card("Q", "H"))
	cards.append(Card("Q", "D"))
	cards.append(Card("4", "S"))
	cards.append(Card("4", "C"))
	cards.append(Card("10", "H"))
	hand3 = Hand(cards)
	assert hand3.handType == 3, "Unit Test Failed : Two Pairs"

	cards = []
	cards.append(Card("K", "H"))
	cards.append(Card("K", "D"))
	cards.append(Card("4", "S"))
	cards.append(Card("4", "C"))
	cards.append(Card("10", "H"))
	hand4 = Hand(cards)
	assert hand4.handType == 3, "Unit Test Failed : Two Pairs"

	assert hand3 < hand4, "Unit Test Failed : Two pairs comparison"

	# Random testing (todo: oracle)
	for i in range(100):
		deck = Deck()
		deck.shuffle()
		cards = []
		for c in range(5):
			cards.append(deck.pop())
		hand1 = Hand(cards)
		while len(cards) > 0:
			deck.push(cards.pop())
		deck.shuffle()
		for c in range(5):
			cards.append(deck.pop())
		hand2 = Hand(cards)
		if (hand1.compare(hand2) == 0):
			print("1 : ", hand1)
			print("2 : ", hand2)
			print("1 < 2 : ", hand1.compare(hand2))
			print("-----")
