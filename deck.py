import random
from typing import List
from card import Card

# Card constants
RANKS = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
SUITS = ["♠", "♥", "♣", "♦"]

class Deck:
    """
    Represents a deck of cards.
    """
    def __init__(self):
        """
        Initializes a new instance of the Deck class.
        """
        self.cards: List[Card] = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        self.shuffle()

    def __str__(self) -> str:
        """
        Returns a string representation of the deck.

        Returns:
            str: The string representation of the deck, showing the number of cards remaining.
        """
        return f"Deck: {len(self.cards)} cards remaining"

    def __repr__(self) -> str:
        """
        Returns a string representation of the deck object.

        Returns:
            str: The string representation of the deck object, showing the cards in the deck.
        """
        return f"Deck({self.cards})"

    def shuffle(self) -> None:
        """
        Shuffles the deck of cards.
        """
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """
        Draws a card from the deck.

        Returns:
            Card: The card drawn from the deck.

        Raises:
            IndexError: If the deck is empty.
        """
        if self.cards:
            return self.cards.pop()
        raise IndexError("Deck is empty")

    def is_empty(self) -> bool:
        """
        Checks if the deck is empty.

        Returns:
            bool: True if the deck is empty, False otherwise.
        """
        return len(self.cards) == 0

    def reset(self) -> None:
        """
        Resets the deck by recreating all the cards and shuffling them.
        """
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        self.shuffle()