import Deck
import Player
from Hand import Hand
import sys


class Poker:
    def __init__(self):
        self.deck = Deck.Deck(True)
        self.muck = []
        self.board = []
        self.pot = 0
        self.smallblindPlayer = 0
        self.smallblindAmount = 10
        self.bigblindPlayer = 1
        self.bigblindAmount = 20
        self.turn = 0

        self.players = []
        self.players.append(Player.AI("Bot", 1000, True))
        self.players.append(Player.AI("Hal", 1000, True))
        self.players.append(Player.AI("Marvin", 1000, True))
        self.players.append(Player.AI("R2D2", 1000, True))
        self.players.append(Player.Human("Guy", 1000))
        assert len(self.players) >= 2, "Need at least 2 players"
        self.initalMoneyAmount = 0
        for p in self.players:
            self.initalMoneyAmount += p.money

    def initTurn(self):
        print("Turn ", self.turn)
        print("########")
        print("")
        assert self.pot == 0, "Pot is not empty at start of turn"
        totalMoney = 0
        for p in self.players:
            totalMoney += p.money
        assert totalMoney == self.initalMoneyAmount

        self.deck.shuffle()
        for player in self.players:
            player.initTurn()
        for player in self.players*2:  # TODO : Distribute cards "the right way" (beginning with the small bet)
            player.giveCard(self.deck.pop())
        self.smallblindPlayer += 1
        self.smallblindPlayer %= len(self.players)
        self.bigblindPlayer += 1
        self.bigblindPlayer %= len(self.players)

    def takeAllCardsFrom(self, player):
        buff = player.takeAllCards()
        while len(buff) > 0:
            self.muck.append(buff.pop())

    def endTurn(self):
        for player in self.players:
            self.takeAllCardsFrom(player)
        self.players = list(filter(lambda x: x.money > 0, self.players))
        # Empty the muck in the deck
        while len(self.muck) > 0:
            self.deck.push(self.muck.pop())
        # Empty the board in the deck
        while len(self.board) > 0:
            self.deck.push(self.board.pop())
        self.turn += 1

    def isFirstBettingRound(self):
        return len(self.board) == 0

    def bettingRound(self):
        print()
        currentBet = 0
        lastRaisePlayer = (self.smallblindPlayer - 1) % len(self.players)
        p = (lastRaisePlayer + 1) % len(self.players)
        while p != lastRaisePlayer:
            player = self.players[p]
            decision = -1

            if (player.folded):
                print("player", str(player), "has folded.")
            elif (player.allin):
                print("player", str(player), "is all-in.")

            # enforce small blind
            elif currentBet == 0 and self.isFirstBettingRound() and player == self.players[self.smallblindPlayer]:
                decision = self.smallblindAmount
            # enforce big blind
            elif currentBet == self.smallblindAmount and self.isFirstBettingRound() and player == self.players[self.bigblindPlayer]:
                decision = self.bigblindAmount
            else:
                while player.canBet() and decision < currentBet:
                    decision = player.chooseAction(currentBet)
                    if decision == "F":
                        decision = 0
                        player.folded = True
                        self.takeAllCardsFrom(player)
                        print(str(player) + " folded")
                    elif decision == "A" or decision >= player.money:
                        player.allin = True
                        decision = player.money
                        print(str(player) + " goes all in!")
                    #else:
                        #print("player", str(player), "decides", decision)

            if decision >= currentBet:
                self.pot += player.bet(decision)
                print(str(player) + " bet " + str(decision))
                if (decision > currentBet):
                    currentBet = decision
                    lastRaisePlayer = p
            p = (p + 1) % len(self.players)
        # Reinitialize players
        for player in self.players:
            player.currentBet = 0

    def burnAndDraw(self, numberOfCards=1):
        self.muck.append(self.deck.pop())
        print("\nBurn 1 card")
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
        return currentWin, currentMax

    def givePotToWinner(self):
        winner, winningHand = self.findWinner()
        if (winner):
            print("\nPlayer", str(winner), "is the winner with a", str(winningHand), "and takes the pot ($" + str(self.pot)+")")
            winner.money += self.pot
        else:
            print("No winner! Pot is distributed between players")
            activePlayers = list(filter(lambda x: not x.folded, self.players))
            assert self.pot % len(activePlayers) == 0, str(self.pot) + " != " + str(len(activePlayers))
            amountPerPlayer = int(self.pot / len(activePlayers))
            for p in activePlayers:
                assert self.pot >= amountPerPlayer
                p.money += amountPerPlayer
                self.pot -= amountPerPlayer
        self.pot = 0

    def play(self):
        for i in range(100):
            print("")
        with open("title.txt") as titleF:
            for line in titleF:
                print(line[:-1])  # remove trailing \n
        while(len(self.players) > 1):
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
        print("The winner is : ", str(self.players[0]))

if __name__ == "__main__":
    if (sys.version_info[0] < 3):
        print("PLEASE LAUNCH WITH PYTHON3")
        sys.exit()
    poker = Poker()
    poker.play()
