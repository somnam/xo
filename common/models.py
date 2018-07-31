from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Game class
class Game(models.Model):
    users = models.ManyToManyField(User)
    name  = models.CharField(max_length=128)

class Chat(models.Model):
    game = models.OneToOneField(Game, primary_key=True)

    def join(self, user):
        msg = Message(chat=self, author=user, type=MESSAGE_TYPES['join'])
        msg.save()
        return msg

    def leave(self, user):
        msg = Message(chat=self, author=user, type=MESSAGE_TYPES['leave'])
        msg.save()
        return msg

    def notify(self, notification):
        msg = Message(
            chat=self, 
            type=MESSAGE_TYPES['notification'], 
            msg=notification
        )
        msg.save()
        return msg

    def say(self, message):
        msg = Message(chat=chat, author=user, message=message)
        msg.save()
        return msg

# Chat message
MESSAGE_TYPES = {
    'join'          : 'j',
    'leave'         : 'l',
    'notification'  : 'n',
}
class Message(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ('j', 'join'),
        ('m', 'message'),
        ('l', 'leave'),
        ('n', 'notification'),
    )

    chat      = models.ForeignKey(Chat)
    # Author can be optional
    author    = models.ForeignKey(User, blank=True, null=True)
    type      = models.CharField(
        max_length=1, 
        choices=MESSAGE_TYPE_CHOICES, 
        default='m'
    )
    # Max up to 2K chars per message
    message   = models.CharField(max_length=2048)
    timestamp = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set message value base on message type
        self._set_message()

        # Call the actual save method
        super(Message, self).save(*args, **kwargs)

    def _set_message(self):
        """Set message value base on message type."""

        type_to_message = {
            MESSAGE_TYPES['join'] : (
                "User '%s' has joined the chat." % 
                self.author
            ),
            MESSAGE_TYPES['leave'] : (
                "User '%s' has left the chat." % 
                self.author
            ),
        }

        message = self.message
        if self.type in type_to_message:
            message = type_to_message[self.type]
        self.message = message

    def __str__(self):
        return self.message
