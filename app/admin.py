from django.contrib import admin
from . import models


class TweetAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'text',
        'sentiment',
        'sent_accuracy',
        'created_at')


class SentimentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name',)


class DataFileAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'file_type',
        'name')


admin.site.register(models.Tweet, TweetAdmin)
admin.site.register(models.Sentiment, SentimentAdmin)
admin.site.register(models.DataFile, DataFileAdmin)
