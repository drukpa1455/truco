# Truco RL

Let's create Reinforcement Learning implementations for [Truco](https://en.wikipedia.org/wiki/Truco)

## Truco Card Game

[Truco](https://en.wikipedia.org/wiki/Truco) is a popular card game originated in Argentina and enjoyed in various countries across South America. This project provides a Python implementation of the Truco game, allowing players to enjoy the game in a digital format.

## Features

- Basic gameplay mechanics of Truco
- Support for two players
- Interactive command-line interface
- Truco: Players can call "Truco" to raise the stakes and potentially win more points
- Envido: Players can bet on the strength of their hand based on the sum of the values of two cards of the same suit
- Flor: Players can bet on having three cards of the same suit
- Passing turns: Players can choose to pass their turn
- Mazo: If both players pass consecutively, a card is drawn from the deck to determine the winner of the round
- Separate scoring system for Truco, Envido, and Flor

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/truco.git
   ```

2. Navigate to the project directory:

   ```
   cd truco
   ```

To run the game in debug mode, use the following command:

```
python truco_simple.py --play --debug
```

To run the test game with AI players, use:

```
python truco_simple.py --test
```

To start an interactive game session without debug prints, use:

```
python truco_simple.py --play
```

### Usage

To start a game of Truco, run the following command:

```
python truco_full.py
```

Follow the on-screen prompts to enter the names of the players and play the game. The game will continue until one player reaches the winning score.

## Files

- `truco_full.py`: The complete implementation of the Truco game with all the features.
- `truco_simple.py`: A simplified version of the Truco game with basic gameplay mechanics.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the existing code style and conventions.

## License

This project is licensed under the [CC](LICENSE).

## Acknowledgements

- The Truco card game rules and mechanics are based on the traditional Argentinian version of the game.
- Special thanks to the contributors who have helped improve this project.

## Contact

For any questions or inquiries, find us @ https://discord.gg/spatiotemporalmesh