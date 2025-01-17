# Speech-To-Text avec Whisper et PyTorch

Ce projet utilise le modèle **Whisper** d'OpenAI pour effectuer la reconnaissance vocale en temps réel.

## 🚀 Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/ton-utilisateur/speech-to-text.git
   cd speech-to-text
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Installer FFmpeg** :
   - Télécharge et installe FFmpeg depuis le site officiel : https://ffmpeg.org/download.html
   - Ajoute FFmpeg au PATH de ton système.

5. **Télécharger les modèles Whisper** :
   - Télécharge le modèle souhaité depuis [Hugging Face](https://huggingface.co/openai/whisper).
   - Place le fichier du modèle dans un dossier `models/` à la racine du projet.

## 🧑‍💻 Utilisation

1. **Lancer le service de reconnaissance vocale** :
   ```bash
   python stt.py
   ```

2. Parle dans le micro pour déclencher la reconnaissance vocale. Le mot-clé défini dans le script (par défaut "activation") déclenchera l'envoi du texte au serveur Node.js.

## 📂 Arborescence du projet

```
speech-to-text/
├── models/               # Dossier pour les fichiers de modèles
├── venv/                 # Environnement virtuel (non inclus dans le dépôt)
├── stt.py                # Script principal
├── requirements.txt      # Dépendances du projet
├── .gitignore            # Fichiers/dossiers à ignorer par Git
├── README.md             # Documentation du projet
```

## ⚙️ Configuration

- **Mot-clé** : Le mot-clé utilisé pour détecter les phrases importantes est défini par la variable `KEYWORD` dans le fichier `stt.py`. Par défaut, c'est "activation".
- **Endpoint Node.js** : Le serveur Node.js doit écouter sur l'URL définie dans `NODE_ENDPOINT` (par défaut : `http://localhost:3000/keyword-detected`).
- **Modèle Whisper** : Tu peux choisir un modèle différent (par exemple, "tiny", "base", "small", "medium", "large") en modifiant la variable `MODEL_NAME` dans le script.

## ✨ Améliorations possibles

1. **Gestion des pauses** :
   - Actuellement, les pauses sont gérées par `PAUSE_THRESHOLD`. Ce paramètre peut être ajusté pour une meilleure précision selon ton environnement sonore.

2. **Amélioration des performances** :
   - Utiliser une GPU compatible avec CUDA pour accélérer la transcription. Assure-toi que PyTorch est installé avec le support GPU.

3. **Sauvegarde des transcriptions** :
   - Ajouter une fonctionnalité pour enregistrer les transcriptions dans un fichier texte ou une base de données.

4. **Interface utilisateur** :
   - Développer une interface graphique pour surveiller et interagir avec les transcriptions en temps réel.

## 📜 Licence
Ce projet est distribué sous la licence MIT. Consulte le fichier `LICENSE` pour plus d'informations.

---

Pour toute question ou contribution, n'hésite pas à ouvrir une issue ou une pull request sur le dépôt GitHub.
