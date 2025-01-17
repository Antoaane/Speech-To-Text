import whisper
import pyaudio
import wave
import requests
import time
import threading
import numpy as np
import collections

# Configuration
KEYWORD = "Merlin"  # Remplace par ton mot-clé
NODE_ENDPOINT = "http://localhost:3000/keyword-detected"  # Endpoint du serveur Node.js
PAUSE_THRESHOLD = 1.0  # Durée d'une pause pour détecter la fin de la phrase
MODEL_NAME = "medium"  # Modèle Whisper ('tiny', 'base', 'small', 'medium', 'large')

# Initialisation du modèle Whisper
print("Chargement du modèle Whisper...")
model = whisper.load_model(MODEL_NAME)
print("Modèle chargé avec succès !")

# Configuration du microphone
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 100  # Niveau sonore pour détecter la parole
BUFFER_MAX_SECONDS = 10  # Longueur max du buffer (5s d'audio)

# Buffer circulaire pour l'audio
audio_buffer = collections.deque(maxlen=int(BUFFER_MAX_SECONDS * RATE / CHUNK))

# Mutex pour protéger le buffer
buffer_lock = threading.Lock()

# Flag pour arrêter proprement
stop_signal = False

def record_audio():
    """Enregistre en continu et ajoute au buffer"""
    global stop_signal
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("🔴 Écoute en continu...")

    while not stop_signal:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_np = np.frombuffer(data, dtype=np.int16)

        # Ajout au buffer circulaire
        with buffer_lock:
            audio_buffer.append(audio_np)

    stream.stop_stream()
    stream.close()
    audio.terminate()

def process_audio():
    """Traite l'audio en continu et détecte les mots-clés"""
    global stop_signal
    
    while not stop_signal:
        time.sleep(0.5)  # Intervalle pour éviter de surcharger la CPU
        
        with buffer_lock:
            if len(audio_buffer) == 0:
                continue  # Pas encore d'audio accumulé

            # Conversion en tableau unique
            audio_data = np.concatenate(list(audio_buffer))
        
        # Vérifier s'il y a du son
        if np.max(np.abs(audio_data)) > SILENCE_THRESHOLD:
            # Sauvegarde dans un fichier temporaire
            filename = "temp_audio.wav"
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(audio_data.tobytes())

            # Transcription
            print("📝 Transcription en cours...")
            text = model.transcribe(filename, language="fr")["text"]
            print(f"Texte reconnu : {text}")

            # Détection du mot-clé
            if detect_keyword(text):
                print(f"🔔 Mot-clé '{KEYWORD}' détecté.")
                keyword_text = text.split(KEYWORD, 1)[-1].strip()
                send_to_node_server(keyword_text)
            else:
                print("Mot-clé non détecté.")

def detect_keyword(text):
    """Vérifie si le mot-clé est présent dans le texte"""
    return KEYWORD in text

def send_to_node_server(text):
    print(f"📤 Texte à envoyer : {text}")
    """Envoie le texte au serveur Node.js"""
    try:
        response = requests.post(NODE_ENDPOINT, json={"text": text})
        print(f"📤 Texte envoyé : {text}")
        print(f"🖥️ Réponse serveur : {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erreur serveur : {e}")

def main():
    """Lance l'écoute et la transcription en parallèle"""
    global stop_signal
    
    print("🎤 Service de reconnaissance prêt !")
    
    # Lancer l'enregistrement et la transcription en parallèle
    record_thread = threading.Thread(target=record_audio)
    process_thread = threading.Thread(target=process_audio)

    record_thread.start()
    process_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Arrêt du service...")
        stop_signal = True

        # Attendre la fin des threads
        record_thread.join()
        process_thread.join()
        print("✅ Service arrêté proprement.")

if __name__ == "__main__":
    main()
