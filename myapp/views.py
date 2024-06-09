from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Player
from .models import Tournament
from .models import Match
from .models import Score
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    users = User.objects.all()
    return render(request, 'dashboard.html', {'user': request.user, 'users': users})

def players(request):
    query = request.GET.get('q')
    country_filter = request.GET.get('country')

    players = Player.objects.all().order_by('full_name')

    if query:
        players = players.filter(full_name__icontains=query)
    if country_filter:
        players = players.filter(country=country_filter)

    countries = Player.objects.order_by('country').values_list('country', flat=True).distinct()

    paginator = Paginator(players, 15)  
    page_number = request.GET.get('page')
    players_page = paginator.get_page(page_number)

    return render(request, 'players.html', {
        'players': players_page,
        'query': query,
        'country_filter': country_filter,
        'countries': countries,
    })

def player_detail(request, pk):
    player = get_object_or_404(Player, id=pk)
    matches = Match.objects.filter(Q(player1_url=player.url) | Q(player2_url=player.url)).order_by('-date')[0:10]
    return render(request, 'player_detail.html', {'player': player, 'matches': matches })

def base(request):
    return render(request, 'base.html')

def tournaments(request):
    query = request.GET.get('q')
    year_filter = request.GET.get('year')
    country_filter = request.GET.get('country')
    city_filter = request.GET.get('city')
    category_filter = request.GET.get('category')

    tournaments = Tournament.objects.all()

    if query:
        tournaments = tournaments.filter(full_name__icontains=query)
    if year_filter:
        tournaments = tournaments.filter(year=year_filter)
    if country_filter:
        tournaments = tournaments.filter(country=country_filter)
    if city_filter:
        tournaments = tournaments.filter(city=city_filter)
    if category_filter:
        tournaments = tournaments.filter(category=category_filter)

    years = Tournament.objects.order_by('year').values_list('year', flat=True).distinct()
    countries = Tournament.objects.order_by('country').values_list('country', flat=True).distinct()
    cities = Tournament.objects.order_by('city').values_list('city', flat=True).distinct()
    categories = Tournament.objects.order_by('category').values_list('category', flat=True).distinct()



    paginator = Paginator(tournaments, 15)  
    page_number = request.GET.get('page')
    tournaments_page = paginator.get_page(page_number)

    return render(request, 'tournaments.html', {
        'tournaments': tournaments_page,
        'query': query,
        'year_filter': year_filter,
        'country_filter': country_filter,
        'city_filter': city_filter,
        'category_filter': category_filter,
        'years': years,
        'countries': countries,
        'cities': cities,
        'categories': categories,
    })
def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, id=pk)
    matches = Match.objects.filter(tournament_id=pk).order_by('-best_of', '-date')[:10]
    return render(request, 'tournament_detail.html', {'tournament': tournament, 'matches': matches })

def matches(request):
    matches = Match.objects.exclude(date__isnull=True).order_by('-date', 'best_of')
    paginator = Paginator(matches, 4)  
    page_number = request.GET.get('page')
    matches_page = paginator.get_page(page_number)

    return render(request, 'matches.html', {
        'matches': matches_page,
    })

def user_logout(request):
    logout(request)
    return render(request, 'logout.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})
