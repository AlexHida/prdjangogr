from django.shortcuts import render
import requests

API_URL = "https://api-inference.huggingface.co/models/grammarly/coedit-large"
API_TOKEN = "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"

QA_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
QA_HEADERS = {"Authorization": "Bearer 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"}

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def videos_index(request):
    return render(request, 'videos_index.html')


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

def index(request):
    resultado = None
    texto_original = None
    if request.method == 'POST':
        input_text = request.POST.get('texto', '')
        texto_original = input_text
        output = corregir_gramatica(input_text)
        if isinstance(output, list) and len(output) > 0:
            resultado = output[0].get('generated_text', '')
    return render(request, 'index.html', {'resultado': resultado, 'texto_original': texto_original})

def qa_index(request):
    respuesta = None
    if request.method == 'POST':
        contexto = request.POST.get('contexto', '')
        pregunta = request.POST.get('pregunta', '')
        respuesta = hacer_pregunta(contexto, pregunta)
    return render(request, 'qa_index.html', {'respuesta': respuesta})
