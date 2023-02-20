from django.contrib import admin

from .models import Comment, Review, Title, Genre, Category, GenreTitle


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


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'year',
                    'rating',
                    'description',
                    'category_id',
                    'genre_id',
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


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)

