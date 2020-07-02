from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Тема',               {'fields': ['title']}),
        ('Текст',               {'fields': ['text']}),
        ('Автор',               {'fields': ['author']}),
        ('Дата публикации', {'fields': ['published_date'],'classes': ['collapse']}),
    ]
    inlines = [CommentInline]
    list_display = ('title', 'published_date', 'was_published_recently',)
    list_filter = ['title',]

admin.site.register(Post, PostAdmin)
