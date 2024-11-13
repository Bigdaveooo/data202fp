import random

# Constants
NUM_DECKS = 6
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Card class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for _ in range(NUM_DECKS) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.total = 0
        self.ace_count = 0

    def add_card(self, card):
        self.hand.append(card)
        if card.rank in ['J', 'Q', 'K']:
            self.total += 10
        elif card.rank == 'A':
            self.total += 11
            self.ace_count += 1
        else:
            self.total += int(card.rank)

        self.adjust_for_aces()

    def adjust_for_aces(self):
        while self.total > 21 and self.ace_count:
            self.total -= 10
            self.ace_count -= 1

    def show_hand(self):
        return f"{self.name}'s hand: " + ', '.join(str(card) for card in self.hand) + f" | Total: {self.total}"

# Dealer class
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def show_hand(self, reveal=False):
        if reveal:
            return f"{self.name}'s hand: " + ', '.join(str(card) for card in self.hand) + f" | Total: {self.total}"
        else:
            return f"{self.name}'s hand: {self.hand[0]}, [Hidden Card]"

# AI decision function
def ai_decision(player_total, dealer_card):
    # Basic strategy for blackjack
    if player_total >= 17:
        return 's'  # Stand
    elif player_total >= 12 and dealer_card.rank in ['4', '5', '6']:
        return 's'  # Stand against weak dealer
    else:
        return 'h'  # Hit

# Game function
def play_blackjack_with_ai():
    deck = Deck()
    dealer = Dealer()
    players = [Player(f"Player {i + 1}") for i in range(5)]

    # Initial dealing
    for _ in range(2):
        dealer.add_card(deck.deal_card())
        for player in players:
            player.add_card(deck.deal_card())

    # Show initial hands
    print(dealer.show_hand())  # Dealer shows one card
    for player in players:
        print(player.show_hand())  # Show all players' hands

    # Players' turn with AI
    for player in players:
        while True:
            print(f"{player.name}, your total is {player.total}. AI is making a decision...")
            choice = ai_decision(player.total, dealer.hand[0])  # Use AI decision
            print(f"AI chose to: {'Hit' if choice == 'h' else 'Stand'}")
            if choice == 'h':
                player.add_card(deck.deal_card())
                print(player.show_hand())
                if player.total > 21:
                    print(f"{player.name} busts!")
                    break
            elif choice == 's':
                break

    # Dealer's turn
    print("\nDealer's turn:")
    print(dealer.show_hand(reveal=True))  # Show dealer's full hand
    while dealer.total < 17:
        dealer.add_card(deck.deal_card())
        print(dealer.show_hand(reveal=True))  # Show dealer's hand after each card is added

    # Determine winners
    print("\nFinal Results:")
    for player in players:
        if player.total > 21:
            print(f"{player.name} loses.")
        elif dealer.total > 21 or player.total > dealer.total:
            print(f"{player.name} wins!")
        elif player.total < dealer.total:
            print(f"{ player.name} loses.")
        else:
            print(f"{player.name} ties with the dealer.")

# Run the game with AI
if __name__ == "__main__":
    play_blackjack_with_ai()