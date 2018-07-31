from django.test import TestCase
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from go.models import Stone
from go.forms import StoneCreateForm, StoneDeleteForm
from unittest.mock import Mock

class StoneCreateFormTest(TestCase):
    # Load fixtures
    fixtures = ['authorization', 'common', 'go']

    def test_Coordinates_CheckExistingStone_RaisesException(self):
        "Checking stone with existing coordinates."

        # Validate stone
        stone = { 'board': 1, 'user': 1, 'row': 0, 'col': 1, 'color': 0 }
        form  = StoneCreateForm(data=stone)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['ERR_STONE_001'])

    def test_Coordinates_CheckNewStone_Passes(self):
        "Checking stone with new coordinates."

        # Validate stone
        stone = { 'board': 1, 'user': 1, 'row': 0, 'col': 2, 'color': 0 }
        form  = StoneCreateForm(data=stone)
        self.assertTrue(form.is_valid())

    def test_CanPlaceStone_PlaceWhiteStoneAfterWhiteMove_RaisesException(self):
        "Checking if user with white stones can place stone after white move"

        # Validate stone
        stone = { 'board': 1, 'user': 2, 'row': 0, 'col': 2, 'color': 1 }
        form  = StoneCreateForm(data=stone)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['ERR_STONE_002'])

    def test_CanPlaceStone_PlaceBlackStoneAfterWhiteMove_Passes(self):
        "Checking if user with black stones can place stone after white move"

        # Create new black stone on board
        stone = { 'board': 1, 'user': 1, 'row': 0, 'col': 2, 'color': 0 }
        form  = StoneCreateForm(data=stone)
        self.assertTrue(form.is_valid())

    def test_CanPlaceStone_PlaceBlackStoneAfterBlackMove_RaisesException(self):
        "Checking if user with black stones can place stone after black move"

        # Create new black stone on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        stone.save()

        # Place next black stone
        stone = Stone(board_id=1, user_id=1, row=0, col=3, color=0)
        form  = StoneCreateForm(data=model_to_dict(stone))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['ERR_STONE_002'])

    def test_CanPlaceStone_PlaceWhiteStoneAfterBlackMove_RaisesException(self):
        "Checking if user with white stones can place stone after black move"

        # Create new black stone on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        stone.save()

        # Place white stone
        stone = Stone(board_id=1, user_id=2, row=0, col=3, color=1)
        form  = StoneCreateForm(data=model_to_dict(stone))
        self.assertTrue(form.is_valid())

class StoneDeleteFormTest(TestCase):
    # Load fixtures
    fixtures = ['authorization', 'common', 'go']

    def test_CanRemoveStone_RemoveStoneFromBoardBeforeMove_RaisesException(self):
        "Checking if user can remove stone from board before his move"

        # Mock request
        request         = Mock()
        request.user    = User.objects.get(pk=1)

        # Remove black stone
        stone = Stone.objects.get(row=0, col=0, color=0)
        stone.row,stone.col = -1,-1

        # Validate stone
        form = StoneDeleteForm(request=request, data=model_to_dict(stone))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['ERR_STONE_003'])

    def test_CanRemoveStone_RemoveOwnStoneFromBoard_RaisesException(self):
        "Checking if user can remove own stone from board"

        # Mock request
        request         = Mock()
        request.user    = User.objects.get(pk=1)

        # Remove white stone
        stone = Stone.objects.get(row=1, col=0, color=1)
        # Update stone state
        stone.row,stone.col = -1,-1

        # Validate stone
        form = StoneDeleteForm(request=request, data=model_to_dict(stone))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['ERR_STONE_003'])

    def test_CanRemoveStone_RemoveCorrectStoneFromBoard_RaisesException(self):
        "Checking if user with white stones can remove black stone after white move."

        # Mock request
        request         = Mock()
        request.user    = User.objects.get(pk=2)

        # Remove black stone by user with white stones
        stone = Stone.objects.get(row=0, col=0, color=0)
        # Update stone state
        stone.row,stone.col = -1,-1

        # Validate stone
        form = StoneDeleteForm(request=request, data=model_to_dict(stone))
        self.assertTrue(form.is_valid())
