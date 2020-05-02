from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid


class Genre(models.Model):

    name = models.CharField('жанр', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Language(models.Model):
    name = models.CharField('язык', max_length=200,
                            help_text='Введите язык для книги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'язык'
        verbose_name_plural = 'языки'


class Book(models.Model):

    title = models.CharField('название книги', max_length=200)
    author = models.ForeignKey(
        'Author', on_delete=models.SET_NULL, null=True, verbose_name='автор')
    summary = models.TextField('описание',
                               max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, verbose_name='Язык')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'кинги'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор для этой конкретной книги во всей библиотеке")
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, verbose_name='название книги')
    imprint = models.CharField('отпечаток', max_length=200)
    due_back = models.DateField('дата возврата', null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Поддержка'),
        ('o', 'Взаймы'),
        ('a', 'Доступный'),
        ('r', 'Зарезервированный'),
    )

    status = models.CharField('статус', max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Наличие книги')

    class Meta:
        ordering = ["due_back"]
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '{} ({})'.format(self.id, self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
