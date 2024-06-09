from django.db import models

class Player(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    url = models.URLField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Tournament(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.CharField(max_length=100)
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    prize = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Match(models.Model):
    tournament_id = models.ForeignKey(Tournament, to_field="id", on_delete=models.CASCADE)
    match_id = models.IntegerField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=100)
    best_of = models.IntegerField()
    player1_name = models.CharField(max_length=100)
    player1_url = models.CharField(max_length=300)
    player2_name = models.CharField(max_length=100)
    player2_url = models.CharField(max_length=300)
    score1 = models.ImageField(null=True, blank=True)
    score2 = models.IntegerField(null=True, blank=True)
    frames_scores = models.CharField(max_length=500, null=True, blank=True)
    is_walkover = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.match_id)


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, to_field="match_id", on_delete=models.CASCADE)
    frame = models.IntegerField()
    player = models.IntegerField()
    score = models.IntegerField()
    fifty_plus_breaks_str = models.CharField(max_length=100)

    def __str__(self):
        return str(self.score)
