import os
from typing import List, Optional
from card import Card
from player import Player
from deck import Deck

# Game constants
NUM_PLAYERS = 2
HAND_SIZE = 3
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

class Game:
    """
    Represents the Truco game.
    """
    def __init__(self, player1: Player, player2: Player, initial_truco_value: int, winning_score: int):
        """
        Initializes a new instance of the Game class.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
            initial_truco_value (int): The initial Truco value.
            winning_score (int): The score required to win the game.
        """
        self.players = [player1, player2]
        self.deck = Deck()
        self.current_player = 0
        self.lead_player = 0
        self.table: List[Card] = []
        self.truco_value = initial_truco_value
        self.winning_score = winning_score
        self.envido_value = 0
        self.flor_value = 0
        self.round_number = 1
        self.scores = [0, 0]
        self.mazo_round = 1

    def clear_screen(self) -> None:
        """
        Clears the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_game_info(self) -> None:
        """
        Displays the current game information.
        """
        self.clear_screen()
        print("=== Truco Game ===")
        print(f"Round: {self.round_number}")
        print(f"Mazo Round: {self.mazo_round}")
        print(f"Scores: {self.players[0]}: {self.scores[0]} | {self.players[1]}: {self.scores[1]}")
        print(f"Truco Value: {self.truco_value}")
        print()

    def deal(self) -> None:
        """
        Deals cards to the players.
        """
        for _ in range(HAND_SIZE):
            for player in self.players:
                card = self.deck.draw()
                player.add_card(card)

    def play_card(self, card: Card) -> None:
        """
        Plays a card from the current player's hand to the table.
        """
        self.table.append(card)
        self.players[self.current_player].remove_card(card)

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
            rank1, rank2 = card1.rank, card2.rank
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

    def check_game_over(self, winner: int) -> bool:
        """
        Checks if the game is over based on the winning score.
        """
        if self.scores[winner] >= self.winning_score:
            raise GameOver(winner)
        return False

    def get_envido_points(self, player_index: int) -> int:
        """
        Calculates the Envido points for a player.
        """
        player_hand = self.players[player_index].hand
        envido_cards = [card for card in player_hand if card.rank in ["7", "6", "5", "4"]]
        if len(envido_cards) >= 2:
            envido_cards.sort(key=lambda card: card.rank)
            envido_ranks = [card.rank for card in envido_cards[:2]]
            envido_value = int(envido_ranks[0]) + int(envido_ranks[1]) + 20
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
            player.clear_hand()
        self.envido_value = 0
        self.flor_value = 0
        self.round_number += 1

    def reset_mazo(self) -> None:
        """
        Resets the Mazo round by shuffling the deck and resetting the round number.
        """
        self.deck.reset()
        self.round_number = 1
        self.mazo_round += 1

    def play_round(self) -> None:
        """
        Plays a single round of the game.
        """
        self.display_game_info()
        self.deal()

        while True:
            player = self.players[self.current_player]
            other_player = self.players[(self.current_player + 1) % NUM_PLAYERS]

            print(f"{player}'s turn")
            print("Hand:", " ".join(str(card) for card in player.hand))

            if self.truco_value == 1:
                truco_input = input(f"{player}, do you want to call Truco? (y/n): ").lower()
                if truco_input == "y":
                    self.truco_value = 2
                    print(f"\n{player} calls Truco!")
                    truco_response = input(f"{other_player}, do you accept Truco? (y/n/r): ").lower()
                    if truco_response == "n":
                        print(f"{other_player} declines Truco. {player} wins the round!")
                        self.update_scores(self.current_player)
                        self.reset_round()
                        return
                    elif truco_response == "r":
                        print(f"{other_player} calls Retruco!")
                        retruco_response = input(f"{player}, do you accept Retruco? (y/n/v): ").lower()
                        if retruco_response == "n":
                            print(f"{player} declines Retruco. {other_player} wins the round!")
                            self.update_scores((self.current_player + 1) % NUM_PLAYERS)
                            self.reset_round()
                            return
                        elif retruco_response == "v":
                            print(f"{player} calls Vale Cuatro!")
                            vale_cuatro_response = input(f"{other_player}, do you accept Vale Cuatro? (y/n): ").lower()
                            if vale_cuatro_response == "n":
                                print(f"{other_player} declines Vale Cuatro. {player} wins the round!")
                                self.update_scores(self.current_player)
                                self.reset_round()
                                return
                            else:
                                print(f"{other_player} accepts Vale Cuatro!")
                                self.truco_value = 4
                        else:
                            print(f"{player} accepts Retruco!")
                            self.truco_value = 3
            else:
                retruco_input = input(f"{player}, do you want to call Retruco? (y/n): ").lower()
                if retruco_input == "y":
                    print(f"\n{player} calls Retruco!")
                    retruco_response = input(f"{other_player}, do you accept Retruco? (y/n/v): ").lower()
                    if retruco_response == "n":
                        print(f"{other_player} declines Retruco. {player} wins the round!")
                        self.update_scores(self.current_player)
                        self.reset_round()
                        return
                    elif retruco_response == "v":
                        print(f"{other_player} calls Vale Cuatro!")
                        vale_cuatro_response = input(f"{player}, do you accept Vale Cuatro? (y/n): ").lower()
                        if vale_cuatro_response == "n":
                            print(f"{player} declines Vale Cuatro. {other_player} wins the round!")
                            self.update_scores((self.current_player + 1) % NUM_PLAYERS)
                            self.reset_round()
                            return
                        else:
                            print(f"{player} accepts Vale Cuatro!")
                            self.truco_value = 4
                    else:
                        print(f"{other_player} accepts Retruco!")
                        self.truco_value = 3

            envido_input = input(f"{player}, do you want to call Envido? (y/n): ").lower()
            if envido_input == "y":
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

            flor_input = input(f"{player}, do you want to call Flor? (y/n): ").lower()
            if flor_input == "y":
                player_flor_points = self.get_flor_points(self.current_player)
                if player_flor_points > 0:
                    print(f"\n{player} calls Flor!")
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

            resign_input = input(f"{player}, do you want to resign? (y/n): ").lower()
            if resign_input == "y":
                print(f"{player} resigns. {other_player} wins the round!")
                self.update_scores((self.current_player + 1) % NUM_PLAYERS)
                self.reset_round()
                return

            if player.hand:
                card_input = input(f"{player}, choose a card to play (e.g., 4♠) or press Enter to pass: ").strip()
                if card_input == "":
                    print(f"{player} passes.")
                else:
                    try:
                        rank, suit = card_input[:-1], card_input[-1]
                        card = Card(rank, suit)
                        if player.has_card(card):
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
                self.check_game_over(winner)
                self.reset_round()
                return

            self.next_player()

class GameOver(Exception):
    """
    Exception raised when the game is over.
    """
    def __init__(self, winner: int):
        self.winner = winner