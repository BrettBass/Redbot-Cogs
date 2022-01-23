# SmokeOrFire

This is a drinking game where the player has a number of guesses to make on the next card in the deck. Depending on whether or not there are cards in play the player will have more or less options to choose from.

How to complete your turn:
1. If there are no current cards in play, the player must make 4 correct guesses in order to finish their turn.
2. If the player is continuing from a previous tern (there are 4 or more cards in play at the start of the players turn) then the player must only get 3 correct consectutive guesses in order to complete their turn. If the player fails to do this, they will revert back to having to get 4 correct consectuve guesses.
3. If the player has currently matched or surpassed their required guesses then they can choose to continue playing at which point the player can choose to pass their turn at any time. If an incorrect guess is made after choosing to continue, the player will revert back to having to get 4 correct consectutive guesses

Types of guesses:
1. smoke - this corresponds to the card being black (can be used from any game state)
2. fire - this corresponds to the card being red (can be used from any game state)
3. higher - this corresponds to the card being higher than the previous card (can only be used from a continued game state which contains inplay cards)
4. lower - this corresponds to the card being lower than the previous card (can only be used from a continued game state which contains inplay cards)
5. same card - this corresponds to the card being the same as the previous card. If a player guesses same card correctly then their turn is automatically passed
passed and all other players have to take a shot instead of a normal drink. (can only be used from a continued game state which contains inplay cards)

Rules for Drinking:
1. Drink amount - The drink amount is equivalent to the amount of cards in play
2. Shot - shots are distbuted
    1. A player correctly guesses same card, everyone but the current player must take a shot
    2. A player can suplement 4 total drinks by taking 1 shot
3. A player must finish their owed drinks before the game continues

This game is currently a CLI game as of development and we be converted to a textchat game for discord and other platfoorms later.