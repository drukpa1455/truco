from typing import List, Tuple
import random

# Card constants
RANKS = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
SUITS = ["♠", "♥", "♣", "♦"]

# Game constants
NUM_PLAYERS = 2
HAND_SIZE = 3
WINNING_SCORE = 12

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

class State:
    def __init__(self):
        self.hands: List[List[Card]] = [[] for _ in range(NUM_PLAYERS)]
        self.table: List[Card] = []
        self.current_player: int = 0
        self.scores: List[int] = [0] * NUM_PLAYERS
        self.winner: int = None

    def deal_cards(self, deck: List[Card]) -> None:
        for _ in range(HAND_SIZE):
            for player in range(NUM_PLAYERS):
                card = deck.pop()
                self.hands[player].append(card)

    def play_card(self, card: Card) -> None:
        self.table.append(card)
        self.hands[self.current_player].remove(card)

    def get_valid_moves(self) -> List[Card]:
        return self.hands[self.current_player]

    def get_winner(self) -> int:
        if len(self.table) == NUM_PLAYERS:
            card1, card2 = self.table
            if RANKS.index(card1.rank) > RANKS.index(card2.rank):
                return 0
            else:
                return 1
        return None

    def update_scores(self, winner: int) -> None:
        self.scores[winner] += 1
        if self.scores[winner] >= WINNING_SCORE:
            self.winner = winner

    def next_player(self) -> None:
        self.current_player = (self.current_player + 1) % NUM_PLAYERS

class Judger:
    def __init__(self, player1, player2):
        self.players = [player1, player2]

    def reset_game(self) -> State:
        deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        random.shuffle(deck)
        state = State()
        state.deal_cards(deck)
        return state

    def play(self, state: State) -> int:
        while state.winner is None:
            player = self.players[state.current_player]
            card = player.act(state)
            state.play_card(card)
            winner = state.get_winner()
            if winner is not None:
                state.update_scores(winner)
            state.next_player()
        return state.winner

class Player:
    def __init__(self, name: str):
        self.name = name

    def act(self, state: State) -> Card:
        valid_moves = state.get_valid_moves()
        card = random.choice(valid_moves)
        return card

class HumanPlayer(Player):
    def act(self, state: State) -> Card:
        valid_moves = state.get_valid_moves()
        print(f"\n{self.name}'s turn")
        print("Hand:", [str(card) for card in valid_moves])
        while True:
            try:
                card_str = input("Choose a card to play (e.g., 4♠): ")
                rank, suit = card_str[:-1], card_str[-1]
                card = Card(rank, suit)
                if card in valid_moves:
                    return card
                else:
                    print("Invalid card. Please choose a card from your hand.")
            except (IndexError, ValueError):
                print("Invalid input. Please enter a valid card (e.g., 4♠).")

def test_game():
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
    assert winner in [0, 1]
    assert state.scores[winner] >= WINNING_SCORE

def play_game():
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
        winner = judger.play(state)
        state = judger.reset_game()

    print(f"\nGame over! {judger.players[winner].name} wins!")

if __name__ == "__main__":
    test_game()
    play_game()
