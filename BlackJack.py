import Deck


def is_black_jack(card1, card2):
    if card1.rankValue == '14' and 10 < card2.rankValue < 14:
        return True
    if card2.rankValue == '14' and 10 < card1.rankValue < 14:
        return True
    return False


class BlackJack(object):

    def __init__(self, numberOfDecks=1):
        self.deck = Deck.Deck(True)
        for i in range(numberOfDecks - 1):
            newDeck = Deck.Deck(True)
            for card in newDeck:
                self.deck.push(newDeck.pop())
        self.deck.shuffle()

    def play(self):
        pass


if __name__ == "__main__":
    bj = BlackJack(3)
