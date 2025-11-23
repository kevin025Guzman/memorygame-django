from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Partida
from collections import defaultdict

from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator



from memory_game import models


# Página principal
@login_required
def index(request):
    nivel = request.session.get('nivel', None)
    return render(request, 'memory_game/index.html', {'nivel': nivel})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')

    return render(request, 'memory_game/login.html')

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Cuenta creada con éxito, ahora puedes iniciar sesión')
        return redirect('login')

    return render(request, 'memory_game/register.html')

# Vista de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista para la selección de nivel
@login_required
def seleccion_nivel(request):
    if request.method == 'POST':
        nivel = request.POST.get('nivel')
        # Guardamos el nivel seleccionado en la sesión del usuario
        request.session['nivel'] = nivel
        return redirect('index')  # Más adelante redirigiremos al tablero del juego

    return render(request, 'memory_game/seleccion_nivel.html')


@login_required
def juego(request):
    nivel = request.session.get('nivel', 'basico')

    # Configuración según nivel
    if nivel == 'basico':
        intentos = 20
        tiempo = 130
    elif nivel == 'medio':
        intentos = 12
        tiempo = 80
    else:
        intentos = 6
        tiempo = 60

    contexto = {
        'nivel': nivel,
        'intentos': intentos,
        'tiempo': tiempo,
    }
    return render(request, 'memory_game/juego.html', contexto)

# Recibir datos de resultados desde JavaScript
@csrf_exempt
@login_required
def registrar_partida(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nivel = data.get('nivel')
        resultado = data.get('resultado')
        tiempo_restante = data.get('tiempo_restante', 0)

        Partida.objects.create(
            usuario=request.user,
            nivel=nivel,
            resultado=resultado,
            tiempo_restante=tiempo_restante
        )

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
def perfil(request):
    # Filtrar partidas del usuario actual
    partidas = Partida.objects.filter(usuario=request.user).order_by('-fecha')

    # Paginación (10 partidas por página)
    paginator = Paginator(partidas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Estadísticas generales
    total_partidas = partidas.count()
    total_victorias = partidas.filter(resultado='victoria').count()
    total_derrotas = partidas.filter(resultado='derrota').count()
    promedio_tiempo = partidas.filter(resultado='victoria').aggregate(Avg('tiempo_restante'))['tiempo_restante__avg'] or 0

    

    nivel_mas_jugado_data = partidas.values('nivel').annotate(total=Count('nivel')).order_by('-total').first()
    nivel_mas_jugado = nivel_mas_jugado_data['nivel'] if nivel_mas_jugado_data else 'N/A'

    niveles_validos = ['basico', 'medio', 'avanzado']
    ranking_queryset = (
        Partida.objects.filter(resultado='victoria', nivel__in=niveles_validos)
        .values('nivel', 'usuario__username')
        .annotate(total_victorias=Count('id'))
        .order_by('nivel', '-total_victorias', 'usuario__username')
    )

    ranking_dict = {nivel: [] for nivel in niveles_validos}
    for entry in ranking_queryset:
        ranking_dict[entry['nivel']].append({
            'username': entry['usuario__username'],
            'total_victorias': entry['total_victorias'],
        })

    ranking_victorias = [
        {
            'nivel': nivel,
            'jugadores': jugadores,
        }
        for nivel, jugadores in ranking_dict.items()
    ]

    context = {
        'total_partidas': total_partidas,
        'total_victorias': total_victorias,
        'total_derrotas': total_derrotas,
        'promedio_tiempo': round(promedio_tiempo, 2),
        'nivel_mas_jugado': nivel_mas_jugado,
        'page_obj': page_obj,
        'ranking_victorias': ranking_victorias,
    }

    return render(request, 'memory_game/perfil.html', context)


