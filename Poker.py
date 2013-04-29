import Card
import Deck
import Player
from Hand import Hand

class Poker:
	def __init__(self):
		self.deck = Deck.Deck(True)
		self.muck = []
		self.board = []
		self.pot = 0
		self.players = []
		self.players.append(Player.AI("Bot", 1000, True))
		self.players.append(Player.AI("Hal", 1000, True))
		self.players.append(Player.AI("Marvin", 1000, True))
		self.players.append(Player.AI("R2D2", 1000, True))
		self.players.append(Player.Human("Guy", 1000))
		assert len(self.players) >= 2, "Need at least 2 players"
		self.smallblindPlayer = 0
		self.smallblindAmount = 10
		self.bigblindPlayer = 1
		self.bigblindAmount = 20
		self.turn = 0

	def initTurn(self):
		print("Turn #" + str(self.turn))
		print("The blinds are ", self.smallblindAmount, ",", self.bigblindAmount)
		assert self.pot == 0, "Pot is not empty at start of turn"

		self.deck.shuffle()

		for player in self.players:
			player.initTurn()

		for player in self.players*2:
			player.giveCard(self.deck.pop())

		# Small Blind
		self.smallblindPlayer += 1
		self.smallblindPlayer %= len(self.players)
		self.pot += self.players[self.smallblindPlayer].bet(self.smallblindAmount)
		print(str(self.players[self.smallblindPlayer]), "bets the small blind. Pot is now", str(self.pot))

		# Big blind
		self.bigblindPlayer += 1
		self.bigblindPlayer %= len(self.players)
		self.pot += self.players[self.bigblindPlayer].bet(self.bigblindAmount)
		print(str(self.players[self.bigblindPlayer]), "bets the big blind. Pot is now", str(self.pot))

	def takeAllCardsFrom(self, player):
		buff = player.takeAllCards()
		while len(buff) > 0:
			self.muck.append(buff.pop())

	def endTurn(self):
		for player in self.players:
			self.takeAllCardsFrom(player)

		# Empty the muck in the deck
		while len(self.muck) > 0:
			self.deck.push(self.muck.pop())

		# Empty the board in the deck
		while len(self.board) > 0:
			self.deck.push(self.board.pop())

		self.turn += 1


	def bettingRound(self):
		currentBet = -1
		lastRaisePlayer = self.bigblindPlayer
		p = (lastRaisePlayer + 1) % len(self.players)
		while(p != lastRaisePlayer):
			player = self.players[p]
			decision = -2
			if (player.folded):
				print("player", str(player), "has folded")
			while not player.folded and decision < currentBet:
				decision = player.chooseAction(currentBet)
				print("player", str(player), "decides", decision)
				if (decision == "F"):
					player.folded = True
					self.takeAllCardsFrom(player)
					print(str(player) + " folded")
				elif (decision >= currentBet):
					self.pot += player.bet(decision)
					print(str(player) + " bet " + str(decision))
					if (decision > currentBet):
						currentBet = decision
						lastRaisePlayer = p
				else:
					print("You must bet above current bet : ", str(currentBet))
			p = (p + 1) % len(self.players)
		# Reinitialize players
		for player in self.players:
			player.currentBet = 0

	def burnAndDraw(self, numberOfCards=1):
		self.muck.append(self.deck.pop())
		print("Burn 1 card")
		for i in range(numberOfCards):
			self.board.append(self.deck.pop())
		self.printBoard()

	def printBoard(self):
		print(self.board)

	def onePlayerLeft(self):
		return len(list(filter(lambda x: not x.folded, self.players))) == 1

	def findWinner(self):
		if self.onePlayerLeft():
			for player in filter(lambda x: not x.folded, self.players):
				return player
		print("The contestant are...")
		currentMax = Hand(self.board)
		currentWin = None
		for activePlayer in filter(lambda x: not x.folded, self.players):
			print("Cards of player", str(activePlayer), str(activePlayer.cards))
			bestHand = Hand.findBestHandIn7(self.board + activePlayer.cards)
			if (bestHand == currentMax):
				assert False, "Multiple winner : not yet implemented..."  # TODO
			elif (bestHand > currentMax):
				currentMax = bestHand
				currentWin = activePlayer
		return currentWin

	def givePotToWinner(self):
		winner = self.findWinner()
		print("Player", str(winner), "is the winner and takes the pot ($" + str(self.pot)+")")
		winner.money += self.pot
		self.pot = 0

	def play(self):
		while(True):
			self.initTurn()

			self.bettingRound()
			if not self.onePlayerLeft():
				self.burnAndDraw(3)

				self.bettingRound()
				if not self.onePlayerLeft():
					self.burnAndDraw()
					self.bettingRound()
					if not self.onePlayerLeft():
						self.burnAndDraw()
						self.bettingRound()

			self.givePotToWinner()
			self.endTurn()

if __name__ == "__main__":
	poker = Poker()
	poker.play()
