from django.shortcuts import render
from django.http import JsonResponse
import pyttsx3
import speech_recognition as sr
from googletrans import Translator, LANGUAGES

def index(request):
    languages = [(code, name) for code, name in LANGUAGES.items()]
    return render(request, 'tts_app/index.html', {'languages': languages})

def speak_text(request):
    text = request.POST.get('text', '')
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed control of voice
    engine.say(text)
    engine.runAndWait()
    return JsonResponse({'status': 'success'})

def recognize_speech(request):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return JsonResponse({'status': 'success', 'text': text})
    except:
        return JsonResponse({'status': 'error', 'text': 'Speech not recognized'})

def translate_text(request):
    text = request.POST.get('text', '')
    target_language = request.POST.get('language', 'es')  # Default to Spanish
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        return JsonResponse({'status': 'success', 'translated_text': translated.text})
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid destination language'})
