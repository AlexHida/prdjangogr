from googleapiclient.discovery import build
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from .forms import EstudianteForm
from .models import Estudiante
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

def index(request):
    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name='Estudiantes').exists():
            estudiante = Estudiante.objects.get(usua=user.username)
            estudiante.asistencia += 1
            estudiante.save()

            # Redirige a la plantilla 'index.html' si el usuario es estudiante
            return render(request, 'index.html', {'estudiante': estudiante})

    estudiantes = Estudiante.objects.all()
    return render(request, 'home.html', {'estudiantes': estudiantes})

#def vista_docente(request):
    #return render(request, 'docente.html')

def register_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()  # Guarda el estudiante en la base de datos
            user = User.objects.create_user(username=estudiante.usua, password=estudiante.pass1)
            estudiante.user = user
            estudiante.save()

            # Asigna al estudiante al grupo "Estudiantes" (si no existe, créalo en el panel de administración)
            group, created = Group.objects.get_or_create(name='Estudiantes')
            user.groups.add(group)

            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('index')  # Cambia 'home' por la URL deseada después del registro
    else:
        form = EstudianteForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')  # Redirige a la página de inicio después de iniciar sesión
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
    if request.method == 'POST':
        input_text = request.POST.get('texto', '')
        texto_original = input_text
        output = corregir_gramatica(input_text)
        if isinstance(output, list) and len(output) > 0:
            resultado = output[0].get('generated_text', '')
            respuestaRecibida = bool(resultado)  # Actualizar la variable

    return render(request, 'correctorGramatica.html', {'resultado': resultado, 'texto_original': texto_original, 'respuestaRecibida': respuestaRecibida})


def corregir_gramatica(input_text):
    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

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


def qa_index(request):
    respuesta = None
    if request.method == 'POST':
        contexto = request.POST.get('contexto', '')
        pregunta = request.POST.get('pregunta', '')
        respuesta = hacer_pregunta(contexto, pregunta)
    return render(request, 'qa_index.html', {'respuesta': respuesta})
