from typing import List, Tuple
import random
import argparse

# Card constants
RANKS = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
SUITS = ["♠", "♥", "♣", "♦"]

# Game constants
NUM_PLAYERS = 2
HAND_SIZE = 3
WINNING_SCORE = 12

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

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

class State:
    """
    Represents the current state of the game.
    """
    def __init__(self):
        self.hands: List[List[Card]] = [[] for _ in range(NUM_PLAYERS)]
        self.table: List[Card] = []
        self.current_player: int = 0
        self.scores: List[int] = [0] * NUM_PLAYERS
        self.winner: int = None
        self.lead_player: int = 0

    def deal_cards(self, deck: List[Card]) -> None:
        """
        Deals cards from the deck to the players' hands.
        """
        for _ in range(HAND_SIZE):
            for hand in self.hands:
                if deck:
                    hand.append(deck.pop())

    def play_card(self, card: Card) -> None:
        """
        Plays a card from the current player's hand to the table.
        """
        self.table.append(card)
        self.hands[self.current_player].remove(card)

    def get_valid_moves(self) -> List[Card]:
        """
        Returns the list of valid cards the current player can play.
        """
        return self.hands[self.current_player]

    def get_winner(self) -> int:
        """
        Determines the winner of the current trick.
        """
        if len(self.table) == NUM_PLAYERS:
            card1, card2 = self.table
            winner = 0 if RANKS.index(card1.rank) > RANKS.index(card2.rank) else 1
            self.lead_player = winner
            return winner
        return None

    def update_scores(self, winner: int) -> None:
        """
        Updates the scores based on the winner of the trick.
        """
        self.scores[winner] += 1
        if self.scores[winner] >= WINNING_SCORE:
            self.winner = winner

    def next_player(self) -> None:
        """
        Moves to the next player's turn.
        """
        self.current_player = (self.current_player + 1) % NUM_PLAYERS

    def reset_scores(self) -> None:
        """
        Resets the scores of both players to zero.
        """
        self.scores = [0] * NUM_PLAYERS

class Judger:
    """
    Manages the game flow and determines the winner.
    """
    def __init__(self, player1, player2):
        self.players = [player1, player2]

    def reset_game(self) -> State:
        """
        Resets the game state and deals cards to the players.
        """
        deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        random.shuffle(deck)
        state = State()
        state.deal_cards(deck)
        return state

    def play(self, state: State, debug: bool = False) -> int:
        """
        Plays the game until a winner is determined or the deck runs out of cards.
        """
        while state.winner is None:
            player = self.players[state.current_player]
            valid_moves = state.get_valid_moves()

            if not valid_moves:
                other_player = (state.current_player + 1) % NUM_PLAYERS
                other_valid_moves = state.hands[other_player]
                if not other_valid_moves:
                    state.winner = None
                    state.reset_scores()
                    break
                state.winner = other_player
                break

            card = player.act(state)
            state.play_card(card)
            if debug:
                print(f"Current player: {player.name}")
                print(f"{player.name} played {card}")
            winner = state.get_winner()
            if winner is not None:
                state.update_scores(winner)
                state.table.clear()
                state.current_player = state.lead_player
                state = self.reset_game()
            else:
                state.next_player()

        return state.winner

class Player:
    """
    Represents a player in the game.
    """
    def __init__(self, name: str):
        self.name = name

    def act(self, state: State) -> Card:
        """
        Selects a card to play based on the current state.
        """
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            raise ValueError(f"No valid moves available for {self.name}")
        return random.choice(valid_moves)

class HumanPlayer(Player):
    """
    Represents a human player who interacts through the console.
    """
    def act(self, state: State) -> Card:
        """
        Prompts the human player to select a card to play.
        """
        valid_moves = state.get_valid_moves()
        print(f"\n{self.name}'s turn")
        print("Hand:", ", ".join(str(card) for card in valid_moves))
        while True:
            card_str = input("Choose a card to play (e.g., 4♠): ").strip()
            if not card_str:
                print("Invalid input. Please enter a valid card (e.g., 4♠).")
                continue
            try:
                rank, suit = card_str[:-1], card_str[-1]
                card = Card(rank, suit)
                if card in valid_moves:
                    return card
            except (IndexError, ValueError):
                print("Invalid input. Please enter a valid card (e.g., 4♠).")
            print("Invalid card. Please choose a card from your hand.")

def test_game():
    """
    Runs a test game simulation with two AI players.
    """
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    judger = Judger(player1, player2)

    state = judger.reset_game()
    assert len(state.hands[0]) == HAND_SIZE
    assert len(state.hands[1]) == HAND_SIZE
    assert state.current_player == 0
    assert state.scores == [0, 0]
    assert state.winner is None

    winner = judger.play(state)
    assert winner in [0, 1, None]
    if winner is None:
        assert all(score == 0 for score in state.scores)
    else:
        assert max(state.scores) >= WINNING_SCORE

def play_game(debug: bool = False):
    """
    Starts an interactive game session with human players.
    """
    player1_name = input("Enter the name of Player 1: ")
    player2_name = input("Enter the name of Player 2: ")

    player1 = HumanPlayer(player1_name)
    player2 = HumanPlayer(player2_name)
    judger = Judger(player1, player2)

    state = judger.reset_game()
    print(f"\nGame started! {player1.name} vs {player2.name}")
    print(f"First to {WINNING_SCORE} points wins.")

    while state.winner is None:
        print(f"\nRound: {sum(state.scores) // 2 + 1}")
        print(f"Scores: {player1.name}: {state.scores[0]}, {player2.name}: {state.scores[1]}")
        winner = judger.play(state, debug=debug)
        if state.winner is None:
            state = judger.reset_game()

    if state.winner is None:
        print("\nGame ended in a tie!")
    else:
        print(f"\nGame over! {judger.players[winner].name} wins!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the Truco card game")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--test", action="store_true", help="Run test game with AI players")
    group.add_argument("--play", action="store_true", help="Start an interactive game session")

    args = parser.parse_args()

    if args.test:
        test_game()
    elif args.play:
        play_game(debug=args.debug)
    else:
        parser.print_help()