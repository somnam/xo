from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from go.models import Board, Stone, STONE_COLORS
from common.models import Game

class BoardTest(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common']

    def test_CreateBoard_CreatesInstance(self):
        "Creating empty Board instance"

        board = Board()
        board.save()
        self.assertIsInstance(board, Board)
        self.assertEqual(board.size, "13x13")
        self.assertEqual(board.rows, 13)
        self.assertEqual(board.columns, 13)

    def test_CreateBoard_CreatesDefinedSizeInstance(self):
        "Creating Board instance of defined size"

        board = Board(size="9x9")
        board.save()
        self.assertEqual(board.size, "9x9")
        self.assertEqual(board.rows, 9)
        self.assertEqual(board.columns, 9)

    def test_AssingBoardToGame_Assigns(self):
        "Creating Board instance and assing to a Game"

        # Create and assing
        game = Game.objects.get(id=1)
        board = Board(game_id=game.id)
        board.save()

        # Check instance
        self.assertIsInstance(board, Board)

        # Get Game by Board id
        self.assertIsInstance(board.game, Game)
        self.assertTrue(board.game.id, game.id)

        # Get Board by Game id
        self.assertIsInstance(game.board, Board)
        self.assertTrue(game.board.pk, board.pk)

    def test_CreateBlackStonesForBoard_Creates(self):
        "Creating black stones for 9x9 borad."

        # Create black stones for borad
        board = Board(game_id=1, size="9x9")
        board.save()
        user = User.objects.get(id=1)
        board.add_stones(user.id, STONE_COLORS['black'])

        # Check stones count
        self.assertEqual(board.stone_set.count(), 41)

        # Check stone properties
        stone = board.stone_set.get(id=1)
        self.assertIsInstance(stone, Stone)
        self.assertEqual(stone.board, board)
        self.assertEqual(stone.user, user)
        self.assertEqual(stone.row, -1)
        self.assertEqual(stone.col, -1)
        self.assertEqual(stone.color, 0)

    def test_AppendBlackStonesToBoard_DoesNotAppend(self):
        "Appending black stones twice to board."

        # Create black stones twice for borad
        board = Board(game_id=1, size="9x9")
        board.save()
        user = User.objects.get(id=1)
        board.add_stones(user.id, STONE_COLORS['black'])
        board.add_stones(user.id, STONE_COLORS['black'])

        # Check stones count
        self.assertEqual(board.stone_set.count(), 41)

    def test_AppendWhiteStonesToBoard_Appends(self):
        "Appending white stones to 9x9 board."

        # Add black and white stones to board
        board = Board(game_id=1, size="9x9")
        board.save()
        user = User.objects.get(id=1)
        board.add_stones(user.id, STONE_COLORS['black'])
        user2 = User.objects.get(id=2)
        board.add_stones(user2.id, STONE_COLORS['white'])

        # Check stones count
        self.assertEqual(board.stone_set.count(), 81)

        # Check stone properties
        stone = board.stone_set.get(id=42)
        self.assertIsInstance(stone, Stone)
        self.assertEqual(stone.board, board)
        self.assertEqual(stone.user, user2)
        self.assertEqual(stone.row, -1)
        self.assertEqual(stone.col, -1)
        self.assertEqual(stone.color, 1)

    def test_AppendWhiteStonesToBoard_DoesNotAppend(self):
        "Appending white stones twice to board."

        # Add black and white stones to board
        board = Board(game_id=1, size="9x9")
        board.save()
        user = User.objects.get(id=1)
        board.add_stones(user.id, STONE_COLORS['black'])
        user2 = User.objects.get(id=2)
        board.add_stones(user2.id, STONE_COLORS['white'])

        # Add white stones for second time
        board.add_stones(user2.id, STONE_COLORS['white'])

        # Check stones count
        self.assertEqual(board.stone_set.count(), 81)

class BoardTestWithGoFixture(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common', 'go']

    def test_GetLatestPlacedStoneColorCode_GetColorForEmptyBoard_ReturnsColorCode(self):
        "Get color code of latest placed stone for empty board."

        board = Board()
        board.save()
        self.assertEqual(board.get_latest_placed_stone_color_code(), 1)

    def test_GetLatestPlacedStoneColorCode_GetColor_ReturnsColorCode(self):
        "Get color code of latest placed stone."

        board = Board(game_id=1, size="9x9")
        self.assertEqual(board.get_latest_placed_stone_color_code(), 1)

class StoneTest(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common', 'go']

    def test_AddStone_CreatesInstance(self):
        "Creating stone instance"

        # Stone is not placed on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        self.assertIsNone(stone.full_clean())
        stone.save()

    def test_AddStone_RaisesException(self):
        "Creating stone instance"
        
        # Stone is placed on board
        stone = Stone(board_id=1, user_id=1, row=0, col=1, color=0)
        with self.assertRaisesRegexp(ValidationError, 'ERR_STONE_001'):
            stone.full_clean()

