# 🚗 DashCam Security System

Système de surveillance vidéo sécurisé avec vérification blockchain.

## 🚀 Applications

- **dashcam_controller.py** : Interface d'enregistrement
- **security_hub.py** : Interface de vérification

## 📦 Installation Locale
```bash
pip install -r requirements.txt
streamlit run dashcam_controller.py
streamlit run security_hub.py
```

## 🌐 Démo en Ligne

[Lien vers l'application déployée]

## 🔐 Configuration

Les clés Supabase sont à configurer dans les fichiers Python.

## 👨‍💻 Auteur

Projet académique - 2026
```

### **4. `.gitignore`**
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
buffer_local/
temp_videos/
*.mp4
.streamlit/secrets.toml
.env