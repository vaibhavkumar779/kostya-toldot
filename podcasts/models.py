from django.db import models


# Create your models here.
class AuthorModel(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    url = models.TextField()
    pic_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'AUTHORS'


class PodcastModel(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.TextField()

    # last_episode = models.ForeignKey('EpisodeModel', blank=True)
    last_episode_id = models.TextField(blank=True, null=True)
    episode_amount = models.IntegerField()
    tags = models.TextField(blank=True, null=True)
    rss_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'PODCASTS'


class EpisodeModel(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.TextField()
    audio_url = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

    pub_date = models.DateField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)

    podcast_id = models.TextField(blank=True, null=True)
    author_id = models.TextField(blank=True, null=True)

    # podcast = models.ForeignKey(PodcastModel,
    #                             on_delete=models.SET_NULL,
    #                             null=True)
    # author = models.ForeignKey(AuthorModel,
    #                            on_delete=models.SET_NULL,
    #                            null=True)

    class Meta:
        db_table = 'EPISODES'
