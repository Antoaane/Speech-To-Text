import whisper
import pyaudio
import wave
import requests
import time

# Configuration
KEYWORD = "activation"  # Remplace par ton mot-clé
NODE_ENDPOINT = "http://localhost:3000/keyword-detected"  # Endpoint du serveur Node.js
PAUSE_THRESHOLD = 1.0  # Durée d'une pause pour détecter la fin de la phrase
MODEL_NAME = "base"  # Modèle Whisper ('tiny', 'base', 'small', 'medium', 'large')

# Initialisation du modèle Whisper
print("Chargement du modèle Whisper...")
model = whisper.load_model(MODEL_NAME)
print("Modèle chargé avec succès !")

# Configuration du microphone
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5  # Longueur d'enregistrement par itération

def record_audio(filename="temp_audio.wav"):
    """Enregistre de l'audio depuis le microphone et sauvegarde dans un fichier temporaire"""
    audio = pyaudio.PyAudio()

    # Configuration du flux audio
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Écoute en cours...")

    frames = []

    # Enregistrement audio
    start_time = time.time()
    while time.time() - start_time < RECORD_SECONDS:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    # Arrêter et fermer le flux
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Sauvegarde de l'audio dans un fichier WAV
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

def transcribe_audio(filename):
    """Transcrit un fichier audio avec Whisper"""
    print("Transcription en cours...")
    result = model.transcribe(filename, language="fr")
    return result["text"]

def detect_keyword(text):
    """Vérifie si le mot-clé est présent dans le texte"""
    return KEYWORD in text

def send_to_node_server(text):
    """Envoie le texte au serveur Node.js"""
    try:
        response = requests.post(NODE_ENDPOINT, json={"text": text})
        print(f"Texte envoyé : {text}")
        print(f"Réponse du serveur Node.js : {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi au serveur Node.js : {e}")

def main():
    """Boucle principale pour écouter et traiter l'audio"""
    print("Service de reconnaissance prêt. Parle dans le micro...")
    
    while True:
        try:
            # Enregistrement de l'audio temporaire
            record_audio()

            # Transcription de l'audio
            text = transcribe_audio("temp_audio.wav")
            print(f"Texte reconnu : {text}")

            # Détection du mot-clé
            if detect_keyword(text):
                print(f"Mot-clé '{KEYWORD}' détecté.")
                # Récupérer le texte à partir du mot-clé
                keyword_text = text.split(KEYWORD, 1)[-1].strip()
                send_to_node_server(keyword_text)
            else:
                print("Mot-clé non détecté.")
        
        except KeyboardInterrupt:
            print("Service arrêté par l'utilisateur.")
            break

if __name__ == "__main__":
    main()
