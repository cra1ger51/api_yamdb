from django.contrib import admin

from .models import Comment, Review


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


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
