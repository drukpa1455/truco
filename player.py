from typing import List
from card import Card

class Player:
    """
    Represents a player in the game.
    """
    def __init__(self, name: str):
        """
        Initializes a new instance of the Player class.

        Args:
            name (str): The name of the player.
        """
        self.name = name
        self.hand: List[Card] = []

    def __str__(self) -> str:
        """
        Returns a string representation of the player.

        Returns:
            str: The name of the player.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Returns a string representation of the player object.

        Returns:
            str: The string representation of the player object in the format "Player('name')" (e.g., "Player('John')").
        """
        return f"Player('{self.name}')"

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the player's hand.

        Args:
            card (Card): The card to be added to the player's hand.
        """
        self.hand.append(card)

    def remove_card(self, card: Card) -> None:
        """
        Removes a card from the player's hand.

        Args:
            card (Card): The card to be removed from the player's hand.
        """
        self.hand.remove(card)

    def clear_hand(self) -> None:
        """
        Clears the player's hand by removing all cards.
        """
        self.hand.clear()

    def has_card(self, card: Card) -> bool:
        """
        Checks if the player has a specific card in their hand.

        Args:
            card (Card): The card to check for in the player's hand.

        Returns:
            bool: True if the player has the card in their hand, False otherwise.
        """
        return card in self.hand

    def get_hand_size(self) -> int:
        """
        Returns the number of cards in the player's hand.

        Returns:
            int: The number of cards in the player's hand.
        """
        return len(self.hand)