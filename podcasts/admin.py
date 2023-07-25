from django.contrib import admin
from podcasts.models import AuthorModel, PodcastModel, EpisodeModel


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'pic_url')


admin.site.register(AuthorModel, AuthorAdmin)


class PodcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'url', 'last_episode_id', 'episode_amount', 'tags', 'rss_url')


admin.site.register(PodcastModel, PodcastAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'url', 'audio_url', 'tags', 'pub_date',
                    'length', 'podcast_id', 'author_id')


admin.site.register(EpisodeModel, EpisodeAdmin)
