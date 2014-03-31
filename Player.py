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
        self.currentBet = 0
        self.folded = False
        self.allin = False

    def initTurn(self):
        assert len(self.cards) == 0, "Player still has cards at the start of a turn"
        assert self.money > 0, "Player " + str(self) + " does not have any money at the start of a turn"
        self.folded = False
        self.allin = False
        self.currentBet = 0

    def chooseAction(self, currentBet):
        """
        returns "F" [fold], "A" [all-in] or an amount (check/raise)
        """
        raise Exception("Player.chooseAction is an Abstract method!")

    def canBet(self):
        return not (self.folded or self.allin)

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
        toPay = amount - self.currentBet
        moneyBuffer = min(toPay, self.money)
        self.currentBet += moneyBuffer
        self.money -= moneyBuffer
        return moneyBuffer


class AI(Player):
    def __init__(self, name, money, alwaysFollow=False):
        Player.__init__(self, name, money)
        self.alwaysFollow = alwaysFollow

    def giveCard(self, card):
        print(self.name, "received a card")
        super()

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
        print("You received : ", str(card))
        super(Human, self).giveCard(card)

    def chooseAction(self, currentBet):
        decision = input("What is " + str(self) + " going to do? (current bet is " + str(currentBet) + ")")
        if (decision in ["F", "A"]):
            return decision
        else:
            # TODO : try/catch
            decision = int(decision)
            return decision
