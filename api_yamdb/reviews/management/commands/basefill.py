from django.core.management.base import BaseCommand, CommandError
import csv, sqlite3
import os
from api_yamdb.settings import BASE_DIR
from reviews.models import (
    Category, Genre, Title, GenreTitle, Comment, Review, User
)


def get_reader(file_name):
    csv_path = os.path.join(BASE_DIR, 'static/data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    print(reader)
    return reader


def get_row(file_name):
    csv_path = os.path.join(BASE_DIR, 'static/data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    return csv_file

class Command(BaseCommand):
    help = 'Заполнение базы данных'

    def handle(self, *args, **options):
        data = (
            ('titles.csv', Title),
            ('users.csv', User),
            ('review.csv', Review),
            ('category.csv', Category),
            ('comments.csv', Comment),
            ('genre_title.csv', GenreTitle),
            ('genre.csv', Genre),
        )

        for fn, table in data:
            reader = get_reader(f'{fn}')
            graphs = get_row
            next(reader, None)
            for row in reader:
                print(row)
                #obj, created = table.objects.get_or_create(
                #    id=row[0],
                #    name=row[1],
                #    slug=row[2]
                #)
