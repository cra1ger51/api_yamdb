from django.contrib import admin

from .models import User, Comment, Review


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'bio',
                    'role',
                    'is_staff',
                    'is_superuser',
                    )


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


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
