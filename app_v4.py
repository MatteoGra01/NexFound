"""
NexFound — Demo V4 · Logica a Sandwich con Branching per Ruolo

Flusso a 8 step lineari:
  1. Home           (comune)
  2. Problema       (comune)
  3. Scelta Ruolo   (comune — salva userRole)
  4. Caso d'uso     (ramificato per ruolo)
  5. Matching       (ramificato per ruolo)
  6. Contatto       (ramificato per ruolo)
  7. Dashboard KPI  (comune)
  8. Conclusione    (comune)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

SEED = 42
np.random.seed(SEED)

st.set_page_config(
    page_title="NexFound — Demo interattiva",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Palette
PRIMARY   = "#172B4D"
PRIMARY_2 = "#243B63"
ACCENT    = "#2EC4B6"
ACCENT_DK = "#1C9E93"
CORAL     = "#FF6B6B"
AMBER     = "#FFB347"
SUCCESS   = "#22C55E"
TEXT      = "#172B4D"
TEXT_2    = "#5D6B82"
TEXT_3    = "#8D98A8"
BG        = "#F6F8FB"
CARD      = "#FFFFFF"
BORDER    = "#E8ECF3"

SETTORI = [
    "AI", "Fintech", "Climate Tech", "HealthTech", "SaaS B2B",
    "HR Tech", "PropTech", "Cybersecurity", "Mobility", "EdTech",
]
STADI     = ["Idea", "MVP", "Traction", "Revenue"]
CITTA     = ["Milano", "Roma", "Torino", "Bologna", "Firenze", "Napoli",
             "Padova", "Bergamo", "Genova", "Verona", "Bari", "Trieste"]
OBIETTIVI = ["Fundraising", "Pilot aziendale", "Partnership", "Mentorship", "Co-founder"]

SECTOR_COLORS = {
    "AI": "#6366F1", "Fintech": "#2EC4B6", "Climate Tech": "#22C55E",
    "HealthTech": "#EF4444", "SaaS B2B": "#3B82F6", "HR Tech": "#A855F7",
    "PropTech": "#F59E0B", "Cybersecurity": "#172B4D", "Mobility": "#06B6D4",
    "EdTech": "#EC4899",
}

STEP_LABELS = [
    "1. Home", "2. Problema", "3. Scegli ruolo",
    "4. Caso d'uso", "5. Matching", "6. Contatto",
    "7. Dashboard", "8. Conclusione",
]

# ─────────────────────────────────────────────────────────────
# CSS  (stile v3 – pulito e compatto)
# ─────────────────────────────────────────────────────────────

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}
.stApp {{ background: {BG}; }}
.block-container {{
    max-width: 1200px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}}

/* ── Sidebar ─────────────────────── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {PRIMARY} 0%, #0F1E36 100%);
    border-right: 1px solid rgba(46,196,182,0.12);
}}
section[data-testid="stSidebar"] * {{
    color: #D6E0EE !important;
}}

/* ── Hero ────────────────────────── */
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
.nf-hero::before {{
    content: '';
    position: absolute;
    top: -50%; right: -12%;
    width: 420px; height: 420px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(46,196,182,0.16) 0%, transparent 70%);
}}
.nf-hero::after {{
    content: '';
    position: absolute;
    bottom: -40%; left: -8%;
    width: 340px; height: 340px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,107,107,0.10) 0%, transparent 70%);
}}
.nf-hero h1 {{
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    margin: 0 0 0.5rem 0;
    position: relative;
    line-height: 1.12;
}}
.nf-hero p {{
    font-size: 1.06rem;
    color: rgba(255,255,255,0.76);
    max-width: 700px;
    line-height: 1.65;
    position: relative;
    margin: 0.3rem 0 1.2rem 0;
}}

/* ── Section heading ─────────────── */
.nf-sec h2 {{
    color: {TEXT};
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 0.15rem 0;
}}
.nf-sec .bar {{
    width: 42px; height: 4px;
    background: {ACCENT};
    border-radius: 2px;
    margin-bottom: 0.8rem;
}}
.nf-sec-sub {{
    color: {TEXT_2};
    font-size: 0.95rem;
    line-height: 1.55;
    margin-bottom: 1.3rem;
}}

/* ── Card ────────────────────────── */
.nf-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
    margin-bottom: 1rem;
}}
.nf-card-soft {{
    background: linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 100%);
}}
.nf-card-title {{
    font-size: 1.02rem; font-weight: 700; color: {TEXT};
    margin-bottom: 0.4rem;
}}
.nf-card-text {{
    font-size: 0.92rem; line-height: 1.65; color: {TEXT_2};
}}

/* ── KPI ─────────────────────────── */
.nf-kpi {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 15px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
    position: relative; overflow: hidden;
    margin-bottom: 0.9rem;
}}
.nf-kpi::before {{
    content: ''; position: absolute; left: 0; top: 0; right: 0;
    height: 3px; background: linear-gradient(90deg, {ACCENT}, {ACCENT_DK});
}}
.nf-kpi-label {{
    font-size: 0.74rem; text-transform: uppercase;
    letter-spacing: 0.06em; font-weight: 700; color: {TEXT_3};
}}
.nf-kpi-value {{
    font-size: 1.9rem; color: {TEXT}; font-weight: 800;
    letter-spacing: -0.04em; line-height: 1.1; margin-top: 0.15rem;
}}
.nf-kpi-delta {{
    font-size: 0.78rem; font-weight: 600; color: {SUCCESS}; margin-top: 0.3rem;
}}

/* ── Pills / Badges ──────────────── */
.nf-pill {{
    display: inline-block; padding: 4px 10px;
    border-radius: 999px; font-size: 0.73rem; font-weight: 700;
    margin-right: 6px; margin-bottom: 6px;
}}
.nf-pill-accent  {{ background: rgba(46,196,182,0.12); color: {ACCENT_DK}; }}
.nf-pill-primary {{ background: rgba(23,43,77,0.08); color: {PRIMARY}; }}
.nf-pill-coral   {{ background: rgba(255,107,107,0.12); color: #D94B4B; }}
.nf-pill-success {{ background: rgba(34,197,94,0.12); color: #16803C; }}
.nf-pill-amber   {{ background: rgba(255,179,71,0.18); color: #A76400; }}

/* ── Profile card ────────────────── */
.nf-profile {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
    margin-bottom: 0.9rem;
    transition: transform .18s ease;
}}
.nf-profile:hover {{ transform: translateY(-2px); }}
.nf-profile-head {{
    display: flex; align-items: center; gap: 12px; margin-bottom: 0.7rem;
}}
.nf-avatar {{
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; flex-shrink: 0;
}}
.nf-avatar-startup  {{ background: linear-gradient(135deg, {ACCENT}, {ACCENT_DK}); }}
.nf-avatar-company  {{ background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_2}); }}
.nf-avatar-investor {{ background: linear-gradient(135deg, {CORAL}, #E05555); }}
.nf-profile-name {{
    font-weight: 800; color: {TEXT}; font-size: 1rem;
    margin: 0; line-height: 1.15;
}}
.nf-profile-sub {{
    color: {TEXT_3}; font-size: 0.8rem; margin: 0.12rem 0 0 0;
}}
.nf-profile-text {{
    color: {TEXT_2}; font-size: 0.88rem; line-height: 1.55; margin-top: 0.45rem;
}}
.nf-progress-wrap {{ margin-top: 0.55rem; }}
.nf-progress-head {{
    display: flex; justify-content: space-between;
    color: {TEXT_3}; font-size: 0.78rem; margin-bottom: 0.25rem;
}}
.nf-progress {{
    width: 100%; height: 7px; background: #EEF2F7;
    border-radius: 999px; overflow: hidden;
}}
.nf-progress-fill {{ height: 100%; border-radius: 999px; }}

/* ── Spotlight ───────────────────── */
.nf-spotlight {{
    background: linear-gradient(135deg, rgba(46,196,182,0.12) 0%, rgba(46,196,182,0.06) 100%);
    border: 1px solid rgba(46,196,182,0.18);
    border-radius: 18px;
    padding: 1.2rem 1.25rem;
    margin-bottom: 1rem;
}}
.nf-spotlight-title {{
    font-size: 0.78rem; text-transform: uppercase;
    letter-spacing: 0.07em; color: {ACCENT_DK};
    font-weight: 800; margin-bottom: 0.35rem;
}}
.nf-spotlight h3 {{
    font-size: 1.25rem; font-weight: 800; color: {TEXT}; margin: 0 0 0.3rem 0;
}}
.nf-spotlight p {{
    font-size: 0.92rem; line-height: 1.6; color: {TEXT_2}; margin: 0;
}}

/* ── Step card ───────────────────── */
.nf-step {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 16px; padding: 1.1rem 1.15rem; height: 100%;
}}
.nf-step-num {{
    width: 30px; height: 30px; border-radius: 999px;
    background: rgba(46,196,182,0.12); color: {ACCENT_DK};
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; margin-bottom: 0.65rem;
}}

/* ── Match card ──────────────────── */
.nf-match {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 16px; padding: 1.1rem 1.2rem;
    box-shadow: 0 2px 10px rgba(23,43,77,0.04), 0 8px 24px rgba(23,43,77,0.06);
    margin-bottom: 1rem; position: relative; overflow: hidden;
}}
.nf-match::before {{
    content: ''; position: absolute; top: 0; left: 0; bottom: 0;
    width: 4px; background: linear-gradient(180deg, {ACCENT}, {ACCENT_DK});
}}
.nf-match-head {{
    display: flex; justify-content: space-between; gap: 14px;
    margin-bottom: 0.5rem;
}}
.nf-match-rank {{
    font-size: 0.72rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.07em; color: {TEXT_3};
}}
.nf-match-name {{
    font-size: 1.05rem; font-weight: 800; color: {TEXT};
    margin: 0.1rem 0 0.25rem 0;
}}
.nf-match-score {{ min-width: 72px; text-align: center; }}
.nf-match-score-value {{
    font-size: 1.9rem; font-weight: 900;
    letter-spacing: -0.05em; line-height: 1;
}}
.nf-match-score-label {{
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: {TEXT_3}; margin-top: 0.1rem;
}}
.nf-list {{
    margin: 0.3rem 0 0 0; padding-left: 1rem;
    color: {TEXT_2}; font-size: 0.88rem; line-height: 1.6;
}}

/* ── Feed row ────────────────────── */
.nf-feed {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 0.95rem 1rem;
    display: flex; gap: 12px; align-items: flex-start;
    margin-bottom: 0.7rem;
}}
.nf-feed-icon {{
    width: 38px; height: 38px; border-radius: 11px;
    background: #F1F5FA; display: flex;
    align-items: center; justify-content: center; flex-shrink: 0;
}}
.nf-feed-type {{
    font-size: 0.72rem; font-weight: 800; color: {ACCENT_DK};
    text-transform: uppercase; letter-spacing: 0.06em;
}}
.nf-feed-text {{ color: {TEXT}; font-size: 0.9rem; line-height: 1.45; }}
.nf-feed-time {{ color: {TEXT_3}; font-size: 0.76rem; white-space: nowrap; }}

/* ── Note / CTA block ────────────── */
.nf-note {{
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DK} 100%);
    border-radius: 18px; padding: 1.5rem 1.6rem;
    color: white; position: relative; overflow: hidden;
}}
.nf-note h3 {{ margin: 0 0 0.35rem 0; font-size: 1.35rem; font-weight: 800; }}
.nf-note p {{ margin: 0; color: rgba(255,255,255,0.84); line-height: 1.6; }}

/* ── Role card ───────────────────── */
.nf-role {{
    background: {CARD}; border: 2px solid {BORDER};
    border-radius: 16px; padding: 1.6rem 1.1rem 1.1rem;
    text-align: center;
    transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
}}
.nf-role:hover {{
    border-color: {ACCENT};
    box-shadow: 0 4px 16px rgba(46,196,182,0.10);
    transform: translateY(-2px);
}}
.nf-role .icon {{ font-size: 2.2rem; margin-bottom: 0.4rem; }}
.nf-role h3 {{
    font-size: 1.05rem; font-weight: 700; color: {TEXT};
    margin: 0 0 0.3rem 0;
}}
.nf-role p {{ font-size: 0.84rem; color: {TEXT_2}; line-height: 1.5; margin: 0; }}

/* ── Compact header ──────────────── */
.nf-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.4rem 0 0.7rem 0; margin-bottom: 0.6rem;
    border-bottom: 2px solid {BORDER};
}}
.nf-header .logo {{
    font-size: 1.35rem; font-weight: 900; color: {TEXT};
    letter-spacing: -0.04em;
}}
.nf-header .role-pill {{
    padding: 5px 14px; border-radius: 8px;
    font-size: 0.82rem; font-weight: 600;
    background: rgba(46,196,182,0.12); color: {ACCENT_DK};
}}

/* ── Request row ─────────────────── */
.nf-req {{
    background: {CARD}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 12px;
}}
.nf-req .req-info {{ flex: 1; }}
.nf-req .req-name {{ font-weight: 700; color: {TEXT}; font-size: 0.9rem; }}
.nf-req .req-meta {{ font-size: 0.78rem; color: {TEXT_3}; }}

/* ── Overrides ───────────────────── */
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px 10px 0 0; font-weight: 700; font-size: 0.85rem;
}}
.js-plotly-plot .plotly .modebar {{ display: none !important; }}
</style>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

_defaults = {
    "currentStep": 0,
    "userRole": None,
    "contact_requests": [
        {"startup": "Nexara", "target": "RetailMax", "tipo": "Azienda",
         "score": 91, "stato": "Call programmata", "data": "14/03/2026 10:30"},
        {"startup": "Nexara", "target": "Mediterraneo Ventures", "tipo": "Investitore",
         "score": 88, "stato": "In revisione", "data": "15/03/2026 15:10"},
    ],
    "saved_matches": [],
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─────────────────────────────────────────────────────────────
# DATA GENERATORS
# ─────────────────────────────────────────────────────────────

@st.cache_data
def generate_startups(n=24):
    names = [
        "Nexara", "FinSmart", "GreenPulse", "MedIntel", "DataForge", "TalentUp",
        "CasaClick", "SecureNet", "MoveFlow", "LearnHub", "Visionary AI", "PayLoop",
        "SolarMind", "VitaLink", "CloudMetrics", "HireWise", "BuildView", "VaultEdge",
        "FleetPulse", "StudyVerse", "Predictiva", "CarbonLess", "NurseBot", "APILayer",
    ]
    founders = [
        "Alice Colombo", "Marco Fontana", "Giulia Bianchi", "Luca Moretti",
        "Sara Ricci", "Andrea Conti", "Francesca De Luca", "Davide Galli",
        "Elena Marchetti", "Tommaso Barbieri", "Chiara Ferro", "Lorenzo Mancini",
        "Valentina Rossetti", "Matteo Pellegrini", "Silvia Caruso", "Federico Villa",
        "Martina Fabbri", "Giorgio Testa", "Eleonora Grasso", "Alessandro Vitale",
        "Beatrice Amato", "Simone Lombardi", "Anna Leone", "Nicola Parisi",
    ]
    descriptions = [
        "Piattaforma AI per personalizzare l'esperienza di acquisto in-store e online nel retail.",
        "Micropagamenti e gestione finanziaria per freelance e creator economy.",
        "Monitoraggio e riduzione delle emissioni CO₂ per PMI tramite IoT.",
        "Sistema di triage medico basato su AI per pronto soccorso e cliniche.",
        "Analytics predittive e reportistica automatizzata per team B2B.",
        "Talent matching basato su competenze e cultura aziendale.",
        "Valutazione immobiliare automatizzata con dati satellitari e catastali.",
        "Cybersecurity avanzata per PMI e startup in cloud.",
        "Mobilità multimodale integrata per aree metropolitane.",
        "Microlearning personalizzato per formazione aziendale continua.",
        "Visione artificiale per il controllo qualità industriale.",
        "Gateway di pagamento istantaneo con riconciliazione automatica.",
        "Gestione e ottimizzazione di impianti fotovoltaici distribuiti.",
        "Telemedicina con monitoraggio remoto per pazienti cronici.",
        "Business intelligence cloud-native per team distribuiti.",
        "Recruiting automation con screening AI-driven.",
        "Digital twin per cantieri edili e monitoraggio costruzioni.",
        "Gestione delle vulnerabilità e compliance automatizzata.",
        "Gestione intelligente di flotte aziendali e ottimizzazione consumi.",
        "Apprendimento immersivo VR per università e corporate.",
        "Manutenzione industriale predittiva basata su sensori IoT.",
        "Marketplace per crediti di carbonio verificati e trasparenti.",
        "Assistente virtuale AI per infermieri e personale sanitario.",
        "API management platform per microservizi enterprise.",
    ]
    rng = np.random.RandomState(SEED)
    rows = [
        {"nome": "Nexara", "settore": "AI",
         "descrizione": descriptions[0], "stadio": "Traction",
         "citta": "Milano", "team_size": 11, "founder": "Alice Colombo",
         "obiettivo": "Pilot aziendale", "users": 5400, "mrr": 18000,
         "growth_pct": 22.4, "score_profilo": 92, "verificata": True,
         "funding_need": "Seed €500K–€1.2M", "readiness": "Alta"},
    ]
    for i in range(1, n):
        settore = SETTORI[i % len(SETTORI)]
        stadio = STADI[rng.randint(0, len(STADI))]
        citta = CITTA[rng.randint(0, len(CITTA))]
        obiettivo = OBIETTIVI[rng.randint(0, len(OBIETTIVI))]
        team = int(rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 24]))
        if stadio == "Idea":
            users, mrr, growth = int(rng.randint(0, 80)), 0, 0.0
            funding, readiness = "Pre-seed €50K–€150K", "In sviluppo"
        elif stadio == "MVP":
            users = int(rng.randint(80, 600))
            mrr = int(rng.randint(0, 2500))
            growth = round(float(rng.uniform(2, 15)), 1)
            funding, readiness = "Seed €150K–€500K", "Media"
        elif stadio == "Traction":
            users = int(rng.randint(600, 12000))
            mrr = int(rng.randint(3000, 22000))
            growth = round(float(rng.uniform(5, 30)), 1)
            funding, readiness = "Seed / Series A €500K–€2M", "Alta"
        else:
            users = int(rng.randint(5000, 95000))
            mrr = int(rng.randint(12000, 100000))
            growth = round(float(rng.uniform(3, 22)), 1)
            funding, readiness = "Series A+ €1M–€5M", "Molto alta"
        rows.append({
            "nome": names[i], "settore": settore, "descrizione": descriptions[i],
            "stadio": stadio, "citta": citta, "team_size": team,
            "founder": founders[i], "obiettivo": obiettivo,
            "users": users, "mrr": mrr, "growth_pct": growth,
            "score_profilo": int(rng.randint(58, 98)),
            "verificata": bool(rng.choice([True, False], p=[0.42, 0.58])),
            "funding_need": funding, "readiness": readiness,
        })
    return pd.DataFrame(rows)


@st.cache_data
def generate_companies():
    return pd.DataFrame([
        {"nome": "RetailMax", "settore": "Retail", "dimensione": "Enterprise",
         "area_innovazione": "AI", "collaborazione": "Pilot", "citta": "Milano",
         "budget_class": "Alto", "tempo_valutazione_gg": 21, "premium": True,
         "descrizione": "Gruppo retail omnicanale alla ricerca di soluzioni AI per personalizzazione e customer experience."},
        {"nome": "Gruppo Rinaldi", "settore": "Manifattura", "dimensione": "Enterprise",
         "area_innovazione": "AI", "collaborazione": "Pilot", "citta": "Torino",
         "budget_class": "Alto", "tempo_valutazione_gg": 30, "premium": True,
         "descrizione": "Gruppo industriale che investe in automazione, visione artificiale e ottimizzazione dei processi."},
        {"nome": "Banca Meridiana", "settore": "Banking & Finance", "dimensione": "Enterprise",
         "area_innovazione": "Fintech", "collaborazione": "Investimento", "citta": "Roma",
         "budget_class": "Alto", "tempo_valutazione_gg": 45, "premium": True,
         "descrizione": "Istituto bancario con focus su open banking, digital onboarding e infrastrutture fintech."},
        {"nome": "EnerVita", "settore": "Energia", "dimensione": "Enterprise",
         "area_innovazione": "Climate Tech", "collaborazione": "Partnership", "citta": "Milano",
         "budget_class": "Alto", "tempo_valutazione_gg": 35, "premium": True,
         "descrizione": "Utility energetica impegnata in smart grid, monitoraggio emissioni e transizione verde."},
        {"nome": "FarmaItalia", "settore": "Farmaceutico", "dimensione": "Enterprise",
         "area_innovazione": "HealthTech", "collaborazione": "Pilot", "citta": "Roma",
         "budget_class": "Medio", "tempo_valutazione_gg": 40, "premium": False,
         "descrizione": "Azienda farmaceutica interessata a digital health, patient monitoring e automazione clinica."},
        {"nome": "TechnoMedia", "settore": "Media & Tech", "dimensione": "Mid-market",
         "area_innovazione": "AI", "collaborazione": "Scouting", "citta": "Milano",
         "budget_class": "Medio", "tempo_valutazione_gg": 18, "premium": True,
         "descrizione": "Gruppo media-tech che esplora nuovi modelli di contenuto, recommendation e AI generativa."},
        {"nome": "AutoItalia", "settore": "Automotive", "dimensione": "Enterprise",
         "area_innovazione": "Mobility", "collaborazione": "Partnership", "citta": "Torino",
         "budget_class": "Alto", "tempo_valutazione_gg": 50, "premium": False,
         "descrizione": "Corporate automotive interessata a mobilità connessa, fleet management e smart operations."},
        {"nome": "InfoServices Group", "settore": "IT & Servizi", "dimensione": "Mid-market",
         "area_innovazione": "SaaS B2B", "collaborazione": "Partnership", "citta": "Bologna",
         "budget_class": "Medio", "tempo_valutazione_gg": 22, "premium": False,
         "descrizione": "System integrator che cerca partnership con startup SaaS e piattaforme enterprise."},
        {"nome": "LogiTrans", "settore": "Logistica", "dimensione": "Mid-market",
         "area_innovazione": "Mobility", "collaborazione": "Pilot", "citta": "Verona",
         "budget_class": "Medio", "tempo_valutazione_gg": 24, "premium": False,
         "descrizione": "Operatore logistico che esplora ottimizzazione last-mile, flotte e routing intelligente."},
        {"nome": "Costruzioni Lombarde", "settore": "Real Estate", "dimensione": "Mid-market",
         "area_innovazione": "PropTech", "collaborazione": "Pilot", "citta": "Bergamo",
         "budget_class": "Medio", "tempo_valutazione_gg": 27, "premium": False,
         "descrizione": "Azienda edile impegnata nella digitalizzazione dei cantieri e nello smart building."},
        {"nome": "AssicuraPlus", "settore": "Assicurazioni", "dimensione": "Enterprise",
         "area_innovazione": "Cybersecurity", "collaborazione": "Scouting", "citta": "Trieste",
         "budget_class": "Alto", "tempo_valutazione_gg": 33, "premium": True,
         "descrizione": "Compagnia assicurativa che cerca startup cyber, antifrode e automazione sinistri."},
        {"nome": "AgriSmart Italia", "settore": "Agricoltura", "dimensione": "PMI",
         "area_innovazione": "Climate Tech", "collaborazione": "Partnership", "citta": "Bologna",
         "budget_class": "Basso", "tempo_valutazione_gg": 16, "premium": False,
         "descrizione": "Impresa innovativa orientata a precision farming, sostenibilità e sensoristica."},
    ])


@st.cache_data
def generate_investors():
    return pd.DataFrame([
        {"nome": "Mediterraneo Ventures", "tipo": "VC", "ticket": "€500K–€3M",
         "ticket_min_k": 500, "ticket_max_k": 3000, "focus_stage": "Seed",
         "settori_preferiti": ["AI", "SaaS B2B", "Fintech"], "geografia": "Italia & Europa",
         "lead_follow": "Lead", "velocita_risposta_gg": 7, "portfolio_size": 28,
         "thesis": "Investiamo in startup tech italiane con forte potenziale di scalabilità e vantaggio competitivo difendibile."},
        {"nome": "Italian Angels Network", "tipo": "Angel", "ticket": "€20K–€100K",
         "ticket_min_k": 20, "ticket_max_k": 100, "focus_stage": "Pre-seed",
         "settori_preferiti": ["AI", "HealthTech", "EdTech", "Climate Tech"], "geografia": "Italia",
         "lead_follow": "Follow", "velocita_risposta_gg": 12, "portfolio_size": 16,
         "thesis": "Supportiamo founder visionari nella fase più iniziale, con forte mentoring operativo."},
        {"nome": "Primo Capital", "tipo": "VC", "ticket": "€1M–€5M",
         "ticket_min_k": 1000, "ticket_max_k": 5000, "focus_stage": "Series A",
         "settori_preferiti": ["Fintech", "SaaS B2B", "Cybersecurity"], "geografia": "Europa",
         "lead_follow": "Lead", "velocita_risposta_gg": 10, "portfolio_size": 34,
         "thesis": "Focus su round Series A per aziende con traction dimostrata e mercato europeo."},
        {"nome": "TechSeed Fund", "tipo": "Micro-VC", "ticket": "€100K–€500K",
         "ticket_min_k": 100, "ticket_max_k": 500, "focus_stage": "Pre-seed",
         "settori_preferiti": ["AI", "SaaS B2B", "HR Tech"], "geografia": "Italia",
         "lead_follow": "Follow", "velocita_risposta_gg": 6, "portfolio_size": 12,
         "thesis": "Primo capitale per team tecnici brillanti che risolvono problemi reali."},
        {"nome": "Innovation Bay Capital", "tipo": "VC", "ticket": "€500K–€2M",
         "ticket_min_k": 500, "ticket_max_k": 2000, "focus_stage": "Seed",
         "settori_preferiti": ["Climate Tech", "Mobility", "AI"], "geografia": "Italia",
         "lead_follow": "Lead", "velocita_risposta_gg": 8, "portfolio_size": 20,
         "thesis": "Cerchiamo innovazione che genera impatto positivo su clima, mobilità e automazione."},
        {"nome": "Alps Ventures", "tipo": "Micro-VC", "ticket": "€100K–€500K",
         "ticket_min_k": 100, "ticket_max_k": 500, "focus_stage": "Pre-seed",
         "settori_preferiti": ["PropTech", "SaaS B2B", "Fintech"], "geografia": "Nord Italia",
         "lead_follow": "Follow", "velocita_risposta_gg": 9, "portfolio_size": 11,
         "thesis": "Investiamo in startup che digitalizzano mercati tradizionali con software scalabile."},
        {"nome": "Futuro Fund", "tipo": "VC", "ticket": "€1M–€5M",
         "ticket_min_k": 1000, "ticket_max_k": 5000, "focus_stage": "Series A",
         "settori_preferiti": ["AI", "HealthTech", "Cybersecurity"], "geografia": "Europa",
         "lead_follow": "Lead", "velocita_risposta_gg": 14, "portfolio_size": 22,
         "thesis": "Puntiamo su AI e cybersecurity per un futuro digitale più sicuro."},
        {"nome": "Digital Growth Partners", "tipo": "VC", "ticket": "€500K–€3M",
         "ticket_min_k": 500, "ticket_max_k": 3000, "focus_stage": "Seed",
         "settori_preferiti": ["SaaS B2B", "Fintech", "HR Tech"], "geografia": "Italia & Europa",
         "lead_follow": "Lead", "velocita_risposta_gg": 11, "portfolio_size": 26,
         "thesis": "Supportiamo la crescita di piattaforme software B2B con metriche solide."},
        {"nome": "EcoInvest", "tipo": "VC", "ticket": "€300K–€2M",
         "ticket_min_k": 300, "ticket_max_k": 2000, "focus_stage": "Seed",
         "settori_preferiti": ["Climate Tech", "Mobility", "PropTech"], "geografia": "Europa",
         "lead_follow": "Lead", "velocita_risposta_gg": 13, "portfolio_size": 19,
         "thesis": "Investiamo esclusivamente in startup a impatto ambientale positivo."},
        {"nome": "HealthVentures Italia", "tipo": "VC", "ticket": "€500K–€3M",
         "ticket_min_k": 500, "ticket_max_k": 3000, "focus_stage": "Seed",
         "settori_preferiti": ["HealthTech", "AI"], "geografia": "Italia",
         "lead_follow": "Lead", "velocita_risposta_gg": 9, "portfolio_size": 18,
         "thesis": "Focus verticale su digital health, medtech e AI clinica."},
        {"nome": "Catalyst Angels", "tipo": "Angel", "ticket": "€10K–€80K",
         "ticket_min_k": 10, "ticket_max_k": 80, "focus_stage": "Pre-seed",
         "settori_preferiti": ["AI", "EdTech", "HealthTech", "Climate Tech"], "geografia": "Italia",
         "lead_follow": "Follow", "velocita_risposta_gg": 5, "portfolio_size": 9,
         "thesis": "Angel investing con forte coinvolgimento operativo e rete di contatti."},
        {"nome": "NordEst Investimenti", "tipo": "Corporate VC", "ticket": "€300K–€2M",
         "ticket_min_k": 300, "ticket_max_k": 2000, "focus_stage": "Seed",
         "settori_preferiti": ["Mobility", "AI", "PropTech"], "geografia": "Nord-Est Italia",
         "lead_follow": "Follow", "velocita_risposta_gg": 15, "portfolio_size": 14,
         "thesis": "Corporate VC che connette startup alla rete industriale del Nord-Est."},
    ])


# ─────────────────────────────────────────────────────────────
# MATCHING ENGINE
# ─────────────────────────────────────────────────────────────

STAGE_COMPAT_INV = {
    "Pre-seed": {"Idea": 95, "MVP": 70, "Traction": 30, "Revenue": 10},
    "Seed":     {"Idea": 40, "MVP": 88, "Traction": 92, "Revenue": 45},
    "Series A": {"Idea": 5,  "MVP": 30, "Traction": 90, "Revenue": 95},
    "Growth":   {"Idea": 0,  "MVP": 5,  "Traction": 45, "Revenue": 92},
}
STAGE_COMPAT_CORP = {
    "PMI":        {"Idea": 45, "MVP": 80, "Traction": 72, "Revenue": 60},
    "Mid-market": {"Idea": 20, "MVP": 60, "Traction": 90, "Revenue": 85},
    "Enterprise": {"Idea": 5,  "MVP": 35, "Traction": 86, "Revenue": 95},
}
OBJ_COLLAB_MAP = {
    "Fundraising":     {"Investimento": 92, "Scouting": 42, "Pilot": 20, "Partnership": 28},
    "Pilot aziendale": {"Pilot": 97, "Scouting": 72, "Partnership": 62, "Investimento": 18},
    "Partnership":     {"Partnership": 95, "Pilot": 70, "Scouting": 55, "Investimento": 20},
    "Mentorship":      {"Partnership": 50, "Pilot": 35, "Scouting": 50, "Investimento": 20},
    "Co-founder":      {"Partnership": 35, "Pilot": 20, "Scouting": 25, "Investimento": 12},
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
GEO_NORTH  = {"Milano", "Torino", "Bergamo", "Padova", "Genova", "Verona", "Trieste"}
GEO_CENTER = {"Roma", "Bologna", "Firenze"}


def _geo(citta):
    if citta in GEO_NORTH:  return "Nord"
    if citta in GEO_CENTER: return "Centro"
    return "Sud"


def compute_investor_match(startup, investor):
    scores, reasons = {}, []
    s_sec = startup["settore"]
    inv_secs = investor["settori_preferiti"]
    if s_sec in inv_secs:
        scores["Settore"] = 96
        reasons.append(f"Il settore {s_sec} è tra i focus dell'investitore.")
    elif any(r in inv_secs for r in RELATED_SECTORS.get(s_sec, [])):
        scores["Settore"] = 64
        reasons.append(f"Il settore {s_sec} è affine ai focus dell'investitore.")
    else:
        scores["Settore"] = 16
    stage_sc = STAGE_COMPAT_INV.get(investor["focus_stage"], {}).get(startup["stadio"], 30)
    scores["Stadio"] = stage_sc
    if stage_sc >= 80:
        reasons.append(f"Lo stadio {startup['stadio']} è coerente con il focus {investor['focus_stage']}.")
    inv_geo = investor["geografia"]
    s_region = _geo(startup["citta"])
    if "Europa" in inv_geo or inv_geo == "Italia" or inv_geo == "Italia & Europa":
        scores["Geografia"] = 86
    elif "Nord" in inv_geo and s_region == "Nord":
        scores["Geografia"] = 95
        reasons.append("Allineamento geografico nel Nord Italia.")
    else:
        scores["Geografia"] = 52
    need_map = {"Idea": 100, "MVP": 300, "Traction": 900, "Revenue": 2500}
    need = need_map.get(startup["stadio"], 500)
    if investor["ticket_min_k"] <= need <= investor["ticket_max_k"]:
        scores["Ticket"] = 95
        reasons.append("Il ticket copre il fabbisogno stimato della startup.")
    elif investor["ticket_min_k"] <= need * 1.3 and need * 0.6 <= investor["ticket_max_k"]:
        scores["Ticket"] = 66
    else:
        scores["Ticket"] = 20
    w = {"Settore": 0.30, "Stadio": 0.25, "Geografia": 0.15, "Ticket": 0.30}
    overall = round(sum(scores[k] * w[k] for k in w))
    return overall, scores, reasons


def compute_company_match(startup, company):
    scores, reasons = {}, []
    if startup["settore"] == company["area_innovazione"]:
        scores["Settore"] = 96
        reasons.append(f"L'area {company['area_innovazione']} coincide con il settore della startup.")
    elif startup["settore"] in RELATED_SECTORS.get(company["area_innovazione"], []):
        scores["Settore"] = 60
        reasons.append("Il settore della startup è affine all'area di innovazione dell'azienda.")
    else:
        scores["Settore"] = 18
    collab_sc = OBJ_COLLAB_MAP.get(startup["obiettivo"], {}).get(company["collaborazione"], 25)
    scores["Collaborazione"] = collab_sc
    if collab_sc >= 70:
        reasons.append(f"L'obiettivo '{startup['obiettivo']}' è compatibile con '{company['collaborazione']}'.")
    stage_sc = STAGE_COMPAT_CORP.get(company["dimensione"], {}).get(startup["stadio"], 35)
    scores["Stadio"] = stage_sc
    if stage_sc >= 75:
        reasons.append(f"La maturità {startup['stadio']} è adatta a una {company['dimensione']}.")
    if _geo(startup["citta"]) == _geo(company["citta"]):
        scores["Geografia"] = 90
        reasons.append("Prossimità geografica favorevole.")
    else:
        scores["Geografia"] = 55
    w = {"Settore": 0.35, "Collaborazione": 0.30, "Stadio": 0.20, "Geografia": 0.15}
    overall = round(sum(scores[k] * w[k] for k in w))
    return overall, scores, reasons


def find_top_matches(entity_row, candidates_df, match_fn, n=5):
    results = []
    for _, cand in candidates_df.iterrows():
        sc, subs, reasons = match_fn(entity_row, cand)
        row = cand.to_dict()
        row.update({"score": sc, "sub_scores": subs, "reasons": reasons})
        results.append(row)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:n], results


# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────

df_startups  = generate_startups()
df_companies = generate_companies()
df_investors = generate_investors()

DEMO_STARTUP = df_startups[df_startups["nome"] == "Nexara"].iloc[0]
DEMO_COMPANY = df_companies[df_companies["nome"] == "RetailMax"].iloc[0]
DEMO_INVESTOR = df_investors[df_investors["nome"] == "Mediterraneo Ventures"].iloc[0]

TOP_CO_FOR_NEXARA, _  = find_top_matches(DEMO_STARTUP, df_companies, compute_company_match, 5)
TOP_INV_FOR_NEXARA, _ = find_top_matches(DEMO_STARTUP, df_investors, compute_investor_match, 5)
TOP_S_FOR_RETAIL, _   = find_top_matches(DEMO_COMPANY, df_startups, lambda co, s: compute_company_match(s, co), 5)
TOP_S_FOR_MEDV, _     = find_top_matches(DEMO_INVESTOR, df_startups, lambda inv, s: compute_investor_match(s, inv), 5)


# ─────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────

def _sc(score):
    if score >= 80: return ACCENT
    if score >= 60: return AMBER
    return CORAL


def _ini(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def _trunc(text, n=120):
    return text if len(text) <= n else text[:n].rstrip() + "…"


def section_title(title, subtitle=""):
    st.markdown(f'<div class="nf-sec"><h2>{title}</h2><div class="bar"></div></div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="nf-sec-sub">{subtitle}</div>', unsafe_allow_html=True)


def kpi_card(label, value, icon="", delta=""):
    st.markdown(f"""
    <div class="nf-kpi">
        <div style="font-size:1.35rem;">{icon}</div>
        <div class="nf-kpi-label">{label}</div>
        <div class="nf-kpi-value">{value}</div>
        <div class="nf-kpi-delta">{delta}</div>
    </div>""", unsafe_allow_html=True)


def profile_progress(score, label="Qualità profilo"):
    c = _sc(score)
    return f"""
    <div class="nf-progress-wrap">
        <div class="nf-progress-head">
            <span>{label}</span>
            <span style="font-weight:700; color:{c};">{score}%</span>
        </div>
        <div class="nf-progress">
            <div class="nf-progress-fill" style="width:{score}%; background:{c};"></div>
        </div>
    </div>"""


def startup_card_html(s):
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
            <div class="nf-avatar nf-avatar-startup">{_ini(s["nome"])}</div>
            <div>
                <div class="nf-profile-name">{s["nome"]}</div>
                <div class="nf-profile-sub">{s["founder"]} · 📍 {s["citta"]}</div>
            </div>
        </div>
        <div>{badges}</div>
        <div class="nf-profile-text">{_trunc(s["descrizione"], 110)}</div>
        <div class="nf-profile-sub" style="margin-top:0.45rem;">👥 {s["team_size"]} persone · 💰 {s["funding_need"]}</div>
        {profile_progress(int(s["score_profilo"]))}
    </div>"""


