"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from models import Game

class GameTest(TestCase):
    # Load fixtures
    fixtures = ['auth']

    def test_CreateGame_CreatesInstance(self):
        "Creating Game instance"

        # Create Game instance
        game = Game()
        game.save()
        self.assertIsInstance(game, Game)

    def test_EditGame_AddsTwoUsers(self):
        "Adding two Users to existing Game instance"

        # Create Game instance
        game = Game()
        game.save()
        self.assertEqual(game.users.count(), 0)

        # Assing Users
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        game.users.add(user1, user2)
        game.save()
        self.assertEqual(game.users.count(), 2)

        # Check User class
        for i in (1,2):
            # Get Game User by id
            self.assertEqual(game.users.filter(id=i).count(), 1)
            # Check User class
            self.assertIsInstance(game.users.get(id=i), User)

        for user in game.users.all():
            # Check Game instance by User
            game = user.game_set.get(id=1)
            self.assertIsInstance(game, Game)
            self.assertEqual(game.id, 1)
            # Get all Game instances for User
            self.assertEqual(user.game_set.count(), 1)

    def test_EditGame_RemovesTwoUsers(self):
        "Removing Users from Game"

        # Create Game instance
        game = Game()
        game.save()

        # Assing Users
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        game.users.add(user1, user2)
        game.save()
        self.assertEqual(game.users.count(), 2)

        # Remove users
        game.users.remove(user1, user2)
        self.assertEqual(game.users.count(), 0)
        for user in (user1, user2):
            self.assertEqual(user.game_set.count(), 0)

