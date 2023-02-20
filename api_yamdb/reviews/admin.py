from django.contrib import admin

from .models import User, Title, Genre, Category, GenreTitle


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


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'genre_id',
                    'title_id',
                    )


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
