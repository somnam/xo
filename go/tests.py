"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Board
from common.models import Game

class BoardTest(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common']

    def test_create_board(self):
        print("")

        # CASE
        print("Create empty Board instance")
        board = Board()
        board.save()
        self.assertIsInstance(board, Board)
        self.assertEqual(board.size, "13x13")
        self.assertEqual(board.rows, 13)
        self.assertEqual(board.columns, 13)

        # CASE
        print("Create Board instance of defined size")
        board = Board(size="9x9")
        board.save()
        self.assertEqual(board.size, "9x9")
        self.assertEqual(board.rows, 9)
        self.assertEqual(board.columns, 9)

    def test_assing_board_to_game(self):
        print("")

        # CASE
        print("Create Board instance and assing to a Game")
        game = Game.objects.get(id=1)
        board = Board(game_id=game.id)
        board.save()
        self.assertIsInstance(board, Board)

        # CASE
        print("Get Game by Board id")
        self.assertIsInstance(board.game, Game)
        self.assertTrue(board.game.id, game.id)

        # CASE
        print("Get Board by Game id")
        self.assertIsInstance(game.board, Board)
        self.assertTrue(game.board.pk, board.pk)
