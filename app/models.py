from django.db import models

# Create your models here.


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=30)
    text = models.CharField(max_length=140)
    created_at = models.DateField()
    sentiment = models.ForeignKey('Sentiment', null=True, on_delete=models.SET_NULL)
    sent_accuracy = models.FloatField()

    def __str__(self):
        return self.text


class Sentiment(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class DataFile(models.Model):
    name = models.CharField(max_length=20)
    file_type = models.CharField(max_length=10)
    file_content = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name
