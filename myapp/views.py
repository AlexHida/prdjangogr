from django.shortcuts import render
import requests

API_URL = "https://api-inference.huggingface.co/models/grammarly/coedit-large"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def corregir_gramatica(input_text):
    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

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
