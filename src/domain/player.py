class Player:
    def __init__(self ):
        self.__nickname = ""
        self.__piece = ""
        self.__color = ""


    @property
    def nickname(self):
        return self.__nickname


    @property
    def piece(self):
        return self.__piece


    @property
    def color(self):
        return self.__color


    @nickname.setter
    def nickname(self, nickname):
        self.__nickname = nickname


    @piece.setter
    def piece(self, piece):
        self.__piece = piece


    @color.setter
    def color(self, color):
        self.__color = color