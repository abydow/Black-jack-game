# Black-jack-game
A python implementation of of the Black jack game

Sure! Here's a detailed **README.md** file explaining your Blackjack game Python code, including its classes and logic:

# Black-jack-game

A Python implementation of the classic Blackjack card game. This terminal-based game allows a player to play Blackjack against a computer dealer following the standard Blackjack rules.

## Overview

This project simulates a Blackjack game with standard rules:
- Player starts with 100 chips and can place bets.
- Cards are dealt from a shuffled deck.
- Player and dealer receive two initial cards.
- Player can "hit" (take a card) or "stand" (end turn).
- Dealer hits until reaching at least 17.
- Blackjack and bust scenarios are handled.
- Winnings and chips are updated accordingly.
- Player can play multiple rounds until they run out of chips or choose to quit.

## Code Structure and Classes

### 1. `Suit` (enum.Enum)

Represents the four suits in a deck of cards:

- HEARTS (♥️)
- DIAMONDS (♦️)
- CLUBS (♣️)
- SPADES (♠️)

### 2. `Rank` (enum.Enum)

Represents ranks of cards, each with an associated Blackjack value and symbol:

- Number cards: TWO (2), THREE (3), ..., TEN (10)
- Face cards: JACK (10), QUEEN (10), KING (10)
- ACE (11)

Provides properties:
- `rank_value` — numeric value used in Blackjack.
- `symbol` — the card's face symbol (e.g., "A" for Ace).

### 3. `Card`

Represents a single playing card:

- Has `suit` (Suit) and `rank` (Rank).
- String representation includes rank symbol and suit (e.g., "A of ♥️").
- Property `value` returns the numeric Blackjack value of the card.

### 4. `Deck`

Represents a deck of 52 playing cards:

- On initialization, creates a standard deck (all Suits × all Ranks).
- Methods:
  - `reset()` — resets and shuffles the deck.
  - `shuffle()` — shuffles the cards.
  - `deal()` — removes and returns the top card (or `None` if empty).
  - `cards_remaining()` — returns how many cards left.

### 5. `Hand`

Represents a hand of cards for a player or dealer:

- Stores a list of `Card` objects.
- Methods and properties:
  - `add_card(card)` — adds a new card.
  - `clear()` — clears the hand.
  - `get_value()` — computes the Blackjack hand value, adjusting Aces as 1 if value exceeds 21.
  - `is_blackjack()` — checks if the hand is a Blackjack (2 cards totaling 21).
  - `is_bust()` — checks if the hand value exceeds 21.
  - String representation of all cards in the hand.
  - Length returns number of cards.

### 6. `Player`

Represents a game player:

- Has a `name`, a `Hand`, a chip count (`chips`, starts at 100), and the current bet (`current_bet`).
- Methods:
  - `place_bet(amount)` — bet chips if sufficient funds, reduces chips by bet amount.
  - `win_bet(multiplier=1.0)` — adds winnings based on bet and multiplier (defaults to even money).
  - `lose_bet()` — resets current bet when player loses.
  - `push_bet()` — returns bet amount on a tie.
  - `can_bet(amount)` — checks if player has enough chips for the bet.
- String representation shows name, chips, hand, and current bet.

### 7. `Dealer` (inherits from Player)

Represents the dealer with extra rules:

- Named "Dealer".
- Method `should_hit()` returns `True` if hand value is less than 17 (dealer hits until total ≥ 17).
- Methods to display visible and hidden cards:
  - `show_hidden_card()` — shows the dealer's hidden card.
  - `show_visible_cards()` — shows the first card, hides the second.

### 8. `BlackjackGame`

Handles the flow of the Blackjack game:

- Maintains a `Deck`, a `Player`, and a `Dealer`.
- Manages the main game loop, rounds, bets, turns, and outcome determination.

Key methods:

- `start_new_game()` — starts the game, handles replay loop until no chips or player quits.
- `play_round()` — plays a full round: betting, dealing, player and dealer turns, winner determination.
- `setup_round()` — clears hands and reshuffles deck if cards run low.
- `place_bet()` — prompts player to enter a valid bet.
- `deal_initial_cards()` — deals two cards each to player and dealer.
- `show_initial_cards()` — displays player hand and dealer's visible card.
- `check_blackjack()` — checks for Blackjack immediately after dealing; resolves if found.
- `player_turn()` — allows the player to hit or stand until bust or stand.
- `dealer_turn()` — dealer hits following Blackjack dealer rules.
- `determine_winner()` — decides the round outcome, adjusting chips accordingly.

## How To Run

- Run the Python script directly.
- Use the console inputs to place bets, choose hit or stand.
- The game continues until chips run out or player chooses to quit.

Example:

```bash
python blackjack.py
```

## Gameplay Summary

- Players start with 100 chips.
- For each round, player places a bet.
- Two cards dealt each to player and dealer (dealer shows one card).
- Player chooses to hit or stand.
- Dealer hits until total is at least 17.
- Winner is decided by closest hand value ≤ 21.
- Bets are updated based on result.
- Player can choose to play again or quit.

## Additional Notes

- Aces adjust dynamically (counted as 11 or 1) to avoid busting.
- Blackjack pays out with a 3:2 multiplier.
- Push returns the player's bet without loss.
- Bad inputs are handled gracefully.


[1] https://github.com/abydow/Black-jack-game
