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

    def __iter__(self):
        return DeckIterator(self)

    def pop(self):
        return self.cards.pop()

    def push(self, card):
        return self.cards.append(card)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        # Fisher-Yates  http://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
        for i in range(len(self) - 1, 1, -1):
            j = random.randint(1, i)
            self.cards[j], self.cards[i] = self.cards[i], self.cards[j]

    def __repr__(self):
        reprStr = ""
        reprStr += "Card Deck ("
        reprStr += str(len(self))
        reprStr += ")\n"
        for card in self.cards:
            reprStr += str(card) + "\n"
        return reprStr


class DeckIterator(object):

    def __init__(self, deck):
        self.deck = deck
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter == len(self.deck):
            raise StopIteration
        nextCard = self.deck.cards[self.counter]
        self.counter += 1
        return nextCard


if __name__ == "__main__":
    deck = Deck(True)
    print(deck)
    for card in deck:
        print("\t", card)
