from player import Player
from game import Game

def main() -> None:
    """
    Main function to start the game.
    """
    print("Welcome to Truco!")
    player1_name = input("Enter the name of Player 1: ")
    player2_name = input("Enter the name of Player 2: ")
    initial_truco_value = int(input("Enter the initial Truco value (default: 1): ") or 1)
    winning_score = int(input("Enter the winning score (default: 12): ") or 12)

    player1 = Player(player1_name)
    player2 = Player(player2_name)
    game = Game(player1, player2, initial_truco_value, winning_score)

    while True:
        try:
            game.play_round()
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting...")
            break
        except EOFError:
            print("\nGame interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break

        play_again = input("Do you want to play another round? (y/n): ").lower()
        if play_again != "y":
            break

        game.reset_mazo()

    print("Thanks for playing Truco!")

if __name__ == "__main__":
    main()