from django.db import models

# Create your models here.


class Usermodel(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    userpic = models.URLField(max_length=80)
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name + "with twitter handle @" + str(self.username) )


class twitter(models.Model):
    username = models.ForeignKey(Usermodel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    last_hq = models.FloatField()
    last_tweet_id = models.CharField(max_length=20)

    def __str__(self):
        return str("@"+ self.username + " happiness quotient is " +
                   str(self.last_hq) + "and last tweet id is " + str(self.last_tweet_id))
