import pyttsx3
import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'tts_app/index.html')

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
