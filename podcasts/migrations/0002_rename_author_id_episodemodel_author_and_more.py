# Generated by Django 4.1.1 on 2022-09-07 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episodemodel',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='episodemodel',
            old_name='podcast_id',
            new_name='podcast',
        ),
    ]
