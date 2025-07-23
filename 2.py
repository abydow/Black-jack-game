import random
from enum import Enum
from typing import List, Optional

class Suit(Enum):
    HEARTS = "♥️"
    DIAMONDS = "♦️"
    CLUBS = "♣️"
    SPADES = "♠️"

class Rank(Enum):
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (10, "J")
    QUEEN = (10, "Q")
    KING = (10, "K")
    ACE = (11, "A")

    @property
    def rank_value(self):
        return self.value[0]

    @property
    def symbol(self):
        return self.value[1]

class Card:
    def __init__(self, suit: Suit, rank: 'Rank'):
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank.symbol} of {self.suit.value}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def value(self) -> int:
        return self.rank.rank_value
    
class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        "crete a new deck of fresh 52 cards"
        self.cards = []
        for suit in Suit:
            for r in Rank:
                self.cards.append(Card(suit, r))
        self.shuffle()

    def shuffle(self):
        "shuffle the deck of cards"
        random.shuffle(self.cards)

    def deal(self) -> Optional[Card]:

        "deal a card from the deck"
        if self.cards:
            return self.cards.pop()
        return None
    def cards_remaining(self) -> int:
        "return the number of cards remaining in the deck"
        return len(self.cards)
    
class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        "add a card to the hand"
        self.cards.append(card)

    def clear(self):
        "clear the hand"
        self.cards = []

    def get_value(self) -> int:
        "get the total value of the hand"
        value = 0
        aces = 0

        for card in self.cards:
            if card.rank == Rank.ACE:
                aces += 1
            value += card.value

        # Adjust for Aces(count Aces as 1 if total value exceeds 21)
        while value > 21 and aces>0:
            value -= 10 # count Ace as 1 instead of 11
            aces -= 1

        return value
    
    def is_blackjack(self) -> bool:
        "check if the hand is a blackjack"
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        "check if the hand is bust"
        return self.get_value() > 21
    
    def __str__(self) -> str:
        "return a string representation of the hand"
        return ' '.join(str(card) for card in self.cards) if self.cards else "Empty Hand"
    def __len__(self) -> int:
        "return the number of cards in the hand"
        return len(self.cards)
    
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()
        self.chips = 100  # Initialize chips for player
        self.current_bet = 0  # Initialize current bet

    def place_bet(self, amount: int) -> bool:
        "place a bet and return the bet amount"
        # In a real game, you would check if the player has enough money
        if amount <= self.chips:
            self.current_bet = amount
            self.chips -= amount
            return True
        return False
    
    def win_bet(self,multiplier: float = 1.0):
        "win the bet and add the bet amount to the player's chips"
        winnings = int(self.current_bet * (1+ multiplier))
        self.chips += winnings
        self.current_bet = 0

    def lose_bet(self):
        "lose the bet and reset the current bet"
        self.current_bet = 0

    def push_bet(self):
        "push the bet and return the bet amount to the player"
        self.chips += self.current_bet
        self.current_bet = 0

    def can_bet(self, amount: int) -> bool:
        "check if the player can place a bet"
        return amount <= self.chips
    def __str__(self) -> str:
        "return a string representation of the player"
        return f"{self.name} - Chips: {self.chips}, Hand: {self.hand}, Current Bet: {self.current_bet}"
    
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def should_hit(self) -> bool:
        "check if the dealer should hit based on the dealer's hand value"
        return self.hand.get_value() < 17
    
    def show_hidden_card(self) -> str:
        "return the dealer's hidden card if it exists"
        if len(self.hand.cards) >= 2:
            return f"Hidden Card: {self.hand.cards[1]}"
        return "No hidden card"
    
    def show_visible_cards(self) -> str:
        "return the dealer's visible cards"
        if self.hand.cards:
            return f"Visible Cards: {self.hand.cards[0]}[Hidden]"
        return "No cards"
    
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Dealer()
        self.game_over = False

    def start_new_game(self):
        "start a new game of blackjack"
        print("="*50)
        print("Starting a new game of Blackjack!")
        print("="*50)

        while self.player.chips > 0:
            self.play_round()

            if self.player.chips <= 0:
                print("You have no chips left! Game over.")
                break
            play_again = input("Do you want to play again? (y/n): ").strip().lower()
            if play_again != 'y':
                break

        print(f"Thanks for playing! Final chips: {self.player.chips}")

    def play_round(self):
        "play a round of blackjack"
        self.setup_round()

        if not self.place_bet():
            return
        self.deal_initial_cards()
        self.show_initial_cards()

        #check for blackjack
        if self.check_blackjack():
            return
        # Player's turn
        self.player_turn()
         
        if not self.player.hand.is_bust():
            # Dealer's turn
            self.dealer_turn()
        # Determine the winner
        self.determine_winner()

    def setup_round(self):
        """setup for a new round"""
        #clear hands
        self.player.hand.clear()
        self.dealer.hand.clear()

        #check if the deck needs to be reset
        if self.deck.cards_remaining() < 10:
            print("Deck is running low, reshuffling...")
            self.deck.reset()

    def place_bet(self) -> bool:
        """Handle bet placement"""
        print(f"\n you have {self.player.chips} chips.")

        while True:
            try:
                bet_amount = int(input("Enter your bet amount: "))
                if bet_amount <= 0:
                    print("Bet must be a positive integer.")
                    continue
                if self.player.can_bet(bet_amount):
                    self.player.place_bet(bet_amount)
                    print(f"You placed a bet of {bet_amount} chips.")
                    return True
                else:
                    print("You don't have enough chips to place that bet.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for the bet amount.")

    def deal_initial_cards(self):
        """Deal initial cards to player and dealer"""
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
    
    def show_initial_cards(self):
        """Show initial cards of player and dealer"""
        print(f"\n{self.player.name}'s Hand: {self.player.hand} (Value: {self.player.hand.get_value()})")
        print(f"{self.dealer.name}'s Hand: {self.dealer.show_visible_cards()} (Value: {self.dealer.hand.get_value()})")

    def check_blackjack(self)-> bool:
        """Check for blackjack"""
        player_bj = self.player.hand.is_blackjack()
        dealer_bj = self.dealer.hand.is_blackjack()

        if player_bj or dealer_bj:
            #reveal dealer's hand
            print(f"\n{self.dealer.name}'s Hand: {self.dealer.hand} (Value: {self.dealer.hand.get_value()})")

            if player_bj and dealer_bj:
                print("Both player and dealer have blackjack! It's a push.")
                self.player.push_bet()

            elif player_bj:
                print(f"{self.player.name} has a blackjack! You win {int(self.player.current_bet * 1.5)} chips.")
                self.player.win_bet(0.5)

            else:
                print(f"{self.dealer.name} has a blackjack! You lose your bet of {self.player.current_bet} chips.")
                self.player.lose_bet()

            return True
        return False
    def player_turn(self):
        """Handle player's turn"""
        while True:
            if self.player.hand.is_bust():
                print(f"{self.player.name}'s Hand: {self.player.hand} (Value: {self.player.hand.get_value()})")
                print("You busted! Dealer wins.")
                self.player.lose_bet()
                return
            action = input("Do you want to (h)it or (s)tand? ").strip().lower()

            if action == 'h':
                card = self.deck.deal()
                self.player.hand.add_card(card)
                print(f"{self.player.name} hits and draws {card}.\n Hand: {self.player.hand} (Value: {self.player.hand.get_value()})")
            elif action == 's':
                print(f"{self.player.name} stands with a hand value of {self.player.hand.get_value()}.")
                break
            else:
                print("Invalid action. Please enter 'h' to hit or 's' to stand.")

    def dealer_turn(self):
        """Handle dealer's turn"""
        print(f"\n{self.dealer.name}'s Turn:")
        
        while self.dealer.should_hit():
            card = self.deck.deal()
            self.dealer.hand.add_card(card)
            print(f"{self.dealer.name} hits and draws {card}.\n Hand: {self.dealer.hand} (Value: {self.dealer.hand.get_value()})")

        if self.dealer.hand.is_bust():
            print(f"{self.dealer.name} busted! {self.player.name} wins.")
            self.player.win_bet()
        else:
            print(f"{self.dealer.name} stands with a hand value of {self.dealer.hand.get_value()}.")

    def determine_winner(self):
        """Determine the winner of the round"""
        if self.player.hand.is_bust():
            return
        player_value = self.player.hand.get_value()
        dealer_value = self.dealer.hand.get_value()

        print(f"\nFinal Hands:\n{self.player.name}: {self.player.hand} (Value: {player_value})\n{self.dealer.name}: {self.dealer.hand} (Value: {dealer_value})")

        if self.dealer.hand.is_bust():
            print(f"{self.dealer.name} busted! {self.player.name} wins.")
            self.player.win_bet()

        elif player_value > dealer_value:
            print(f"{self.player.name} wins with a hand value of {player_value} against {self.dealer.name}'s {dealer_value}.")
            self.player.win_bet()
        
        elif player_value < dealer_value:
            print(f"{self.dealer.name} wins with a hand value of {dealer_value} against {self.player.name}'s {player_value}.")
            self.player.lose_bet()

        else:
            print(f"It's a push! Both {self.player.name} and {self.dealer.name} have a hand value of {player_value}.")
            self.player.push_bet()

        print(f"{self.player.name} now has {self.player.chips} chips.")

def main():
    """Main function to start the game"""
    game = BlackjackGame()
    game.start_new_game()

if __name__ == "__main__":
    main()

