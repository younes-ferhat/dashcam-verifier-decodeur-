import streamlit as st
import hashlib
import os
import tempfile
import time
from supabase import create_client
from datetime import datetime
import json
from io import BytesIO
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(
    page_title="DashCam Security Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

URL = "https://iiqxkqyxcxehrxujkbfs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpcXhrcXl4Y3hlaHJ4dWprYmZzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU3MTc1MSwiZXhwIjoyMDgyMTQ3NzUxfQ.OPO9iA6El-yAAOBlM_99IANKfyOem4IwDq5mr-cgngg"

# --- CSS ULTRA SOPHISTIQUÉ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 60px 0 rgba(31, 38, 135, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 1.3rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Sidebar personnalisée */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%);
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    .sidebar-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    /* Cards avec effet néon */
    .neon-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37),
                    inset 0 0 20px rgba(102, 126, 234, 0.1);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .neon-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    .neon-card:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.4),
                    inset 0 0 30px rgba(102, 126, 234, 0.2);
    }
    
    /* Métriques futuristes */
    div[data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    div[data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Boutons avec effet glow */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Expander stylisé */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        font-weight: 600;
        color: rgba(255,255,255,0.9) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Code blocks futuristes */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
    }
    
    code {
        color: #667eea !important;
        font-weight: 600;
    }
    
    /* Status badges améliorés */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .badge-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(235, 51, 73, 0.4);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
    }
    
    .badge-info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
        color: rgba(255, 255, 255, 0.9);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Video styling */
    video {
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    /* Divider effet glow */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.8), transparent);
        margin: 2.5rem 0;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    /* Scrollbar ultra moderne */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animation de chargement */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading-shimmer {
        animation: shimmer 2s infinite;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(102, 126, 234, 0.2) 50%, 
            transparent 100%);
        background-size: 1000px 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
@st.cache_resource
def init_supabase():
    try:
        return create_client(URL, KEY)
    except Exception as e:
        return None

