"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from models import Game

class GameTest(TestCase):
    # Load User fixtures
    fixtures = ['auth']

    def test_create_game(self):
        print()

        print("Create Game instance")
        game = Game()
        self.assertTrue(isinstance(game, Game))

    def test_assing_players(self):
        print()

        print("Create empty Game instance")
        game = Game()
        game.save()
        self.assertEqual(len(game.users.filter()), 0)

        print("Add two users to existing Game instance")
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        game.users.add(user1, user2)
        game.save()
        self.assertEqual(len(game.users.filter()), 2)

        print("Get Game user by id")
        self.assertEqual(len(game.users.filter(id=1)), 1)

        print("Check User class")
        self.assertTrue(isinstance(game.users.get(id=1), User))

        for user in game.users.filter():
            print("Check Game instance by User %s" % user)
            game = user.game_set.get(id=1)
            self.assertTrue(isinstance(game, Game))


