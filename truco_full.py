"""
Truco Game
==========

This module contains the implementation of the Truco card game, including the basic
gameplay mechanics and additional features such as Truco, Envido, and Flor.

The game is designed to be played by two players, each starting with three cards.
The objective is to win the most rounds and reach a certain number of points.

Author: Your Name
Date: YYYY-MM-DD
"""

from typing import List, Tuple, Optional
import random

# Card constants
RANKS = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
SUITS = ["♠", "♥", "♣", "♦"]

# Game constants
NUM_PLAYERS = 2
HAND_SIZE = 3
WINNING_SCORE = 30
TRUCO_POINTS = 2
ENVIDO_POINTS = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
    22: 22,
    23: 23,
    24: 24,
    25: 25,
    26: 26,
    27: 27,
    28: 28,
    29: 29,
    30: 30,
    31: 31,
    32: 32,
    33: 33
}
FLOR_POINTS = 3

class Card:
    """
    Represents a playing card with a rank and a suit.
    """
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"Card('{self.rank}', '{self.suit}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False

class Player:
    """
    Represents a player in the game.
    """
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Player('{self.name}')"

class Deck:
    """
    Represents a deck of cards.
    """
    def __init__(self):
        self.cards: List[Card] = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffles the deck of cards.
        """
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """
        Draws a card from the deck.
        """
        if self.cards:
            return self.cards.pop()
        raise IndexError("Deck is empty")

class Game:
    """
    Represents the Truco game.
    """
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.deck = Deck()
        self.current_player = 0
        self.lead_player = 0
        self.table: List[Card] = []
        self.truco_called = False
        self.truco_value = 1
        self.envido_called = False
        self.envido_value = 0
        self.flor_called = False
        self.flor_value = 0
        self.round_number = 1
        self.scores = [0, 0]

    def deal(self) -> None:
        """
        Deals cards to the players.
        """
        for player in self.players:
            player.hand = [self.deck.draw() for _ in range(HAND_SIZE)]

    def play_card(self, card: Card) -> None:
        """
        Plays a card from the current player's hand to the table.
        """
        self.table.append(card)
        self.players[self.current_player].hand.remove(card)

    def get_valid_moves(self) -> List[Card]:
        """
        Returns the list of valid cards the current player can play.
        """
        return self.players[self.current_player].hand

    def get_winner(self) -> Optional[int]:
        """
        Determines the winner of the current round.
        """
        if len(self.table) == NUM_PLAYERS:
            card1, card2 = self.table
            rank1, rank2 = RANKS.index(card1.rank), RANKS.index(card2.rank)
            if rank1 > rank2:
                winner = 0
            elif rank2 > rank1:
                winner = 1
            else:
                winner = None  # Tie
            self.lead_player = winner if winner is not None else self.lead_player
            return winner
        return None

    def update_scores(self, winner: int) -> None:
        """
        Updates the scores based on the winner of the round.
        """
        self.scores[winner] += self.truco_value
        self.scores[winner] += self.envido_value
        self.scores[winner] += self.flor_value

        if self.scores[winner] >= WINNING_SCORE:
            raise GameOver(winner)

    def get_envido_points(self, player_index: int) -> int:
        """
        Calculates the Envido points for a player.
        """
        player_hand = self.players[player_index].hand
        envido_cards = [card for card in player_hand if card.rank in ["7", "6", "5", "4"]]
        if len(envido_cards) >= 2:
            envido_cards.sort(key=lambda card: RANKS.index(card.rank))
            envido_ranks = [RANKS.index(card.rank) for card in envido_cards[:2]]
            envido_value = sum(envido_ranks) + 20
            return ENVIDO_POINTS.get(envido_value, 0)
        return 0

    def get_flor_points(self, player_index: int) -> int:
        """
        Calculates the Flor points for a player.
        """
        player_hand = self.players[player_index].hand
        suits = set(card.suit for card in player_hand)
        if len(suits) == 1:
            return FLOR_POINTS
        return 0

    def next_player(self) -> None:
        """
        Moves to the next player's turn.
        """
        self.current_player = (self.current_player + 1) % NUM_PLAYERS

    def reset_round(self) -> None:
        """
        Resets the round by clearing the table and resetting the player's hands.
        """
        self.table.clear()
        for player in self.players:
            player.hand.clear()
        self.truco_called = False
        self.truco_value = 1
        self.envido_called = False
        self.envido_value = 0
        self.flor_called = False
        self.flor_value = 0
        self.round_number += 1

    def play_round(self) -> None:
        """
        Plays a single round of the game.
        """
        print(f"\nRound {self.round_number}")
        self.deal()
        while True:
            player = self.players[self.current_player]
            print(f"\n{player}'s turn")
            print("Hand:", ", ".join(str(card) for card in player.hand))
            print(f"Scores: {self.players[0]}: {self.scores[0]} | {self.players[1]}: {self.scores[1]}")

            if not self.truco_called:
                truco_input = input("Do you want to call Truco? (y/n): ").lower()
                if truco_input == "y":
                    self.truco_called = True
                    self.truco_value = TRUCO_POINTS
                    other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]
                    print(f"\n{player} calls Truco!")
                    truco_response = input(f"{other_player}, do you accept Truco? (y/n): ").lower()
                    if truco_response == "n":
                        print(f"{other_player} declines Truco. {player} wins the round!")
                        self.update_scores(self.current_player)
                        self.reset_round()
                        return

            if not self.envido_called:
                envido_input = input("Do you want to call Envido? (y/n): ").lower()
                if envido_input == "y":
                    self.envido_called = True
                    other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]
                    print(f"\n{player} calls Envido!")
                    envido_response = input(f"{other_player}, do you accept Envido? (y/n): ").lower()
                    if envido_response == "y":
                        player_envido_points = self.get_envido_points(self.current_player)
                        other_player_envido_points = self.get_envido_points((self.current_player + 1) % NUM_PLAYERS)
                        if player_envido_points > other_player_envido_points:
                            print(f"{player} wins the Envido!")
                            self.envido_value = player_envido_points
                        elif other_player_envido_points > player_envido_points:
                            print(f"{other_player} wins the Envido!")
                            self.envido_value = other_player_envido_points
                        else:
                            print("Envido is a tie!")
                    else:
                        print(f"{other_player} declines Envido.")

            if not self.flor_called:
                flor_input = input("Do you want to call Flor? (y/n): ").lower()
                if flor_input == "y":
                    self.flor_called = True
                    player_flor_points = self.get_flor_points(self.current_player)
                    if player_flor_points > 0:
                        print(f"\n{player} calls Flor!")
                        other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]
                        flor_response = input(f"{other_player}, do you accept Flor? (y/n): ").lower()
                        if flor_response == "y":
                            other_player_flor_points = self.get_flor_points((self.current_player + 1) % NUM_PLAYERS)
                            if player_flor_points > other_player_flor_points:
                                print(f"{player} wins the Flor!")
                                self.flor_value = player_flor_points
                            elif other_player_flor_points > player_flor_points:
                                print(f"{other_player} wins the Flor!")
                                self.flor_value = other_player_flor_points
                            else:
                                print("Flor is a tie!")
                        else:
                            print(f"{other_player} declines Flor.")
                    else:
                        print(f"{player} doesn't have a valid Flor.")

            if player.hand:
                card_input = input("Choose a card to play (e.g., 4♠) or press Enter to pass: ").strip()
                if card_input == "":
                    print(f"{player} passes.")
                else:
                    try:
                        rank, suit = card_input[:-1], card_input[-1]
                        card = Card(rank, suit)
                        if card in player.hand:
                            self.play_card(card)
                            print(f"{player} plays {card}")
                        else:
                            print("Invalid card. Please choose a card from your hand.")
                            continue
                    except (IndexError, ValueError):
                        print("Invalid input. Please enter a valid card (e.g., 4♠) or press Enter to pass.")
                        continue

            winner = self.get_winner()
            if winner is not None:
                self.update_scores(winner)
                print(f"\nRound winner: {self.players[winner]}")
                self.reset_round()
                return

            self.next_player()

    def play(self) -> None:
        """
        Plays the game until a winner is determined.
        """
        while True:
            try:
                self.play_round()
            except GameOver as e:
                print(f"\nGame over! {self.players[e.winner]} wins!")
                print(f"Final scores: {self.players[0]}: {self.scores[0]} | {self.players[1]}: {self.scores[1]}")
                break

class GameOver(Exception):
    """
    Exception raised when the game is over.
    """
    def __init__(self, winner: int):
        self.winner = winner

def main() -> None:
    """
    Main function to start the game.
    """
    print("Welcome to Truco!")
    player1_name = input("Enter the name of Player 1: ")
    player2_name = input("Enter the name of Player 2: ")

    player1 = Player(player1_name)
    player2 = Player(player2_name)

    game = Game(player1, player2)
    game.play()

if __name__ == "__main__":
    main()