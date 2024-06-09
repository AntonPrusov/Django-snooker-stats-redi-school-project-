import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import Player, Tournament, Match, Score
from datetime import datetime

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(settings.BASE_DIR, 'myapp', 'init_data')

        # Load players
        with open(os.path.join(base_dir, 'players.csv'), encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                player_full_name = row['full_name']
                player_url = row['url']
                player_exists = Player.objects.filter(url=player_url).exists()
                if not player_exists:
                    Player.objects.create(
                        full_name=player_full_name,
                        url=player_url,
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        country=row['country']
                    )

        # Load tournaments
        with open(os.path.join(base_dir, 'tournaments.csv'), encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tournament_id = row['id']
                tournament_exists = Tournament.objects.filter(id=tournament_id).exists()
                if not tournament_exists:
                    Tournament.objects.create(
                        id=tournament_id,
                        season=row['season'],
                        year=row['year'],
                        name=row['name'],
                        full_name=row['full_name'],
                        url=row['url'],
                        status=row.get('status', ''),
                        category=row.get('category', ''),
                        prize=row.get('prize', ''),
                        country=row.get('country', ''),
                        city=row.get('city', '')
                    )

        # Load matches
        with open(os.path.join(base_dir, 'matches.csv'), encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tournament_id = row['tournament_id']
                tournament = Tournament.objects.get(id=tournament_id)
                match_id = row['match_id']
                match_exists = Match.objects.filter(match_id=match_id).exists()
                if tournament and not match_exists:
                    # Check if the date field is empty
                    date_str = row['date'].split(' - ')[0]
                    date = None
                    if date_str:
                        date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    Match.objects.create(
                        tournament_id=tournament,
                        match_id=match_id,
                        date=date,
                        stage=row['stage'],
                        best_of=int(row['best_of']),
                        player1_name=row['player1_name'],
                        player1_url=row['player1_url'],
                        player2_name=row['player2_name'],
                        player2_url=row['player2_url'],
                        score1=row['score1'],
                        score2=row.get('score2', None),
                        frames_scores=row.get('frames_scores', ''),
                        is_walkover=row.get('is_walkover', False)
                    )


        # Load scores
        with open(os.path.join(base_dir, 'scores.csv'), encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                match_id = row['match_id']
                match = Match.objects.get(match_id=match_id)
                Score.objects.create(
                    match=match,
                    frame=int(row['frame']),
                    player=int(row['player']),
                    score=int(row['score']),
                    fifty_plus_breaks_str=row['fifty_plus_breaks_str']
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data from CSV files'))
