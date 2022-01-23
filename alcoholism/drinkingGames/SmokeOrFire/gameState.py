import deck


class GameState:
    def __init__(self):
        self.deck = deck.Deck()
        self.drinks = 0
        self.guesses = 4
        self.passed = False
        self.continued = False
        self.deck.shuffle()
        self.quit = False
    
    def quitGame(self):
        self.quit = True

    def checkQuit(self):
        return self.quit

    def getDrinks(self):
        return self.drinks
    
    def getGuesses(self):
        return self.guesses
    
    def getPassed(self):
        return self.passed
    
    def getContinued(self):
        return self.continued
    
    def getCard(self):
        return self.deck.deal()
    
    def setDrinks(self, drinks):
        self.drinks = drinks
    
    def setGuesses(self, guesses):
        self.guesses = guesses
    
    def setPassed(self, passed):
        self.passed = passed
    
    def setContinued(self, continued):
        self.continued = continued
    
    def lastCard(self):
        return self.deck.lastCardPlayed()
    
    def previousCard(self):
        return self.deck.previousCard()
    
    def newTurn(self):
        self.guesses = 0
        self.passed = False
    
    def turn(self):
        #there's a new tern if the player has passed and the player has not continued
        return not self.passed or self.continued
    
    def CardsInPlay(self):
        return self.deck.inPlay

    def noCardsInPlay(self):
        return len(self.deck.inPlay) == 0
    
    def checkGuess(self, guess, card):
        self.drinks += 1
        if ( guess == 's' and card.getColor() == 'Black'
            or guess == 'f' and card.getColor() == 'Red'
            or guess == 'h' and card.getValue() > self.previousCard().getValue()
            or guess == 'l' and card.getValue() < self.previousCard().getValue() ):
                self.guesses = self.guesses - 1
                return True

        elif guess == 'sc' and card.getValue() == self.previousCard().getValue():
            self.guesses = -999
            return True

        else:
            self.guesses = 4
            self.deck.discardAllInPlay()
    

    def checkSameCard(self):
        return self.guesses < -900
    
    def owedDrinks(self):
        if( self.guesses == 4 ):
            drinks = self.drinks
            self.drinks = 0
            return drinks

        else:
            return 0
    
    def newTurn(self):
        self.guesses = 4
        self.passed = False
    
    def checkPass(self):
        self.passed = self.guesses <= 0
        return self.passed

    def continueGame(self, continued):
        self.continued = continued