import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# ============================================================
# CONFIG
# ============================================================

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

st.set_page_config(
    page_title="NexFound — Demo prodotto",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Palette
PRIMARY = "#172B4D"
PRIMARY_2 = "#243B63"
ACCENT = "#2EC4B6"
ACCENT_DARK = "#1C9E93"
CORAL = "#FF6B6B"
AMBER = "#FFB347"
SUCCESS = "#22C55E"
TEXT = "#172B4D"
TEXT_2 = "#5D6B82"
TEXT_3 = "#8D98A8"
BG = "#F6F8FB"
CARD = "#FFFFFF"
BORDER = "#E8ECF3"

SETTORI = [
    "AI", "Fintech", "Climate Tech", "HealthTech", "SaaS B2B",
    "HR Tech", "PropTech", "Cybersecurity", "Mobility", "EdTech"
]
STADI = ["Idea", "MVP", "Traction", "Revenue"]
OBIETTIVI = ["Fundraising", "Pilot aziendale", "Partnership", "Mentorship", "Co-founder"]

SECTOR_COLORS = {
    "AI": "#6366F1",
    "Fintech": "#2EC4B6",
    "Climate Tech": "#22C55E",
    "HealthTech": "#EF4444",
    "SaaS B2B": "#3B82F6",
    "HR Tech": "#A855F7",
    "PropTech": "#F59E0B",
    "Cybersecurity": "#172B4D",
    "Mobility": "#06B6D4",
    "EdTech": "#EC4899",
}

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: {BG};
        }}

        .block-container {{
            max-width: 1240px;
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY} 0%, #0F1E36 100%);
            border-right: 1px solid rgba(46,196,182,0.18);
        }}

        section[data-testid="stSidebar"] * {{
            color: #D6E0EE !important;
        }}

        .nf-hero {{
            background: linear-gradient(135deg, {PRIMARY} 0%, #10213C 55%, {PRIMARY_2} 100%);
            border-radius: 22px;
            padding: 3rem;
            color: white;
            position: relative;
            overflow: hidden;
            margin-bottom: 1.6rem;
            border: 1px solid rgba(255,255,255,0.06);
        }}

        .nf-hero:before {{
            content: "";
            position: absolute;
            width: 460px;
            height: 460px;
            right: -120px;
            top: -120px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(46,196,182,0.18) 0%, transparent 70%);
        }}

        .nf-hero:after {{
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            left: -80px;
            bottom: -140px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(255,107,107,0.10) 0%, transparent 70%);
        }}

        .nf-hero h1 {{
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            margin: 0 0 0.4rem 0;
            position: relative;
        }}

        .nf-hero p {{
            font-size: 1.08rem;
            color: rgba(255,255,255,0.78);
            line-height: 1.65;
            max-width: 760px;
            margin: 0.4rem 0 1.5rem 0;
            position: relative;
        }}

        .nf-section-title {{
            margin-bottom: 0.2rem;
        }}

        .nf-section-title h2 {{
            color: {TEXT};
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.2rem;
        }}

        .nf-section-line {{
            width: 46px;
            height: 4px;
            border-radius: 999px;
            background: {ACCENT};
            margin-bottom: 0.9rem;
        }}

        .nf-section-sub {{
            color: {TEXT_2};
            font-size: 0.98rem;
            line-height: 1.55;
            margin-bottom: 1.4rem;
        }}

        .nf-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1.25rem 1.3rem;
            box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
            margin-bottom: 1rem;
        }}

        .nf-card-soft {{
            background: linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 100%);
        }}

        .nf-card-title {{
            font-size: 1.02rem;
            font-weight: 700;
            color: {TEXT};
            margin-bottom: 0.4rem;
        }}

        .nf-card-text {{
            font-size: 0.92rem;
            line-height: 1.65;
            color: {TEXT_2};
        }}

        .nf-kpi {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 15px;
            padding: 1rem 1.1rem;
            box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
            position: relative;
            overflow: hidden;
            margin-bottom: 0.9rem;
        }}

        .nf-kpi:before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {ACCENT}, {ACCENT_DARK});
        }}

        .nf-kpi-label {{
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
            color: {TEXT_3};
        }}

        .nf-kpi-value {{
            font-size: 1.9rem;
            color: {TEXT};
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.1;
            margin-top: 0.15rem;
        }}

        .nf-kpi-delta {{
            font-size: 0.78rem;
            font-weight: 600;
            color: {SUCCESS};
            margin-top: 0.3rem;
        }}

        .nf-pill {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.73rem;
            font-weight: 700;
            margin-right: 6px;
            margin-bottom: 6px;
            letter-spacing: 0.01em;
        }}

        .nf-pill-accent {{ background: rgba(46,196,182,0.12); color: {ACCENT_DARK}; }}
        .nf-pill-primary {{ background: rgba(23,43,77,0.08); color: {PRIMARY}; }}
        .nf-pill-coral {{ background: rgba(255,107,107,0.12); color: #D94B4B; }}
        .nf-pill-success {{ background: rgba(34,197,94,0.12); color: #16803C; }}
        .nf-pill-amber {{ background: rgba(255,179,71,0.18); color: #A76400; }}
        .nf-pill-gray {{ background: #F2F5FA; color: {TEXT_3}; }}

        .nf-profile {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1.25rem 1.3rem;
            box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
            margin-bottom: 0.9rem;
            transition: transform .18s ease;
        }}

        .nf-profile:hover {{
            transform: translateY(-2px);
        }}

        .nf-profile-head {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.7rem;
        }}

        .nf-avatar {{
            width: 42px;
            height: 42px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            flex-shrink: 0;
        }}

        .nf-avatar-startup {{ background: linear-gradient(135deg, {ACCENT}, {ACCENT_DARK}); }}
        .nf-avatar-company {{ background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_2}); }}
        .nf-avatar-investor {{ background: linear-gradient(135deg, {CORAL}, #E05555); }}

        .nf-profile-name {{
            font-weight: 800;
            color: {TEXT};
            font-size: 1rem;
            margin: 0;
            line-height: 1.15;
        }}

        .nf-profile-sub {{
            color: {TEXT_3};
            font-size: 0.8rem;
            margin: 0.12rem 0 0 0;
        }}

        .nf-profile-text {{
            color: {TEXT_2};
            font-size: 0.88rem;
            line-height: 1.55;
            margin-top: 0.45rem;
        }}

        .nf-progress-wrap {{
            margin-top: 0.55rem;
        }}

        .nf-progress-head {{
            display: flex;
            justify-content: space-between;
            color: {TEXT_3};
            font-size: 0.78rem;
            margin-bottom: 0.25rem;
        }}

        .nf-progress {{
            width: 100%;
            height: 7px;
            background: #EEF2F7;
            border-radius: 999px;
            overflow: hidden;
        }}

        .nf-progress-fill {{
            height: 100%;
            border-radius: 999px;
        }}

        .nf-spotlight {{
            background: linear-gradient(135deg, rgba(46,196,182,0.12) 0%, rgba(46,196,182,0.06) 100%);
            border: 1px solid rgba(46,196,182,0.18);
            border-radius: 18px;
            padding: 1.2rem 1.25rem;
            margin-bottom: 1rem;
        }}

        .nf-spotlight-title {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: {ACCENT_DARK};
            font-weight: 800;
            margin-bottom: 0.35rem;
        }}

        .nf-spotlight h3 {{
            font-size: 1.25rem;
            font-weight: 800;
            color: {TEXT};
            margin: 0 0 0.3rem 0;
        }}

        .nf-spotlight p {{
            font-size: 0.92rem;
            line-height: 1.6;
            color: {TEXT_2};
            margin: 0;
        }}

        .nf-step {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1.1rem 1.15rem;
            height: 100%;
        }}

        .nf-step-num {{
            width: 30px;
            height: 30px;
            border-radius: 999px;
            background: rgba(46,196,182,0.12);
            color: {ACCENT_DARK};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            margin-bottom: 0.65rem;
        }}

        .nf-match {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }}

        .nf-match:before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(180deg, {ACCENT}, {ACCENT_DARK});
        }}

        .nf-match-head {{
            display: flex;
            justify-content: space-between;
            gap: 14px;
            margin-bottom: 0.5rem;
        }}

        .nf-match-rank {{
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: {TEXT_3};
        }}

        .nf-match-name {{
            font-size: 1.05rem;
            font-weight: 800;
            color: {TEXT};
            margin: 0.1rem 0 0.25rem 0;
        }}

        .nf-match-score {{
            min-width: 72px;
            text-align: center;
        }}

        .nf-match-score-value {{
            font-size: 1.9rem;
            font-weight: 900;
            letter-spacing: -0.05em;
            line-height: 1;
        }}

        .nf-match-score-label {{
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {TEXT_3};
            margin-top: 0.1rem;
        }}

        .nf-list {{
            margin: 0.3rem 0 0 0;
            padding-left: 1rem;
            color: {TEXT_2};
            font-size: 0.88rem;
            line-height: 1.6;
        }}

        .nf-feed {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 0.95rem 1rem;
            display: flex;
            gap: 12px;
            align-items: flex-start;
            margin-bottom: 0.7rem;
        }}

        .nf-feed-icon {{
            width: 38px;
            height: 38px;
            border-radius: 11px;
            background: #F1F5FA;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .nf-feed-type {{
            font-size: 0.72rem;
            font-weight: 800;
            color: {ACCENT_DARK};
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        .nf-feed-text {{
            color: {TEXT};
            font-size: 0.9rem;
            line-height: 1.45;
        }}

        .nf-feed-time {{
            color: {TEXT_3};
            font-size: 0.76rem;
            white-space: nowrap;
        }}

        .nf-note {{
            background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DARK} 100%);
            border-radius: 18px;
            padding: 1.5rem 1.6rem;
            color: white;
            position: relative;
            overflow: hidden;
        }}

        .nf-note h3 {{
            margin: 0 0 0.35rem 0;
            font-size: 1.35rem;
            font-weight: 800;
        }}

        .nf-note p {{
            margin: 0;
            color: rgba(255,255,255,0.84);
            line-height: 1.6;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            font-weight: 700;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA
# ============================================================

@st.cache_data
def generate_startups(n=24):
    names = [
        "Nexara", "FinSmart", "GreenPulse", "MedIntel", "DataForge", "TalentUp",
        "CasaClick", "SecureNet", "MoveFlow", "LearnHub", "Visionary AI", "PayLoop",
        "SolarMind", "VitaLink", "CloudMetrics", "HireWise", "BuildView", "VaultEdge",
        "FleetPulse", "StudyVerse", "Predictiva", "CarbonLess", "NurseBot", "APILayer"
    ]
    founders = [
        "Alice Colombo", "Marco Fontana", "Giulia Bianchi", "Luca Moretti", "Sara Ricci", "Andrea Conti",
        "Francesca De Luca", "Davide Galli", "Elena Marchetti", "Tommaso Barbieri", "Chiara Ferro", "Lorenzo Mancini",
        "Valentina Rossetti", "Matteo Pellegrini", "Silvia Caruso", "Federico Villa", "Martina Fabbri", "Giorgio Testa",
        "Eleonora Grasso", "Alessandro Vitale", "Beatrice Amato", "Simone Lombardi", "Anna Leone", "Nicola Parisi"
    ]
    descriptions = [
        "Piattaforma di intelligenza artificiale per personalizzare il retail fisico e digitale.",
        "Soluzione fintech per micropagamenti e gestione finanziaria per freelance.",
        "Monitoraggio e riduzione delle emissioni di CO₂ per PMI tramite IoT.",
        "Sistema di triage medico basato su AI per pronto soccorso e cliniche.",
        "Suite SaaS per analytics predittive e reportistica automatizzata B2B.",
        "Piattaforma di talent matching basata su competenze e cultura aziendale.",
        "Piattaforma di valutazione immobiliare automatizzata con dati satellitari.",
        "Soluzione di cybersecurity avanzata per PMI e startup in cloud.",
        "App per la mobilità multimodale integrata nelle aree metropolitane.",
        "Piattaforma di microlearning personalizzato per formazione aziendale continua.",
        "Motore di visione artificiale per il controllo qualità industriale.",
        "Gateway di pagamento istantaneo con riconciliazione automatica per e-commerce.",
        "Software per la gestione e ottimizzazione di impianti fotovoltaici distribuiti.",
        "Piattaforma di telemedicina con monitoraggio remoto per pazienti cronici.",
        "Dashboard di business intelligence cloud-native per team distribuiti.",
        "Piattaforma di recruiting automation con screening AI-driven.",
        "Digital twin per cantieri edili e monitoraggio costruzioni.",
        "Piattaforma di gestione delle vulnerabilità e compliance automatizzata.",
        "Gestione intelligente di flotte aziendali e ottimizzazione consumi.",
        "Ambiente di apprendimento immersivo VR per università e corporate.",
        "Piattaforma predittiva per manutenzione industriale basata su sensori.",
        "Marketplace per crediti di carbonio verificati e trasparenti.",
        "Assistente virtuale AI per infermieri e personale sanitario.",
        "API management platform per microservizi enterprise."
    ]
    cities = [
        "Milano", "Roma", "Torino", "Bologna", "Firenze", "Napoli",
        "Padova", "Bergamo", "Genova", "Verona", "Bari", "Trieste"
    ]

    rng = np.random.RandomState(SEED)
    rows = []

    # Startup demo principale
    rows.append(
        {
            "nome": "Nexara",
            "settore": "AI",
            "descrizione": "Piattaforma di intelligenza artificiale che personalizza l’esperienza di acquisto in-store e online per il retail.",
            "stadio": "Traction",
            "citta": "Milano",
            "team_size": 11,
            "founder": "Alice Colombo",
            "obiettivo": "Pilot aziendale",
            "users": 5400,
            "mrr": 18000,
            "growth_pct": 22.4,
            "score_profilo": 92,
            "verificata": True,
            "funding_need": "Seed €500K–€1.2M",
            "readiness": "Alta",
        }
    )

    for i in range(1, n):
        settore = SETTORI[i % len(SETTORI)]
        stadio = STADI[rng.randint(0, len(STADI))]
        citta = cities[rng.randint(0, len(cities))]
        obiettivo = OBIETTIVI[rng.randint(0, len(OBIETTIVI))]
        team = int(rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 24, 32]))
        if stadio == "Idea":
            users = int(rng.randint(0, 80))
            mrr = 0
            growth = 0.0
            funding = "Pre-seed €50K–€150K"
            readiness = "In sviluppo"
        elif stadio == "MVP":
            users = int(rng.randint(80, 600))
            mrr = int(rng.randint(0, 2500))
            growth = round(rng.uniform(2, 15), 1)
            funding = "Seed €150K–€500K"
            readiness = "Media"
        elif stadio == "Traction":
            users = int(rng.randint(600, 12000))
            mrr = int(rng.randint(3000, 22000))
            growth = round(rng.uniform(5, 30), 1)
            funding = "Seed / Series A €500K–€2M"
            readiness = "Alta"
        else:
            users = int(rng.randint(5000, 95000))
            mrr = int(rng.randint(12000, 100000))
            growth = round(rng.uniform(3, 22), 1)
            funding = "Series A+ €1M–€5M"
            readiness = "Molto alta"

        rows.append(
            {
                "nome": names[i],
                "settore": settore,
                "descrizione": descriptions[i],
                "stadio": stadio,
                "citta": citta,
                "team_size": team,
                "founder": founders[i],
                "obiettivo": obiettivo,
                "users": users,
                "mrr": mrr,
                "growth_pct": growth,
                "score_profilo": int(rng.randint(58, 98)),
                "verificata": bool(rng.choice([True, False], p=[0.42, 0.58])),
                "funding_need": funding,
                "readiness": readiness,
            }
        )

    return pd.DataFrame(rows)


@st.cache_data
def generate_companies():
    rows = [
        {
            "nome": "RetailMax",
            "settore": "Retail",
            "dimensione": "Enterprise",
            "area_innovazione": "AI",
            "collaborazione": "Pilot",
            "citta": "Milano",
            "budget_class": "Alto",
            "tempo_valutazione_gg": 21,
            "descrizione": "Gruppo retail omnicanale alla ricerca di soluzioni AI per personalizzazione, analytics e customer experience.",
            "premium": True,
        },
        {
            "nome": "Gruppo Rinaldi",
            "settore": "Manifattura",
            "dimensione": "Enterprise",
            "area_innovazione": "AI",
            "collaborazione": "Pilot",
            "citta": "Torino",
            "budget_class": "Alto",
            "tempo_valutazione_gg": 30,
            "descrizione": "Gruppo industriale che investe in automazione, visione artificiale e ottimizzazione dei processi.",
            "premium": True,
        },
        {
            "nome": "Banca Meridiana",
            "settore": "Banking & Finance",
            "dimensione": "Enterprise",
            "area_innovazione": "Fintech",
            "collaborazione": "Investimento",
            "citta": "Roma",
            "budget_class": "Alto",
            "tempo_valutazione_gg": 45,
            "descrizione": "Istituto bancario con focus su open banking, digital onboarding e infrastrutture fintech.",
            "premium": True,
        },
        {
            "nome": "EnerVita",
            "settore": "Energia",
            "dimensione": "Enterprise",
            "area_innovazione": "Climate Tech",
            "collaborazione": "Partnership",
            "citta": "Milano",
            "budget_class": "Alto",
            "tempo_valutazione_gg": 35,
            "descrizione": "Utility energetica impegnata in smart grid, monitoraggio emissioni e transizione verde.",
            "premium": True,
        },
        {
            "nome": "FarmaItalia",
            "settore": "Farmaceutico",
            "dimensione": "Enterprise",
            "area_innovazione": "HealthTech",
            "collaborazione": "Pilot",
            "citta": "Roma",
            "budget_class": "Medio",
            "tempo_valutazione_gg": 40,
            "descrizione": "Azienda farmaceutica interessata a digital health, patient monitoring e automazione clinica.",
            "premium": False,
        },
        {
            "nome": "TechnoMedia",
            "settore": "Media & Tech",
            "dimensione": "Mid-market",
            "area_innovazione": "AI",
            "collaborazione": "Scouting",
            "citta": "Milano",
            "budget_class": "Medio",
            "tempo_valutazione_gg": 18,
            "descrizione": "Gruppo media-tech che esplora nuovi modelli di contenuto, recommendation e AI generativa.",
            "premium": True,
        },
        {
            "nome": "AutoItalia",
            "settore": "Automotive",
            "dimensione": "Enterprise",
            "area_innovazione": "Mobility",
            "collaborazione": "Partnership",
            "citta": "Torino",
            "budget_class": "Alto",
            "tempo_valutazione_gg": 50,
            "descrizione": "Corporate automotive interessata a mobilità connessa, fleet management e smart operations.",
            "premium": False,
        },
        {
            "nome": "InfoServices Group",
            "settore": "IT & Servizi",
            "dimensione": "Mid-market",
            "area_innovazione": "SaaS B2B",
            "collaborazione": "Partnership",
            "citta": "Bologna",
            "budget_class": "Medio",
            "tempo_valutazione_gg": 22,
            "descrizione": "System integrator che cerca partnership con startup SaaS e piattaforme enterprise.",
            "premium": False,
        },
        {
            "nome": "LogiTrans",
            "settore": "Logistica",
            "dimensione": "Mid-market",
            "area_innovazione": "Mobility",
            "collaborazione": "Pilot",
            "citta": "Verona",
            "budget_class": "Medio",
            "tempo_valutazione_gg": 24,
            "descrizione": "Operatore logistico che esplora ottimizzazione last-mile, flotte e routing intelligente.",
            "premium": False,
        },
        {
            "nome": "Costruzioni Lombarde",
            "settore": "Real Estate",
            "dimensione": "Mid-market",
            "area_innovazione": "PropTech",
            "collaborazione": "Pilot",
            "citta": "Bergamo",
            "budget_class": "Medio",
            "tempo_valutazione_gg": 27,
            "descrizione": "Azienda edile impegnata nella digitalizzazione dei cantieri e nello smart building.",
            "premium": False,
        },
        {
            "nome": "AssicuraPlus",
            "settore": "Assicurazioni",
            "dimensione": "Enterprise",
            "area_innovazione": "Cybersecurity",
            "collaborazione": "Scouting",
            "citta": "Trieste",
            "budget_class": "Alto",
            "tempo_valutazione_gg": 33,
            "descrizione": "Compagnia assicurativa che cerca startup cyber, antifrode e automazione sinistri.",
            "premium": True,
        },
        {
            "nome": "AgriSmart Italia",
            "settore": "Agricoltura",
            "dimensione": "PMI",
            "area_innovazione": "Climate Tech",
            "collaborazione": "Partnership",
            "citta": "Bologna",
            "budget_class": "Basso",
            "tempo_valutazione_gg": 16,
            "descrizione": "Impresa innovativa orientata a precision farming, sostenibilità e sensoristica.",
            "premium": False,
        },
    ]
    return pd.DataFrame(rows)


@st.cache_data
def generate_investors():
    rows = [
        {
            "nome": "Mediterraneo Ventures",
            "tipo": "VC",
            "ticket": "€500K–€3M",
            "ticket_min_k": 500,
            "ticket_max_k": 3000,
            "focus_stage": "Seed",
            "settori_preferiti": ["AI", "SaaS B2B", "Fintech"],
            "geografia": "Italia & Europa",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 7,
            "portfolio_size": 28,
            "thesis": "Investiamo in startup tech italiane con forte potenziale di scalabilità e vantaggio competitivo difendibile.",
        },
        {
            "nome": "Italian Angels Network",
            "tipo": "Angel",
            "ticket": "€20K–€100K",
            "ticket_min_k": 20,
            "ticket_max_k": 100,
            "focus_stage": "Pre-seed",
            "settori_preferiti": ["AI", "HealthTech", "EdTech", "Climate Tech"],
            "geografia": "Italia",
            "lead_follow": "Follow",
            "velocita_risposta_gg": 12,
            "portfolio_size": 16,
            "thesis": "Supportiamo founder visionari nella fase più iniziale, con forte mentoring operativo.",
        },
        {
            "nome": "Primo Capital",
            "tipo": "VC",
            "ticket": "€1M–€5M",
            "ticket_min_k": 1000,
            "ticket_max_k": 5000,
            "focus_stage": "Series A",
            "settori_preferiti": ["Fintech", "SaaS B2B", "Cybersecurity"],
            "geografia": "Europa",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 10,
            "portfolio_size": 34,
            "thesis": "Focus su round Series A per aziende con traction dimostrata e mercato europeo.",
        },
        {
            "nome": "TechSeed Fund",
            "tipo": "Micro-VC",
            "ticket": "€100K–€500K",
            "ticket_min_k": 100,
            "ticket_max_k": 500,
            "focus_stage": "Pre-seed",
            "settori_preferiti": ["AI", "SaaS B2B", "HR Tech"],
            "geografia": "Italia",
            "lead_follow": "Follow",
            "velocita_risposta_gg": 6,
            "portfolio_size": 12,
            "thesis": "Primo capitale per team tecnici brillanti che risolvono problemi reali.",
        },
        {
            "nome": "Innovation Bay Capital",
            "tipo": "VC",
            "ticket": "€500K–€2M",
            "ticket_min_k": 500,
            "ticket_max_k": 2000,
            "focus_stage": "Seed",
            "settori_preferiti": ["Climate Tech", "Mobility", "AI"],
            "geografia": "Italia",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 8,
            "portfolio_size": 20,
            "thesis": "Cerchiamo innovazione che genera impatto positivo su clima, mobilità e automazione.",
        },
        {
            "nome": "Alps Ventures",
            "tipo": "Micro-VC",
            "ticket": "€100K–€500K",
            "ticket_min_k": 100,
            "ticket_max_k": 500,
            "focus_stage": "Pre-seed",
            "settori_preferiti": ["PropTech", "SaaS B2B", "Fintech"],
            "geografia": "Nord Italia",
            "lead_follow": "Follow",
            "velocita_risposta_gg": 9,
            "portfolio_size": 11,
            "thesis": "Investiamo in startup che digitalizzano mercati tradizionali con software scalabile.",
        },
        {
            "nome": "Futuro Fund",
            "tipo": "VC",
            "ticket": "€1M–€5M",
            "ticket_min_k": 1000,
            "ticket_max_k": 5000,
            "focus_stage": "Series A",
            "settori_preferiti": ["AI", "HealthTech", "Cybersecurity"],
            "geografia": "Europa",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 14,
            "portfolio_size": 22,
            "thesis": "Puntiamo su AI e cybersecurity per un futuro digitale più sicuro.",
        },
        {
            "nome": "Digital Growth Partners",
            "tipo": "VC",
            "ticket": "€500K–€3M",
            "ticket_min_k": 500,
            "ticket_max_k": 3000,
            "focus_stage": "Seed",
            "settori_preferiti": ["SaaS B2B", "Fintech", "HR Tech"],
            "geografia": "Italia & Europa",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 11,
            "portfolio_size": 26,
            "thesis": "Supportiamo la crescita di piattaforme software B2B con metriche solide.",
        },
        {
            "nome": "EcoInvest",
            "tipo": "VC",
            "ticket": "€300K–€2M",
            "ticket_min_k": 300,
            "ticket_max_k": 2000,
            "focus_stage": "Seed",
            "settori_preferiti": ["Climate Tech", "Mobility", "PropTech"],
            "geografia": "Europa",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 13,
            "portfolio_size": 19,
            "thesis": "Investiamo esclusivamente in startup a impatto ambientale positivo.",
        },
        {
            "nome": "HealthVentures Italia",
            "tipo": "VC",
            "ticket": "€500K–€3M",
            "ticket_min_k": 500,
            "ticket_max_k": 3000,
            "focus_stage": "Seed",
            "settori_preferiti": ["HealthTech", "AI"],
            "geografia": "Italia",
            "lead_follow": "Lead",
            "velocita_risposta_gg": 9,
            "portfolio_size": 18,
            "thesis": "Focus verticale su digital health, medtech e AI clinica.",
        },
        {
            "nome": "Catalyst Angels",
            "tipo": "Angel",
            "ticket": "€10K–€80K",
            "ticket_min_k": 10,
            "ticket_max_k": 80,
            "focus_stage": "Pre-seed",
            "settori_preferiti": ["AI", "EdTech", "HealthTech", "Climate Tech"],
            "geografia": "Italia",
            "lead_follow": "Follow",
            "velocita_risposta_gg": 5,
            "portfolio_size": 9,
            "thesis": "Angel investing con forte coinvolgimento operativo e rete di contatti.",
        },
        {
            "nome": "NordEst Investimenti",
            "tipo": "Corporate VC",
            "ticket": "€300K–€2M",
            "ticket_min_k": 300,
            "ticket_max_k": 2000,
            "focus_stage": "Seed",
            "settori_preferiti": ["Mobility", "AI", "PropTech"],
            "geografia": "Nord-Est Italia",
            "lead_follow": "Follow",
            "velocita_risposta_gg": 15,
            "portfolio_size": 14,
            "thesis": "Corporate VC che connette startup alla rete industriale del Nord-Est.",
        },
    ]
    return pd.DataFrame(rows)


@st.cache_data
def generate_feed():
    return [
        {"icona": "🚀", "tipo": "Milestone", "testo": "Nexara ha superato 5.400 utenti attivi e il 22% di crescita mensile.", "tempo": "2 ore fa"},
        {"icona": "🏢", "tipo": "Challenge", "testo": "RetailMax cerca startup AI per personalizzazione in-store e pricing dinamico.", "tempo": "4 ore fa"},
        {"icona": "💰", "tipo": "Round aperto", "testo": "FinSmart ha aperto un round Seed da €400K sulla piattaforma.", "tempo": "6 ore fa"},
        {"icona": "🤝", "tipo": "Pilot", "testo": "GreenPulse ha avviato un pilot con EnerVita sul monitoraggio emissioni.", "tempo": "1 giorno fa"},
        {"icona": "✅", "tipo": "Verifica", "testo": "VitaLink ha completato la verifica del profilo startup.", "tempo": "1 giorno fa"},
        {"icona": "📋", "tipo": "Thesis", "testo": "Mediterraneo Ventures ha aggiornato la propria thesis su AI e vertical SaaS.", "tempo": "2 giorni fa"},
        {"icona": "🔔", "tipo": "Nuova azienda", "testo": "AssicuraPlus si è registrata per scouting Cybersecurity.", "tempo": "2 giorni fa"},
        {"icona": "📈", "tipo": "KPI", "testo": "Match generati +12% settimana su settimana.", "tempo": "3 giorni fa"},
    ]


# ============================================================
# MATCHING ENGINE
# ============================================================

STAGE_COMPAT_INV = {
    "Pre-seed": {"Idea": 95, "MVP": 70, "Traction": 30, "Revenue": 10},
    "Seed": {"Idea": 40, "MVP": 88, "Traction": 92, "Revenue": 45},
    "Series A": {"Idea": 5, "MVP": 30, "Traction": 90, "Revenue": 95},
    "Growth": {"Idea": 0, "MVP": 5, "Traction": 45, "Revenue": 92},
}

STAGE_COMPAT_CORP = {
    "PMI": {"Idea": 45, "MVP": 80, "Traction": 72, "Revenue": 60},
    "Mid-market": {"Idea": 20, "MVP": 60, "Traction": 90, "Revenue": 85},
    "Enterprise": {"Idea": 5, "MVP": 35, "Traction": 86, "Revenue": 95},
}

OBJ_COLLAB_MAP = {
    "Fundraising": {"Investimento": 92, "Scouting": 42, "Pilot": 20, "Partnership": 28},
    "Pilot aziendale": {"Pilot": 97, "Scouting": 72, "Partnership": 62, "Investimento": 18},
    "Partnership": {"Partnership": 95, "Pilot": 70, "Scouting": 55, "Investimento": 20},
    "Mentorship": {"Partnership": 50, "Pilot": 35, "Scouting": 50, "Investimento": 20},
    "Co-founder": {"Partnership": 35, "Pilot": 20, "Scouting": 25, "Investimento": 12},
}

RELATED_SECTORS = {
    "AI": ["SaaS B2B", "Cybersecurity", "HealthTech"],
    "Fintech": ["SaaS B2B", "Cybersecurity"],
    "Climate Tech": ["Mobility", "PropTech"],
    "HealthTech": ["AI", "EdTech"],
    "SaaS B2B": ["AI", "HR Tech", "Cybersecurity"],
    "HR Tech": ["SaaS B2B", "EdTech", "AI"],
    "PropTech": ["SaaS B2B", "Climate Tech"],
    "Cybersecurity": ["SaaS B2B", "AI", "Fintech"],
    "Mobility": ["Climate Tech", "AI"],
    "EdTech": ["HR Tech", "AI", "SaaS B2B"],
}

GEO_NORTH = {"Milano", "Torino", "Bergamo", "Padova", "Genova", "Verona", "Trieste"}
GEO_CENTER = {"Roma", "Bologna", "Firenze"}
GEO_SOUTH = {"Napoli", "Bari", "Palermo", "Catania"}


def geo_region(citta: str) -> str:
    if citta in GEO_NORTH:
        return "Nord"
    if citta in GEO_CENTER:
        return "Centro"
    return "Sud"


def compute_investor_match(startup, investor):
    scores = {}
    reasons = []

    s_sector = startup["settore"]
    inv_sectors = investor["settori_preferiti"]

    if s_sector in inv_sectors:
        scores["Settore"] = 96
        reasons.append(f"Il settore {s_sector} è esplicitamente tra i focus dell'investitore.")
    elif any(rel in inv_sectors for rel in RELATED_SECTORS.get(s_sector, [])):
        scores["Settore"] = 64
        reasons.append(f"Il settore {s_sector} è affine ai focus dell'investitore.")
    else:
        scores["Settore"] = 16

    stage_score = STAGE_COMPAT_INV.get(investor["focus_stage"], {}).get(startup["stadio"], 30)
    scores["Stadio"] = stage_score
    if stage_score >= 80:
        reasons.append(f"Lo stadio {startup['stadio']} è coerente con il focus {investor['focus_stage']}.")

    inv_geo = investor["geografia"]
    s_region = geo_region(startup["citta"])
    if "Europa" in inv_geo or inv_geo == "Italia" or inv_geo == "Italia & Europa":
        scores["Geografia"] = 86
    elif "Nord" in inv_geo and s_region == "Nord":
        scores["Geografia"] = 95
        reasons.append("Allineamento geografico favorevole.")
    elif "Sud" in inv_geo and s_region == "Sud":
        scores["Geografia"] = 95
    else:
        scores["Geografia"] = 52

    need_map = {"Idea": 100, "MVP": 300, "Traction": 900, "Revenue": 2500}
    need = need_map[startup["stadio"]]

    if investor["ticket_min_k"] <= need <= investor["ticket_max_k"]:
        scores["Ticket"] = 95
        reasons.append("Il ticket è compatibile con il fabbisogno stimato della startup.")
    elif investor["ticket_min_k"] <= need * 1.3 and need * 0.6 <= investor["ticket_max_k"]:
        scores["Ticket"] = 66
    else:
        scores["Ticket"] = 20

    weights = {"Settore": 0.30, "Stadio": 0.25, "Geografia": 0.15, "Ticket": 0.30}
    overall = round(sum(scores[k] * weights[k] for k in weights))
    return overall, scores, reasons


def compute_company_match(startup, company):
    scores = {}
    reasons = []

    if startup["settore"] == company["area_innovazione"]:
        scores["Settore"] = 96
        reasons.append(f"L'area di innovazione {company['area_innovazione']} coincide con il settore della startup.")
    elif startup["settore"] in RELATED_SECTORS.get(company["area_innovazione"], []):
        scores["Settore"] = 60
        reasons.append("Il settore della startup è affine alle priorità di innovazione dell'azienda.")
    else:
        scores["Settore"] = 18

    collab_score = OBJ_COLLAB_MAP.get(startup["obiettivo"], {}).get(company["collaborazione"], 25)
    scores["Collaborazione"] = collab_score
    if collab_score >= 70:
        reasons.append(f"L'obiettivo '{startup['obiettivo']}' è compatibile con '{company['collaborazione']}'.")

    stage_score = STAGE_COMPAT_CORP.get(company["dimensione"], {}).get(startup["stadio"], 35)
    scores["Stadio"] = stage_score
    if stage_score >= 75:
        reasons.append(f"La maturità della startup è adatta a una {company['dimensione']}.")

    if geo_region(startup["citta"]) == geo_region(company["citta"]):
        scores["Geografia"] = 90
        reasons.append("La prossimità geografica rende più semplice avviare un pilot.")
    else:
        scores["Geografia"] = 55

    weights = {"Settore": 0.35, "Collaborazione": 0.30, "Stadio": 0.20, "Geografia": 0.15}
    overall = round(sum(scores[k] * weights[k] for k in weights))
    return overall, scores, reasons


# ============================================================
# HELPERS
# ============================================================

def initials(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()


def truncate(text: str, max_len=120) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "..."


def score_color(score: int) -> str:
    if score >= 80:
        return ACCENT
    if score >= 60:
        return AMBER
    return CORAL


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="nf-section-title"><h2>{title}</h2></div>
        <div class="nf-section-line"></div>
        <div class="nf-section-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, icon: str = "", delta: str = ""):
    st.markdown(
        f"""
        <div class="nf-kpi">
            <div style="font-size:1.35rem;">{icon}</div>
            <div class="nf-kpi-label">{label}</div>
            <div class="nf-kpi-value">{value}</div>
            <div class="nf-kpi-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def profile_progress(score: int, label: str = "Qualità profilo") -> str:
    return f"""
    <div class="nf-progress-wrap">
        <div class="nf-progress-head">
            <span>{label}</span>
            <span style="font-weight:700; color:{score_color(score)};">{score}%</span>
        </div>
        <div class="nf-progress">
            <div class="nf-progress-fill" style="width:{score}%; background:{score_color(score)};"></div>
        </div>
    </div>
    """


def startup_card_html(s) -> str:
    badges = (
        f'<span class="nf-pill nf-pill-accent">{s["settore"]}</span>'
        f'<span class="nf-pill nf-pill-coral">{s["stadio"]}</span>'
        f'<span class="nf-pill nf-pill-primary">{s["obiettivo"]}</span>'
    )
    if s["verificata"]:
        badges += '<span class="nf-pill nf-pill-success">Verificata</span>'

    return f"""
    <div class="nf-profile">
        <div class="nf-profile-head">
            <div class="nf-avatar nf-avatar-startup">{initials(s["nome"])}</div>
            <div>
                <div class="nf-profile-name">{s["nome"]}</div>
                <div class="nf-profile-sub">{s["founder"]} · 📍 {s["citta"]}</div>
            </div>
        </div>
        <div>{badges}</div>
        <div class="nf-profile-text">{truncate(s["descrizione"], 110)}</div>
        <div class="nf-profile-sub" style="margin-top:0.45rem;">👥 {s["team_size"]} persone · 💰 {s["funding_need"]}</div>
        {profile_progress(int(s["score_profilo"]))}
    </div>
    """


def company_card_html(c) -> str:
    badges = (
        f'<span class="nf-pill nf-pill-accent">{c["area_innovazione"]}</span>'
        f'<span class="nf-pill nf-pill-coral">{c["dimensione"]}</span>'
        f'<span class="nf-pill nf-pill-primary">{c["collaborazione"]}</span>'
    )
    if c["premium"]:
        badges += '<span class="nf-pill nf-pill-amber">Premium</span>'

    return f"""
    <div class="nf-profile">
        <div class="nf-profile-head">
            <div class="nf-avatar nf-avatar-company">{initials(c["nome"])}</div>
            <div>
                <div class="nf-profile-name">{c["nome"]}</div>
                <div class="nf-profile-sub">{c["settore"]} · 📍 {c["citta"]}</div>
            </div>
        </div>
        <div>{badges}</div>
        <div class="nf-profile-text">{truncate(c["descrizione"], 120)}</div>
        <div class="nf-profile-sub" style="margin-top:0.45rem;">💳 Budget {c["budget_class"]} · ⏱️ {c["tempo_valutazione_gg"]} giorni</div>
    </div>
    """


def investor_card_html(i) -> str:
    badges = (
        f'<span class="nf-pill nf-pill-accent">{i["tipo"]}</span>'
        f'<span class="nf-pill nf-pill-coral">{i["focus_stage"]}</span>'
        f'<span class="nf-pill nf-pill-primary">{i["lead_follow"]}</span>'
    )
    sectors = ", ".join(i["settori_preferiti"][:3])
    return f"""
    <div class="nf-profile">
        <div class="nf-profile-head">
            <div class="nf-avatar nf-avatar-investor">{initials(i["nome"])}</div>
            <div>
                <div class="nf-profile-name">{i["nome"]}</div>
                <div class="nf-profile-sub">{i["geografia"]}</div>
            </div>
        </div>
        <div>{badges}</div>
        <div class="nf-profile-text">{truncate(i["thesis"], 120)}</div>
        <div class="nf-profile-sub" style="margin-top:0.45rem;">🎯 {sectors} · 💰 {i["ticket"]}</div>
    </div>
    """


def radar_chart(scores_dict, title=""):
    cats = list(scores_dict.keys())
    vals = list(scores_dict.values())
    cats = cats + [cats[0]]
    vals = vals + [vals[0]]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=vals,
            theta=cats,
            fill="toself",
            fillcolor="rgba(46,196,182,0.18)",
            line=dict(color=ACCENT, width=2.5),
            marker=dict(color=ACCENT, size=5),
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(0,0,0,0.08)"),
            angularaxis=dict(gridcolor="rgba(0,0,0,0.08)"),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title=title,
        height=280,
        margin=dict(l=40, r=40, t=40, b=30),
    )
    return fig


def safe_append_request(req_dict):
    exists = any(
        r["startup"] == req_dict["startup"] and r["target"] == req_dict["target"] and r["tipo"] == req_dict["tipo"]
        for r in st.session_state.contact_requests
    )
    if not exists:
        st.session_state.contact_requests.append(req_dict)


def goto(page_name: str):
    st.session_state.page = page_name


def get_top_investor_matches(startup_row, investors_df, n=5):
    results = []
    for _, inv in investors_df.iterrows():
        score, subs, reasons = compute_investor_match(startup_row, inv)
        results.append(
            {
                "nome": inv["nome"],
                "tipo": inv["tipo"],
                "ticket": inv["ticket"],
                "geografia": inv["geografia"],
                "focus_stage": inv["focus_stage"],
                "settori_preferiti": inv["settori_preferiti"],
                "score": score,
                "sub_scores": subs,
                "reasons": reasons,
            }
        )
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:n], results


def get_top_company_matches(startup_row, companies_df, n=5):
    results = []
    for _, co in companies_df.iterrows():
        score, subs, reasons = compute_company_match(startup_row, co)
        results.append(
            {
                "nome": co["nome"],
                "dimensione": co["dimensione"],
                "collaborazione": co["collaborazione"],
                "area_innovazione": co["area_innovazione"],
                "citta": co["citta"],
                "score": score,
                "sub_scores": subs,
                "reasons": reasons,
            }
        )
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:n], results


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

if "demo_startup" not in st.session_state:
    st.session_state.demo_startup = "Nexara"

if "saved_matches" not in st.session_state:
    st.session_state.saved_matches = []

if "contact_requests" not in st.session_state:
    st.session_state.contact_requests = [
        {
            "startup": "Nexara",
            "target": "RetailMax",
            "tipo": "Azienda",
            "score": 91,
            "stato": "Call programmata",
            "data": "14/03/2026 10:30",
        },
        {
            "startup": "Nexara",
            "target": "Mediterraneo Ventures",
            "tipo": "Investitore",
            "score": 88,
            "stato": "In revisione",
            "data": "15/03/2026 15:10",
        },
    ]

# ============================================================
# LOAD DATA
# ============================================================

df_startups = generate_startups()
df_companies = generate_companies()
df_investors = generate_investors()
feed_items = generate_feed()

DEMO_STARTUP_ROW = df_startups[df_startups["nome"] == st.session_state.demo_startup].iloc[0]
TOP_DEMO_INV, ALL_DEMO_INV = get_top_investor_matches(DEMO_STARTUP_ROW, df_investors, n=5)
TOP_DEMO_CO, ALL_DEMO_CO = get_top_company_matches(DEMO_STARTUP_ROW, df_companies, n=5)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding-top:0.4rem; padding-bottom:0.75rem;">
            <div style="font-size:1.75rem; font-weight:900; letter-spacing:-0.04em;">
                🔗 <span style="color:{ACCENT};">NexFound</span>
            </div>
            <div style="font-size:0.72rem; color:rgba(214,224,238,0.55); text-transform:uppercase; letter-spacing:0.08em;">
                Demo prodotto · caso d'uso
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Percorso demo consigliato")
    if st.button("1. Home", use_container_width=True):
        goto("🏠 Home")
    if st.button("2. Problema", use_container_width=True):
        goto("⚡ Problema di Mercato")
    if st.button("3. Caso d'uso guidato", use_container_width=True):
        goto("🧭 Caso d'uso guidato")
    if st.button("4. Matching intelligente", use_container_width=True):
        goto("🎯 Matching Intelligente")
    if st.button("5. Flusso di contatto", use_container_width=True):
        goto("📨 Flusso di Contatto")
    if st.button("6. Dashboard KPI", use_container_width=True):
        goto("📊 Dashboard KPI")
    if st.button("7. Conclusione", use_container_width=True):
        goto("✨ Conclusione")

    st.markdown("---")
    st.markdown("### Esplora il prodotto")
    page_select = st.radio(
        "Navigazione",
        [
            "🏠 Home",
            "⚡ Problema di Mercato",
            "🔗 Ecosistema",
            "🧭 Caso d'uso guidato",
            "🎯 Matching Intelligente",
            "📨 Flusso di Contatto",
            "📚 Directory",
            "📰 Feed Piattaforma",
            "📊 Dashboard KPI",
            "✨ Conclusione",
        ],
        index=[
            "🏠 Home",
            "⚡ Problema di Mercato",
            "🔗 Ecosistema",
            "🧭 Caso d'uso guidato",
            "🎯 Matching Intelligente",
            "📨 Flusso di Contatto",
            "📚 Directory",
            "📰 Feed Piattaforma",
            "📊 Dashboard KPI",
            "✨ Conclusione",
        ].index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = page_select

    st.markdown("---")
    st.markdown(
        f"""
        <div style="font-size:0.76rem; color:rgba(214,224,238,0.62); line-height:1.7;">
            <b>Come leggere la demo</b><br>
            Questa app usa dati sintetici ma realistici per mostrare come NexFound funzionerebbe come prodotto.<br><br>
            <b>Focus della presentazione:</b><br>
            • Alice / Nexara come caso d'uso<br>
            • matching spiegabile<br>
            • passaggio da profilo → contatto → call
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SECTIONS
# ============================================================

def section_home():
    st.markdown(
        f"""
        <div class="nf-hero">
            <h1>Nex<span style="color:{ACCENT};">Found</span></h1>
            <p>
                La piattaforma che connette <b>startup</b>, <b>aziende</b> e <b>investitori</b>
                con un motore di matching intelligente, profili strutturati e flussi di contatto
                pensati per trasformare opportunità potenziali in collaborazioni concrete.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Campione startup demo", str(len(df_startups)), "🚀", "dataset sintetico")
    with c2:
        kpi_card("Campione aziende demo", str(len(df_companies)), "🏢", "dataset sintetico")
    with c3:
        kpi_card("Campione investitori demo", str(len(df_investors)), "💰", "dataset sintetico")
    with c4:
        kpi_card("Match simulati", "1.247", "🎯", "+12% vs mese prec.")

    st.markdown(
        f"""
        <div class="nf-card nf-card-soft">
            <div class="nf-card-title">Perché questa demo funziona in presentazione</div>
            <div class="nf-card-text">
                Invece di mostrare solo schermate e directory, la demo segue un caso d'uso preciso:
                <b>Alice Colombo</b>, founder di <b>Nexara</b>, entra in piattaforma, completa il profilo,
                riceve match rilevanti, invia una richiesta di contatto e arriva a una call.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="nf-spotlight">
            <div class="nf-spotlight-title">Demo moment</div>
            <h3>Nexara riceve subito 3 match ad alta compatibilità</h3>
            <p>
                La piattaforma suggerisce opportunità rilevanti in pochi secondi,
                spiegando perché il match è forte.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    p1, p2, p3 = st.columns(3)
    for col, item in zip(
        [p1, p2, p3],
        [
            {"label": "Corporate #1", "name": TOP_DEMO_CO[0]["nome"], "score": TOP_DEMO_CO[0]["score"], "meta": TOP_DEMO_CO[0]["collaborazione"]},
            {"label": "Corporate #2", "name": TOP_DEMO_CO[1]["nome"], "score": TOP_DEMO_CO[1]["score"], "meta": TOP_DEMO_CO[1]["collaborazione"]},
            {"label": "Investor #1", "name": TOP_DEMO_INV[0]["nome"], "score": TOP_DEMO_INV[0]["score"], "meta": TOP_DEMO_INV[0]["focus_stage"]},
        ],
    ):
        with col:
            st.markdown(
                f"""
                <div class="nf-match">
                    <div class="nf-match-head">
                        <div>
                            <div class="nf-match-rank">{item["label"]}</div>
                            <div class="nf-match-name">{item["name"]}</div>
                            <span class="nf-pill nf-pill-primary">{item["meta"]}</span>
                        </div>
                        <div class="nf-match-score">
                            <div class="nf-match-score-value" style="color:{score_color(item["score"])};">{item["score"]}%</div>
                            <div class="nf-match-score-label">Fit</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    b1, b2, b3 = st.columns([1.2, 1.2, 3])
    with b1:
        if st.button("Apri il caso d'uso", use_container_width=True, type="primary"):
            goto("🧭 Caso d'uso guidato")
            st.rerun()
    with b2:
        if st.button("Vai al matching", use_container_width=True):
            goto("🎯 Matching Intelligente")
            st.rerun()


def section_problema():
    section_header(
        "Il problema di mercato",
        "Startup, aziende e investitori hanno interessi compatibili, ma oggi faticano ancora a incontrarsi nel modo giusto."
    )

    tabs = st.tabs(["🚀 Startup", "🏢 Aziende", "💰 Investitori"])

    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        data = [
            ("Poca visibilità qualificata", "Molte startup hanno buone idee ma non raggiungono le persone giuste."),
            ("Accesso limitato", "Arrivare a corporate e investitori richiede spesso network personale o eventi casuali."),
            ("Contatti poco rilevanti", "La maggior parte dell'outreach genera conversazioni a basso potenziale."),
        ]
        for col, (title, text) in zip([c1, c2, c3], data):
            with col:
                st.markdown(f'<div class="nf-card"><div class="nf-card-title">{title}</div><div class="nf-card-text">{text}</div></div>', unsafe_allow_html=True)

    with tabs[1]:
        c1, c2, c3 = st.columns(3)
        data = [
            ("Scouting dispersivo", "Le aziende faticano a costruire pipeline di innovazione efficienti."),
            ("Filtraggio inefficiente", "Capire quali startup meritano attenzione richiede tempo e risorse."),
            ("Canale poco strutturato", "Open innovation e venture clienting sono spesso gestiti in modo artigianale."),
        ]
        for col, (title, text) in zip([c1, c2, c3], data):
            with col:
                st.markdown(f'<div class="nf-card"><div class="nf-card-title">{title}</div><div class="nf-card-text">{text}</div></div>', unsafe_allow_html=True)

    with tabs[2]:
        c1, c2, c3 = st.columns(3)
        data = [
            ("Deal flow rumoroso", "Troppi profili, pochi segnali chiari."),
            ("Poche metriche strutturate", "La comparabilità tra startup early-stage è ancora debole."),
            ("Tempo sprecato", "Il filtraggio manuale toglie spazio ad analisi, relazione e supporto."),
        ]
        for col, (title, text) in zip([c1, c2, c3], data):
            with col:
                st.markdown(f'<div class="nf-card"><div class="nf-card-title">{title}</div><div class="nf-card-text">{text}</div></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="nf-note">
            <h3>NexFound non è un social generico</h3>
            <p>
                È una piattaforma di matching e relazione che aiuta le startup a emergere,
                le aziende a fare scouting e gli investitori a trovare deal flow qualificato.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_ecosistema():
    section_header(
        "L'ecosistema NexFound",
        "Tre attori, una piattaforma, un flusso chiaro dall'incontro all'opportunità."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">🚀 Startup</div>
                <div class="nf-card-text">
                    • Profilo strutturato<br>
                    • Badge di verifica<br>
                    • Match automatici<br>
                    • Visibilità qualificata<br>
                    • Gestione intro e follow-up
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">🏢 Aziende</div>
                <div class="nf-card-text">
                    • Scouting più ordinato<br>
                    • Ricerca per settore/stadio<br>
                    • Pilot e partnership<br>
                    • Open innovation più veloce<br>
                    • Pipeline interna più chiara
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">💰 Investitori</div>
                <div class="nf-card-text">
                    • Deal flow più filtrato<br>
                    • Startup comparabili<br>
                    • Thesis più applicabile<br>
                    • Riduzione del rumore<br>
                    • Focus sulle opportunità giuste
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="nf-card nf-card-soft">
            <div class="nf-card-title">Flusso di valore</div>
            <div class="nf-card-text">
                <b>Profilo startup</b> → <b>Matching intelligente</b> → <b>Richiesta di contatto</b> →
                <b>Intro accettata</b> → <b>Call / pilot / investimento</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_case_study():
    s = DEMO_STARTUP_ROW
    section_header(
        "Caso d'uso guidato — Alice e Nexara",
        "Questa è la parte da mostrare in presentazione: una founder entra, viene scoperta e apre contatti di qualità."
    )

    left, right = st.columns([1.55, 1])

    with left:
        st.markdown(
            f"""
            <div class="nf-spotlight">
                <div class="nf-spotlight-title">Founder scenario</div>
                <h3>Alice Colombo vuole aprire un pilot con una corporate retail</h3>
                <p>
                    Alice è founder di <b>Nexara</b>, una startup AI in fase di <b>{s["stadio"]}</b>.
                    Ha già traction, un team di <b>{s["team_size"]}</b> persone e una priorità molto chiara:
                    trovare un <b>pilot aziendale</b> con un gruppo retail o una corporate interessata alla personalizzazione customer-facing.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(startup_card_html(s), unsafe_allow_html=True)

    with right:
        k1, k2 = st.columns(2)
        with k1:
            kpi_card("Utenti", f'{int(s["users"]):,}', "👥", "attivi")
        with k2:
            kpi_card("MRR", f'€{int(s["mrr"]):,}', "💰", "ricavi mensili")
        k3, k4 = st.columns(2)
        with k3:
            kpi_card("Crescita", f'{s["growth_pct"]}%', "📈", "mese su mese")
        with k4:
            kpi_card("Profilo", f'{s["score_profilo"]}/100', "⭐", "readiness alta")

    st.markdown("### Il percorso di Alice su NexFound")
    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("1", "Compila il profilo", "Inserisce settore, stage, traction, obiettivi e materiali chiave."),
        ("2", "Riceve match", "La piattaforma genera corporate e investitori compatibili."),
        ("3", "Invia richiesta", "Alice manda una intro request contestualizzata."),
        ("4", "Avvia la relazione", "La richiesta viene accettata e si passa a call o pilot."),
    ]
    for col, (num, title, text) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(
                f"""
                <div class="nf-step">
                    <div class="nf-step-num">{num}</div>
                    <div class="nf-card-title">{title}</div>
                    <div class="nf-card-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### I match che contano davvero")
    mc1, mc2 = st.columns(2)

    with mc1:
        st.markdown("**Top corporate per Nexara**")
        for r in TOP_DEMO_CO[:3]:
            st.markdown(
                f"""
                <div class="nf-match">
                    <div class="nf-match-head">
                        <div>
                            <div class="nf-match-rank">Corporate match</div>
                            <div class="nf-match-name">{r["nome"]}</div>
                            <span class="nf-pill nf-pill-accent">{r["area_innovazione"]}</span>
                            <span class="nf-pill nf-pill-primary">{r["collaborazione"]}</span>
                        </div>
                        <div class="nf-match-score">
                            <div class="nf-match-score-value" style="color:{score_color(r["score"])};">{r["score"]}%</div>
                            <div class="nf-match-score-label">Compatibilità</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with mc2:
        st.markdown("**Top investitori per Nexara**")
        for r in TOP_DEMO_INV[:3]:
            st.markdown(
                f"""
                <div class="nf-match">
                    <div class="nf-match-head">
                        <div>
                            <div class="nf-match-rank">Investor match</div>
                            <div class="nf-match-name">{r["nome"]}</div>
                            <span class="nf-pill nf-pill-accent">{r["tipo"]}</span>
                            <span class="nf-pill nf-pill-primary">{r["focus_stage"]}</span>
                        </div>
                        <div class="nf-match-score">
                            <div class="nf-match-score-value" style="color:{score_color(r["score"])};">{r["score"]}%</div>
                            <div class="nf-match-score-label">Compatibilità</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    b1, b2 = st.columns([1.3, 4])
    with b1:
        if st.button("Apri il matching", use_container_width=True, type="primary"):
            goto("🎯 Matching Intelligente")
            st.rerun()
    with b2:
        st.caption("Suggerimento demo: da qui passa subito alla sezione Matching Intelligente e apri Nexara.")


def section_matching():
    section_header(
        "Matching Intelligente",
        "Il cuore del prodotto: ogni connessione è motivata, spiegabile e presentabile."
    )

    startup_name = st.selectbox(
        "Seleziona una startup",
        df_startups["nome"].tolist(),
        index=df_startups["nome"].tolist().index(st.session_state.demo_startup) if st.session_state.demo_startup in df_startups["nome"].tolist() else 0,
    )
    s = df_startups[df_startups["nome"] == startup_name].iloc[0]

    st.markdown(startup_card_html(s), unsafe_allow_html=True)

    mode = st.radio("Tipo di matching", ["Corporate", "Investitori"], horizontal=True)

    if mode == "Corporate":
        top_matches, all_matches = get_top_company_matches(s, df_companies, n=5)
        best = top_matches[0]

        st.markdown(
            f"""
            <div class="nf-spotlight">
                <div class="nf-spotlight-title">Best match</div>
                <h3>{best["nome"]} — {best["score"]}% di compatibilità</h3>
                <p>
                    È il match corporate più forte per <b>{s["nome"]}</b> in base a settore,
                    tipologia di collaborazione, maturità della startup e vicinanza operativa.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for idx, r in enumerate(top_matches):
            col_a, col_b = st.columns([3.1, 1.9])
            with col_a:
                reasons_html = "".join([f"<li>{x}</li>" for x in r["reasons"]]) if r["reasons"] else "<li>Compatibilità parziale.</li>"
                st.markdown(
                    f"""
                    <div class="nf-match">
                        <div class="nf-match-head">
                            <div>
                                <div class="nf-match-rank">Match #{idx+1}</div>
                                <div class="nf-match-name">{r["nome"]}</div>
                                <span class="nf-pill nf-pill-accent">{r["area_innovazione"]}</span>
                                <span class="nf-pill nf-pill-coral">{r["dimensione"]}</span>
                                <span class="nf-pill nf-pill-primary">{r["collaborazione"]}</span>
                            </div>
                            <div class="nf-match-score">
                                <div class="nf-match-score-value" style="color:{score_color(r["score"])};">{r["score"]}%</div>
                                <div class="nf-match-score-label">Fit</div>
                            </div>
                        </div>
                        <div class="nf-card-text" style="margin-top:0.3rem;"><b>Perché questo match è forte</b></div>
                        <ul class="nf-list">{reasons_html}</ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Salva match con {r['nome']}", key=f"save_co_{idx}", use_container_width=True):
                    record = {"startup": s["nome"], "target": r["nome"], "tipo": "Azienda", "score": r["score"]}
                    if record not in st.session_state.saved_matches:
                        st.session_state.saved_matches.append(record)
                    st.success(f"Match salvato: {r['nome']}")
            with col_b:
                st.plotly_chart(radar_chart(r["sub_scores"], "Score per criterio"), use_container_width=True, key=f"rad_co_{idx}")

    else:
        top_matches, all_matches = get_top_investor_matches(s, df_investors, n=5)
        best = top_matches[0]

        st.markdown(
            f"""
            <div class="nf-spotlight">
                <div class="nf-spotlight-title">Best match</div>
                <h3>{best["nome"]} — {best["score"]}% di compatibilità</h3>
                <p>
                    È il miglior investitore per <b>{s["nome"]}</b> considerando focus settoriale,
                    stage thesis, ticket e geografia.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for idx, r in enumerate(top_matches):
            col_a, col_b = st.columns([3.1, 1.9])
            with col_a:
                reasons_html = "".join([f"<li>{x}</li>" for x in r["reasons"]]) if r["reasons"] else "<li>Compatibilità parziale.</li>"
                sectors = ", ".join(r["settori_preferiti"][:3])
                st.markdown(
                    f"""
                    <div class="nf-match">
                        <div class="nf-match-head">
                            <div>
                                <div class="nf-match-rank">Match #{idx+1}</div>
                                <div class="nf-match-name">{r["nome"]}</div>
                                <span class="nf-pill nf-pill-accent">{r["tipo"]}</span>
                                <span class="nf-pill nf-pill-coral">{r["focus_stage"]}</span>
                                <span class="nf-pill nf-pill-primary">{r["ticket"]}</span>
                                <div class="nf-profile-sub" style="margin-top:0.35rem;">🎯 {sectors}</div>
                            </div>
                            <div class="nf-match-score">
                                <div class="nf-match-score-value" style="color:{score_color(r["score"])};">{r["score"]}%</div>
                                <div class="nf-match-score-label">Fit</div>
                            </div>
                        </div>
                        <div class="nf-card-text" style="margin-top:0.3rem;"><b>Perché questo match è forte</b></div>
                        <ul class="nf-list">{reasons_html}</ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Salva match con {r['nome']}", key=f"save_inv_{idx}", use_container_width=True):
                    record = {"startup": s["nome"], "target": r["nome"], "tipo": "Investitore", "score": r["score"]}
                    if record not in st.session_state.saved_matches:
                        st.session_state.saved_matches.append(record)
                    st.success(f"Match salvato: {r['nome']}")
            with col_b:
                st.plotly_chart(radar_chart(r["sub_scores"], "Score per criterio"), use_container_width=True, key=f"rad_inv_{idx}")

    scores_dist = [x["score"] for x in all_matches]
    bins = ["0–30", "31–50", "51–70", "71–85", "86–100"]
    counts = [
        sum(s <= 30 for s in scores_dist),
        sum(31 <= s <= 50 for s in scores_dist),
        sum(51 <= s <= 70 for s in scores_dist),
        sum(71 <= s <= 85 for s in scores_dist),
        sum(86 <= s <= 100 for s in scores_dist),
    ]
    fig = px.bar(
        x=bins,
        y=counts,
        labels={"x": "Fascia punteggio", "y": "Numero match"},
        color_discrete_sequence=[ACCENT],
    )
    fig.update_layout(
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)")
    )
    st.plotly_chart(fig, use_container_width=True)

    cta1, cta2 = st.columns([1.4, 4])
    with cta1:
        if st.button("Vai al contatto", use_container_width=True, type="primary"):
            goto("📨 Flusso di Contatto")
            st.rerun()


def section_contatto():
    section_header(
        "Flusso di Contatto",
        "Qui la demo smette di essere una directory e diventa un vero prodotto: dalla scoperta alla conversazione."
    )

    col1, col2, col3, col4 = st.columns(4)
    total_views = 4200
    saved = max(len(st.session_state.saved_matches), 12)
    sent = len(st.session_state.contact_requests)
    accepted = sum(1 for r in st.session_state.contact_requests if r["stato"] in ["Accettata", "Call programmata"])

    with col1:
        kpi_card("Profili visualizzati", f"{total_views:,}", "👀", "")
    with col2:
        kpi_card("Match salvati", str(saved), "⭐", "")
    with col3:
        kpi_card("Richieste inviate", str(sent), "📨", "")
    with col4:
        kpi_card("Intro positive", str(accepted), "🤝", "")

    startup_name = st.selectbox(
        "Startup richiedente",
        df_startups["nome"].tolist(),
        index=df_startups["nome"].tolist().index(st.session_state.demo_startup),
        key="contact_startup_select",
    )
    s = df_startups[df_startups["nome"] == startup_name].iloc[0]

    target_type = st.radio("Destinatario", ["Azienda", "Investitore"], horizontal=True)

    if target_type == "Azienda":
        target_options = [r["nome"] for r in TOP_DEMO_CO] if startup_name == "Nexara" else df_companies["nome"].tolist()
        default_index = target_options.index("RetailMax") if "RetailMax" in target_options else 0
        target_name = st.selectbox("Seleziona azienda", target_options, index=default_index)
        co = df_companies[df_companies["nome"] == target_name].iloc[0]
        score, _, _ = compute_company_match(s, co)
        suggested_status = "Call programmata" if target_name == "RetailMax" and startup_name == "Nexara" else "Inviata"

        message = (
            f"Gentile team Innovazione di {target_name},\n\n"
            f"mi chiamo {s['founder']}, founder di {s['nome']}, una startup {s['settore']} in fase di {s['stadio']}.\n\n"
            f"Stiamo cercando un {s['obiettivo'].lower()} e crediamo che la nostra soluzione possa essere rilevante per la vostra area di innovazione ({co['area_innovazione']}).\n\n"
            f"{s['descrizione']}\n\n"
            f"Ci farebbe piacere organizzare una breve call per capire se ci sono le condizioni per un {co['collaborazione'].lower()}.\n\n"
            f"Cordiali saluti,\n{s['founder']}\n{s['nome']}"
        )
    else:
        target_options = [r["nome"] for r in TOP_DEMO_INV] if startup_name == "Nexara" else df_investors["nome"].tolist()
        default_index = target_options.index("Mediterraneo Ventures") if "Mediterraneo Ventures" in target_options else 0
        target_name = st.selectbox("Seleziona investitore", target_options, index=default_index)
        inv = df_investors[df_investors["nome"] == target_name].iloc[0]
        score, _, _ = compute_investor_match(s, inv)
        suggested_status = "In revisione"

        message = (
            f"Gentile team di {target_name},\n\n"
            f"mi chiamo {s['founder']} e sono founder di {s['nome']}, startup {s['settore']} in fase di {s['stadio']}.\n\n"
            f"Stiamo costruendo una soluzione con traction concreta e cerchiamo {s['obiettivo'].lower()} / supporto alla crescita. "
            f"Il vostro focus su {', '.join(inv['settori_preferiti'][:2])} e il vostro range di investimento ci sembrano particolarmente allineati.\n\n"
            f"{s['descrizione']}\n\n"
            f"Sarei felice di condividere alcune metriche e capire se può esserci un fit per una call introduttiva.\n\n"
            f"Cordiali saluti,\n{s['founder']}\n{s['nome']}"
        )

    st.markdown(
        f"""
        <div class="nf-card">
            <div class="nf-card-title">Preview della richiesta</div>
            <div class="nf-card-text">
                Match score: <b style="color:{score_color(score)};">{score}%</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_area("Messaggio generato", message, height=220)

    c_send, c_hint = st.columns([1.2, 3])
    with c_send:
        if st.button("Invia richiesta", use_container_width=True, type="primary"):
            safe_append_request(
                {
                    "startup": startup_name,
                    "target": target_name,
                    "tipo": target_type,
                    "score": score,
                    "stato": suggested_status if startup_name == "Nexara" else "Inviata",
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                }
            )
            st.success(f"Richiesta inviata a {target_name}.")
    with c_hint:
        st.caption("In demo live, usa Nexara → RetailMax per mostrare un passaggio completo fino a 'Call programmata'.")

    st.markdown("### Stato delle richieste")
    if not st.session_state.contact_requests:
        st.info("Nessuna richiesta inviata.")
    else:
        status_options = ["Inviata", "In revisione", "Accettata", "Call programmata"]
        status_badges = {
            "Inviata": ("nf-pill-amber", "Inviata"),
            "In revisione": ("nf-pill-primary", "In revisione"),
            "Accettata": ("nf-pill-success", "Accettata"),
            "Call programmata": ("nf-pill-accent", "Call programmata"),
        }

        for idx, req in enumerate(st.session_state.contact_requests):
            c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1.6])
            with c1:
                st.markdown(f"**{req['startup']}**")
            with c2:
                st.markdown(f"→ {req['target']}")
            with c3:
                st.markdown(f"<span style='font-weight:800; color:{score_color(req['score'])};'>{req['score']}%</span>", unsafe_allow_html=True)
            with c4:
                new_status = st.selectbox(
                    f"Stato {idx}",
                    status_options,
                    index=status_options.index(req["stato"]),
                    key=f"req_status_{idx}",
                    label_visibility="collapsed",
                )
                st.session_state.contact_requests[idx]["stato"] = new_status
            with c5:
                cls, label = status_badges[new_status]
                st.markdown(f'<span class="nf-pill {cls}">{label}</span>', unsafe_allow_html=True)


def section_directory():
    section_header(
        "Directory",
        "Una vista più esplorativa del prodotto: startup, aziende e investitori in un unico posto."
    )

    tab_s, tab_c, tab_i = st.tabs(["🚀 Startup", "🏢 Aziende", "💰 Investitori"])

    with tab_s:
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            settore = st.multiselect("Settore", sorted(df_startups["settore"].unique()), key="dir_s_settore")
        with f2:
            stadio = st.multiselect("Stadio", sorted(df_startups["stadio"].unique()), key="dir_s_stadio")
        with f3:
            città = st.multiselect("Città", sorted(df_startups["citta"].unique()), key="dir_s_citta")
        with f4:
            ver = st.selectbox("Verifica", ["Tutte", "Verificate", "Non verificate"], key="dir_s_ver")

        filtered = df_startups.copy()
        if settore:
            filtered = filtered[filtered["settore"].isin(settore)]
        if stadio:
            filtered = filtered[filtered["stadio"].isin(stadio)]
        if città:
            filtered = filtered[filtered["citta"].isin(città)]
        if ver == "Verificate":
            filtered = filtered[filtered["verificata"]]
        elif ver == "Non verificate":
            filtered = filtered[~filtered["verificata"]]

        st.markdown(f"**{len(filtered)} startup trovate**")
        if filtered.empty:
            st.warning("Nessun risultato trovato con i filtri selezionati.")
        else:
            for row_start in range(0, min(len(filtered), 12), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    idx = row_start + j
                    if idx < len(filtered):
                        with col:
                            st.markdown(startup_card_html(filtered.iloc[idx]), unsafe_allow_html=True)

            selected = st.selectbox("Dettaglio startup", filtered["nome"].tolist(), key="dir_startup_detail")
            s = filtered[filtered["nome"] == selected].iloc[0]

            st.markdown(
                f"""
                <div class="nf-card">
                    <div class="nf-card-title">{s["nome"]}</div>
                    <div class="nf-card-text">
                        <b>Founder:</b> {s["founder"]}<br>
                        <b>Settore:</b> {s["settore"]}<br>
                        <b>Stadio:</b> {s["stadio"]}<br>
                        <b>Città:</b> {s["citta"]}<br>
                        <b>Obiettivo:</b> {s["obiettivo"]}<br>
                        <b>Fabbisogno:</b> {s["funding_need"]}<br><br>
                        {s["descrizione"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_c:
        f1, f2, f3 = st.columns(3)
        with f1:
            dim = st.multiselect("Dimensione", sorted(df_companies["dimensione"].unique()), key="dir_c_dim")
        with f2:
            area = st.multiselect("Area innovazione", sorted(df_companies["area_innovazione"].unique()), key="dir_c_area")
        with f3:
            coll = st.multiselect("Collaborazione", sorted(df_companies["collaborazione"].unique()), key="dir_c_coll")

        filtered = df_companies.copy()
        if dim:
            filtered = filtered[filtered["dimensione"].isin(dim)]
        if area:
            filtered = filtered[filtered["area_innovazione"].isin(area)]
        if coll:
            filtered = filtered[filtered["collaborazione"].isin(coll)]

        st.markdown(f"**{len(filtered)} aziende trovate**")
        if filtered.empty:
            st.warning("Nessun risultato trovato con i filtri selezionati.")
        else:
            for row_start in range(0, min(len(filtered), 9), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    idx = row_start + j
                    if idx < len(filtered):
                        with col:
                            st.markdown(company_card_html(filtered.iloc[idx]), unsafe_allow_html=True)

            selected = st.selectbox("Dettaglio azienda", filtered["nome"].tolist(), key="dir_company_detail")
            c = filtered[filtered["nome"] == selected].iloc[0]

            st.markdown(
                f"""
                <div class="nf-card">
                    <div class="nf-card-title">{c["nome"]}</div>
                    <div class="nf-card-text">
                        <b>Settore:</b> {c["settore"]}<br>
                        <b>Dimensione:</b> {c["dimensione"]}<br>
                        <b>Area innovazione:</b> {c["area_innovazione"]}<br>
                        <b>Collaborazione:</b> {c["collaborazione"]}<br>
                        <b>Città:</b> {c["citta"]}<br>
                        <b>Budget:</b> {c["budget_class"]}<br>
                        <b>Tempo medio valutazione:</b> {c["tempo_valutazione_gg"]} giorni<br><br>
                        {c["descrizione"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_i:
        f1, f2, f3 = st.columns(3)
        with f1:
            tipo = st.multiselect("Tipo", sorted(df_investors["tipo"].unique()), key="dir_i_tipo")
        with f2:
            stage = st.multiselect("Focus stage", sorted(df_investors["focus_stage"].unique()), key="dir_i_stage")
        with f3:
            sec = st.multiselect("Settori", SETTORI, key="dir_i_sec")

        filtered = df_investors.copy()
        if tipo:
            filtered = filtered[filtered["tipo"].isin(tipo)]
        if stage:
            filtered = filtered[filtered["focus_stage"].isin(stage)]
        if sec:
            filtered = filtered[filtered["settori_preferiti"].apply(lambda x: any(s in x for s in sec))]

        st.markdown(f"**{len(filtered)} investitori trovati**")
        if filtered.empty:
            st.warning("Nessun risultato trovato con i filtri selezionati.")
        else:
            for row_start in range(0, min(len(filtered), 9), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    idx = row_start + j
                    if idx < len(filtered):
                        with col:
                            st.markdown(investor_card_html(filtered.iloc[idx]), unsafe_allow_html=True)

            selected = st.selectbox("Dettaglio investitore", filtered["nome"].tolist(), key="dir_investor_detail")
            i = filtered[filtered["nome"] == selected].iloc[0]

            st.markdown(
                f"""
                <div class="nf-card">
                    <div class="nf-card-title">{i["nome"]}</div>
                    <div class="nf-card-text">
                        <b>Tipo:</b> {i["tipo"]}<br>
                        <b>Stage focus:</b> {i["focus_stage"]}<br>
                        <b>Ticket:</b> {i["ticket"]}<br>
                        <b>Geografia:</b> {i["geografia"]}<br>
                        <b>Lead / follow:</b> {i["lead_follow"]}<br>
                        <b>Portfolio:</b> {i["portfolio_size"]} startup<br>
                        <b>Velocità media:</b> {i["velocita_risposta_gg"]} giorni<br>
                        <b>Settori:</b> {", ".join(i["settori_preferiti"])}<br><br>
                        {i["thesis"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def section_feed():
    section_header(
        "Feed Piattaforma",
        "Un feed professionale che mostra segnali di attività e opportunità nell’ecosistema."
    )

    for item in feed_items:
        st.markdown(
            f"""
            <div class="nf-feed">
                <div class="nf-feed-icon">{item["icona"]}</div>
                <div style="flex:1;">
                    <div class="nf-feed-type">{item["tipo"]}</div>
                    <div class="nf-feed-text">{item["testo"]}</div>
                </div>
                <div class="nf-feed-time">{item["tempo"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def section_dashboard():
    section_header(
        "Dashboard KPI",
        "Le metriche che raccontano il valore della piattaforma a incubatori, partner e investitori."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Startup registrate", "247", "🚀", "+18 questo mese")
    with c2:
        kpi_card("Aziende attive", "68", "🏢", "+5 questo mese")
    with c3:
        kpi_card("Investitori attivi", "42", "💰", "+3 questo mese")
    with c4:
        kpi_card("Startup verificate", "112", "✅", "45% del totale")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        kpi_card("Match generati", "1.247", "🎯", "+12% vs mese prec.")
    with c6:
        kpi_card("Richieste inviate", "583", "📨", "+8% vs mese prec.")
    with c7:
        kpi_card("Tasso risposta", "56%", "📊", "+3pp vs mese prec.")
    with c8:
        kpi_card("Call fissate", "156", "📞", "+11% vs mese prec.")

    tab1, tab2, tab3, tab4 = st.tabs(["Settori", "Stage", "Funnel", "Trend"])

    with tab1:
        sector_counts = df_startups["settore"].value_counts().reset_index()
        sector_counts.columns = ["Settore", "Numero"]
        fig = px.bar(
            sector_counts,
            x="Settore",
            y="Numero",
            color="Settore",
            color_discrete_map=SECTOR_COLORS,
        )
        fig.update_layout(
            height=360,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)")
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        stage_counts = df_startups["stadio"].value_counts().reset_index()
        stage_counts.columns = ["Stadio", "Numero"]
        fig = px.pie(
            stage_counts,
            names="Stadio",
            values="Numero",
            hole=0.45,
            color_discrete_sequence=[PRIMARY, ACCENT, CORAL, AMBER],
        )
        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        funnel_y = ["Profili visualizzati", "Match generati", "Match salvati", "Richieste inviate", "Intro accettate", "Call fissate"]
        funnel_x = [8400, 1247, 890, 583, 328, 156]
        fig = go.Figure(go.Funnel(
            y=funnel_y,
            x=funnel_x,
            textinfo="value+percent initial",
            marker=dict(color=[PRIMARY, PRIMARY_2, "#315A92", ACCENT, ACCENT_DARK, CORAL]),
            connector=dict(line=dict(color=BORDER)),
        ))
        fig.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        months = pd.date_range("2025-01-01", periods=12, freq="MS")
        rng = np.random.RandomState(SEED)
        startup_growth = np.cumsum(rng.randint(8, 22, size=12)) + 70
        match_growth = np.cumsum(rng.randint(35, 95, size=12)) + 200
        intro_growth = np.cumsum(rng.randint(12, 38, size=12)) + 50

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=startup_growth, mode="lines+markers", name="Startup registrate", line=dict(color=PRIMARY, width=2.5)))
        fig.add_trace(go.Scatter(x=months, y=match_growth, mode="lines+markers", name="Match generati", line=dict(color=ACCENT, width=2.5)))
        fig.add_trace(go.Scatter(x=months, y=intro_growth, mode="lines+markers", name="Richieste inviate", line=dict(color=CORAL, width=2.5, dash="dot")))
        fig.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)


def section_conclusion():
    section_header(
        "Conclusione",
        "Questa demo mostra NexFound come prodotto, non solo come idea."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">Cosa rende forte NexFound</div>
                <div class="nf-card-text">
                    • Posizionamento chiaro: startup + corporate + investitori<br>
                    • Matching spiegabile e non casuale<br>
                    • Profili strutturati, non semplici pagine social<br>
                    • Workflow che va oltre la scoperta e arriva al contatto<br>
                    • Demo centrata su un use case reale e memorabile
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">Cosa dimostra questa POC</div>
                <div class="nf-card-text">
                    La piattaforma è già comprensibile come esperienza utente:
                    si vede bene come una startup entra, come viene letta,
                    come vengono generati i match e come nasce una relazione operativa.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">Prossimi passi realistici</div>
                <div class="nf-card-text">
                    1. Validazione con startup e corporate pilota<br>
                    2. MVP con autenticazione e profili reali<br>
                    3. Algoritmo di ranking più sofisticato<br>
                    4. Workflow intro / call / data room<br>
                    5. Partnership con incubatori e innovation hub
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="nf-card">
                <div class="nf-card-title">Messaggio finale</div>
                <div class="nf-card-text">
                    NexFound non vuole essere “un altro social”.
                    Vuole diventare il luogo in cui le idee promettenti trovano davvero
                    il capitale, i partner e le corporate che possono farle crescere.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="nf-note">
            <h3>NexFound — dove l'innovazione incontra l'opportunità</h3>
            <p>
                Una piattaforma pensata per far emergere le startup giuste davanti alle persone giuste,
                con il giusto contesto per iniziare una relazione di valore.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# ROUTER
# ============================================================

page_map = {
    "🏠 Home": section_home,
    "⚡ Problema di Mercato": section_problema,
    "🔗 Ecosistema": section_ecosistema,
    "🧭 Caso d'uso guidato": section_case_study,
    "🎯 Matching Intelligente": section_matching,
    "📨 Flusso di Contatto": section_contatto,
    "📚 Directory": section_directory,
    "📰 Feed Piattaforma": section_feed,
    "📊 Dashboard KPI": section_dashboard,
    "✨ Conclusione": section_conclusion,
}

page_map[st.session_state.page]()