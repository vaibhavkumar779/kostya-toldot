# Generated by Django 4.1.1 on 2022-09-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0004_remove_episodemodel_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodemodel',
            name='audio_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='episodemodel',
            name='length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='episodemodel',
            name='pub_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='episodemodel',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='podcastmodel',
            name='rss_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='podcastmodel',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
    ]