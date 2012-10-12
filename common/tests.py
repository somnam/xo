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

    def test_create_game(self):
        print("")

        # CASE
        print("Create empty Game instance")
        game = Game()
        game.save()
        self.assertIsInstance(game, Game)

    def test_assing_players(self):
        print("")

        # CASE
        print("Create Game instance")
        game = Game()
        game.save()
        self.assertEqual(game.users.count(), 0)

        # CASE
        print("Add two Users to existing Game instance")
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        game.users.add(user1, user2)
        game.save()
        self.assertEqual(game.users.count(), 2)

        # CASE
        for i in (1,2):
            print("Get Game User by id")
            self.assertEqual(game.users.filter(id=i).count(), 1)
            print("Check User class")
            self.assertIsInstance(game.users.get(id=i), User)

        # CASE
        for user in game.users.all():
            print("Check Game instance by User %s" % user)
            game = user.game_set.get(id=1)
            self.assertIsInstance(game, Game)
            self.assertEqual(game.id, 1)
            print("Get all Game instances for User %s" % user)
            self.assertEqual(user.game_set.all().count(), 1)

        # CASE
        print("Remove Users from Game")
        game.users.remove(user1, user2)
        self.assertEqual(game.users.count(), 0)
        for user in (user1, user):
            self.assertEqual(user.game_set.count(), 0)

