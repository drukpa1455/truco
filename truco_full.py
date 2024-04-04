"""
Truco Game
==========

This module contains the implementation of the Truco card game, including the basic
gameplay mechanics and additional features such as Truco, Envido, Flor, and Mazo.

The game is designed to be played by two players, each starting with three cards.
The objective is to win the most rounds and reach a certain number of points.

Author: Drukpa Kunley
Date: 2024-04-04
"""

from typing import List, Tuple, Optional
import random

# Card constants
RANKS = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
SUITS = ["♠", "♥", "♣", "♦"]

# Game constants
NUM_PLAYERS = 2
HAND_SIZE = 3
WINNING_SCORE = 12
TRUCO_POINTS = 3
ENVIDO_POINTS = 2
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
        self.score = 0
        self.envido_score = 0
        self.flor_score = 0

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
        self.truco_accepted = False
        self.envido_called = False
        self.envido_accepted = False
        self.flor_called = False
        self.flor_accepted = False
        self.mazo_drawn = False

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
        if self.truco_accepted:
            self.players[winner].score += TRUCO_POINTS
        else:
            self.players[winner].score += 1

        if self.envido_accepted:
            envido_winner = self.get_envido_winner()
            self.players[envido_winner].envido_score += ENVIDO_POINTS

        if self.flor_accepted:
            flor_winner = self.get_flor_winner()
            self.players[flor_winner].flor_score += FLOR_POINTS

        if self.players[winner].score >= WINNING_SCORE:
            raise GameOver(winner)

    def get_envido_winner(self) -> int:
        """
        Determines the winner of the Envido.
        """
        envido_scores = [self.calculate_envido_score(player.hand) for player in self.players]
        if envido_scores[0] > envido_scores[1]:
            return 0
        elif envido_scores[1] > envido_scores[0]:
            return 1
        else:
            return None  # Tie

    def calculate_envido_score(self, hand: List[Card]) -> int:
        """
        Calculates the Envido score for a given hand.
        """
        suit_scores = {}
        for card in hand:
            if card.suit not in suit_scores:
                suit_scores[card.suit] = 0
            if card.rank in ["J", "Q", "K"]:
                suit_scores[card.suit] += 10
            elif card.rank == "A":
                suit_scores[card.suit] += 11
            elif card.rank in ["2", "3"]:
                suit_scores[card.suit] += int(card.rank)
        return max(suit_scores.values(), default=0)

    def get_flor_winner(self) -> Optional[int]:
        """
        Determines the winner of the Flor.
        """
        flor_scores = [self.calculate_flor_score(player.hand) for player in self.players]
        if flor_scores[0] > flor_scores[1]:
            return 0
        elif flor_scores[1] > flor_scores[0]:
            return 1
        else:
            return None  # Tie

    def calculate_flor_score(self, hand: List[Card]) -> int:
        """
        Calculates the Flor score for a given hand.
        """
        suits = [card.suit for card in hand]
        if len(set(suits)) == 1:
            return sum(RANKS.index(card.rank) for card in hand)
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
        self.truco_accepted = False
        self.envido_called = False
        self.envido_accepted = False
        self.flor_called = False
        self.flor_accepted = False
        self.mazo_drawn = False

    def play_round(self) -> None:
        """
        Plays a single round of the game.
        """
        self.deal()
        while True:
            player = self.players[self.current_player]
            print(f"\n{player}'s turn")
            print("Hand:", ", ".join(str(card) for card in player.hand))

            if not self.truco_called:
                truco_input = input("Do you want to call Truco? (y/n): ").lower()
                if truco_input == "y":
                    self.truco_called = True
                    other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]
                    print(f"\n{player} calls Truco!")
                    truco_response = input(f"{other_player}, do you accept Truco? (y/n): ").lower()
                    if truco_response == "y":
                        self.truco_accepted = True
                        print(f"{other_player} accepts Truco!")
                    else:
                        print(f"{other_player} declines Truco. {player} wins the round!")
                        self.update_scores(self.current_player)
                        self.reset_round()
                        self.current_player = self.lead_player
                        return

            if not self.envido_called:
                envido_input = input("Do you want to call Envido? (y/n): ").lower()
                if envido_input == "y":
                    self.envido_called = True
                    other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]
                    print(f"\n{player} calls Envido!")
                    envido_response = input(f"{other_player}, do you accept Envido? (y/n): ").lower()
                    if envido_response == "y":
                        self.envido_accepted = True
                        print(f"{other_player} accepts Envido!")
                    else:
                        print(f"{other_player} declines Envido. {player} wins the Envido!")
                        player.envido_score += ENVIDO_POINTS

            if not self.flor_called:
                flor_input = input("Do you want to call Flor? (y/n): ").lower()
                if flor_input == "y":
                    self.flor_called = True
                    other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]
                    print(f"\n{player} calls Flor!")
                    flor_response = input(f"{other_player}, do you accept Flor? (y/n): ").lower()
                    if flor_response == "y":
                        self.flor_accepted = True
                        print(f"{other_player} accepts Flor!")
                    else:
                        print(f"{other_player} declines Flor. {player} wins the Flor!")
                        player.flor_score += FLOR_POINTS

            if player.hand:
                card_input = input("Choose a card to play (e.g., 4♠) or pass (p): ").strip()
                if card_input == "p":
                    print(f"{player} passes.")
                    if self.mazo_drawn:
                        print("Both players passed. The round is a tie!")
                        self.reset_round()
                        return
                    self.mazo_drawn = True
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
                        print("Invalid input. Please enter a valid card (e.g., 4♠) or pass (p).")
                        continue

            winner = self.get_winner()
            if winner is not None:
                self.update_scores(winner)
                print(f"\nRound winner: {self.players[winner]}")
                self.reset_round()
                self.current_player = self.lead_player
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
                print("Final scores:")
                for player in self.players:
                    print(f"{player}: {player.score} points (Envido: {player.envido_score}, Flor: {player.flor_score})")
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