def company_card_html(c):
    badges = (
        f'<span class="nf-pill nf-pill-accent">{c["area_innovazione"]}</span>'
        f'<span class="nf-pill nf-pill-coral">{c["dimensione"]}</span>'
        f'<span class="nf-pill nf-pill-primary">{c["collaborazione"]}</span>'
    )
    if c.get("premium"):
        badges += '<span class="nf-pill nf-pill-amber">Premium</span>'
    return f"""
    <div class="nf-profile">
        <div class="nf-profile-head">
            <div class="nf-avatar nf-avatar-company">{_ini(c["nome"])}</div>
            <div>
                <div class="nf-profile-name">{c["nome"]}</div>
                <div class="nf-profile-sub">{c["settore"]} · 📍 {c["citta"]}</div>
            </div>
        </div>
        <div>{badges}</div>
        <div class="nf-profile-text">{_trunc(c["descrizione"], 120)}</div>
        <div class="nf-profile-sub" style="margin-top:0.45rem;">💳 Budget {c["budget_class"]} · ⏱️ {c["tempo_valutazione_gg"]} giorni</div>
    </div>"""


def investor_card_html(inv):
    badges = (
        f'<span class="nf-pill nf-pill-accent">{inv["tipo"]}</span>'
        f'<span class="nf-pill nf-pill-coral">{inv["focus_stage"]}</span>'
        f'<span class="nf-pill nf-pill-primary">{inv["lead_follow"]}</span>'
    )
    secs = ", ".join(inv["settori_preferiti"][:3]) if isinstance(inv["settori_preferiti"], list) else str(inv["settori_preferiti"])
    return f"""
    <div class="nf-profile">
        <div class="nf-profile-head">
            <div class="nf-avatar nf-avatar-investor">{_ini(inv["nome"])}</div>
            <div>
                <div class="nf-profile-name">{inv["nome"]}</div>
                <div class="nf-profile-sub">{inv["geografia"]}</div>
            </div>
        </div>
        <div>{badges}</div>
        <div class="nf-profile-text">{_trunc(inv["thesis"], 120)}</div>
        <div class="nf-profile-sub" style="margin-top:0.45rem;">🎯 {secs} · 💰 {inv["ticket"]}</div>
    </div>"""


