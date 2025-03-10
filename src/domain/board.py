class Board:
    def __init__(self):
        self.__positions = ["A1", "A4", "A7",
                            "B2", "B4", "B6",
                            "C3", "C4", "C5",
                            "D1", "D2", "D3", "D5", "D6", "D7",
                            "E3", "E4", "E5",
                            "F2", "F4", "F6",
                            "G1", "G4", "G7"]


        self.__moves = [["A1", "D1"], ["D1", "G1"],
                        ["B2", "D2"], ["D2", "F2"],
                        ["C3", "D3"], ["D3", "E3"],
                        ["A4", "B4"], ["B4", "C4"],
                        ["E4", "F4"], ["F4", "G4"],
                        ["C5", "D5"], ["D5", "E5"],
                        ["B6", "D6"], ["D6", "F6"],
                        ["A7", "D7"], ["D7", "G7"],
                        ["A1", "A4"], ["A4", "A7"],
                        ["B2", "B4"], ["B4", "B6"],
                        ["C3", "C4"], ["C4", "C5"],
                        ["D1", "D2"], ["D2", "D3"],
                        ["D5", "D6"], ["D6", "D7"],
                        ["E3", "E4"], ["E4", "E5"],
                        ["F2", "F4"], ["F4", "F6"],
                        ["G1", "G4"], ["G4", "G7"]]


        self.__mills = [["A1", "D1", "G1"], ["B2", "D2", "F2"],
                        ["C3", "D3", "E3"], ["C5", "D5", "E5"],
                        ["B6", "D6", "F6"], ["A7", "D7", "G7"],
                        ["A4", "B4", "C4"], ["E4", "F4", "G4"],
                        ["A1", "A4", "A7"], ["B2", "B4", "B6"],
                        ["C3", "C4", "C5"], ["E3", "E4", "E5"],
                        ["F2", "F4", "F6"], ["G1", "G4", "G7"],
                        ["D1", "D2", "D3"], ["D5", "D6", "D7"]]


        self.__base_table = """
   A      B      C        D        E      F      G
1  ○ ──────────────────── ○ ──────────────────── ○
   │                      │                      │
2  │      ○ ───────────── ○ ───────────── ○      │
   │      │               │               │      │
3  │      │      ○ ────── ○ ────── ○      │      │
   │      │      │                 │      │      │
   │      │      │                 │      │      │
4  ○ ──── ○ ──── ○                 ○ ──── ○ ──── ○
   │      │      │                 │      │      │
   │      │      │                 │      │      │
5  │      │      ○ ────── ○ ────── ○      │      │
   │      │               │               │      │
6  │      ○ ───────────── ○ ───────────── ○      │
   │                      │                      │
7  ○ ──────────────────── ○ ──────────────────── ○
"""

    @property
    def positions(self):
        return self.__positions


    @property
    def moves(self):
        return self.__moves


    @property
    def mills(self):
        return self.__mills


    @property
    def base_table(self):
        return self.__base_table