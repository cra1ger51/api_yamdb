from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'text',
                    'score',
                    'author',
                    'score',
                    'pub_date',
                    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'review',
                    'text',
                    'author',
                    'pub_date',
                    )


class GenreTitleInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreTitleInline, )
    list_display = ('id',
                    'name',
                    'year',
                    'description',
                    'category',
                    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'slug',
                    )


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'slug',
                    )
    inlines = (GenreTitleInline,)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
