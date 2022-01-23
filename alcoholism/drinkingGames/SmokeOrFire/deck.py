#a deck object is created to hold a list of cards
#it will hold the cards in play, ready to play, and the cards that have been played
import random
import card

class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []
        self.inPlay = []
        self.buildDeck()
        self.shuffle()
    
    def buildDeck(self):
        for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
            for value in range(1, 14):
                self.cards.append(card.Card(suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) == 0:
            #this could break if discard is empty
            self.cards = self.discard
            self.discard = []
            self.shuffle()
        Card = self.cards.pop()
        self.inPlay.append(Card)
        return Card
    
    def discard(self, Card):
        self.discard.append(Card)
        self.inPlay.remove(Card)
    
    def discardAllInPlay(self):
        self.discard += self.inPlay
        self.inPlay = []

    def getInPlay(self):
        return self.inPlay
    
    def lastCardPlayed(self):
        if len(self.inPlay) > 0:
            return self.inPlay[-1]
        else:
            return card.Card("", 0)
    
    def previousCard(self):
        if len(self.inPlay) > 0:
            return self.inPlay[-2]
        else:
            return card.Card("", 0)
