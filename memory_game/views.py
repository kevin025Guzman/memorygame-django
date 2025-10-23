from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Partida
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
        intentos = 10
        tiempo = 60
    elif nivel == 'medio':
        intentos = 6
        tiempo = 50
    else:
        intentos = 4
        tiempo = 40

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
    partidas = Partida.objects.filter(usuario=request.user).order_by('-fecha')

    total_victorias = partidas.filter(resultado='victoria').count()
    total_derrotas = partidas.filter(resultado='derrota').count()
    total_partidas = partidas.count()

    promedio_tiempo = partidas.aggregate(Avg('tiempo_restante'))['tiempo_restante__avg'] or 0
    nivel_mas_jugado = partidas.values('nivel').annotate(total=Count('nivel')).order_by('-total').first()

    nivel_mas_jugado = nivel_mas_jugado['nivel'] if nivel_mas_jugado else "N/A"

    contexto = {
        'partidas': partidas,
        'total_victorias': total_victorias,
        'total_derrotas': total_derrotas,
        'total_partidas': total_partidas,
        'promedio_tiempo': round(promedio_tiempo, 2),
        'nivel_mas_jugado': nivel_mas_jugado,
    }

    return render(request, 'memory_game/perfil.html', contexto)


