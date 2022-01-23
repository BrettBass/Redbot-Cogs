class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if self.suit == 'Spades' or self.suit == 'Clubs':
            self.color = 'Black'
        else:
            self.color = 'Red'
    
    def __str__(self):
        return self.strValue() + " of " + self.suit
    
    def strValue(self):
        if self.value == 1:
            return "Ace"
        elif self.value == 11:
            return "Jack"
        elif self.value == 12:
            return "Queen"
        elif self.value == 13:
            return "King"
        else:
            return str(self.value)
    
    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
    def getColor(self):
        return self.color