from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('seleccion-nivel/', views.seleccion_nivel, name='seleccion_nivel'), 
    path('juego/', views.juego, name='juego'),
    path('registrar-partida/', views.registrar_partida, name='registrar_partida'),
    path('perfil/', views.perfil, name='perfil'),

]
