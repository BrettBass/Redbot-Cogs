from .deck import *
#define a class to hold deck information of multiple decks called shoe
class Shoe:
    def __init__(self, decks):
        self.decks = decks
        self.cards = []
        self.build()

    def build(self):
        for deck in range(self.decks):
            deck = Deck()
            self.cards.extend(deck.cards)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
    
    def cut(self):
        random.shuffle(self.cards)
        cut = random.randint(0, len(self.cards))
        self.cards = self.cards[cut:] + self.cards[:cut]