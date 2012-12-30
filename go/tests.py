"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from go.models import Board, Stone, STONE_COLORS
from common.models import Game

class BoardTest(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common']

    def test_add_board(self):
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

    def test_crate_stones(self):
        print("")

        # CASE
        print("Create black stones for 9x9 borad.")
        game  = Game.objects.get(id=1)
        user  = User.objects.get(id=1)
        board = Board(game_id=game.id, size="9x9")
        board.save()
        board.add_stones(user.id, STONE_COLORS['black'])
        self.assertEqual(board.stone_set.count(), 41)
        stone = board.stone_set.get(id=1)
        self.assertIsInstance(stone, Stone)
        self.assertEqual(stone.board, board)
        self.assertEqual(stone.user, user)
        self.assertEqual(stone.row, -1)
        self.assertEqual(stone.col, -1)
        self.assertEqual(stone.color, 0)

        # CASE
        print("Try appending black stones again to board.")
        board.add_stones(user.id, STONE_COLORS['black'])
        self.assertEqual(board.stone_set.count(), 41)

        # CASE
        print("Append white stones to 9x9 board.")
        user2 = User.objects.get(id=2)
        board.add_stones(user2.id, STONE_COLORS['white'])
        self.assertEqual(board.stone_set.count(), 81)
        stone = board.stone_set.get(id=42)
        self.assertIsInstance(stone, Stone)
        self.assertEqual(stone.board, board)
        self.assertEqual(stone.user, user2)
        self.assertEqual(stone.row, -1)
        self.assertEqual(stone.col, -1)
        self.assertEqual(stone.color, 1)

        # CASE 
        print("Try appending white stones again to board.")
        board.add_stones(user2.id, STONE_COLORS['white'])
        self.assertEqual(board.stone_set.count(), 81)
