from django.contrib.auth.models import (
    AbstractUser, PermissionsMixin)
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# class User(AbstractUser, PermissionsMixin):
#     password = models.CharField(
#         max_length=200,
#         default='password',
#         verbose_name='Пароль'
#     )
#     first_name = models.TextField(blank=True, verbose_name='Имя')
#     last_name = models.TextField(blank=True, verbose_name='Фамилия')
#     username = models.CharField(
#         max_length=255,
#         unique=True,
#         verbose_name='Имя'
#     )
#     email = models.EmailField(unique=True, verbose_name='Электронная почта')
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username

#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        unique=True,
        verbose_name="Имя тега"
        )
    color = models.CharField(
        max_length=7,
        null=False,
        verbose_name="Цвет тега"
        )
    slug = models.CharField(
        max_length=400,
        verbose_name=u'Tag slug',
        unique=True,
        null=False
        )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        unique=True,
        verbose_name="Ингридиент"
        )
    quantity = models.IntegerField(verbose_name="Количество")
    unit = models.CharField(
        max_length=200,
        null=False,
        verbose_name="Единица измерения"
        )


class Recipe(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cooktime = models.IntegerField()
    tag = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='img/',
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
