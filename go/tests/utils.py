from django.test import TestCase
from django.utils import simplejson
from django.contrib.auth.models import User
from common.models import Game
from go.models import Board
import go.utils
from mock import Mock

class UtilTest(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common', 'go']

    def test_GetBoardUpdateJson_EmptyBoard_ReturnsJson(self):
        "Serializing update data for empty board."

        # Create new board
        game = Game()
        game.save()
        board = Board(game_id=game.id)
        board.save()

        expect = simplejson.dumps({
            'placed_stones'     : [],
            'next_move_color'   : 'black',
        })

        result = go.utils.get_board_update_json(game.id)

        self.assertEqual(result, expect)

    def test_GetBoardUpdateJson_BoardWithStones_ReturnsJson(self):
        "Serializing update data for board with set stones."

        expect = simplejson.dumps({
            'placed_stones'         : [
                { 
                    'pk'        : 1, 
                    'model'     : 'go.stone', 
                    'fields'    : { 'color': 0, 'col': 0, 'row': 0 },
                },
                { 
                    'pk'        : 2, 
                    'model'     : 'go.stone', 
                    'fields'    : { 'color': 0, 'col': 1, 'row': 1 },
                },
                { 
                    'pk'        : 42, 
                    'model'     : 'go.stone', 
                    'fields'    : { 'color': 1, 'col': 0, 'row': 1 },
                },
                { 
                    'pk'        : 43, 
                    'model'     : 'go.stone', 
                    'fields'    : { 'color': 1, 'col': 1, 'row': 0 },
                },
            ],
            'next_move_color'   : 'black',
        })

        result = go.utils.get_board_update_json(1)

        self.assertEqual(result, expect)

    def test_StoneUpdate_AddInvalidStone_AddsStone(self):

        # Mock request
        request      = Mock(); 
        request.user = User.objects.get(pk=1)
        request.POST = { 'row': 0, 'col': 1 }

        # Get game board
        game_id = 1
        board   = Board.objects.get(pk=game_id)

        # Store count of placed stones
        latest_stones_count = board.get_placed_stones().count()

        # Add new stone to board
        go.utils.stone_update(request, game_id)

        # Compare stones count
        self.assertEqual(
            board.get_placed_stones().count(),
            latest_stones_count
        )

    def test_StoneUpdate_AddValidStone_AddsStone(self):

        # Mock request
        request      = Mock(); 
        request.user = User.objects.get(pk=1)
        request.POST = { 'row': 0, 'col': 2 }

        # Get game board
        game_id = 1
        board   = Board.objects.get(pk=game_id)

        # Store count of placed stones
        latest_stones_count = board.get_placed_stones().count()

        # Add new stone to board
        go.utils.stone_update(request, game_id)

        # Compare stones count
        self.assertEqual(
            board.get_placed_stones().count(),
            (latest_stones_count+1)
        )

    def test_StoneUpdate_DeleteNotExistingStone_Passes(self):

        # Mock request
        request      = Mock(); 
        request.user = User.objects.get(pk=1)
        request.POST = { 'row': 0, 'col': 2, 'action': 'del' }

        # Get game board
        game_id = 1
        board   = Board.objects.get(pk=game_id)

        # Store count of placed stones
        latest_stones_count = board.get_placed_stones().count()

        # Remove stone from board
        go.utils.stone_update(request, game_id)

        # Compare stones count
        self.assertEqual(
            board.get_placed_stones().count(),
            latest_stones_count
        )

    def test_StoneUpdate_DeleteExistingStone_DeletesStone(self):

        # Mock request
        request      = Mock(); 
        request.user = User.objects.get(pk=2)
        request.POST = { 'row': 1, 'col': 1, 'action': 'del' }

        # Get game board
        game_id = 1
        board   = Board.objects.get(pk=game_id)

        # Store count of placed stones
        latest_stones_count = board.get_placed_stones().count()

        # Remove stone from board
        go.utils.stone_update(request, game_id)

        # Compare stones count
        self.assertEqual(
            board.get_placed_stones().count(),
            (latest_stones_count - 1)
        )

    def test_StoneUpdate_DeleteInvalidStone_FormSaveFails(self):

        # Mock request
        request      = Mock(); 
        request.user = User.objects.get(pk=1)
        request.POST = { 'row': 1, 'col': 1, 'action': 'del' }

        # Get game board
        game_id = 1
        board   = Board.objects.get(pk=game_id)

        # Store count of placed stones
        latest_stones_count = board.get_placed_stones().count()

        # Remove stone from board
        go.utils.stone_update(request, game_id)

        # Compare stones count
        self.assertEqual(
            board.get_placed_stones().count(),
            latest_stones_count
        )

    def test_GetChatUpdateJson_ChatWithMessages_ReturnsJson(self):
        expect = simplejson.dumps({
            'chat_messages': [
                {
                    'pk'        : 1,
                    'model'     : 'common.message',
                    'fields'    : {
                        'timestamp'     : '21:22:55',
                        'message'       : "User 'test1' has joined the chat.",
                        'type'          : 'j',
                        'author'        : 'test1',
                    },
                },
                {
                    'pk'        : 2,
                    'model'     : 'common.message',
                    'fields'    : {
                        'timestamp'     : '23:06:40',
                        'message'       : 'Twix',
                        'type'          : 'm',
                        'author'        : 'test1',
                    },
                },
                {
                    'pk'        : 3,
                    'model'     : 'common.message',
                    'fields'    : {
                        'timestamp'     : '23:07:36',
                        'message'       : 'Snickers',
                        'type'          : 'm',
                        'author'        : 'test1',
                    },
                },
                {
                    'pk'        : 4,
                    'model'     : 'common.message',
                    'fields'    : {
                        'timestamp'     : '23:08:32',
                        'message'       : 'Mars',
                        'type'          : 'm',
                        'author'        : 'test1',
                    },
                },
            ],
        })

        result = go.utils.get_chat_update_json(1)

        self.assertEqual(result, expect)