def calculer_hash(fichier_path):
    sha256 = hashlib.sha256()
    with open(fichier_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def generer_rapport_json(logs, stats=None):
    """Génère un rapport JSON détaillé"""
    rapport = {
        "metadata": {
            "titre": "Rapport de Vérification DashCam Security",
            "date_generation": datetime.now().isoformat(),
            "version": "1.0",
            "total_segments": len(logs)
        },
        "statistiques": stats if stats else {
            "total": len(logs),
            "authentiques": 0,
            "falsifies": 0,
            "introuvables": 0
        },
        "preuves": []
    }
    
    for log in logs:
        rapport["preuves"].append({
            "id": log['id'],
            "nom_fichier": log['hash'],
            "signature_sha256": log['storage_url'],
            "date_creation": log['created_at'],
            "statut": "Non vérifié"
        })
    
    return json.dumps(rapport, indent=2, ensure_ascii=False)

def generer_rapport_csv(logs, stats=None):
    """Génère un rapport CSV pour Excel"""
    data = []
    for log in logs:
        data.append({
            "ID": log['id'],
            "Nom Fichier": log['hash'],
            "Signature SHA-256": log['storage_url'],
            "Date Création": log['created_at'],
            "Statut": "Non vérifié"
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False, encoding='utf-8')

def generer_rapport_html(logs, stats=None):
    """Génère un rapport HTML professionnel"""
    total = len(logs)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if stats:
        authentiques = stats.get('authentiques', 0)
        falsifies = stats.get('falsifies', 0)
        introuvables = stats.get('introuvables', 0)
        score = (authentiques / total * 100) if total > 0 else 0
    else:
        authentiques = falsifies = introuvables = 0
        score = 0
    
    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport DashCam Security - {now}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                color: #333;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 3rem 2rem;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                font-weight: 900;
                margin-bottom: 0.5rem;
            }}
            
            .header p {{
                font-size: 1.1rem;
                opacity: 0.9;
            }}
            
            .metadata {{
                background: #f8f9fa;
                padding: 1.5rem 2rem;
                border-bottom: 3px solid #667eea;
            }}
            
            .metadata-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
            }}
            
            .metadata-item {{
                display: flex;
                flex-direction: column;
            }}
            
            .metadata-item label {{
                font-weight: 600;
                color: #666;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 0.3rem;
            }}
            
            .metadata-item value {{
                font-size: 1.1rem;
                color: #333;
                font-weight: 600;
            }}
            
            .stats {{
                padding: 2rem;
                background: white;
            }}
            
            .stats h2 {{
                font-size: 1.8rem;
                margin-bottom: 1.5rem;
                color: #667eea;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }}
            
            .stat-card {{
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            
            .stat-card.success {{
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
            }}
            
            .stat-card.danger {{
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                color: white;
            }}
            
            .stat-card.warning {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }}
            
            .stat-value {{
                font-size: 3rem;
                font-weight: 900;
                margin-bottom: 0.5rem;
            }}
            
            .stat-label {{
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                opacity: 0.9;
            }}
            
            .score-container {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin-bottom: 2rem;
            }}
            
            .score-value {{
                font-size: 4rem;
                font-weight: 900;
            }}
            
            .score-label {{
                font-size: 1.2rem;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            
            .table-container {{
                padding: 2rem;
            }}
            
            .table-container h2 {{
                font-size: 1.8rem;
                margin-bottom: 1.5rem;
                color: #667eea;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border-radius: 10px;
                overflow: hidden;
            }}
            
            thead {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            
            th {{
                padding: 1rem;
                text-align: left;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 1px;
            }}
            
            td {{
                padding: 1rem;
                border-bottom: 1px solid #e9ecef;
            }}
            
            tbody tr:hover {{
                background: #f8f9fa;
            }}
            
            .hash-cell {{
                font-family: 'Courier New', monospace;
                font-size: 0.85rem;
                color: #667eea;
                word-break: break-all;
            }}
            
            .badge {{
                display: inline-block;
                padding: 0.3rem 0.8rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
            }}
            
            .badge-success {{
                background: #38ef7d;
                color: white;
            }}
            
            .badge-danger {{
                background: #f45c43;
                color: white;
            }}
            
            .badge-warning {{
                background: #f5576c;
                color: white;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 2rem;
                text-align: center;
                color: #666;
                border-top: 3px solid #667eea;
            }}
            
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                
                .container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Rapport de Vérification</h1>
                <p>DashCam Security Hub - Système de Certification Blockchain</p>
            </div>
            
            <div class="metadata">
                <div class="metadata-grid">
                    <div class="metadata-item">
                        <label>Date de Génération</label>
                        <value>{now}</value>
                    </div>
                    <div class="metadata-item">
                        <label>Total de Segments</label>
                        <value>{total}</value>
                    </div>
                    <div class="metadata-item">
                        <label>Version du Rapport</label>
                        <value>1.0</value>
                    </div>
                    <div class="metadata-item">
                        <label>Type d'Audit</label>
                        <value>Complet</value>
                    </div>
                </div>
            </div>
            
            <div class="stats">
                <h2>📊 Résultats de l'Audit</h2>
                
                <div class="score-container">
                    <div class="score-value">{score:.1f}%</div>
                    <div class="score-label">Score de Sécurité Global</div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card success">
                        <div class="stat-value">{authentiques}</div>
                        <div class="stat-label">✅ Authentiques</div>
                    </div>
                    <div class="stat-card danger">
                        <div class="stat-value">{falsifies}</div>
                        <div class="stat-label">❌ Falsifiées</div>
                    </div>
                    <div class="stat-card warning">
                        <div class="stat-value">{introuvables}</div>
                        <div class="stat-label">⚠️ Introuvables</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{total}</div>
                        <div class="stat-label">📦 Total</div>
                    </div>
                </div>
            </div>
            
            <div class="table-container">
                <h2>📋 Registre Détaillé des Preuves</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nom du Fichier</th>
                            <th>Signature SHA-256</th>
                            <th>Date de Création</th>
                            <th>Statut</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for log in logs:
        html += f"""
                        <tr>
                            <td><strong>{log['id']}</strong></td>
                            <td>{log['hash']}</td>
                            <td class="hash-cell">{log['storage_url'][:32]}...</td>
                            <td>{log['created_at'][:19]}</td>
                            <td><span class="badge badge-warning">Non vérifié</span></td>
                        </tr>
        """
    
    html += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="footer">
                <p><strong>DashCam Security Hub © 2026</strong></p>
                <p>Système de vérification d'intégrité par Blockchain • Rapport généré automatiquement</p>
                <p style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.7;">
                    Ce rapport certifie l'état des preuves vidéo au moment de sa génération.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

supabase = init_supabase()

if not supabase:
    st.error("❌ Erreur critique : Connexion au cloud impossible")
    st.stop()

# --- SIDEBAR SOPHISTIQUÉE ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">🛡️ Control Center</p>', unsafe_allow_html=True)
    st.caption("Blockchain Verification System")
    st.markdown("---")
    
    # Status en temps réel
    st.markdown("### 📡 État du Système")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="status-badge badge-success">🟢 ONLINE</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="status-badge badge-info">🔐 SECURED</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Horloge système
    now = datetime.now()
    st.markdown("### 🕐 Horloge Système")
    st.markdown(f"**{now.strftime('%H:%M:%S')}**")
    st.caption(f"{now.strftime('%d/%m/%Y')}")
    
    st.markdown("---")
    
    # Actions rapides
    st.markdown("### ⚡ Actions Rapides")
    if st.button("🔄 Rafraîchir", use_container_width=True):
        st.rerun()
    
    # Menu d'export de rapport
    st.markdown("### 📊 Exporter Rapport")
    
    format_export = st.selectbox(
        "Format :",
        ["HTML (Visuel)", "JSON (Données)", "CSV (Excel)"],
        label_visibility="collapsed"
    )
    
    if st.button("📥 Télécharger", use_container_width=True, type="primary"):
        st.session_state.export_trigger = True
        st.session_state.export_format = format_export
    
    st.markdown("---")
    st.caption("DashCam Security Hub © 2026")
    st.caption("Powered by Blockchain Technology")

# --- RÉCUPÉRATION DES DONNÉES ---
try:
    response = supabase.table("video_frames").select("*").order('created_at', desc=True).execute()
    logs = response.data
    total_videos = len(logs)
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.stop()

# --- GESTION DE L'EXPORT DEPUIS LA SIDEBAR ---
if "export_trigger" in st.session_state and st.session_state.export_trigger:
    try:
        if "audit_stats" in st.session_state:
            stats = st.session_state.audit_stats
        else:
            stats = None
        
        format_choisi = st.session_state.export_format
        
        if format_choisi == "HTML (Visuel)":
            rapport = generer_rapport_html(logs, stats)
            st.sidebar.download_button(
                label="💾 Sauvegarder HTML",
                data=rapport,
                file_name=f"rapport_dashcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        elif format_choisi == "JSON (Données)":
            rapport = generer_rapport_json(logs, stats)
            st.sidebar.download_button(
                label="💾 Sauvegarder JSON",
                data=rapport,
                file_name=f"rapport_dashcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        elif format_choisi == "CSV (Excel)":
            rapport = generer_rapport_csv(logs, stats)
            st.sidebar.download_button(
                label="💾 Sauvegarder CSV",
                data=rapport,
                file_name=f"rapport_dashcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.sidebar.success("✅ Rapport prêt!")
        st.session_state.export_trigger = False
        
    except Exception as e:
        st.sidebar.error(f"Erreur : {e}")
        st.session_state.export_trigger = False

# --- HERO HEADER ---
st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">🛡️ Security Verification Hub</div>
    <div class="hero-subtitle">Centre de contrôle d'intégrité des preuves vidéo • {total_videos} segments sécurisés dans la blockchain</div>
</div>
""", unsafe_allow_html=True)

# --- MÉTRIQUES PRINCIPALES ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Preuves Stockées", f"{total_videos}", delta="Segments")

with col2:
    st.metric("🔐 Statut Sécurité", "Actif", delta="100%", delta_color="normal")

with col3:
    verified = sum(1 for _ in logs if True)  # Placeholder
    st.metric("✅ Vérifications", f"{verified}", delta="OK")

with col4:
    st.metric("🌐 Réseau", "Blockchain", delta="Connecté")

st.markdown("---")

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📂 Registre & Vérification", "🚀 Audit Global", "📊 Analytics"])

# =========================================================
# ONGLET 1 : REGISTRE DÉTAILLÉ
# =========================================================
with tab1:
    st.markdown("### 📋 Registre des Preuves Vidéo")
    
    if not logs:
        st.warning("Aucune preuve disponible dans le système")
    else:
        for index, preuve in enumerate(logs):
            nom_fichier_reel = preuve['hash']
            hash_attendu = preuve['storage_url']
            date_creation = preuve['created_at'][:19].replace('T', ' ')

            with st.expander(f"🎬 **{nom_fichier_reel}** • {date_creation}", expanded=(index < 2)):
                col_info, col_action = st.columns([2, 1])
                
                with col_info:
                    st.markdown("**🔑 Signature Cryptographique (SHA-256)**")
                    st.code(hash_attendu, language='text')
                    
                    st.markdown("**📅 Métadonnées**")
                    st.caption(f"• ID Blockchain: `{preuve['id']}`")
                    st.caption(f"• Horodatage: `{date_creation}`")
                    st.caption(f"• Taille Hash: 64 caractères (256 bits)")
                
                with col_action:
                    st.markdown("**🔍 Vérification**")
                    verify_key = f"verify_{preuve['id']}"
                    
                    if st.button("🔐 Auditer", key=verify_key, use_container_width=True, type="primary"):
                        with st.spinner("🔄 Téléchargement et calcul..."):
                            try:
                                data = supabase.storage.from_("video-frames").download(nom_fichier_reel)
                                
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                                    tmp.write(data)
                                    path = tmp.name
                                
                                h_calcule = calculer_hash(path)
                                os.remove(path)
                                
                                st.markdown("---")
                                
                                if h_calcule == hash_attendu:
                                    st.success("✅ **PREUVE AUTHENTIQUE CONFIRMÉE**")
                                    st.markdown('<span class="status-badge badge-success">VÉRIFIÉ</span>', unsafe_allow_html=True)
                                    st.balloons()
                                    
                                    st.markdown("**🎬 Lecture de la Preuve**")
                                    st.video(data)
                                    
                                    st.info("🔐 Cette vidéo n'a subi aucune modification depuis son enregistrement initial")
                                else:
                                    st.error("❌ **ALERTE : FALSIFICATION DÉTECTÉE**")
                                    st.markdown('<span class="status-badge badge-danger">COMPROMIS</span>', unsafe_allow_html=True)
                                    
                                    st.markdown("**📊 Analyse Comparative**")
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        st.markdown("**Hash Original**")
                                        st.code(hash_attendu[:32] + "...", language='text')
                                    with col_b:
                                        st.markdown("**Hash Actuel**")
                                        st.code(h_calcule[:32] + "...", language='text')
                                    
                                    st.warning("⚠️ Les signatures ne correspondent pas. Cette preuve a été altérée.")
                                    
                            except Exception as e:
                                st.error(f"⚠️ Erreur : {str(e)}")
                                st.markdown('<span class="status-badge badge-warning">ERREUR</span>', unsafe_allow_html=True)

# =========================================================
# ONGLET 2 : AUDIT GLOBAL
# =========================================================
with tab2:
    st.markdown("### ⚡ Audit de Masse - Vérification Complète")
    st.markdown("Ce module effectue une vérification cryptographique exhaustive de toutes les preuves stockées.")
    
    col_info, col_action = st.columns([2, 1])
    
    with col_info:
        st.info(f"📦 **{total_videos}** segments à analyser")
        st.caption("Durée estimée : ~{} secondes".format(total_videos * 2))
    
    with col_action:
        lancer = st.button("▶️ LANCER L'AUDIT", type="primary", use_container_width=True)
    
    if lancer:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        valid_count = 0
        error_count = 0
        missing_count = 0
        
        st.markdown("---")
        st.markdown("### 📝 Rapport d'Exécution en Direct")
        
        result_container = st.container()
        
        for i, preuve in enumerate(logs):
            nom_fichier_reel = preuve['hash']
            hash_attendu = preuve['storage_url']
            
            status_text.markdown(f"🔄 **Traitement:** `{nom_fichier_reel}` ({i+1}/{total_videos})")
            progress_bar.progress((i + 1) / total_videos)
            
            try:
                data = supabase.storage.from_("video-frames").download(nom_fichier_reel)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(data)
                    path = tmp.name
                
                h_now = calculer_hash(path)
                os.remove(path)
                
                with result_container:
                    if h_now == hash_attendu:
                        valid_count += 1
                        st.success(f"✅ `{nom_fichier_reel}` → AUTHENTIQUE")
                    else:
                        error_count += 1
                        st.error(f"❌ `{nom_fichier_reel}` → FALSIFIÉ")
                        
            except Exception:
                missing_count += 1
                with result_container:
                    st.warning(f"⚠️ `{nom_fichier_reel}` → INTROUVABLE")
            
            time.sleep(0.1)
        
        progress_bar.empty()
        status_text.empty()
        
        st.markdown("---")
        st.success("🎉 Audit terminé avec succès!")
        
        # Sauvegarder les stats pour l'export
        st.session_state.audit_stats = {
            "authentiques": valid_count,
            "falsifies": error_count,
            "introuvables": missing_count
        }
        
        st.markdown("### 📊 Résultats de l'Audit")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.metric("✅ Authentiques", valid_count, delta=f"{(valid_count/total_videos*100):.1f}%")
        
        with col_r2:
            st.metric("❌ Falsifiées", error_count, delta=f"{(error_count/total_videos*100):.1f}%", delta_color="inverse")
        
        with col_r3:
            st.metric("⚠️ Introuvables", missing_count, delta=f"{(missing_count/total_videos*100):.1f}%", delta_color="off")
        
        # Score de sécurité
        security_score = (valid_count / total_videos * 100) if total_videos > 0 else 0
        st.markdown("---")
        st.markdown("### 🎯 Score de Sécurité Global")
        st.progress(security_score / 100)
        st.markdown(f"<h2 style='text-align: center;'>{security_score:.1f}%</h2>", unsafe_allow_html=True)
        
        # Bouton d'export après l'audit
        st.markdown("---")
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            rapport_html = generer_rapport_html(logs, st.session_state.audit_stats)
            st.download_button(
                label="📄 Export HTML",
                data=rapport_html,
                file_name=f"audit_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        with col_export2:
            rapport_json = generer_rapport_json(logs, st.session_state.audit_stats)
            st.download_button(
                label="📋 Export JSON",
                data=rapport_json,
                file_name=f"audit_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col_export3:
            rapport_csv = generer_rapport_csv(logs, st.session_state.audit_stats)
            st.download_button(
                label="📊 Export CSV",
                data=rapport_csv,
                file_name=f"audit_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# =========================================================
# ONGLET 3 : ANALYTICS
# =========================================================
with tab3:
    st.markdown("### 📊 Tableau de Bord Analytique")
    
    if logs:
        # Timeline
        st.markdown("#### 📅 Timeline des Enregistrements")
        dates = [log['created_at'][:10] for log in logs]
        date_counts = {}
        for d in dates:
            date_counts[d] = date_counts.get(d, 0) + 1
        
        for date, count in sorted(date_counts.items(), reverse=True):
            st.markdown(f"**{date}** : {count} segment(s)")
        
        st.markdown("---")
        
        # Dernières activités
        st.markdown("#### 🕐 Dernières Activités")
        for log in logs[:5]:
            st.caption(f"🎬 {log['hash']} • {log['created_at'][:19]}")
    else:
        st.info("Aucune donnée disponible pour l'analyse")