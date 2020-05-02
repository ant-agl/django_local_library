from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language


admin.site.register(Genre)
admin.site.register(Language)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'borrower', 'due_back']
    list_filter = ['book', 'status', 'due_back']
    fields = ['book', 'imprint', 'status', 'borrower', 'due_back']


class BookInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'language']
    list_filter = ['author', 'language']
    fields = ['title', 'author', 'genre', 'language', 'summary', 'isbn']
    inlines = [BookInstanceInline]


class BookInline(admin.TabularInline):
    extra = 0
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
