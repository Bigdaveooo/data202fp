import random
import sqlite3
import csv

# Constants
NUM_DECKS = 6
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Card class
class Card:
    def __init__(self, rank):
        self.rank = rank

    def __str__(self):
        return self.rank

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(rank) for _ in range(NUM_DECKS) for rank in RANKS]
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

# Database setup
def setup_database():
    conn = sqlite3.connect('blackjack_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            player_hands TEXT,
            dealer_hand TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save results to the database
def save_results(player_hands, dealer_hand, result):
    conn = sqlite3.connect('blackjack_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (player_hands, dealer_hand, result)
        VALUES (?, ?, ?)
    ''', (player_hands, dealer_hand, result))
    conn.commit()
    conn.close()

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

    # Players' turn with AI
    for player in players:
        while True:
            choice = ai_decision(player.total, dealer.hand[0])  # Use AI decision
            if choice == 'h':
                player.add_card(deck.deal_card())
                if player.total > 21:
                    break
            elif choice == 's':
                break

    # Dealer's turn
    while dealer.total < 17:
        dealer.add_card(deck.deal_card())

    # Determine winners and prepare results
    results = []
    for player in players:
        if player.total > 21:
            results.append(f"{player.name} loses.")
        elif dealer.total > 21 or player.total > dealer.total:
            results.append(f"{player.name} wins!")
        elif player.total < dealer.total:
            results.append(f"{player .name} loses.")
        else:
            results.append(f"{player.name} ties with the dealer.")

    # Prepare data for saving
    player_hands = ', '.join(f"{player.name}: {', '.join(str(card) for card in player.hand)}" for player in players)
    dealer_hand = dealer.show_hand(reveal=True)
    result_summary = ', '.join(results)

    # Save results to the database
    save_results(player_hands, dealer_hand, result_summary)

# Export results to CSV
def export_to_csv(filename):
    conn = sqlite3.connect('blackjack_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM results')
    rows = cursor.fetchall()

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Player Hands', 'Dealer Hand', 'Result'])  # Header
        writer.writerows(rows)

    conn.close()

# Run the game multiple times
def run_multiple_games(num_games):
    setup_database()
    for _ in range(num_games):
        play_blackjack_with_ai()
    export_to_csv('blackjack_results.csv')  # Export results after running games

# Execute the program
if __name__ == "__main__":
    run_multiple_games(10000)