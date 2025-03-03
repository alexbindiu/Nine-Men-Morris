from rich.console import Console
from src.domain.board import Board
from src.service.service import Service
from src.repository.repository import Repository

class MainUI:
    """
    MainUI class handles the user interface for the Nine Men's Morris game.
    It provides methods to display the game rules, menu, and start the game.
    """
    def __init__(self):
        self.__console = Console()
        self.__board = Board()


    @property
    def console(self):
        return self.__console


    @property
    def board(self):
        return self.__board


    def print_rules(self):
        """
        Prints the rules of Nine Men's Morris game to the console.
        """
        self.console.print("""
Nine Men's Morris is a strategy board game. 
Each player starts with nine pieces.
Players alternate placing a piece on a grid, aiming to form "mills" (three in a row). 
Forming a mill allows a player to remove an opponent's piece. 
After all pieces are placed, players move their pieces to adjacent spots. 
When reduced to three pieces, a player can "jump" to any empty spot. 
The game ends when a player has fewer than three pieces or cannot make a legal move.

If you want to add a piece or remove an opponent's piece, 
you must type its position, like "A2", "G7" etc.
If you want to move a piece, you must type the current position and the new position, 
like "A1 D1", "D3 E3" etc.

To exit the game, type "exit".

        """)


    def print_menu(self):
        """
        Prints the main menu options to the console.
        """
        self.console.print("\nPlease choose an option:")
        self.console.print("1. Play against another player")
        self.console.print("2. Play against the CPU")
        self.console.print("3. View the rules")
        self.console.print("4. Exit")


    def start(self):
        """
        Starts the main loop of the game, displaying the menu and handling user input.
        """
        self.console.print("Welcome to Nine Men's Morris!")

        while True:
            self.print_menu()
            option = self.console.input(">>> ")
            if option == "1":
                from src.ui.pvp_ui import PvpUI
                PvpUI(Service(Repository(), self.board), self.board, self.console).start()
            elif option == "2":
                from src.ui.pvcpu_ui import PvCpuUI
                PvCpuUI(Service(Repository(), self.board), self.board, self.console).start()
            elif option == "3":
                self.print_rules()
            elif option == "4":
                break
            else:
                self.console.print("Invalid option")