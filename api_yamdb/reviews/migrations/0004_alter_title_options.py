# Generated by Django 3.2 on 2023-02-16 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_title_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-id'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]