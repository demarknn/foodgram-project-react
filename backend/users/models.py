from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='почта пользователя',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.email)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique subscriptions'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        # def __str__(self):
        #     return str(self.following)
