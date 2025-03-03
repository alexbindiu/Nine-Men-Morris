class Repository:
    """
    Initializes the Repository with default values.
    """
    def __init__(self):
        self.__list_of_men_1 = []
        self.__list_of_men_2 = []
        self.__remaining_pieces_1 = 9
        self.__remaining_pieces_2 = 9
        self.__turn = 1


    @property
    def list_of_men_1(self):
        return self.__list_of_men_1


    @property
    def list_of_men_2(self):
        return self.__list_of_men_2


    @property
    def remaining_pieces_1(self):
        return self.__remaining_pieces_1


    @property
    def remaining_pieces_2(self):
        return self.__remaining_pieces_2


    @property
    def turn(self):
        return self.__turn


    @list_of_men_1.setter
    def list_of_men_1(self, list_of_men):
        self.__list_of_men_1 = list_of_men


    @list_of_men_2.setter
    def list_of_men_2(self, list_of_men):
        self.__list_of_men_2 = list_of_men


    @remaining_pieces_1.setter
    def remaining_pieces_1(self, remaining_pieces):
        self.__remaining_pieces_1 = remaining_pieces


    @remaining_pieces_2.setter
    def remaining_pieces_2(self, remaining_pieces):
        self.__remaining_pieces_2 = remaining_pieces


    @turn.setter
    def turn(self, turn):
        self.__turn = turn


    def add_man_1(self, position):
        self.list_of_men_1.append(position)


    def add_man_2(self, position):
        self.list_of_men_2.append(position)


    def remove_man_1(self, position):
        self.list_of_men_1.remove(position)


    def remove_man_2(self, position):
        self.list_of_men_2.remove(position)


    def replace_man_1(self, old_position, new_position):
        self.remove_man_1(old_position)
        self.add_man_1(new_position)


    def replace_man_2(self, old_position, new_position):
        self.remove_man_2(old_position)
        self.add_man_2(new_position)


    def decrease_remaining_pieces_1(self):
        self.remaining_pieces_1 -= 1


    def decrease_remaining_pieces_2(self):
        self.remaining_pieces_2 -= 1


    def increase_remaining_pieces_1(self):
        self.remaining_pieces_1 += 1


    def increase_remaining_pieces_2(self):
        self.remaining_pieces_2 += 1


    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1