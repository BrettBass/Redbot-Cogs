from .shoe import *
from .user import *

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.getNumericValue()
        if card.getNumericValue() == 11:
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def first_card(self):
        return self.cards[0].getNumericValue()
    
#build a player object which will hold an id, bet amount and multiple hands
class Player:
    def __init__(self, id, bet):
        self.user = User.User(id, bet)
        self.hands = []
        self.hands.append(Hand())
        self.active_hand = 0
        self.status = {"split":[False], "double_down":[False], "push":[False],
                              "blackjack":[False], "surrender":[False], "loss":[False]}

        self.user.game_session_active = False


    def add_hand(self):
        self.hands.append(Hand())
        for s in self.status:
            self.status[s].append(False)

    def hit(self, card):
        self.hands[self.active_hand].add_card(card)
        self.hands[self.active_hand].adjust_for_ace()

    def double_down(self, card):
        self.status["double_down"][self.active_hand] = True
        self.user.bet *= 2
        self.hit(card)

    def split_hand(self):
        self.status["split"] = True
        self.add_hand()
        card1 = self.hands[self.active_hand]
        card2 = self.hands[self.active_hand + 1]
        self.hit(card1)
        self.active_hand += 1
        self.hit(card2)
        self.active_hand -= 1
    
    def can_double(self):
        if len(self.hands[self.active_hand].cards) <= 2:
            return True
        else:
            return False
    
    def check_blackjack(self):
        if self.hands[self.active_hand].value == 21:
            self.status["blackjack"][self.active_hand] = True
            return True
        else:
            return False
    
    def check_split(self):
        return False
        # if self.hands[self.active_hand].value == self.hands[self.active_hand + 1].value:
        #     return True
        # else:
        #     return False

    def set_game_session_active(self, active):
        self.user.game_session_active = active
    
    def get_id(self):
        return self.user.id
    
    def check_soft_17(self):
        if self.hands[self.active_hand].value == 17 and self.hands[self.active_hand].aces:
            return True
        else:
            return False

    def check_bust(self):
        if self.hands[self.active_hand].value > 21:
            self.status["loss"][self.active_hand] = True
            return True
        else:
            return False
    
    def next_hand(self):
        self.active_hand += 1

    def calculate_payout(self):
        payment = 0
        for i in range(len(self.hands)):
            if self.status["loss"][i]:
                payment += self.user.bet * -1

            elif self.status["blackjack"][i] or self.status["double_down"][i]:
                payment += self.user.bet * 2
            
            elif self.status["surrender"][i]:
                import math
                payment += math.ceil(self.user.bet/2) * -1
            
            elif self.status["push"][i]:
                continue
            else:
                payment += self.user.bet

        return payment


def start_game(dict):
    players = []
    for id in dict:
        players.append(id, dict[id])
    
    dealer = Player(0, 0)

    #create playable shoe
    shoe = Card.shoe(7)
    shoe.build()
    shoe.shuffle()
    shoe.burn()

    #give everybody 2 cards
    for i in range(2):
        for player in players:
            player.hit(shoe.deal())
        dealer.hit(shoe.deal())

    #check players for blackjack or split
    for i in range(len(players)):
        if players[i].check_blackjack():
            print("Player " + str(players[i].get_id()) + " has blackjack")
            players[i].status["blackjack"][0] = True
        elif players[i].check_split():
            players[i].status["split"][0] = True
    
    #check dealer for blackjack
    if dealer.check_blackjack():
        print("Dealer has blackjack")
        dealer.status["blackjack"][0] = True
    
    # have players play out their hands
    for player in players:
        while player.active_hand < len(player.hands):
            if player.status["blackjack"][player.active_hand]:
                player.next_hand()
                continue

            if player.check_bust():
                player.status["loss"][player.active_hand] = True
                player.next_hand()
                #DUCK
                #Print some bust message. EXAMPLE "you fucking lost via bust, tuff shit"
                continue
            
            msg = "hit, stand"
            
            if player.can_double():
                msg += ", double, surrender"
            
            if player.can_split():
                msg += ", split"
            
            msg += "."

            #DUCK
            # I need you to print:
            # {player.user.id}: {player.hand.value}
            # "dealer is showing: " {dealer.first_card()}
            #  {msg}
            print(msg)

            #DUCK
            # get players input, should be one of the following below
            # if you want, it's defaulted to stand if they give a bs input
            # if they try to split or double when they're not allowed to it'll
            # default stand
            # if you want to do exception handling feel free, i do like to curse
            # inbetween commands lol
            player_input = str(input())

            if player_input == "hit":
                player.hit(shoe.deal())

            elif player_input == "split" and player.check_split():
                player.status["split"]
                player.split_hand()
            
            elif player_input == "double" and player.can_double():
                player.status["double"][player.active_hand]
                player.double_down(shoe.deal())
                player.next_hand()

            else:
                player.status["stand"][player.active_hand] = True
                player.next_hand() 