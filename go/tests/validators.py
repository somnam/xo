from django.test import TestCase
from django.core.exceptions import ValidationError
from go.models import Stone
from go.validators import StoneValidator

class StoneValidatorTest(TestCase):
    # Load fixtures
    fixtures = ['auth', 'common', 'go']

    def test_Coordinates_CheckExistingStone_RaisesException(self):
        "Checking stone with existing coordinates."

        # Get stone placed on board and validate it
        stone = Stone(board_id=1, user_id=1, row=0, col=1, color=0)
        validator = StoneValidator(stone)
        with self.assertRaisesRegexp(ValidationError, 'ERR_STONE_001'):
            validator.coordinates()

    def test_Coordinates_CheckNewStone_Passes(self):
        "Checking stone with new coordinates."

        # Create stone not placed on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        validator = StoneValidator(stone)
        self.assertIsNone(validator.coordinates())

    def test_CanPlaceStone_PlaceWhiteStoneAfterWhiteMove_RaisesException(self):
        "Checking if user with white stones can place stone after white move"

        # Create new white stone on board
        stone = Stone(board_id=1, user_id=2, row=0, col=2, color=1)
        validator = StoneValidator(stone)
        with self.assertRaisesRegexp(ValidationError, 'ERR_STONE_002'):
            validator.can_place_stone()

    def test_CanPlaceStone_PlaceBlackStoneAfterWhiteMove_Passes(self):
        "Checking if user with black stones can place stone after white move"

        # Create new black stone on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        validator = StoneValidator(stone)
        self.assertIsNone(validator.can_place_stone())

    def test_CanPlaceStone_PlaceBlackStoneAfterBlackMove_RaisesException(self):
        "Checking if user with black stones can place stone after black move"

        # Create new black stone on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        validator = StoneValidator(stone)
        self.assertIsNone(validator.can_place_stone())
        stone.save()

        # Place next black stone
        stone = Stone(board_id=1, user_id=1, row=0, col=3, color=0)
        validator = StoneValidator(stone)
        with self.assertRaisesRegexp(ValidationError, 'ERR_STONE_002'):
            validator.can_place_stone()

    def test_CanPlaceStone_PlaceWhiteStoneAfterBlackMove_RaisesException(self):
        "Checking if user with white stones can place stone after black move"

        # Create new black stone on board
        stone = Stone(board_id=1, user_id=1, row=0, col=2, color=0)
        validator = StoneValidator(stone)
        self.assertIsNone(validator.can_place_stone())
        stone.save()

        # Place white stone
        stone = Stone(board_id=1, user_id=2, row=0, col=3, color=1)
        validator = StoneValidator(stone)
        self.assertIsNone(validator.can_place_stone())
