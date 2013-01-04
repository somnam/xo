from django.test import TestCase
from django.utils import simplejson
from common.models import Game
from go.models import Board
import go.utils

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
