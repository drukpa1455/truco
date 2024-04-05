class Card:
    """
    Represents a playing card with a rank and a suit.
    """
    def __init__(self, rank: str, suit: str):
        """
        Initializes a new instance of the Card class.

        Args:
            rank (str): The rank of the card (e.g., "4", "5", "6", "7", "Q", "J", "K", "A", "2", "3").
            suit (str): The suit of the card (e.g., "♠", "♥", "♣", "♦").
        """
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        """
        Returns a string representation of the card.

        Returns:
            str: The string representation of the card in the format "rank+suit" (e.g., "4♠", "K♥").
        """
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the card object.

        Returns:
            str: The string representation of the card object in the format "Card('rank', 'suit')" (e.g., "Card('4', '♠')").
        """
        return f"Card('{self.rank}', '{self.suit}')"

    def __eq__(self, other: object) -> bool:
        """
        Compares the card with another object for equality.

        Args:
            other (object): The object to compare with the card.

        Returns:
            bool: True if the card is equal to the other object, False otherwise.
        """
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False