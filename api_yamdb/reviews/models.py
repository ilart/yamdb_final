import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from api_yamdb.settings import COMMENT_LEN, REVIEW_LEN

User = get_user_model()


class Category(models.Model):
    """Модель категория"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанр"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведение"""
    name = models.CharField('Название', max_length=100)
    year = models.IntegerField(
        'Год выпуска',
        validators=[
            MaxValueValidator(
                dt.date.today().year,
                'Год не может быть больше текущего'
            ),
            MinValueValidator(
                0,
                'Год не может быть меньше 0'
            )
        ]
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name="category", blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField('Описание')

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модуль привязки произведения и жанра"""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        ordering = ['title']
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'


class Review(models.Model):
    """Модель отзыв"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='username пользователя',
        related_name='reviews'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(validators=[
        MaxValueValidator(
            10,
            'Оценка не может быть больше 10'
        ),
        MinValueValidator(
            0,
            'Оценка не может быть меньше 0'
        )
    ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Объект',
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date', )
        constraints = [
            UniqueConstraint(
                name='unique_review',
                fields=['author', 'title']
            )
        ]

    def __str__(self):
        return self.title[:REVIEW_LEN]


class Comment(models.Model):
    """Модель комментарий"""
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date', )

    def __str__(self):
        return self.text[:COMMENT_LEN]
