from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
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
    title = models.CharField(max_length=200)
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
