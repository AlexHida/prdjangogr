from googleapiclient.discovery import build
from django.shortcuts import render
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


def videos_index(request):
    channel_id = "UCzdHLjHljz5eR1UnmznUH7w"  # ID del canal específico
    videos = get_youtube_videos(channel_id)

    return render(request, 'videos_index.html', {'videos': videos})


def ayuda(request):
    return render(request, 'ayuda.html')

def correctorGramatica(request):
    resultado = None
    texto_original = None
    if request.method == 'POST':
        input_text = request.POST.get('texto', '')
        texto_original = input_text
        output = corregir_gramatica(input_text)
        if isinstance(output, list) and len(output) > 0:
            resultado = output[0].get('generated_text', '')
    return render(request, 'correctorGramatica.html', {'resultado': resultado, 'texto_original': texto_original})


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


def index(request):
    return render(request, 'index.html')

def qa_index(request):
    respuesta = None
    if request.method == 'POST':
        contexto = request.POST.get('contexto', '')
        pregunta = request.POST.get('pregunta', '')
        respuesta = hacer_pregunta(contexto, pregunta)
    return render(request, 'qa_index.html', {'respuesta': respuesta})
