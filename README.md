# Truco RL
Reinforcement Learning implementations for [Truco](https://en.wikipedia.org/wiki/Truco)

## TODO
1. Implement the "Truco" feature: In the real game, players can call "Truco" to raise the stakes and potentially win more points. If a player calls "Truco" and the opponent accepts, the winner of that round gets 3 points instead of 1. If the opponent declines, the caller automatically wins 1 point.
2. Add the "Envido" feature: "Envido" is a separate game within Truco where players bet on the strength of their hand based on the sum of the values of two cards of the same suit. The player with the higher sum wins the "Envido" points.
3. Implement the "Flor" feature: "Flor" is another separate game within Truco where players bet on having three cards of the same suit. The player with the higher-ranking "Flor" wins the points.
4. Add the option for players to pass their turn: In the real game, players can choose to pass their turn if they don't want to play a card. The game continues with the next player.
5. Implement the "Mazo" feature: If both players pass their turn consecutively, the round is considered a draw, and the players have the option to draw a card from the "Mazo" (deck) to determine the winner of the round.
6. Add a scoring system for "Truco", "Envido", and "Flor": Implement a separate scoring system for these additional features, as they have different point values compared to the regular game.
7. Improve the user interface: You can enhance the user interface by displaying the current round, scores, and player's turn more prominently. You can also consider adding a visual representation of the cards on the table.

## truco.py
To run the game in debug mode, use the following command:
`python truco.py --play --debug`

To run the test game with AI players, use:
`python truco.py --test`

To start an interactive game session without debug prints, use:
`python truco.py --play`
