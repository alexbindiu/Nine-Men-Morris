from src.domain.player import Player
import time

class PvCpuUI:
    """
    User interface class for Player vs CPU mode in Nine Men's Morris game.
    """

    def __init__(self, service, board, console):
        self.__board = board
        self.__console = console
        self.__player = Player()
        self.__cpu = Player()
        self.__service = service


    @property
    def board(self):
        return self.__board


    @property
    def console(self):
        return self.__console


    @property
    def player(self):
        return self.__player


    @property
    def cpu(self):
        return self.__cpu


    @property
    def service(self):
        return self.__service


    def print_rules(self):
        """
        Print the game rules to the console.
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


    def read_name(self):
        """
        Read the player's name and assign pieces and colors.
        """
        self.player.nickname = self.console.input("Enter player's nickname: ")
        self.player.piece = "▲"
        self.player.color = "red"
        self.console.print("Great! Your piece is [red]▲[/red]")

        self.cpu.nickname = "CPU"
        self.cpu.piece = "●"
        self.cpu.color = "blue"


    def start(self):
        """
        Start the game and handle the main game loop.
        """
        self.read_name()
        self.console.print("Here is the board:")
        while True:
            if self.check_winner():
                break

            self.print_board(self.board)

            if self.service.repository.turn == 1:
                command = self.read_command()
            else:
                self.cpu_thinking()
                command = self.service.cpu_command()

            if len(command) < 1:
                self.console.print("Invalid command!\n")
                self.print_rules()
                continue

            if command[0] == "EXIT":
                break

            for place in command:
                if place not in self.board.positions:
                    self.console.print("Invalid position!\n")
                    self.print_rules()
                    continue

            if len(command) == 1:
                self.add_man(command[0])
            elif len(command) == 2:
                if command in self.board.moves or command[::-1] in self.board.moves:
                    self.move_man(command[0], command[1])
                else:
                    self.fly(command[0], command[1])


    def cpu_thinking(self):
        """
        Simulate CPU thinking time.
        """
        time.sleep(0.5)
        self.console.print("\nCPU is thinking...\n")
        time.sleep(0.5)


    def check_winner(self):
        """
        Check if there is a winner.

        :return: True if there is a winner, False otherwise.
        """
        winner = self.service.check_winner()
        if winner == 1:
            self.console.print(f"Congratulations, {self.player.nickname}! You won!")
            return True
        elif winner == 2:
            self.console.print(f"Better luck next time, CPU won!")
            return True


    def add_man(self, position):
        """
        Add a piece to the board.

        :param position: The position to add the piece.
        """
        try:
            if self.service.repository.turn == 1:
                self.service.add_man_1(position)
                self.console.print("You added the piece!")
                if self.service.check_mill_created(position, self.service.list_of_men_1()):
                    self.remove_man()
            else:
                self.service.add_man_2(position)
                self.console.print(f"I added a piece at {position}!")
                if self.service.check_mill_created(position, self.service.list_of_men_2()):
                    self.remove_man()

            self.service.repository.change_turn()
        except ValueError as ve:
            self.console.print(ve)


    def move_man(self, old_position, new_position):
        """
        Move a piece on the board.

        :param old_position: The current position of the piece.
        :param new_position: The new position of the piece.
        """
        try:
            if self.service.repository.turn == 1:
                self.service.replace_man_1(old_position, new_position)
                self.console.print("You moved the piece!")
                if self.service.check_mill_created(new_position, self.service.list_of_men_1()):
                    self.remove_man()
            else:
                self.service.replace_man_2(old_position, new_position)
                self.console.print(f"I moved the piece from {old_position} to {new_position}!")
                if self.service.check_mill_created(new_position, self.service.list_of_men_2()):
                    self.remove_man()

            self.service.repository.change_turn()
        except ValueError as ve:
            self.console.print(ve)


    def fly(self, old_position, new_position):
        """
        Move a piece to any empty spot when the player has only three pieces left.

        :param old_position: The current position of the piece.
        :param new_position: The new position of the piece.
        """
        try:
            if self.service.repository.turn == 1:
                self.service.fly_man_1(old_position, new_position)
                self.console.print("You moved the piece!")
                if self.service.check_mill_created(new_position, self.service.list_of_men_1()):
                    self.remove_man()
            else:
                self.service.fly_man_2(old_position, new_position)
                self.console.print(f"I moved the piece from {old_position} to {new_position}!")
                if self.service.check_mill_created(new_position, self.service.list_of_men_2()):
                    self.remove_man()

            self.service.repository.change_turn()
        except ValueError as ve:
            self.console.print(ve)


    def remove_man(self):
        """
        Remove a piece from the board.
        """
        self.print_board(self.board)
        try:
            if self.service.repository.turn == 1:
                position = (self.console.input("Enter the position of the piece you want to remove: \n>>>")
                            .upper().strip())
                self.service.remove_man_2(position)
                self.console.print("You removed the piece!")
            else:
                self.cpu_thinking()
                position = self.service.cpu_remove_man()
                self.service.remove_man_1(position)
                self.console.print(f"I removed the piece from {position}!")

        except ValueError as ve:
            self.console.print(ve)
            self.remove_man()


    def read_command(self):
        """
        Read the player's command.

        :return: The command as a list of strings.
        """
        command = self.console.input(f"{self.player.nickname}'s turn: \n>>> ")
        command = command.upper().strip()
        command = list(filter(lambda x: x != "", command.split(" ")))

        return command


    def print_board(self, board):
        """
        Print the game board to the console.

        :param board: The game board.
        """
        board = board.base_table
        list_of_men_1 = self.service.list_of_men_1()
        list_of_men_2 = self.service.list_of_men_2()

        lines = board.splitlines()
        current_row_as_index = 0

        lines[1] = "[bright_cyan]" + lines[1] + "[/bright_cyan]"

        for i in range(len(lines)):
            line = list(lines[i])

            if "○" in line:
                current_row_as_index += 1

            places_on_row = []
            for place in self.board.positions:
                if str(current_row_as_index) in place:
                    places_on_row.append(place)
            places_on_row = sorted(places_on_row, key=lambda x: list(x)[0], reverse=False)

            for j in range(len(line) -1, -1, -1):
                if line[j] == "○":
                    if places_on_row:
                        place = places_on_row.pop()

                        if place in list_of_men_1:
                            line[j] = f"[{self.player.color}]{self.player.piece}[/{self.player.color}]"
                        elif place in list_of_men_2:
                            line[j] = f"[{self.cpu.color}]{self.cpu.piece}[/{self.cpu.color}]"

            lines[i] = "".join(line)

        board = "\n".join(lines)
        self.console.print(board)