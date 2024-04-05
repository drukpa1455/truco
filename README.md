# Truco RL

Let's create Reinforcement Learning implementations for [Truco](https://en.wikipedia.org/wiki/Truco)

## Truco Card Game

[Truco](https://en.wikipedia.org/wiki/Truco) is a popular card game originated in Argentina and enjoyed in various countries across South America. This project provides a Python implementation of the Truco game, allowing players to enjoy the game in a digital format.

## Features

- Basic gameplay mechanics of Truco
- Support for two players
- Interactive command-line interface
- Truco: Players can call "Truco" to raise the stakes and potentially win more points
- Retruco and Vale Cuatro: Players can further raise the stakes with "Retruco" and "Vale Cuatro" calls
- Envido: Players can bet on the strength of their hand based on the sum of the values of two cards of the same suit
- Flor: Players can bet on having three cards of the same suit
- Contra Flor al Resto: Players can counter the Flor bet with a higher Flor
- Passing turns: Players can choose to pass their turn
- Mazo: If both players pass consecutively, a card is drawn from the deck to determine the winner of the round
- Resign: Players can resign the game, declaring the opponent as the winner
- Replay: Players have the option to play another game after the current one ends
- Separate scoring system for Truco, Envido, and Flor

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

```git clone https://github.com/your-username/truco.git```

2. Navigate to the project directory:

```cd truco```

## Files

- `main.py`: The main game loop and user interaction.
- `game.py`: Contains the `Game` class and game-related constants.
- `player.py`: Contains the `Player` class.
- `deck.py`: Contains the `Deck` class.
- `card.py`: Contains the `Card` class.
- `truco_min.py`: A simplified version of the Truco game with basic gameplay mechanics in a single file.
- `truco_med.py`: A medium-complexity version of the Truco game with additional features in a single file.

### Usage

To start a game of Truco, run the following command:

```python main.py```

Follow the on-screen prompts to enter the names of the players, choose the game settings, and play the game. The game will continue until one player reaches the winning score or chooses to stop playing.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the existing code style and conventions.

## License

This project is licensed under the [CC](LICENSE).

## Acknowledgements

- The Truco card game rules and mechanics are based on the traditional Argentinian version of the game.
- Special thanks to the contributors who have helped improve this project.

## Contact

For any questions or inquiries, find us @ https://discord.gg/spatiotemporalmesh
