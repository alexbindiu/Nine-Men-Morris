import math

class Service:
    """
    Service class to manage the game, including adding, removing, replacing, and flying pieces.
    """
    def __init__(self, repository, board):
        self.__repository = repository
        self.__board = board


    @property
    def repository(self):
        return self.__repository


    @property
    def board(self):
        return self.__board


    def add_man_1(self, position):
        """
        Adds a piece for player 1 at the specified position.

        Args:
            position (str): The position to add the piece.

        Raises:
            ValueError: An error will appear if the position is invalid, not empty, or no pieces are left.
        """
        self.__check_adding(position, self.repository.remaining_pieces_1)
        self.repository.add_man_1(position)
        self.repository.decrease_remaining_pieces_1()


    def add_man_2(self, position):
        """
        Adds a piece for player 2 at the specified position.

        Args:
            position (str): The position to add the piece.

        Raises:
            ValueError: An error will appear if the position is invalid, not empty, or no pieces are left.
        """
        self.__check_adding(position, self.repository.remaining_pieces_2)
        self.repository.add_man_2(position)
        self.repository.decrease_remaining_pieces_2()


    def __check_adding(self, position, remaining_pieces):
        """
        Checks if a piece can be added at the specified position.

        Args:
            position (str): The position to check.
            remaining_pieces (int): The number of unplaced pieces.

        Raises:
            ValueError: An error will appear if the position is invalid, not empty, or no pieces are left.
        """
        if not self.check_position_exists(position):
            raise ValueError("Invalid position!")
        if not self.check_position_is_empty(position):
            raise ValueError("Position is not empty!")
        if remaining_pieces == 0:
            raise ValueError("No more pieces left!")


    def remove_man_1(self, position):
        """
        Removes a piece for player 1 from the specified position.

        Args:
            position (str): The position to remove the piece from.

        Raises:
            ValueError: An error will appear if the position is invalid, no piece is present, or the piece is part of a mill.
        """
        self.__check_removing(position, self.list_of_men_1())
        if self.check_mill_created(position, self.list_of_men_1()):
            if not self.check_player_can_destroy_mill(self.list_of_men_1()):
                raise ValueError("Can't remove a piece from a mill as long as there are other pieces!")
        self.repository.remove_man_1(position)


    def remove_man_2(self, position):
        """
        Removes a piece for player 2 from the specified position.

        Args:
            position (str): The position to remove the piece from.

        Raises:
            ValueError: An error will appear if the position is invalid, no piece is present, or the piece is part of a mill.
        """
        self.__check_removing(position, self.list_of_men_2())
        if self.check_mill_created(position, self.list_of_men_2()):
            if not self.check_player_can_destroy_mill(self.list_of_men_2()):
                raise ValueError("Can't remove a piece from a mill as long as there are other pieces!")
        self.repository.remove_man_2(position)


    def __check_removing(self, position, list_of_men):
        """
        Checks if a piece can be removed from the specified position.

        Args:
            position (str): The position to check.
            list_of_men (list): The list of already placed pieces for the player.

        Raises:
            ValueError: An error will appear if the position is invalid or no piece is present.
        """
        if not self.check_position_exists(position):
            raise ValueError("Invalid position!")
        if position not in list_of_men:
            raise ValueError("There is no piece of your opponent at this position!")


    def replace_man_1(self, old_position, new_position):
        """
        Moves a piece for player 1 from the current position to a new position.

        Args:
            old_position (str): The current position of the piece.
            new_position (str): The new position to move the piece to.

        Raises:
            ValueError: An error will appear if the move is not allowed.
        """
        self.__check_replacing(old_position, new_position, self.list_of_men_1(),
                               self.repository.remaining_pieces_1)

        self.repository.replace_man_1(old_position, new_position)


    def replace_man_2(self, old_position, new_position):
        """
        Moves a piece for player 2 from the current position to a new position.

        Args:
            old_position (str): The current position of the piece.
            new_position (str): The new position to move the piece to.

        Raises:
            ValueError: An error will appear if the move is not allowed.
        """
        self.__check_replacing(old_position, new_position, self.list_of_men_2(),
                               self.repository.remaining_pieces_2)

        self.repository.replace_man_2(old_position, new_position)


    def __check_replacing(self, old_position, new_position, list_of_men, remaining_pieces):
        """
        Checks if a piece can be moved from the current position to a new position.

        Args:
            old_position (str): The current position of the piece.
            new_position (str): The new position to move the piece to.
            list_of_men (list): The list of already placed pieces for the player.
            remaining_pieces (int): The number of unplaced pieces.

        Raises:
            ValueError: If the move is not allowed.
        """
        if remaining_pieces != 0:
            raise ValueError("You can't move yet!")
        if not self.check_position_exists(old_position):
            raise ValueError("First position doesn't exist!")
        if not self.check_position_exists(new_position):
            raise ValueError("Second position doesn't exist!")
        if old_position not in list_of_men:
            raise ValueError("No piece at first position!")
        if not self.check_position_is_empty(new_position):
            raise ValueError("Second position is not empty!")

    def fly_man_1(self, old_position, new_position):
        """
        Moves a piece for player 1 from the old position to the new position (flying).

        Args:
            old_position (str): The current position of the piece.
            new_position (str): The new position to move the piece to.

        Raises:
            ValueError: If the move is not allowed.
        """
        self.__check_flying(old_position, new_position, self.list_of_men_1(),
                            self.repository.remaining_pieces_1)

        self.repository.replace_man_1(old_position, new_position)


    def fly_man_2(self, old_position, new_position):
        """
        Moves a piece for player 2 from the old position to the new position (flying).

        Args:
            old_position (str): The current position of the piece.
            new_position (str): The new position to move the piece to.

        Raises:
            ValueError: If the move is not allowed.
        """
        self.__check_flying(old_position, new_position, self.list_of_men_2(),
                            self.repository.remaining_pieces_2)

        self.repository.replace_man_2(old_position, new_position)


    def __check_flying(self, old_position, new_position, list_of_men, remaining_pieces):
        """
        Checks if a piece can be moved from the old position to the new position (flying).

        Args:
            old_position (str): The current position of the piece.
            new_position (str): The new position to move the piece to.
            list_of_men (list): The list of already placed pieces for the player.
            remaining_pieces (int): The number of unplaced pieces.

        Raises:
            ValueError: If the move is not allowed.
        """
        if remaining_pieces != 0:
            raise ValueError("You can't fly yet!")
        if len(list_of_men) != 3:
            raise ValueError("You can't fly yet!")
        if not self.check_position_exists(old_position):
            raise ValueError("First position doesn't exist!")
        if not self.check_position_exists(new_position):
            raise ValueError("Second position doesn't exist!")
        if old_position not in list_of_men:
            raise ValueError("No piece at first position!")
        if not self.check_position_is_empty(new_position):
            raise ValueError("Second position is not empty!")


    def list_of_men_1(self):
        """
        Returns the list of already placed pieces for player 1.

        Returns:
            list: The list of already placed pieces for player 1.
        """
        return self.repository.list_of_men_1


    def list_of_men_2(self):
        """
      	Returns the list of already placed pieces for player 2.

        Returns:
            list: The list of already placed pieces for player 2.

        """
        return self.repository.list_of_men_2


    def check_position_exists(self, position):
        """
        Checks if the specified position exists on the board.

        Args:
            position (str): The position to check.

        Returns:
            bool: True if the position exists, False otherwise.
        """
        if position in self.board.positions:
            return True


    def check_position_is_empty(self, position):
        """
        Checks if the specified position is empty.

        Args:
            position (str): The position to check.

        Returns:
            bool: True if the position is empty, False otherwise.
        """
        if (position in self.list_of_men_1()
                or position in self.list_of_men_2()):
            return False
        return True


    def check_winner(self):
        """
        Checks if there is a winner.

        Returns:
            int: 1 if player 1 wins, 2 if player 2 wins, None otherwise.
        """
        if self.repository.remaining_pieces_1 == 0 and len(self.list_of_men_1()) <= 2:
            return 2
        if self.repository.remaining_pieces_2 == 0 and len(self.list_of_men_2()) <= 2:
            return 1


    def check_mill_created(self, position, list_of_men):
        """
        Checks if a mill is created with the piece placed at the specified position.

        Args:
            position (str): The position to check.
            list_of_men (list): The list of already placed pieces for the player.

        Returns:
            bool: True if a mill is created, False otherwise.
        """
        for mill in self.board.mills:
            if position in mill:
                for man in mill:
                    if man not in list_of_men:
                        break
                    elif man == mill[-1]:
                        return True
        return False


    def check_player_can_destroy_mill(self, list_of_men):
        """
        Checks if the player can destroy a mill.

        Args:
            list_of_men (list): The list of already placed pieces for the player.

        Returns:
            bool: True if the player can destroy a mill, False otherwise.
        """
        for mill in self.board.mills:
            founded = 0
            for man in mill:
                if man in list_of_men:
                    founded += 1

            if not founded == 3:
                return False
        return True


    def change_turn(self):
        """
        Changes whose player turn is next.
        """
        self.repository.change_turn()


    def cpu_command(self):
        """
        Determines the best command for the CPU to execute using the minimax algorithm.

        Returns:
            list: The best command for the CPU to execute.
        """
        depth = 3
        if len(self.list_of_men_2()) == 3:
            depth = 2

        is_maximizing = True
        best_score = -math.inf
        best_command = None

        possible_commands = self.generate_commands("CPU")

        for command in possible_commands:
            self.apply_command(command, "CPU")

            evaluation = self.minimax(depth - 1, not is_maximizing)
            if self.check_mill_created(command[1], self.list_of_men_2()):
                evaluation += 50
            if self.check_mill_blocked(command[1], self.list_of_men_1()):
                evaluation += 30

            self.undo_command(command, "CPU")

            if evaluation >= best_score:
                best_score = evaluation
                best_command = command

        if len(best_command) == 2:
            if best_command[0] is not None:
                return list(best_command)
            return [best_command[1]]


    def minimax(self, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        """
        Implements the minimax algorithm with alpha-beta pruning to evaluate the best move.

        Args:
            depth (int): The depth of the search tree.
            is_maximizing (bool): True if the current move is maximizing, False otherwise.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.

        Returns:
            float: The evaluation score of the board.
        """
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_board("CPU", "Player")

        if is_maximizing:
            max_eval = -math.inf
            possible_commands = self.generate_commands("CPU")

            for command in possible_commands:
                self.apply_command(command, "CPU")
                evaluation = self.minimax(depth - 1, not is_maximizing)
                self.undo_command(command, "CPU")

                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = math.inf
            possible_commands = self.generate_commands("Player")

            for command in possible_commands:
                self.apply_command(command, "Player")
                evaluation = self.minimax(depth - 1, not is_maximizing)
                self.undo_command(command, "Player")

                min_eval = min(min_eval, evaluation)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break

            return min_eval


    def check_mill_blocked(self, position, list_of_men):
        """
        Checks if a mill is blocked by a piece placed at the specified position.

        Args:
            position (str): The position to check.
            list_of_men (list): The list of already placed pieces for the player.

        Returns:
            bool: True if a mill is blocked, False otherwise.
        """
        for mill in self.board.mills:
            if position in mill:
                for man in mill:
                    if man != position and man not in list_of_men:
                        break
                    if man == mill[-1]:
                        if man != position and man not in list_of_men:
                            break
                        return True
        return False


    def player_can_create_mill(self, position, mill):
        """
        Checks if the player can create a mill placing a piece at the specified position.

        Args:
            position (str): The position to check.
            mill (list): The list of positions forming a mill.

        Returns:
            bool: True if the player can create a mill, False otherwise.
        """
        if self.repository.remaining_pieces_1:
            return True
        else:
            for move in self.board.moves:
                if position in move:
                    second_position = move[0] if position == move[1] else move[1]
                    if second_position in mill:
                        continue
                    if second_position in self.list_of_men_1():
                        return True

        return False


    def generate_commands(self, current_player):
        """
        Generates all possible commands for the current player.

        Args:
            current_player (str): The current player ("Player" or "CPU").

        Returns:
            list: A list of possible commands.
        """
        commands = []
        list_of_men = self.list_of_men_1() if current_player == "Player" else self.list_of_men_2()

        # Placement Phase
        if self.repository.remaining_pieces_1 > 0 or self.repository.remaining_pieces_2 > 0:
            for position in self.board.positions:
                if self.check_position_is_empty(position):
                    commands.append((None, position))

        # Movement Phase
        else:
            for old_position in list_of_men:
                for new_position in self.get_adjacent_positions(old_position):
                    if self.check_position_is_empty(new_position):
                        commands.append((old_position, new_position))

        # Flying Phase
        if len(list_of_men) == 3 and (self.repository.remaining_pieces_1 == 0 or self.repository.remaining_pieces_2 == 0):
            for old_position in list_of_men:
                for position in self.board.positions:
                    if self.check_position_is_empty(position):
                        commands.append((old_position, position))

        return commands


    def apply_command(self, command, player):
        """
        Applies the specified command for the given player.

        Args:
            command (tuple): The command to apply.
            player (str): The player executing the command ("Player" or "CPU").
        """
        old_position, new_position = command
        if old_position is None:
            # Placement phase
            self.add_man_1(new_position) if player == "Player" else self.add_man_2(new_position)
        else:
            # Moving or Flying phase
            if player == "Player":
                self.replace_man_1(old_position, new_position)
            else:
                self.replace_man_2(old_position, new_position)


    def undo_command(self, command, player):
        """
        Undoes the specified command for the given player.

        Args:
            command (tuple): The command to undo.
            player (str): The player executing the command ("Player" or "CPU").
        """
        old_position, new_position = command
        if old_position is None:
            # Placement phase
            self.repository.remove_man_1(new_position) if player == "Player" else self.repository.remove_man_2(new_position)
            self.repository.increase_remaining_pieces_1() if player == "Player" else self.repository.increase_remaining_pieces_2()
        else:
            # Moving or Flying phase
            if player == "Player":
                self.repository.replace_man_1(new_position, old_position)
            else:
                self.repository.replace_man_2(new_position, old_position)


    def cpu_remove_man(self):
        """
        Determines for the CPU the best piece to remove from the opponent.

        Returns:
            str: The position of the piece to remove.
        """
        list_of_men_opponent = self.list_of_men_1()
        best_score = -math.inf
        best_command = None

        for elem in list_of_men_opponent:
            if self.check_mill_created(elem, list_of_men_opponent):
                continue
            self.repository.remove_man_1(elem)
            score = self.evaluate_board("CPU", "Player")
            self.repository.add_man_1(elem)

            if score > best_score:
                best_score = score
                best_command = elem

        if best_command is None:
            for elem in list_of_men_opponent:
                self.repository.remove_man_1(elem)
                score = self.evaluate_board("CPU", "Player")
                self.repository.add_man_1(elem)

                if score > best_score:
                    best_score = score
                    best_command = elem

        return best_command


    def evaluate_board(self, current_player, opponent):
        """
        Evaluates the board and returns a score based on the current state.

        Args:
            current_player (str): The current player ("Player" or "CPU").
            opponent (str): The opponent player ("Player" or "CPU").

        Returns:
            int: The evaluation score of the board.
        """
        list_of_men_current = self.list_of_men_1() if current_player == "Player" else self.list_of_men_2()
        list_of_men_opponent = self.list_of_men_1() if opponent == "Player" else self.list_of_men_2()

        # Score components
        mills_formed = sum(1 for mill in self.board.mills if all(pos in list_of_men_current for pos in mill))
        mills_blocked = sum(1 for mill in self.board.mills if all(pos in list_of_men_opponent for pos in mill))

        # Heuristic: Favor mills formed, discourage mills blocked
        score = mills_formed * 10 - mills_blocked * 8

        # Mobility: Encourage having more options
        mobility = len(self.generate_commands(current_player))
        score += mobility

        return score


    def get_adjacent_positions(self, position):
        """
        Returns the adjacent positions for the specified position.

        Args:
            position (str): The position to get adjacent positions for.

        Returns:
            list: A list of adjacent positions.
        """
        adjacent_positions = []
        for move in self.board.moves:
            if position in move:
                adjacent = move[0] if position == move[1] else move[1]
                if self.check_position_exists(adjacent) and self.check_position_is_empty(adjacent):
                    adjacent_positions.append(adjacent)

        return adjacent_positions