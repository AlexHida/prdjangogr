from googleapiclient.discovery import build
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from .forms import EstudianteForm
from .models import Estudiante
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import requests

#Correción Gramatical
API_URL = "https://api-inference.huggingface.co/models/pszemraj/grammar-synthesis-base"
API_TOKEN = "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"
#Preguntas y Respuestas
QA_API_URL = "https://api-inference.huggingface.co/models/IProject-10/xlm-roberta-base-finetuned-squad2"
QA_HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}
#Clave YouTube
YOUTUBE_API_KEY = "AIzaSyD7vY_shdAc7UCBzfalnzFQlQ904XrVP0w"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def addsupU(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Verifica si el usuario ya existe
        if User.objects.filter(username=username).exists():
            # Agrega un mensaje de error
            messages.error(request, 'El usuario ya existe. Por favor, elige otro nombre de usuario.')
        elif password != password_confirm:
            # Agrega un mensaje de error si las contraseñas no coinciden
            messages.error(request, 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo.')
        else:
            # Cuando el usuario no existe y las contraseñas coinciden, crea el superusuario
            User.objects.create_superuser(username=username, password=password)
            return redirect('index')  # Redirige a la página de inicio de sesión o a donde desees

    return render(request, 'addsupuser.html')

def index(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name='Estudiantes').exists():
            # Obtiene el estudiante actualmente autenticado
            estudiante = Estudiante.objects.get(usua=user.username)
            
            # Renderiza la plantilla 'index.html' solo con el estudiante autenticado
            return render(request, 'index.html', {'estudiante': estudiante})

    # Si el usuario no está autenticado o no es un estudiante, muestra la lista completa
    estudiantes = Estudiante.objects.all()
    return render(request, 'home.html', {'estudiantes': estudiantes})

#def vista_docente(request):
    #return render(request, 'docente.html')

def register_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            password = request.POST['pass1']
            password_confirm = request.POST['password_confirm']

            if password == password_confirm:
                estudiante = form.save()
                user = User.objects.create_user(username=estudiante.usua, password=password)
                estudiante.user = user
                estudiante.save()

                group, created = Group.objects.get_or_create(name='Estudiantes')
                user.groups.add(group)

                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo.')

    else:
        form = EstudianteForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige a la página de inicio después de iniciar sesión
            else:
                messages.error(request, 'Usuario o contraseña incorrectos. Inténtalo de nuevo.')  # Agrega un mensaje de error
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Inténtalo de nuevo.')  # Agrega un mensaje de error
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 

def videos_index(request):
    channel_id = "UCzdHLjHljz5eR1UnmznUH7w"  # ID del canal específico
    videos = get_youtube_videos(channel_id)

    return render(request, 'videos_index.html', {'videos': videos})


def ayuda(request):
    return render(request, 'ayuda.html')

def correctorGramatica(request):
    resultado = None
    texto_original = None
    respuestaRecibida = False  # Inicializar la variable
    estudiante = None
    mensaje_error = None  # Inicializar el mensaje de error

    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name='Estudiantes').exists():
            estudiante = Estudiante.objects.get(usua=user.username)

    if request.method == 'POST':
        # Verifica si el formulario se envió correctamente
        if 'texto' in request.POST:
            input_text = request.POST.get('texto', '').strip()  # Elimina espacios en blanco
            texto_original = input_text

            if not input_text:  # Verifica si el campo está vacío
                messages.error(request, 'Por favor, ingresa texto en el campo.')
            else:
                output = corregir_gramatica(input_text)
                if isinstance(output, list) and len(output) > 0:
                    resultado = output[0].get('generated_text', '')
                    respuestaRecibida = bool(resultado)  # Actualizar la variable

                    # Si hay un estudiante autenticado, incrementa TaGramar
                    if estudiante:
                        estudiante.TaGramar += 1
                        estudiante.save()

    return render(request, 'correctorGramatica.html', {'resultado': resultado, 'texto_original': texto_original, 'respuestaRecibida': respuestaRecibida, 'estudiante': estudiante, 'mensaje_error': mensaje_error})


def corregir_gramatica(input_text):
    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

from django.contrib import messages  # Importa messages

def qa_index(request):
    respuesta = None
    estudiante = None
    
    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name='Estudiantes').exists():
            estudiante = Estudiante.objects.get(usua=user.username)
    
    if request.method == 'POST':
        contexto = request.POST.get('contexto', '').strip()  # Obtiene el valor y elimina espacios en blanco
        pregunta = request.POST.get('pregunta', '').strip()  # Obtiene el valor y elimina espacios en blanco

        # Verifica si se ingresó texto en ambos campos
        if not contexto or not pregunta:
            messages.error(request, 'Por favor, ingresa texto en ambos campos.')
        else:
            respuesta = hacer_pregunta(contexto, pregunta)
            
            # Si hay un estudiante autenticado y la respuesta no está vacía, incrementa TaPreguntas
            if estudiante and respuesta:
                estudiante.TaPreguntas += 1
                estudiante.save()
            
    return render(request, 'qa_index.html', {'respuesta': respuesta, 'estudiante': estudiante})



def hacer_pregunta(contexto, pregunta):
    payload = {
        "inputs": {
            "question": pregunta,
            "context": contexto,
        }
    }
    response = requests.post(QA_API_URL, headers=QA_HEADERS, json=payload)
    
    try:
        data = response.json()
        answer = data.get('answer', '')
    except (ValueError, KeyError):
        answer = "No se pudo obtener una respuesta"

    return answer



def get_youtube_videos(channel_id, max_results=10):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        channelId=channel_id,
        type="video",
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get("items", []):
        video = {
            "title": search_result["snippet"]["title"],
            "video_id": search_result["id"]["videoId"],
        }
        videos.append(video)

    return videos




