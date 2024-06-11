from django.shortcuts import render
from django.http import JsonResponse
import pyttsx3
import speech_recognition as sr
from googletrans import Translator, LANGUAGES

def index(request):
    languages = [(code, name) for code, name in LANGUAGES.items()]
    return render(request, 'tts_app/index.html', {'languages': languages, 'voices': get_voices()})

def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_list = [{'id': voice.id, 'name': voice.name} for voice in voices]
    return voice_list

def speak_text(request):
    text = request.POST.get('text', '')
    voice_id = request.POST.get('voice_id', '')
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed control of voice
    if voice_id:
        engine.setProperty('voice', voice_id)
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
    except sr.UnknownValueError:
        return JsonResponse({'status': 'error', 'message': 'Google Speech Recognition could not understand the audio'})
    except sr.RequestError as e:
        return JsonResponse({'status': 'error', 'message': 'Could not request results from Google Speech Recognition service; {0}'.format(e)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def translate_text(request):
    try:
        text = request.POST.get('text', '')
        if not text:
            raise ValueError("No text provided")
        target_language = request.POST.get('language', 'es')  # Default to Spanish
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        return JsonResponse({'status': 'success', 'translated_text': translated.text})
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': 'Invalid destination language'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
