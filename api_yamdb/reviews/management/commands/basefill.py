import csv
import os

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from api_yamdb.settings import BASE_DIR
from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title)
from users.models import User


def get_reader(file_name):
    csv_path = os.path.join(BASE_DIR, 'static/data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    return reader


class Command(BaseCommand):
    help = 'Заполнение базы данных'

    def handle(self, *args, **options):
        reader = get_reader('category.csv')
        next(reader, None)
        for row in reader:
            obj, created = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )

        reader = get_reader('genre.csv')
        next(reader, None)
        for row in reader:
            obj, created = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )

        reader = get_reader('titles.csv')
        next(reader, None)
        for row in reader:
            obj, created = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category_id=row[3]
            )

        reader = get_reader('genre_title.csv')
        next(reader, None)
        for row in reader:
            obj, created = GenreTitle.objects.get_or_create(
                id=row[0],
                title_id=row[1],
                genre_id=row[2]

            )
        reader = get_reader('users.csv')
        next(reader, None)
        for row in reader:
            obj, created = User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )

        reader = get_reader('review.csv')
        next(reader, None)
        for row in reader:
            obj_user = get_object_or_404(User, id=row[3])
            obj, created = Review.objects.get_or_create(
                id=row[0],
                title_id=row[1],
                text=row[2],
                author=obj_user,
                score=row[4],
                pub_date=row[5]
            )

        reader = get_reader('comments.csv')
        next(reader, None)
        for row in reader:
            obj_user = get_object_or_404(User, id=row[3])
            obj_review = get_object_or_404(Review, id=row[1])
            obj_title = obj_review.title_id
            obj, created = Comment.objects.get_or_create(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author=obj_user,
                pub_date=row[4],
                title_id=obj_title
            )
