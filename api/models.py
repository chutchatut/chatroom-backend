from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', )


class Join(models.Model):
    user = models.ForeignKey(
        User,
        related_name='boards',
        on_delete=models.CASCADE,
    )
    board = models.ForeignKey(
        Board,
        related_name='users',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "%s is in %s" % (self.user.username, str(self.board), )

    class Meta:
        unique_together = ('user', 'board', )


class Message(models.Model):
    user = models.ForeignKey(
        User,
        related_name='messages',
        on_delete=models.CASCADE,
    )
    board = models.ForeignKey(
        Board,
        related_name='messages',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
