from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('', views.dashboard, name='dashboard'),
    path('players/', views.players, name='players'),
    path('players/<slug:pk>/', views.player_detail, name='player_detail'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/<slug:pk>/', views.tournament_detail, name='tournament_detail'),
    path('matches/', views.matches, name='matches'),
    path('logout/', views.user_logout, name='logout'),
]