def radar_chart(scores_dict, title=""):
    cats = list(scores_dict.keys())
    vals = list(scores_dict.values())
    cats += [cats[0]]
    vals += [vals[0]]
    fig = go.Figure(data=go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor="rgba(46,196,182,0.18)",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(color=ACCENT, size=5),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(0,0,0,0.08)"),
            angularaxis=dict(gridcolor="rgba(0,0,0,0.08)"),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, title=title, height=280,
        margin=dict(l=40, r=40, t=40, b=30),
    )
    return fig


def add_contact_request(startup_name, target_name, target_type, score):
    exists = any(
        r["startup"] == startup_name and r["target"] == target_name
        for r in st.session_state.contact_requests
    )
    if not exists:
        st.session_state.contact_requests.append({
            "startup": startup_name, "target": target_name,
            "tipo": target_type, "score": score,
            "stato": "Inviata",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        })
        return True
    return False


# ─────────────────────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────────────────────

def goto_step(n):
    st.session_state.currentStep = n


def render_nav_buttons():
    step = st.session_state.currentStep
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_l:
        if step > 0:
            if st.button("← Indietro", use_container_width=True, key="nav_back"):
                goto_step(step - 1)
                st.rerun()
    with col_r:
        if step < 7:
            # Step 2 (indice 2) richiede che userRole sia scelto per proseguire
            can_advance = True
            if step == 2 and st.session_state.userRole is None:
                can_advance = False
            if can_advance:
                if st.button("Avanti →", use_container_width=True, type="primary", key="nav_next"):
                    goto_step(step + 1)
                    st.rerun()


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:0.4rem 0 0.75rem 0;">
            <div style="font-size:1.65rem; font-weight:900; letter-spacing:-0.04em;">
                🔗 <span style="color:{ACCENT};">NexFound</span>
            </div>
            <div style="font-size:0.7rem; color:rgba(214,224,238,0.5);
                 text-transform:uppercase; letter-spacing:0.08em;">
                Demo V4 · Percorso guidato
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### Percorso demo")
        for i, label in enumerate(STEP_LABELS):
            is_current = i == st.session_state.currentStep
            is_done = i < st.session_state.currentStep
            prefix = "✅ " if is_done else ("▶ " if is_current else "○ ")
            btn_type = "primary" if is_current else "secondary"
            if st.button(f"{prefix}{label}", key=f"sb_{i}", use_container_width=True,
                         type=btn_type):
                # Allow going back or forward only to completed/current steps
                if i <= st.session_state.currentStep or (i == st.session_state.currentStep + 1):
                    goto_step(i)
                    st.rerun()

        if st.session_state.userRole:
            labels = {"startup": "🚀 Startup", "azienda": "🏢 Azienda", "investitore": "💰 Investitore"}
            st.markdown("---")
            st.markdown(f"**Ruolo attivo:** {labels[st.session_state.userRole]}")
            if st.button("← Cambia ruolo", use_container_width=True, key="change_role"):
                st.session_state.userRole = None
                st.session_state.currentStep = 2
                st.rerun()

        st.markdown("---")
        n_req = len(st.session_state.contact_requests)
        n_saved = len(st.session_state.saved_matches)
        st.markdown(f"""
        <div style="font-size:0.82rem; line-height:1.7;">
            📨 <b>{n_req}</b> richieste inviate<br>
            ⭐ <b>{n_saved}</b> match salvati
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:0.68rem; color:rgba(214,224,238,0.35);
             text-align:center; line-height:1.5;">
            Dati dimostrativi · © 2026 NexFound
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# STEP 1: HOME (comune)
# ─────────────────────────────────────────────────────────────

def step_home():
    st.markdown(f"""
    <div class="nf-hero">
        <h1>Nex<span style="color:{ACCENT};">Found</span></h1>
        <p>
            La piattaforma che connette <b>startup</b>, <b>aziende</b> e <b>investitori</b>
            con un motore di matching intelligente, profili strutturati e flussi di contatto
            pensati per trasformare opportunità potenziali in collaborazioni concrete.
        </p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Startup nel campione", str(len(df_startups)), "🚀", "dataset sintetico")
    with c2: kpi_card("Aziende nel campione", str(len(df_companies)), "🏢", "dataset sintetico")
    with c3: kpi_card("Investitori nel campione", str(len(df_investors)), "💰", "dataset sintetico")
    with c4: kpi_card("Match simulati", "1.247", "🎯", "+12% vs mese prec.")

    st.markdown(f"""
    <div class="nf-card nf-card-soft">
        <div class="nf-card-title">Come funziona questa demo</div>
        <div class="nf-card-text">
            Seguirai un percorso guidato di <b>8 step</b>: ti mostriamo il problema di mercato,
            ti facciamo scegliere il tuo ruolo, e poi vivi in prima persona il matching,
            il contatto e la dashboard. Ogni percorso è personalizzato per il tuo ruolo.
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nf-spotlight">
        <div class="nf-spotlight-title">Anteprima</div>
        <h3>Nexara riceve subito 3 match ad alta compatibilità</h3>
        <p>
            La piattaforma suggerisce opportunità rilevanti in pochi secondi,
            spiegando perché il match è forte.
        </p>
    </div>""", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    previews = [
        {"label": "Corporate #1", "name": TOP_CO_FOR_NEXARA[0]["nome"],
         "score": TOP_CO_FOR_NEXARA[0]["score"], "meta": TOP_CO_FOR_NEXARA[0]["collaborazione"]},
        {"label": "Corporate #2", "name": TOP_CO_FOR_NEXARA[1]["nome"],
         "score": TOP_CO_FOR_NEXARA[1]["score"], "meta": TOP_CO_FOR_NEXARA[1]["collaborazione"]},
        {"label": "Investor #1", "name": TOP_INV_FOR_NEXARA[0]["nome"],
         "score": TOP_INV_FOR_NEXARA[0]["score"], "meta": TOP_INV_FOR_NEXARA[0]["tipo"]},
    ]
    for col, item in zip([p1, p2, p3], previews):
        with col:
            st.markdown(f"""
            <div class="nf-match">
                <div class="nf-match-head">
                    <div>
                        <div class="nf-match-rank">{item["label"]}</div>
                        <div class="nf-match-name">{item["name"]}</div>
                        <span class="nf-pill nf-pill-primary">{item["meta"]}</span>
                    </div>
                    <div class="nf-match-score">
                        <div class="nf-match-score-value" style="color:{_sc(item['score'])};">{item["score"]}%</div>
                        <div class="nf-match-score-label">Fit</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    render_nav_buttons()


# ─────────────────────────────────────────────────────────────
# STEP 2: PROBLEMA (comune)
# ─────────────────────────────────────────────────────────────

def step_problema():
    section_title(
        "Il problema di mercato",
        "Startup, aziende e investitori hanno interessi compatibili, ma oggi faticano ancora a incontrarsi nel modo giusto.",
    )

    tabs = st.tabs(["🚀 Startup", "🏢 Aziende", "💰 Investitori"])

    pain_points = {
        0: [
            ("Poca visibilità qualificata", "Molte startup hanno buone idee ma non raggiungono le persone giuste."),
            ("Accesso limitato", "Arrivare a corporate e investitori richiede spesso network personale o eventi casuali."),
            ("Contatti poco rilevanti", "La maggior parte dell'outreach genera conversazioni a basso potenziale."),
        ],
        1: [
            ("Scouting dispersivo", "Le aziende faticano a costruire pipeline di innovazione efficienti."),
            ("Filtraggio inefficiente", "Capire quali startup meritano attenzione richiede tempo e risorse."),
            ("Canale poco strutturato", "Open innovation e venture clienting sono spesso gestiti in modo artigianale."),
        ],
        2: [
            ("Deal flow rumoroso", "Troppi profili, pochi segnali chiari."),
            ("Poche metriche strutturate", "La comparabilità tra startup early-stage è ancora debole."),
            ("Tempo sprecato", "Il filtraggio manuale toglie spazio ad analisi, relazione e supporto."),
        ],
    }

    for tab_idx, tab in enumerate(tabs):
        with tab:
            cols = st.columns(3)
            for col, (title, text) in zip(cols, pain_points[tab_idx]):
                with col:
                    st.markdown(f'<div class="nf-card"><div class="nf-card-title">{title}</div><div class="nf-card-text">{text}</div></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nf-note">
        <h3>NexFound non è un social generico</h3>
        <p>
            È una piattaforma di matching e relazione che aiuta le startup a emergere,
            le aziende a fare scouting e gli investitori a trovare deal flow qualificato.
        </p>
    </div>""", unsafe_allow_html=True)

    render_nav_buttons()


# ─────────────────────────────────────────────────────────────
# STEP 3: SCELTA RUOLO (comune — salva userRole)
# ─────────────────────────────────────────────────────────────

def step_scelta_ruolo():
    section_title(
        "Dimmi chi sei",
        "Seleziona il tuo ruolo. Ti mostreremo un percorso personalizzato con le opportunità più rilevanti per te.",
    )

    c1, c2, c3 = st.columns(3)
    roles = [
        ("startup", "🚀", "Sono una Startup",
         "Trova investitori e aziende partner per raccogliere capitali o avviare un pilot.", c1),
        ("azienda", "🏢", "Sono un'Azienda",
         "Trova startup innovative per scouting, pilot, partnership e open innovation.", c2),
        ("investitore", "💰", "Sono un Investitore",
         "Trova startup in linea con la tua tesi, filtrate per settore, stadio e geografia.", c3),
    ]
    for role_id, icon, title, desc, col in roles:
        with col:
            is_selected = st.session_state.userRole == role_id
            border = f"border-color: {ACCENT}; box-shadow: 0 4px 16px rgba(46,196,182,0.15);" if is_selected else ""
            st.markdown(f"""
            <div class="nf-role" style="{border}">
                <div class="icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>""", unsafe_allow_html=True)
            if st.button(
                "✓ Selezionato" if is_selected else "Seleziona →",
                key=f"role_{role_id}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
            ):
                st.session_state.userRole = role_id
                st.rerun()

    if st.session_state.userRole:
        role_names = {"startup": "Startup", "azienda": "Azienda", "investitore": "Investitore"}
        st.success(f"Ruolo selezionato: **{role_names[st.session_state.userRole]}**. Premi Avanti per continuare.")

    render_nav_buttons()


# ─────────────────────────────────────────────────────────────
# STEP 4: CASO D'USO GUIDATO (ramificato)
# ─────────────────────────────────────────────────────────────

def step_caso_uso():
    role = st.session_state.userRole
    if role == "startup":
        _caso_uso_startup()
    elif role == "azienda":
        _caso_uso_azienda()
    else:
        _caso_uso_investitore()
    render_nav_buttons()


def _caso_uso_startup():
    s = DEMO_STARTUP
    section_title(
        "Caso d'uso guidato — Alice e Nexara",
        "Una founder entra in piattaforma, viene scoperta e apre contatti di qualità.",
    )

    left, right = st.columns([1.55, 1])
    with left:
        st.markdown(f"""
        <div class="nf-spotlight">
            <div class="nf-spotlight-title">Founder scenario</div>
            <h3>Alice Colombo vuole aprire un pilot con una corporate retail</h3>
            <p>
                Alice è founder di <b>Nexara</b>, una startup AI in fase di <b>{s["stadio"]}</b>.
                Ha già traction, un team di <b>{s["team_size"]}</b> persone e una priorità molto chiara:
                trovare un <b>pilot aziendale</b> con un gruppo retail o una corporate interessata
                alla personalizzazione customer-facing.
            </p>
        </div>""", unsafe_allow_html=True)
        st.markdown(startup_card_html(s), unsafe_allow_html=True)

    with right:
        k1, k2 = st.columns(2)
        with k1: kpi_card("Utenti", f'{int(s["users"]):,}', "👥", "attivi")
        with k2: kpi_card("MRR", f'€{int(s["mrr"]):,}', "💰", "ricavi mensili")
        k3, k4 = st.columns(2)
        with k3: kpi_card("Crescita", f'{s["growth_pct"]}%', "📈", "mese su mese")
        with k4: kpi_card("Profilo", f'{s["score_profilo"]}/100', "⭐", "readiness alta")

    _render_journey_steps([
        ("1", "Compila il profilo", "Inserisce settore, stage, traction, obiettivi e materiali chiave."),
        ("2", "Riceve match", "La piattaforma genera corporate e investitori compatibili."),
        ("3", "Invia richiesta", "Alice manda una intro request contestualizzata."),
        ("4", "Avvia la relazione", "La richiesta viene accettata e si passa a call o pilot."),
    ])

    _render_match_preview("Top corporate per Nexara", TOP_CO_FOR_NEXARA[:3], "Corporate", "area_innovazione", "collaborazione")
    _render_match_preview("Top investitori per Nexara", TOP_INV_FOR_NEXARA[:3], "Investor", "tipo", "focus_stage")


def _caso_uso_azienda():
    co = DEMO_COMPANY
    section_title(
        "Caso d'uso guidato — RetailMax e l'innovazione AI",
        "Una corporate entra in piattaforma per trovare startup pronte a un pilot nel suo settore.",
    )

    left, right = st.columns([1.55, 1])
    with left:
        st.markdown(f"""
        <div class="nf-spotlight">
            <div class="nf-spotlight-title">Corporate scenario</div>
            <h3>RetailMax cerca startup AI per la customer experience</h3>
            <p>
                <b>RetailMax</b> è un gruppo retail <b>{co["dimensione"]}</b> con sede a <b>{co["citta"]}</b>.
                Il team innovazione vuole lanciare un <b>{co["collaborazione"].lower()}</b> con una startup
                che porti soluzioni AI per personalizzazione in-store, pricing dinamico e analytics avanzate.
            </p>
        </div>""", unsafe_allow_html=True)
        st.markdown(company_card_html(co), unsafe_allow_html=True)

    with right:
        k1, k2 = st.columns(2)
        with k1: kpi_card("Area innovazione", co["area_innovazione"], "🎯", "focus primario")
        with k2: kpi_card("Collaborazione", co["collaborazione"], "🤝", "tipo preferito")
        k3, k4 = st.columns(2)
        with k3: kpi_card("Budget", co["budget_class"], "💳", "disponibilità")
        with k4: kpi_card("Tempo valutazione", f'{co["tempo_valutazione_gg"]}gg', "⏱️", "media decisionale")

    _render_journey_steps([
        ("1", "Definisce i criteri", "Pubblica il suo interesse per AI, settore retail, tipo collaborazione pilot."),
        ("2", "Riceve match", "La piattaforma suggerisce startup con settore, livello di maturità e posizione compatibili."),
        ("3", "Valuta e contatta", "RetailMax esamina i profili e invia richieste di intro mirate."),
        ("4", "Avvia il pilot", "Il contatto viene accettato e si procede con la collaborazione."),
    ])

    _render_match_preview("Top startup per RetailMax", TOP_S_FOR_RETAIL[:3], "Startup", "settore", "stadio")


def _caso_uso_investitore():
    inv = DEMO_INVESTOR
    section_title(
        "Caso d'uso guidato — Mediterraneo Ventures e il deal flow",
        "Un investitore accede alla piattaforma per trovare startup allineate con la propria thesis.",
    )

    left, right = st.columns([1.55, 1])
    with left:
        secs = ", ".join(inv["settori_preferiti"][:3])
        st.markdown(f"""
        <div class="nf-spotlight">
            <div class="nf-spotlight-title">Investitore scenario</div>
            <h3>Mediterraneo Ventures cerca deal flow Seed in AI e SaaS</h3>
            <p>
                <b>Mediterraneo Ventures</b> è un fondo <b>{inv["tipo"]}</b> con ticket <b>{inv["ticket"]}</b>
                e focus su <b>{secs}</b>. Cerca startup in fase <b>{inv["focus_stage"]}</b>
                con traction dimostrata e un vantaggio competitivo difendibile.
            </p>
        </div>""", unsafe_allow_html=True)
        st.markdown(investor_card_html(inv), unsafe_allow_html=True)

    with right:
        k1, k2 = st.columns(2)
        with k1: kpi_card("Ticket", inv["ticket"], "💰", "range investimento")
        with k2: kpi_card("Focus stage", inv["focus_stage"], "🎯", "stadio preferito")
        k3, k4 = st.columns(2)
        with k3: kpi_card("Portfolio", str(inv["portfolio_size"]), "📁", "startup in portfolio")
        with k4: kpi_card("Risposta", f'{inv["velocita_risposta_gg"]}gg', "⚡", "tempo medio")

    _render_journey_steps([
        ("1", "Pubblica la thesis", "Definisce settori, stage, ticket e preferenze geografiche."),
        ("2", "Riceve deal flow filtrato", "La piattaforma mostra solo startup compatibili con la sua thesis."),
        ("3", "Analizza e richiede intro", "Esamina profili strutturati e avvia il contatto."),
        ("4", "Procede con il deal", "Dalla intro alla call conoscitiva, fino all'investimento."),
    ])

    _render_match_preview("Top startup per Mediterraneo Ventures", TOP_S_FOR_MEDV[:3], "Startup", "settore", "stadio")


def _render_journey_steps(steps):
    st.markdown("### Il percorso su NexFound")
    cols = st.columns(len(steps))
    for col, (num, title, text) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="nf-step">
                <div class="nf-step-num">{num}</div>
                <div class="nf-card-title">{title}</div>
                <div class="nf-card-text">{text}</div>
            </div>""", unsafe_allow_html=True)


def _render_match_preview(title, matches, match_type, badge1_key, badge2_key):
    st.markdown(f"### {title}")
    for r in matches:
        st.markdown(f"""
        <div class="nf-match">
            <div class="nf-match-head">
                <div>
                    <div class="nf-match-rank">{match_type} match</div>
                    <div class="nf-match-name">{r["nome"]}</div>
                    <span class="nf-pill nf-pill-accent">{r.get(badge1_key, "")}</span>
                    <span class="nf-pill nf-pill-primary">{r.get(badge2_key, "")}</span>
                </div>
                <div class="nf-match-score">
                    <div class="nf-match-score-value" style="color:{_sc(r['score'])};">{r["score"]}%</div>
                    <div class="nf-match-score-label">Compatibilità</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# STEP 5: MATCHING INTELLIGENTE (ramificato)
# ─────────────────────────────────────────────────────────────

def step_matching():
    role = st.session_state.userRole
    if role == "startup":
        _matching_startup()
    elif role == "azienda":
        _matching_azienda()
    else:
        _matching_investitore()
    render_nav_buttons()


def _matching_startup():
    section_title(
        "Matching Intelligente — Startup",
        "Il cuore del prodotto: ogni connessione è motivata, spiegabile e presentabile.",
    )

    startup_name = st.selectbox("Seleziona la tua startup", df_startups["nome"].tolist(), key="m_startup")
    s = df_startups[df_startups["nome"] == startup_name].iloc[0]
    st.markdown(startup_card_html(s), unsafe_allow_html=True)

    mode = st.radio("Tipo di matching", ["Corporate", "Investitori"], horizontal=True, key="m_mode_s")

    if mode == "Corporate":
        top, all_m = find_top_matches(s, df_companies, compute_company_match, 5)
        _render_full_matches(top, all_m, "corporate", s["nome"],
                             lambda r: (f'<span class="nf-pill nf-pill-accent">{r["area_innovazione"]}</span>'
                                        f'<span class="nf-pill nf-pill-coral">{r["dimensione"]}</span>'
                                        f'<span class="nf-pill nf-pill-primary">{r["collaborazione"]}</span>'),
                             "Azienda")
    else:
        top, all_m = find_top_matches(s, df_investors, compute_investor_match, 5)
        _render_full_matches(top, all_m, "investitori", s["nome"],
                             lambda r: (f'<span class="nf-pill nf-pill-accent">{r["tipo"]}</span>'
                                        f'<span class="nf-pill nf-pill-coral">{r["focus_stage"]}</span>'
                                        f'<span class="nf-pill nf-pill-primary">{r["ticket"]}</span>'),
                             "Investitore")


def _matching_azienda():
    section_title(
        "Matching Intelligente — Azienda",
        "Trova startup compatibili per scouting, pilot e partnership.",
    )

    company_name = st.selectbox("Seleziona il profilo aziendale", df_companies["nome"].tolist(), key="m_company")
    co = df_companies[df_companies["nome"] == company_name].iloc[0]
    st.markdown(company_card_html(co), unsafe_allow_html=True)

    top, all_m = find_top_matches(co, df_startups,
                                  lambda company_row, startup_row: compute_company_match(startup_row, company_row), 5)
    _render_full_matches(top, all_m, "startup", co["nome"],
                         lambda r: (f'<span class="nf-pill nf-pill-accent">{r["settore"]}</span>'
                                    f'<span class="nf-pill nf-pill-coral">{r["stadio"]}</span>'
                                    f'<span class="nf-pill nf-pill-primary">{r.get("obiettivo", "")}</span>'),
                         "Startup")


def _matching_investitore():
    section_title(
        "Matching Intelligente — Investitore",
        "Deal flow filtrato e compatibile con la tua thesis.",
    )

    inv_name = st.selectbox("Seleziona il profilo investitore", df_investors["nome"].tolist(), key="m_investor")
    inv = df_investors[df_investors["nome"] == inv_name].iloc[0]
    st.markdown(investor_card_html(inv), unsafe_allow_html=True)

    top, all_m = find_top_matches(inv, df_startups,
                                  lambda investor_row, startup_row: compute_investor_match(startup_row, investor_row), 5)
    _render_full_matches(top, all_m, "startup", inv["nome"],
                         lambda r: (f'<span class="nf-pill nf-pill-accent">{r["settore"]}</span>'
                                    f'<span class="nf-pill nf-pill-coral">{r["stadio"]}</span>'
                                    f'<span class="nf-pill nf-pill-primary">{r.get("obiettivo", "")}</span>'),
                         "Investitore")


def _render_full_matches(top_matches, all_matches, target_label, source_name, badges_fn, contact_type):
    best = top_matches[0]
    st.markdown(f"""
    <div class="nf-spotlight">
        <div class="nf-spotlight-title">Best match</div>
        <h3>{best["nome"]} — {best["score"]}% di compatibilità</h3>
        <p>Match più forte per <b>{source_name}</b> basato su settore, stadio, compatibilità e geografia.</p>
    </div>""", unsafe_allow_html=True)

    for idx, r in enumerate(top_matches):
        col_a, col_b = st.columns([3.1, 1.9])
        with col_a:
            reasons_html = "".join(f"<li>{x}</li>" for x in r["reasons"]) if r.get("reasons") else "<li>Compatibilità parziale.</li>"
            st.markdown(f"""
            <div class="nf-match">
                <div class="nf-match-head">
                    <div>
                        <div class="nf-match-rank">Match #{idx+1}</div>
                        <div class="nf-match-name">{r["nome"]}</div>
                        {badges_fn(r)}
                    </div>
                    <div class="nf-match-score">
                        <div class="nf-match-score-value" style="color:{_sc(r['score'])};">{r["score"]}%</div>
                        <div class="nf-match-score-label">Fit</div>
                    </div>
                </div>
                <div class="nf-card-text" style="margin-top:0.3rem;"><b>Perché questo match è forte</b></div>
                <ul class="nf-list">{reasons_html}</ul>
            </div>""", unsafe_allow_html=True)

            bc1, bc2, _ = st.columns([1, 1, 3])
            with bc1:
                if st.button("📨 Richiedi intro", key=f"intro_m_{idx}", use_container_width=True, type="primary"):
                    if add_contact_request(source_name, r["nome"], contact_type, r["score"]):
                        st.success(f"Richiesta inviata a {r['nome']}.")
                    else:
                        st.info("Richiesta già inviata.")
            with bc2:
                if st.button("⭐ Salva", key=f"save_m_{idx}", use_container_width=True):
                    rec = {"startup": source_name, "target": r["nome"], "tipo": contact_type, "score": r["score"]}
                    if rec not in st.session_state.saved_matches:
                        st.session_state.saved_matches.append(rec)
                    st.success("Match salvato.")

        with col_b:
            st.plotly_chart(radar_chart(r["sub_scores"], "Score per criterio"),
                            use_container_width=True, key=f"rad_m_{idx}")

    # Distribuzione score
    scores_dist = [x["score"] for x in all_matches]
    bins = ["0–30", "31–50", "51–70", "71–85", "86–100"]
    counts = [
        sum(s <= 30 for s in scores_dist),
        sum(31 <= s <= 50 for s in scores_dist),
        sum(51 <= s <= 70 for s in scores_dist),
        sum(71 <= s <= 85 for s in scores_dist),
        sum(86 <= s <= 100 for s in scores_dist),
    ]
    fig = px.bar(x=bins, y=counts, labels={"x": "Fascia punteggio", "y": "Numero match"},
                 color_discrete_sequence=[ACCENT])
    fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(gridcolor="rgba(0,0,0,0.06)"))
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# STEP 6: FLUSSO DI CONTATTO (ramificato)
# ─────────────────────────────────────────────────────────────

def step_contatto():
    role = st.session_state.userRole
    if role == "startup":
        _contatto_startup()
    elif role == "azienda":
        _contatto_azienda()
    else:
        _contatto_investitore()
    _render_request_status()
    render_nav_buttons()


def _contatto_startup():
    section_title(
        "Flusso di Contatto — Startup",
        "Dalla scoperta alla conversazione: scegli un target e invia la tua intro request.",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi_card("Profili visualizzati", "4.200", "👀", "")
    with col2: kpi_card("Match salvati", str(max(len(st.session_state.saved_matches), 12)), "⭐", "")
    with col3: kpi_card("Richieste inviate", str(len(st.session_state.contact_requests)), "📨", "")
    with col4: kpi_card("Intro positive", str(sum(1 for r in st.session_state.contact_requests if r["stato"] in ["Accettata", "Call programmata"])), "🤝", "")

    startup_name = st.selectbox("La tua startup", df_startups["nome"].tolist(), key="c_startup")
    s = df_startups[df_startups["nome"] == startup_name].iloc[0]

    target_type = st.radio("Destinatario", ["Azienda", "Investitore"], horizontal=True, key="c_target_type_s")

    if target_type == "Azienda":
        target_name = st.selectbox("Seleziona azienda", df_companies["nome"].tolist(), key="c_target_co")
        co = df_companies[df_companies["nome"] == target_name].iloc[0]
        score, _, _ = compute_company_match(s, co)
        message = (
            f"Gentile team Innovazione di {target_name},\n\n"
            f"mi chiamo {s['founder']}, founder di {s['nome']}, una startup {s['settore']} in fase di {s['stadio']}.\n\n"
            f"Stiamo cercando un {s['obiettivo'].lower()} e crediamo che la nostra soluzione possa essere rilevante "
            f"per la vostra area di innovazione ({co['area_innovazione']}).\n\n"
            f"{s['descrizione']}\n\n"
            f"Ci farebbe piacere organizzare una breve call per capire se ci sono le condizioni.\n\n"
            f"Cordiali saluti,\n{s['founder']}\n{s['nome']}"
        )
    else:
        target_name = st.selectbox("Seleziona investitore", df_investors["nome"].tolist(), key="c_target_inv")
        inv = df_investors[df_investors["nome"] == target_name].iloc[0]
        score, _, _ = compute_investor_match(s, inv)
        secs = ", ".join(inv["settori_preferiti"][:2])
        message = (
            f"Gentile team di {target_name},\n\n"
            f"mi chiamo {s['founder']} e sono founder di {s['nome']}, startup {s['settore']} in fase di {s['stadio']}.\n\n"
            f"Cerchiamo {s['obiettivo'].lower()} e il vostro focus su {secs} ci sembra allineato.\n\n"
            f"{s['descrizione']}\n\n"
            f"Sarei felice di condividere metriche e capire se può esserci un fit.\n\n"
            f"Cordiali saluti,\n{s['founder']}\n{s['nome']}"
        )

    _render_contact_form(score, message, startup_name, target_name, target_type)


def _contatto_azienda():
    section_title(
        "Flusso di Contatto — Azienda",
        "Seleziona una startup compatibile e avvia il processo di scouting o pilot.",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi_card("Startup analizzate", str(len(df_startups)), "🔍", "")
    with col2: kpi_card("Match salvati", str(max(len(st.session_state.saved_matches), 8)), "⭐", "")
    with col3: kpi_card("Richieste inviate", str(len(st.session_state.contact_requests)), "📨", "")
    with col4: kpi_card("Pilot avviati", "3", "🧪", "in corso")

    company_name = st.selectbox("La tua azienda", df_companies["nome"].tolist(), key="c_company")
    co = df_companies[df_companies["nome"] == company_name].iloc[0]

    target_name = st.selectbox("Seleziona startup", df_startups["nome"].tolist(), key="c_target_su")
    s = df_startups[df_startups["nome"] == target_name].iloc[0]
    score, _, _ = compute_company_match(s, co)

    message = (
        f"Gentile {s['founder']},\n\n"
        f"siamo {co['nome']}, un'azienda {co['settore']} ({co['dimensione']}) con sede a {co['citta']}.\n\n"
        f"Il nostro team innovazione è interessato alla vostra soluzione in ambito {s['settore']}. "
        f"Stiamo cercando opportunità di {co['collaborazione'].lower()} e il vostro profilo ci sembra molto rilevante.\n\n"
        f"Ci farebbe piacere organizzare una call conoscitiva per esplorare possibili sinergie.\n\n"
        f"Cordiali saluti,\nTeam Innovazione\n{co['nome']}"
    )

    _render_contact_form(score, message, target_name, company_name, "Azienda")


def _contatto_investitore():
    section_title(
        "Flusso di Contatto — Investitore",
        "Richiedi un'intro alle startup più allineate con la tua thesis.",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi_card("Startup screened", str(len(df_startups)), "📋", "")
    with col2: kpi_card("Match salvati", str(max(len(st.session_state.saved_matches), 6)), "⭐", "")
    with col3: kpi_card("Intro richieste", str(len(st.session_state.contact_requests)), "📨", "")
    with col4: kpi_card("Deal in pipeline", "2", "🎯", "attivi")

    inv_name = st.selectbox("Il tuo profilo investitore", df_investors["nome"].tolist(), key="c_investor")
    inv = df_investors[df_investors["nome"] == inv_name].iloc[0]

    target_name = st.selectbox("Seleziona startup", df_startups["nome"].tolist(), key="c_target_si")
    s = df_startups[df_startups["nome"] == target_name].iloc[0]
    score, _, _ = compute_investor_match(s, inv)

    secs = ", ".join(inv["settori_preferiti"][:2])
    message = (
        f"Gentile {s['founder']},\n\n"
        f"siamo {inv['nome']}, un fondo {inv['tipo']} con focus su {secs} e ticket {inv['ticket']}.\n\n"
        f"Il vostro profilo in ambito {s['settore']} (fase {s['stadio']}) ci sembra molto interessante "
        f"rispetto alla nostra thesis. Vorremmo capire se ci sono le condizioni per approfondire.\n\n"
        f"Sarebbe disponibile per una call conoscitiva di 30 minuti?\n\n"
        f"Cordiali saluti,\nTeam Investimenti\n{inv['nome']}"
    )

    _render_contact_form(score, message, target_name, inv_name, "Investitore")


def _render_contact_form(score, message, startup_name, target_name, target_type):
    st.markdown(f"""
    <div class="nf-card">
        <div class="nf-card-title">Preview della richiesta</div>
        <div class="nf-card-text">
            Match score: <b style="color:{_sc(score)};">{score}%</b>
        </div>
    </div>""", unsafe_allow_html=True)

    st.text_area("Messaggio generato", message, height=200, key="contact_msg")

    c_send, _ = st.columns([1.2, 3])
    with c_send:
        if st.button("📨 Invia richiesta", use_container_width=True, type="primary", key="send_contact"):
            if add_contact_request(startup_name, target_name, target_type, score):
                st.success(f"Richiesta inviata a {target_name}.")
            else:
                st.info("Richiesta già inviata.")


def _render_request_status():
    if not st.session_state.contact_requests:
        return

    st.markdown("### Stato delle richieste")
    status_options = ["Inviata", "In revisione", "Accettata", "Call programmata"]
    status_colors = {
        "Inviata": AMBER, "In revisione": PRIMARY,
        "Accettata": SUCCESS, "Call programmata": ACCENT,
    }

    for idx, req in enumerate(st.session_state.contact_requests):
        c1, c2, c3, c4 = st.columns([2.5, 2.5, 1, 2])
        with c1:
            st.markdown(f"**{req['startup']}**")
        with c2:
            st.markdown(f"→ {req['target']}")
        with c3:
            sc_color = _sc(req["score"])
            st.markdown(f"<span style='font-weight:800; color:{sc_color};'>{req['score']}%</span>", unsafe_allow_html=True)
        with c4:
            new_status = st.selectbox(
                f"Stato", status_options,
                index=status_options.index(req["stato"]),
                key=f"req_st_{idx}", label_visibility="collapsed",
            )
            st.session_state.contact_requests[idx]["stato"] = new_status


# ─────────────────────────────────────────────────────────────
# STEP 7: DASHBOARD KPI (comune)
# ─────────────────────────────────────────────────────────────

def step_dashboard():
    section_title(
        "Dashboard KPI",
        "Le metriche che raccontano il valore della piattaforma a incubatori, partner e investitori.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Startup registrate", "247", "🚀", "+18 questo mese")
    with c2: kpi_card("Aziende attive", "68", "🏢", "+5 questo mese")
    with c3: kpi_card("Investitori attivi", "42", "💰", "+3 questo mese")
    with c4: kpi_card("Startup verificate", "112", "✅", "45% del totale")

    c5, c6, c7, c8 = st.columns(4)
    with c5: kpi_card("Match generati", "1.247", "🎯", "+12% vs mese prec.")
    with c6: kpi_card("Richieste inviate", "583", "📨", "+8% vs mese prec.")
    with c7: kpi_card("Tasso risposta", "56%", "📊", "+3pp vs mese prec.")
    with c8: kpi_card("Call fissate", "156", "📞", "+11% vs mese prec.")

    tab1, tab2, tab3, tab4 = st.tabs(["Settori", "Stage", "Funnel", "Trend"])

    with tab1:
        sector_counts = df_startups["settore"].value_counts().reset_index()
        sector_counts.columns = ["Settore", "Numero"]
        fig = px.bar(sector_counts, x="Settore", y="Numero", color="Settore",
                     color_discrete_map=SECTOR_COLORS)
        fig.update_layout(height=360, showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=20, b=20),
                          yaxis=dict(gridcolor="rgba(0,0,0,0.06)"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        stage_counts = df_startups["stadio"].value_counts().reset_index()
        stage_counts.columns = ["Stadio", "Numero"]
        fig = px.pie(stage_counts, names="Stadio", values="Numero", hole=0.45,
                     color_discrete_sequence=[PRIMARY, ACCENT, CORAL, AMBER])
        fig.update_layout(height=360, paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        funnel_y = ["Profili visualizzati", "Match generati", "Match salvati",
                    "Richieste inviate", "Intro accettate", "Call fissate"]
        funnel_x = [8400, 1247, 890, 583, 328, 156]
        fig = go.Figure(go.Funnel(
            y=funnel_y, x=funnel_x,
            textinfo="value+percent initial",
            marker=dict(color=[PRIMARY, PRIMARY_2, "#315A92", ACCENT, ACCENT_DK, CORAL]),
            connector=dict(line=dict(color=BORDER)),
        ))
        fig.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        months = pd.date_range("2025-01-01", periods=12, freq="MS")
        rng = np.random.RandomState(SEED)
        startup_g = np.cumsum(rng.randint(8, 22, size=12)) + 70
        match_g = np.cumsum(rng.randint(35, 95, size=12)) + 200
        intro_g = np.cumsum(rng.randint(12, 38, size=12)) + 50

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=startup_g, mode="lines+markers",
                                 name="Startup registrate", line=dict(color=PRIMARY, width=2.5)))
        fig.add_trace(go.Scatter(x=months, y=match_g, mode="lines+markers",
                                 name="Match generati", line=dict(color=ACCENT, width=2.5)))
        fig.add_trace(go.Scatter(x=months, y=intro_g, mode="lines+markers",
                                 name="Richieste inviate", line=dict(color=CORAL, width=2.5, dash="dot")))
        fig.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=20, r=20, t=20, b=20),
                          yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    render_nav_buttons()


# ─────────────────────────────────────────────────────────────
# STEP 8: CONCLUSIONE (comune)
# ─────────────────────────────────────────────────────────────

def step_conclusione():
    section_title(
        "Conclusione",
        "Questa demo mostra NexFound come prodotto, non solo come idea.",
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="nf-card">
            <div class="nf-card-title">Cosa rende forte NexFound</div>
            <div class="nf-card-text">
                • Posizionamento chiaro: startup + corporate + investitori<br>
                • Matching spiegabile e non casuale<br>
                • Profili strutturati, non semplici pagine social<br>
                • Workflow che va oltre la scoperta e arriva al contatto<br>
                • Demo centrata su un use case reale e memorabile
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="nf-card">
            <div class="nf-card-title">Cosa dimostra questa POC</div>
            <div class="nf-card-text">
                La piattaforma è già comprensibile come esperienza utente:
                si vede bene come un utente entra, come viene letto il suo profilo,
                come vengono generati i match e come nasce una relazione operativa.
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="nf-card">
            <div class="nf-card-title">Prossimi passi realistici</div>
            <div class="nf-card-text">
                1. Validazione con startup e corporate pilota<br>
                2. MVP con autenticazione e profili reali<br>
                3. Algoritmo di ranking più sofisticato<br>
                4. Workflow intro / call / data room<br>
                5. Partnership con incubatori e innovation hub
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="nf-card">
            <div class="nf-card-title">Messaggio finale</div>
            <div class="nf-card-text">
                NexFound non vuole essere "un altro social".
                Vuole diventare il luogo in cui le idee promettenti trovano davvero
                il capitale, i partner e le corporate che possono farle crescere.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nf-note">
        <h3>NexFound — dove l'innovazione incontra l'opportunità</h3>
        <p>
            Una piattaforma pensata per far emergere le startup giuste davanti alle persone giuste,
            con il giusto contesto per iniziare una relazione di valore.
        </p>
    </div>""", unsafe_allow_html=True)

    # CTA finale
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DK} 100%);
         border-radius: 16px; padding: 2.2rem 2rem; text-align: center;
         position: relative; overflow: hidden; margin-top: 2rem;">
        <h2 style="color: #fff; font-size: 1.4rem; font-weight: 800;
            margin: 0 0 0.4rem 0; position: relative;">
            Vuoi provare NexFound con i tuoi dati?
        </h2>
        <p style="color: rgba(255,255,255,0.78); font-size: 0.92rem;
            max-width: 480px; margin: 0 auto; line-height: 1.5; position: relative;">
            Prenota una demo personalizzata e scopri come accelerare le tue connessioni strategiche.
        </p>
    </div>""", unsafe_allow_html=True)

    render_nav_buttons()


# ─────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────

STEP_FNS = [
    step_home,           # 0
    step_problema,       # 1
    step_scelta_ruolo,   # 2
    step_caso_uso,       # 3
    step_matching,       # 4
    step_contatto,       # 5
    step_dashboard,      # 6
    step_conclusione,    # 7
]


def main():
    render_sidebar()

    step = st.session_state.currentStep

    # Se si prova ad accedere agli step 3-5 senza ruolo, torna a step 2
    if step in (3, 4, 5) and st.session_state.userRole is None:
        st.session_state.currentStep = 2
        step = 2

    # Header compatto dopo la selezione del ruolo (step >= 3)
    if step >= 3 and st.session_state.userRole:
        labels = {"startup": "🚀 Startup", "azienda": "🏢 Azienda", "investitore": "💰 Investitore"}
        st.markdown(f"""
        <div class="nf-header">
            <div class="logo">🔗 Nex<span style="color:{ACCENT};">Found</span></div>
            <div class="role-pill">{labels[st.session_state.userRole]} · Step {step + 1}/8</div>
        </div>""", unsafe_allow_html=True)

    STEP_FNS[step]()


if __name__ == "__main__":
    main()
