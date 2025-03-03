import unittest
from src.repository.repository import Repository
from src.service.service import Service
from src.domain.board import Board

class TestRepository(unittest.TestCase):
    def test_initializing(self):
        repo = Repository()
        self.assertEqual(repo.list_of_men_1, [])
        self.assertEqual(repo.list_of_men_2, [])
        self.assertEqual(repo.remaining_pieces_1, 9)
        self.assertEqual(repo.remaining_pieces_2, 9)
        self.assertEqual(repo.turn, 1)

    def test_add_man_1(self):
        repo = Repository()
        repo.add_man_1((1, 1))
        self.assertIn((1, 1), repo.list_of_men_1)

    def test_add_man_2(self):
        repo = Repository()
        repo.add_man_2((2, 2))
        self.assertIn((2, 2), repo.list_of_men_2)

    def test_remove_man_1(self):
        repo = Repository()
        repo.add_man_1((1, 1))
        repo.remove_man_1((1, 1))
        self.assertNotIn((1, 1), repo.list_of_men_1)

    def test_remove_man_2(self):
        repo = Repository()
        repo.add_man_2((2, 2))
        repo.remove_man_2((2, 2))
        self.assertNotIn((2, 2), repo.list_of_men_2)

    def test_replace_man_1(self):
        repo = Repository()
        repo.add_man_1((1, 1))
        repo.replace_man_1((1, 1), (1, 2))
        self.assertNotIn((1, 1), repo.list_of_men_1)
        self.assertIn((1, 2), repo.list_of_men_1)

    def test_replace_man_2(self):
        repo = Repository()
        repo.add_man_2((2, 2))
        repo.replace_man_2((2, 2), (2, 3))
        self.assertNotIn((2, 2), repo.list_of_men_2)
        self.assertIn((2, 3), repo.list_of_men_2)

    def test_decrease_remaining_pieces_1(self):
        repo = Repository()
        repo.decrease_remaining_pieces_1()
        self.assertEqual(repo.remaining_pieces_1, 8)

    def test_decrease_remaining_pieces_2(self):
        repo = Repository()
        repo.decrease_remaining_pieces_2()
        self.assertEqual(repo.remaining_pieces_2, 8)

    def test_increase_remaining_pieces_1(self):
        repo = Repository()
        repo.decrease_remaining_pieces_1()
        repo.increase_remaining_pieces_1()
        self.assertEqual(repo.remaining_pieces_1, 9)

    def test_increase_remaining_pieces_2(self):
        repo = Repository()
        repo.decrease_remaining_pieces_2()
        repo.increase_remaining_pieces_2()
        self.assertEqual(repo.remaining_pieces_2, 9)

    def test_change_turn(self):
        repo = Repository()
        repo.change_turn()
        self.assertEqual(repo.turn, 2)
        repo.change_turn()
        self.assertEqual(repo.turn, 1)


class TestService(unittest.TestCase):

    def setUp(self):
        self.repository = Repository()
        self.board = Board()
        self.service = Service(self.repository, self.board)

    def test_adding(self):
        self.repository.remaining_pieces_1 = 1
        self.repository.list_of_men_1 = []
        self.repository.list_of_men_2 = []

        self.service.add_man_1('A1')

        self.assertIn('A1', self.repository.list_of_men_1)
        self.assertEqual(self.repository.remaining_pieces_1, 0)

    def test_adding_invalid(self):
        self.repository.remaining_pieces_1 = 1
        self.repository.list_of_men_1 = []
        self.repository.list_of_men_2 = []

        with self.assertRaises(ValueError):
            self.service.add_man_1('B1')

    def test_removing(self):
        self.repository.list_of_men_1 = ['A1']

        self.service.remove_man_1('A1')

        self.assertNotIn('A1', self.repository.list_of_men_1)

    def test_removing_from_invalid_position(self):
        self.repository.list_of_men_1 = ['A1']

        with self.assertRaises(ValueError):
            self.service.remove_man_1('B1')

    def test_replacing_piece(self):
        self.repository.remaining_pieces_1 = 0
        self.repository.list_of_men_1 = ['A1']

        self.service.replace_man_1('A1', 'A4')

        self.assertNotIn('A1', self.repository.list_of_men_1)
        self.assertIn('A4', self.repository.list_of_men_1)

    def test_replacing_to_invalid_position(self):
        self.repository.remaining_pieces_1 = 0
        self.repository.list_of_men_1 = ['A1']

        with self.assertRaises(ValueError):
            self.service.replace_man_1('A1', 'B1')

    def test_flying(self):
        self.repository.remaining_pieces_1 = 0
        self.repository.list_of_men_1 = ['A1', 'B2', 'A7']

        self.service.fly_man_1('A1', 'A4')

        self.assertNotIn('A1', self.repository.list_of_men_1)
        self.assertIn('A4', self.repository.list_of_men_1)

    def test_flying_to_invalid_position(self):
        self.repository.remaining_pieces_1 = 0
        self.repository.list_of_men_1 = ['A1', 'A4', 'A7']

        with self.assertRaises(ValueError):
            self.service.fly_man_1('A1', 'B1')

    def test_cpu_command(self):
        self.repository.remaining_pieces_1 = 0
        self.repository.remaining_pieces_2 = 0
        self.repository.list_of_men_2 = ['A1', 'A4', 'B2']

        best_command = self.service.cpu_command()

        self.assertEqual(best_command, ['B2', 'A7'])

    def test_minimax(self):
        self.repository.remaining_pieces_1 = 0
        self.repository.remaining_pieces_2 = 0
        self.repository.list_of_men_2 = ['A1', 'A4', 'A7']

        evaluation = self.service.minimax(2, True)

        self.assertIsInstance(evaluation, int)

    def test_check_mill_blocked(self):
        self.repository.list_of_men_1 = ['A1', 'A4']
        self.repository.list_of_men_2 = ['A7']

        result = self.service.check_mill_blocked('A7', self.repository.list_of_men_2)

        self.assertFalse(result)

    def test_player_can_create_mill(self):
        self.repository.remaining_pieces_1 = 1

        result = self.service.player_can_create_mill('A1', ['A1', 'A2', 'A3'])

        self.assertTrue(result)

    def test_generate_commands(self):
        self.repository.remaining_pieces_1 = 1
        self.repository.list_of_men_1 = ['A1']

        commands = self.service.generate_commands("Player")

        self.assertIn((None, 'A4'), commands)

    def test_apply_command(self):
        self.repository.remaining_pieces_1 = 1
        self.repository.list_of_men_1 = []

        self.service.apply_command((None, 'A1'), "Player")

        self.assertIn('A1', self.repository.list_of_men_1)

    def test_undo_command(self):
        self.repository.remaining_pieces_1 = 1
        self.repository.list_of_men_1 = ['A1']

        self.service.undo_command((None, 'A1'), "Player")

        self.assertNotIn('A1', self.repository.list_of_men_1)
        self.assertEqual(self.repository.remaining_pieces_1, 2)

    def test_cpu_remove_man(self):
        self.repository.list_of_men_1 = ['A1', 'A2', 'A3']

        best_piece = self.service.cpu_remove_man()

        self.assertEqual(best_piece, 'A1')

    def test_evaluate_board(self):
        self.repository.list_of_men_1 = ['A1', 'A2']
        self.repository.list_of_men_2 = ['A3']

        score = self.service.evaluate_board("Player", "CPU")

        self.assertIsInstance(score, int)

    def test_get_adjacent_positions(self):
        adjacent_positions = self.service.get_adjacent_positions('A1')

        self.assertIn('D1', adjacent_positions)


if __name__ == '__main__':
    unittest.main()