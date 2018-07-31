from django.test import TestCase
from django.contrib.auth.models import User
from common.models import Game, Chat, Message, MESSAGE_TYPES

class GameTest(TestCase):
    # Load fixtures
    fixtures = ['authorization']

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

class MessageTest(TestCase):
    # Load fixtures
    fixtures = ['authorization', 'common']

    def test_CreateMessage_CreatesInstance(self):

        # Create Message instance
        chat    = Chat.objects.get(pk=1)
        message = Message(chat=chat)
        message.save()
        self.assertIsInstance(message, Message)

    def test_CreateJoinMessage_PrintsMessage(self):

        # Create Join Message
        chat    = Chat.objects.get(pk=1)
        user    = User.objects.get(pk=1)
        message = Message(chat=chat, author=user, type=MESSAGE_TYPES['join'])
        message.save()
        self.assertEqual(
            str(message),
            "User 'test1' has joined the chat."
        )

    def test_CreateLeaveMessage_PrintsMessage(self):

        # Create Leave Message
        chat    = Chat.objects.get(pk=1)
        user    = User.objects.get(pk=1)
        message = Message(chat=chat, author=user, type=MESSAGE_TYPES['leave'])
        message.save()
        self.assertEqual(
            str(message),
            "User 'test1' has left the chat."
        )

    def test_CreateNotificationMessage_PrintsMessage(self):

        # Create Notification Message
        chat    = Chat.objects.get(pk=1)
        message = Message(
            chat=chat, 
            type=MESSAGE_TYPES['notification'],
            message='This is a notification.'
        )
        message.save()
        self.assertEqual(
            str(message),
            'This is a notification.',
        )

    def test_CreateMessage_PrintsMessage(self):

        # Create Message
        chat    = Chat.objects.get(pk=1)
        user    = User.objects.get(pk=1)
        message = Message(chat=chat, author=user, message='This is a message.')
        message.save()
        self.assertEqual(
            ('[%s]: %s' % (message.author, str(message))),
            '[test1]: This is a message.',
        )

class ChatTest(TestCase):
    # Load fixtures
    fixtures = ['authorization', 'common']

    def test_CreateChat_CreatesInstance(self):

        # Create chat instance
        chat = Chat()
        chat.save()
        self.assertIsInstance(chat, Chat)

    def test_CreateChat_AppendToGame(self):

        # Append chat to game
        game = Game.objects.get(pk=1)
        chat = Chat(game_id=game.id)
        chat.save()
        game.save()

        # Check instances
        self.assertIsInstance(chat, Chat)
        self.assertIsInstance(chat.game, Game)
        self.assertIsInstance(game.chat, Chat)
        self.assertEqual(chat.game.id, game.id)
        self.assertEqual(game.chat.game_id, game.id)

        # Check users
        self.assertEqual(chat.game.users.count(), 2)
        for i in (1,2):
            self.assertIsInstance(chat.game.users.get(id=i), User)

    def test_UserJoin_PrintMessage(self):

        game = Game.objects.get(pk=1)
        chat = Chat(game=game)
        chat.save()


