# -*- coding: utf-8 -*-

class Card:
	rankDict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}
	suitList = ["H", "D", "S", "C"]

	def __init__(self, rank, suit):
		self.setRank(rank)
		self.setSuit(suit)

	def setRank(self, rank):
		assert rank in Card.rankDict
		self.rank = rank
		self.rankValue = Card.rankDict[rank]

	def setSuit(self, suit):
		assert suit in Card.suitList
		self.suit = suit

	def __str__(self):
		printStr = ""
		printStr += self.rank
		if (self.suit == "H"):
			printStr += "♥"
		if (self.suit == "D"):
			printStr += "♦"
		if (self.suit == "S"):
			printStr += "♠"
		if (self.suit == "C"):
			printStr += "♣"
		return printStr

	def __repr__(self):
		return str(self)
		# reprStr = ""
		# if (self.rank == "1"):
		# 	reprStr += "One"
		# elif (self.rank == "2"):
		# 	reprStr += "Two"
		# elif (self.rank == "3"):
		# 	reprStr += "Three"
		# elif (self.rank == "4"):
		# 	reprStr += "Four"
		# elif (self.rank == "5"):
		# 	reprStr += "Five"
		# elif (self.rank == "6"):
		# 	reprStr += "Six"
		# elif (self.rank == "7"):
		# 	reprStr += "Seven"
		# elif (self.rank == "8"):
		# 	reprStr += "Height"
		# elif (self.rank == "9"):
		# 	reprStr += "Nine"
		# elif (self.rank == "10"):
		# 	reprStr += "Ten"
		# elif (self.rank == "J"):
		# 	reprStr += "Jack"
		# elif (self.rank == "Q"):
		# 	reprStr += "Queen"
		# elif (self.rank == "K"):
		# 	reprStr += "King"
		# elif (self.rank == "A"):
		# 	reprStr += "Ace"
		# reprStr += " of "
		# if (self.suit == "H"):
		# 	reprStr += "Hearts"
		# if (self.suit == "D"):
		# 	reprStr += "Diamonds"
		# if (self.suit == "S"):
		# 	reprStr += "Spades"
		# if (self.suit == "C"):
		# 	reprStr += "Clubs"
		# return reprStr

	def __lt__(self, other):
		return self.rankValue < other.rankValue
