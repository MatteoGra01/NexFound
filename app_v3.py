"""
NexFound — Trova il match giusto per il tuo obiettivo.

Piattaforma di matching intelligente tra startup, aziende e investitori.
Single-page, role-first, outcome-driven experience.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# CONFIGURAZIONE
# ─────────────────────────────────────────────────────────────

SEED = 42
np.random.seed(SEED)

st.set_page_config(
    page_title="NexFound — Matching intelligente",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
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
CARD_BG   = "#FFFFFF"
BORDER    = "#E8ECF3"

SETTORI   = ["AI", "Fintech", "Climate Tech", "HealthTech", "SaaS B2B",
             "HR Tech", "PropTech", "Cybersecurity", "Mobility", "EdTech"]
STADI     = ["Idea", "MVP", "Traction", "Revenue"]
CITTA     = ["Milano", "Roma", "Torino", "Bologna", "Firenze", "Napoli",
             "Padova", "Bergamo", "Genova", "Verona", "Bari", "Trieste"]
OBIETTIVI = ["Fundraising", "Pilot aziendale", "Partnership", "Mentorship", "Co-founder"]


# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}
.block-container {{
    max-width: 1100px;
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
    border-radius: 20px;
    padding: 3.2rem 3rem 2.8rem;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}}
.nf-hero::before {{
    content: '';
    position: absolute;
    top: -50%; right: -12%;
    width: 420px; height: 420px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(46,196,182,0.14) 0%, transparent 70%);
}}
.nf-hero h1 {{
    font-size: 2.7rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    margin: 0 0 0.6rem 0;
    position: relative;
    line-height: 1.15;
}}
.nf-hero p {{
    font-size: 1.06rem;
    color: rgba(255,255,255,0.72);
    max-width: 600px;
    line-height: 1.65;
    position: relative;
    margin: 0;
}}
.nf-hero .proof {{
    margin-top: 1.4rem;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.02em;
    position: relative;
}}

/* ── Compact header ──────────────── */
.nf-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.4rem 0 0.7rem 0;
    margin-bottom: 0.6rem;
    border-bottom: 2px solid {BORDER};
}}
.nf-header .logo {{
    font-size: 1.35rem;
    font-weight: 900;
    color: {TEXT};
    letter-spacing: -0.04em;
}}
.nf-header .role-pill {{
    padding: 5px 14px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    background: rgba(46,196,182,0.12);
    color: {ACCENT_DK};
}}

/* ── Role card ───────────────────── */
.nf-role {{
    background: {CARD_BG};
    border: 2px solid {BORDER};
    border-radius: 16px;
    padding: 1.6rem 1.1rem 1.1rem;
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
.nf-role p {{
    font-size: 0.84rem; color: {TEXT_2}; line-height: 1.5; margin: 0;
}}

/* ── Section heading ─────────────── */
.nf-sec h2 {{
    font-size: 1.5rem; font-weight: 800; letter-spacing: -0.03em;
    color: {TEXT}; margin: 0 0 0.15rem 0;
}}
.nf-sec .bar {{
    width: 38px; height: 3px; background: {ACCENT};
    border-radius: 2px; margin: 5px 0 0 0;
}}
.nf-sec-sub {{
    font-size: 0.92rem; color: {TEXT_2};
    margin: 0.4rem 0 1.3rem 0; line-height: 1.5;
}}

/* ── Info box ────────────────────── */
.nf-info {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT}; border-radius: 12px;
    padding: 1rem 1.3rem; margin-bottom: 1.2rem;
}}
.nf-info p {{ color: {TEXT_2}; font-size: 0.9rem; line-height: 1.6; margin: 0; }}

/* ── Profile compact ─────────────── */
.nf-profile {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT}; border-radius: 12px;
    padding: 0.85rem 1.2rem; margin-bottom: 1rem;
}}
.nf-profile .name {{ font-weight: 700; color: {TEXT}; font-size: 1rem; }}
.nf-profile .meta {{ font-size: 0.83rem; color: {TEXT_2}; margin-top: 2px; }}

/* ── Badge ───────────────────────── */
.nf-b {{
    display: inline-block; padding: 3px 9px; border-radius: 6px;
    font-size: 0.71rem; font-weight: 600;
    margin-right: 4px; margin-bottom: 4px;
}}
.nf-b-accent  {{ background: rgba(46,196,182,0.12); color: {ACCENT_DK}; }}
.nf-b-primary {{ background: rgba(23,43,77,0.08); color: {PRIMARY}; }}
.nf-b-coral   {{ background: rgba(255,107,107,0.12); color: #D94B4B; }}
.nf-b-success {{ background: rgba(34,197,94,0.12); color: #16803C; }}
.nf-b-amber   {{ background: rgba(255,179,71,0.15); color: #A76400; }}
.nf-b-gray    {{ background: #F1F4F9; color: {TEXT_3}; }}

/* ── Match card ──────────────────── */
.nf-match {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.15rem 1.25rem;
    margin-bottom: 0.85rem; position: relative; overflow: hidden;
    box-shadow: 0 1px 3px rgba(23,43,77,0.04), 0 4px 12px rgba(23,43,77,0.05);
    transition: transform 0.12s, box-shadow 0.12s;
}}
.nf-match:hover {{
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(23,43,77,0.06), 0 8px 20px rgba(23,43,77,0.08);
}}
.nf-match::before {{
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
}}
.nf-match-high::before {{ background: {ACCENT}; }}
.nf-match-mid::before  {{ background: {AMBER}; }}
.nf-match-low::before  {{ background: {CORAL}; }}
.nf-match .m-top {{
    display: flex; justify-content: space-between; align-items: flex-start;
}}
.nf-match .m-rank {{
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.05em; color: {TEXT_3};
}}
.nf-match .m-name {{
    font-size: 1.06rem; font-weight: 800; color: {TEXT}; margin: 2px 0 5px 0;
}}
.nf-match .m-score {{ text-align: center; min-width: 58px; }}
.nf-match .m-score-val {{
    font-size: 1.8rem; font-weight: 900; line-height: 1; letter-spacing: -0.04em;
}}
.nf-match .m-score-lbl {{
    font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.05em; color: {TEXT_3};
}}
.nf-match .m-why {{
    margin-top: 0.55rem; padding-top: 0.55rem; border-top: 1px solid {BORDER};
}}
.nf-match .m-why-t {{
    font-size: 0.72rem; font-weight: 700; color: {TEXT_3};
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.2rem;
}}
.nf-match .m-why ul {{
    margin: 0; padding-left: 1rem;
    font-size: 0.85rem; color: {TEXT_2}; line-height: 1.55;
}}

/* ── CTA block ───────────────────── */
.nf-cta {{
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DK} 100%);
    border-radius: 16px; padding: 2.2rem 2rem; text-align: center;
    position: relative; overflow: hidden; margin-top: 2rem;
}}
.nf-cta::before {{
    content: ''; position: absolute; top: -40%; right: -15%;
    width: 260px; height: 260px; border-radius: 50%;
    background: rgba(255,255,255,0.06);
}}
.nf-cta h2 {{
    color: #fff; font-size: 1.4rem; font-weight: 800;
    margin: 0 0 0.4rem 0; position: relative;
}}
.nf-cta p {{
    color: rgba(255,255,255,0.78); font-size: 0.92rem;
    max-width: 480px; margin: 0 auto; line-height: 1.5; position: relative;
}}

/* ── Steps flow ──────────────────── */
.nf-steps {{
    display: flex; align-items: center; justify-content: center;
    gap: 0.3rem; flex-wrap: wrap; margin: 1.3rem 0;
}}
.nf-steps .step {{
    padding: 7px 14px; background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 8px; font-size: 0.83rem; font-weight: 500; color: {TEXT};
}}
.nf-steps .arrow {{ color: {ACCENT}; font-weight: 700; font-size: 1rem; }}

/* ── Mini metric ─────────────────── */
.nf-met {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 0.6rem 0.8rem; margin-bottom: 0.5rem;
    text-align: center;
}}
.nf-met .lbl {{
    font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.05em;
    font-weight: 600; color: {TEXT_3}; margin: 0;
}}
.nf-met .val {{
    font-size: 1.2rem; font-weight: 800; color: {TEXT};
    letter-spacing: -0.03em; margin: 0.08rem 0 0 0;
}}

/* ── Request row ─────────────────── */
.nf-req {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 12px;
}}
.nf-req .req-info {{ flex: 1; }}
.nf-req .req-name {{ font-weight: 700; color: {TEXT}; font-size: 0.9rem; }}
.nf-req .req-meta {{ font-size: 0.78rem; color: {TEXT_3}; }}

/* ── Overrides ───────────────────── */
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px 8px 0 0; font-weight: 600; font-size: 0.85rem;
}}
.js-plotly-plot .plotly .modebar {{ display: none !important; }}
</style>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

for _k, _v in {"role": None, "contact_requests": [], "saved_matches": []}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─────────────────────────────────────────────────────────────
# DATI
# ─────────────────────────────────────────────────────────────

@st.cache_data
def load_startups():
    rng = np.random.RandomState(SEED)
    names = [
        "Nexara", "FinSmart", "GreenPulse", "MedIntel", "DataForge",
        "TalentUp", "CasaClick", "SecureNet", "MoveFlow", "LearnHub",
        "Visionary AI", "PayLoop", "SolarMind", "VitaLink", "CloudMetrics",
        "HireWise", "BuildView", "VaultEdge", "FleetPulse", "StudyVerse",
        "Predictiva", "CarbonLess", "NurseBot", "APILayer",
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
        "AI per personalizzare l'esperienza di acquisto in-store e online nel retail.",
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
    rows = []
    for i in range(24):
        settore = SETTORI[i % len(SETTORI)]
        if i == 0:
            rows.append({
                "nome": "Nexara", "settore": "AI",
                "descrizione": descriptions[0], "stadio": "Traction",
                "citta": "Milano", "team_size": 11, "founder": "Alice Colombo",
                "obiettivo": "Pilot aziendale", "users": 5400, "mrr": 18000,
                "growth_pct": 22.4, "score_profilo": 92, "verificata": True,
                "funding_need": "Seed €500K–€1.2M",
            })
            continue
        stadio = STADI[rng.randint(0, len(STADI))]
        citta = CITTA[rng.randint(0, len(CITTA))]
        obiettivo = OBIETTIVI[rng.randint(0, len(OBIETTIVI))]
        team = int(rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 24]))
        if stadio == "Idea":
            users, mrr, growth = int(rng.randint(0, 80)), 0, 0.0
            funding = "Pre-seed €50K–€150K"
        elif stadio == "MVP":
            users = int(rng.randint(80, 600))
            mrr = int(rng.randint(0, 2500))
            growth = round(float(rng.uniform(2, 15)), 1)
            funding = "Seed €150K–€500K"
        elif stadio == "Traction":
            users = int(rng.randint(600, 12000))
            mrr = int(rng.randint(3000, 22000))
            growth = round(float(rng.uniform(5, 30)), 1)
            funding = "Seed / Series A €500K–€2M"
        else:
            users = int(rng.randint(5000, 95000))
            mrr = int(rng.randint(12000, 100000))
            growth = round(float(rng.uniform(3, 22)), 1)
            funding = "Series A+ €1M–€5M"
        rows.append({
            "nome": names[i], "settore": settore, "descrizione": descriptions[i],
            "stadio": stadio, "citta": citta, "team_size": team,
            "founder": founders[i], "obiettivo": obiettivo,
            "users": users, "mrr": mrr, "growth_pct": growth,
            "score_profilo": int(rng.randint(58, 98)),
            "verificata": bool(rng.choice([True, False], p=[0.42, 0.58])),
            "funding_need": funding,
        })
    return pd.DataFrame(rows)


@st.cache_data
def load_companies():
    return pd.DataFrame([
        {"nome": "RetailMax", "settore": "Retail", "dimensione": "Enterprise",
         "area_innovazione": "AI", "collaborazione": "Pilot", "citta": "Milano",
         "budget_class": "Alto", "tempo_gg": 21,
         "descrizione": "Gruppo retail omnicanale alla ricerca di soluzioni AI per personalizzazione e customer experience."},
        {"nome": "Gruppo Rinaldi", "settore": "Manifattura", "dimensione": "Enterprise",
         "area_innovazione": "AI", "collaborazione": "Pilot", "citta": "Torino",
         "budget_class": "Alto", "tempo_gg": 30,
         "descrizione": "Gruppo industriale che investe in automazione, visione artificiale e ottimizzazione dei processi."},
        {"nome": "Banca Meridiana", "settore": "Banking & Finance", "dimensione": "Enterprise",
         "area_innovazione": "Fintech", "collaborazione": "Investimento", "citta": "Roma",
         "budget_class": "Alto", "tempo_gg": 45,
         "descrizione": "Istituto bancario con focus su open banking, digital onboarding e infrastrutture fintech."},
        {"nome": "EnerVita", "settore": "Energia", "dimensione": "Enterprise",
         "area_innovazione": "Climate Tech", "collaborazione": "Partnership", "citta": "Milano",
         "budget_class": "Alto", "tempo_gg": 35,
         "descrizione": "Utility energetica impegnata in smart grid, monitoraggio emissioni e transizione verde."},
        {"nome": "FarmaItalia", "settore": "Farmaceutico", "dimensione": "Enterprise",
         "area_innovazione": "HealthTech", "collaborazione": "Pilot", "citta": "Roma",
         "budget_class": "Medio", "tempo_gg": 40,
         "descrizione": "Azienda farmaceutica interessata a digital health, patient monitoring e automazione clinica."},
        {"nome": "TechnoMedia", "settore": "Media & Tech", "dimensione": "Mid-market",
         "area_innovazione": "AI", "collaborazione": "Scouting", "citta": "Milano",
         "budget_class": "Medio", "tempo_gg": 18,
         "descrizione": "Gruppo media-tech che esplora nuovi modelli di contenuto, recommendation e AI generativa."},
        {"nome": "AutoItalia", "settore": "Automotive", "dimensione": "Enterprise",
         "area_innovazione": "Mobility", "collaborazione": "Partnership", "citta": "Torino",
         "budget_class": "Alto", "tempo_gg": 50,
         "descrizione": "Corporate automotive interessata a mobilità connessa, fleet management e smart operations."},
        {"nome": "InfoServices Group", "settore": "IT & Servizi", "dimensione": "Mid-market",
         "area_innovazione": "SaaS B2B", "collaborazione": "Partnership", "citta": "Bologna",
         "budget_class": "Medio", "tempo_gg": 22,
         "descrizione": "System integrator che cerca partnership con startup SaaS e piattaforme enterprise."},
        {"nome": "LogiTrans", "settore": "Logistica", "dimensione": "Mid-market",
         "area_innovazione": "Mobility", "collaborazione": "Pilot", "citta": "Verona",
         "budget_class": "Medio", "tempo_gg": 24,
         "descrizione": "Operatore logistico che esplora ottimizzazione last-mile, flotte e routing intelligente."},
        {"nome": "Costruzioni Lombarde", "settore": "Real Estate", "dimensione": "Mid-market",
         "area_innovazione": "PropTech", "collaborazione": "Pilot", "citta": "Bergamo",
         "budget_class": "Medio", "tempo_gg": 27,
         "descrizione": "Azienda edile impegnata nella digitalizzazione dei cantieri e nello smart building."},
        {"nome": "AssicuraPlus", "settore": "Assicurazioni", "dimensione": "Enterprise",
         "area_innovazione": "Cybersecurity", "collaborazione": "Scouting", "citta": "Trieste",
         "budget_class": "Alto", "tempo_gg": 33,
         "descrizione": "Compagnia assicurativa che cerca startup cyber, antifrode e automazione sinistri."},
        {"nome": "AgriSmart Italia", "settore": "Agricoltura", "dimensione": "PMI",
         "area_innovazione": "Climate Tech", "collaborazione": "Partnership", "citta": "Bologna",
         "budget_class": "Basso", "tempo_gg": 16,
         "descrizione": "Impresa innovativa orientata a precision farming, sostenibilità e sensoristica."},
    ])


@st.cache_data
def load_investors():
    return pd.DataFrame([
        {"nome": "Mediterraneo Ventures", "tipo": "VC", "ticket": "€500K–€3M",
         "ticket_min_k": 500, "ticket_max_k": 3000, "focus_stage": "Seed",
         "settori_preferiti": ["AI", "SaaS B2B", "Fintech"], "geografia": "Italia & Europa",
         "lead_follow": "Lead", "velocita_gg": 7, "portfolio_size": 28,
         "thesis": "Startup tech italiane con forte potenziale di scalabilità e vantaggio competitivo difendibile."},
        {"nome": "Italian Angels Network", "tipo": "Angel", "ticket": "€20K–€100K",
         "ticket_min_k": 20, "ticket_max_k": 100, "focus_stage": "Pre-seed",
         "settori_preferiti": ["AI", "HealthTech", "EdTech", "Climate Tech"], "geografia": "Italia",
         "lead_follow": "Follow", "velocita_gg": 12, "portfolio_size": 16,
         "thesis": "Founder visionari nella fase più iniziale, con forte mentoring operativo."},
        {"nome": "Primo Capital", "tipo": "VC", "ticket": "€1M–€5M",
         "ticket_min_k": 1000, "ticket_max_k": 5000, "focus_stage": "Series A",
         "settori_preferiti": ["Fintech", "SaaS B2B", "Cybersecurity"], "geografia": "Europa",
         "lead_follow": "Lead", "velocita_gg": 10, "portfolio_size": 34,
         "thesis": "Round Series A per aziende con traction dimostrata e mercato europeo."},
        {"nome": "TechSeed Fund", "tipo": "Micro-VC", "ticket": "€100K–€500K",
         "ticket_min_k": 100, "ticket_max_k": 500, "focus_stage": "Pre-seed",
         "settori_preferiti": ["AI", "SaaS B2B", "HR Tech"], "geografia": "Italia",
         "lead_follow": "Follow", "velocita_gg": 6, "portfolio_size": 12,
         "thesis": "Primo capitale per team tecnici brillanti che risolvono problemi reali."},
        {"nome": "Innovation Bay Capital", "tipo": "VC", "ticket": "€500K–€2M",
         "ticket_min_k": 500, "ticket_max_k": 2000, "focus_stage": "Seed",
         "settori_preferiti": ["Climate Tech", "Mobility", "AI"], "geografia": "Italia",
         "lead_follow": "Lead", "velocita_gg": 8, "portfolio_size": 20,
         "thesis": "Innovazione che genera impatto positivo su clima, mobilità e automazione."},
        {"nome": "Alps Ventures", "tipo": "Micro-VC", "ticket": "€100K–€500K",
         "ticket_min_k": 100, "ticket_max_k": 500, "focus_stage": "Pre-seed",
         "settori_preferiti": ["PropTech", "SaaS B2B", "Fintech"], "geografia": "Nord Italia",
         "lead_follow": "Follow", "velocita_gg": 9, "portfolio_size": 11,
         "thesis": "Startup che digitalizzano mercati tradizionali con software scalabile."},
        {"nome": "Futuro Fund", "tipo": "VC", "ticket": "€1M–€5M",
         "ticket_min_k": 1000, "ticket_max_k": 5000, "focus_stage": "Series A",
         "settori_preferiti": ["AI", "HealthTech", "Cybersecurity"], "geografia": "Europa",
         "lead_follow": "Lead", "velocita_gg": 14, "portfolio_size": 22,
         "thesis": "AI e cybersecurity per un futuro digitale più sicuro."},
        {"nome": "Digital Growth Partners", "tipo": "VC", "ticket": "€500K–€3M",
         "ticket_min_k": 500, "ticket_max_k": 3000, "focus_stage": "Seed",
         "settori_preferiti": ["SaaS B2B", "Fintech", "HR Tech"], "geografia": "Italia & Europa",
         "lead_follow": "Lead", "velocita_gg": 11, "portfolio_size": 26,
         "thesis": "Piattaforme software B2B con metriche solide e team forte."},
        {"nome": "EcoInvest", "tipo": "VC", "ticket": "€300K–€2M",
         "ticket_min_k": 300, "ticket_max_k": 2000, "focus_stage": "Seed",
         "settori_preferiti": ["Climate Tech", "Mobility", "PropTech"], "geografia": "Europa",
         "lead_follow": "Lead", "velocita_gg": 13, "portfolio_size": 19,
         "thesis": "Investimenti esclusivamente in startup a impatto ambientale positivo."},
        {"nome": "HealthVentures Italia", "tipo": "VC", "ticket": "€500K–€3M",
         "ticket_min_k": 500, "ticket_max_k": 3000, "focus_stage": "Seed",
         "settori_preferiti": ["HealthTech", "AI"], "geografia": "Italia",
         "lead_follow": "Lead", "velocita_gg": 9, "portfolio_size": 18,
         "thesis": "Focus verticale su digital health, medtech e AI clinica."},
        {"nome": "Catalyst Angels", "tipo": "Angel", "ticket": "€10K–€80K",
         "ticket_min_k": 10, "ticket_max_k": 80, "focus_stage": "Pre-seed",
         "settori_preferiti": ["AI", "EdTech", "HealthTech", "Climate Tech"], "geografia": "Italia",
         "lead_follow": "Follow", "velocita_gg": 5, "portfolio_size": 9,
         "thesis": "Angel investing con forte coinvolgimento operativo e rete di contatti."},
        {"nome": "NordEst Investimenti", "tipo": "Corporate VC", "ticket": "€300K–€2M",
         "ticket_min_k": 300, "ticket_max_k": 2000, "focus_stage": "Seed",
         "settori_preferiti": ["Mobility", "AI", "PropTech"], "geografia": "Nord-Est Italia",
         "lead_follow": "Follow", "velocita_gg": 15, "portfolio_size": 14,
         "thesis": "Corporate VC che connette startup alla rete industriale del Nord-Est."},
    ])


# ─────────────────────────────────────────────────────────────
# MOTORE DI MATCHING
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


def match_investor(startup, investor):
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


def match_company(startup, company):
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
        reasons.append("Prossimità geografica favorevole alla collaborazione.")
    else:
        scores["Geografia"] = 55

    w = {"Settore": 0.35, "Collaborazione": 0.30, "Stadio": 0.20, "Geografia": 0.15}
    overall = round(sum(scores[k] * w[k] for k in w))
    return overall, scores, reasons


def find_investors_for_startup(startup_row, investors_df, n=5):
    results = []
    for _, inv in investors_df.iterrows():
        sc, subs, reasons = match_investor(startup_row, inv)
        results.append({
            "nome": inv["nome"], "tipo": inv["tipo"], "ticket": inv["ticket"],
            "focus_stage": inv["focus_stage"], "geografia": inv["geografia"],
            "settori": inv["settori_preferiti"], "thesis": inv["thesis"],
            "velocita_gg": inv["velocita_gg"],
            "score": sc, "sub_scores": subs, "reasons": reasons,
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:n]


def find_companies_for_startup(startup_row, companies_df, n=5):
    results = []
    for _, co in companies_df.iterrows():
        sc, subs, reasons = match_company(startup_row, co)
        results.append({
            "nome": co["nome"], "settore": co["settore"],
            "dimensione": co["dimensione"], "area_innovazione": co["area_innovazione"],
            "collaborazione": co["collaborazione"], "citta": co["citta"],
            "descrizione": co["descrizione"], "budget_class": co["budget_class"],
            "score": sc, "sub_scores": subs, "reasons": reasons,
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:n]


def find_startups_for_company(company_row, startups_df, n=5):
    results = []
    for _, s in startups_df.iterrows():
        sc, subs, reasons = match_company(s, company_row)
        results.append({
            "nome": s["nome"], "settore": s["settore"], "stadio": s["stadio"],
            "descrizione": s["descrizione"], "founder": s["founder"],
            "citta": s["citta"], "team_size": s["team_size"],
            "users": s["users"], "mrr": s["mrr"], "growth_pct": s["growth_pct"],
            "verificata": s["verificata"], "funding_need": s["funding_need"],
            "obiettivo": s["obiettivo"],
            "score": sc, "sub_scores": subs, "reasons": reasons,
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:n]


def find_startups_for_investor(investor_row, startups_df, n=5):
    results = []
    for _, s in startups_df.iterrows():
        sc, subs, reasons = match_investor(s, investor_row)
        results.append({
            "nome": s["nome"], "settore": s["settore"], "stadio": s["stadio"],
            "descrizione": s["descrizione"], "founder": s["founder"],
            "citta": s["citta"], "team_size": s["team_size"],
            "users": s["users"], "mrr": s["mrr"], "growth_pct": s["growth_pct"],
            "verificata": s["verificata"], "funding_need": s["funding_need"],
            "obiettivo": s["obiettivo"],
            "score": sc, "sub_scores": subs, "reasons": reasons,
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:n]


# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────

df_startups  = load_startups()
df_companies = load_companies()
df_investors = load_investors()


# ─────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────

def _sc(score):
    """Score color."""
    if score >= 75: return ACCENT
    if score >= 55: return AMBER
    return CORAL


def _scls(score):
    """Score CSS class."""
    if score >= 75: return "nf-match-high"
    if score >= 55: return "nf-match-mid"
    return "nf-match-low"


def _ini(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def _trunc(text, n=120):
    return text if len(text) <= n else text[:n].rstrip() + "…"


def section_title(title, subtitle=""):
    st.markdown(f'<div class="nf-sec"><h2>{title}</h2><div class="bar"></div></div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="nf-sec-sub">{subtitle}</div>', unsafe_allow_html=True)


def sub_scores_bars(scores_dict):
    html = '<div style="margin-top:0.4rem;">'
    for key, value in scores_dict.items():
        c = _sc(value)
        html += (
            f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:3px;">'
            f'<span style="font-size:0.7rem; color:{TEXT_3}; width:80px; text-align:right;">{key}</span>'
            f'<div style="flex:1; height:4px; background:#EEF2F7; border-radius:2px; overflow:hidden;">'
            f'<div style="height:100%; width:{value}%; background:{c}; border-radius:2px;"></div></div>'
            f'<span style="font-size:0.7rem; font-weight:600; color:{c}; width:28px;">{value}%</span>'
            f'</div>'
        )
    html += '</div>'
    return html


def render_match_card(rank, name, score, badges_html, meta_html, reasons, sub_scores, extra_html=""):
    cls = _scls(score)
    sc_c = _sc(score)
    reasons_li = "".join(f"<li>{r}</li>" for r in reasons) if reasons else "<li>Compatibilità parziale su alcuni criteri.</li>"
    bars = sub_scores_bars(sub_scores)
    meta_block = f'<div style="margin-top:0.25rem; font-size:0.82rem; color:{TEXT_3};">{meta_html}</div>' if meta_html else ''
    return (
        f'<div class="nf-match {cls}">'
        f'<div class="m-top"><div>'
        f'<div class="m-rank">Match \#{rank}</div>'
        f'<div class="m-name">{name}</div>'
        f'<div>{badges_html}</div>'
        f'{meta_block}'
        f'{extra_html}'
        f'</div>'
        f'<div class="m-score">'
        f'<div class="m-score-val" style="color:{sc_c};">{score}%</div>'
        f'<div class="m-score-lbl">Compatibilità</div>'
        f'</div></div>'
        f'<div class="m-why">'
        f'<div class="m-why-t">Perché questo match</div>'
        f'<ul>{reasons_li}</ul>'
        f'{bars}'
        f'</div></div>'
    )


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
# SEZIONE: HERO + ROLE SELECTION
# ─────────────────────────────────────────────────────────────

def render_hero():
    st.markdown(f"""
    <div class="nf-hero">
        <div style="font-size:0.78rem; letter-spacing:0.1em; color:rgba(255,255,255,0.4);
             text-transform:uppercase; margin-bottom:0.6rem; position:relative;">
            NEXFOUND
        </div>
        <h1>Trova il <span style="color:{ACCENT};">match giusto</span><br>
        per il tuo obiettivo</h1>
        <p>
            Che tu sia una startup in cerca di capitali, un'azienda che fa scouting
            o un investitore alla ricerca di deal flow — NexFound ti porta dritto
            alle opportunità più rilevanti e ti spiega perché.
        </p>
        <div class="proof">
            10 settori coperti · 24 startup · 12 aziende · 12 investitori
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_role_selection():
    st.markdown(f"### Dimmi chi sei")
    st.markdown(f'<p style="color:{TEXT_2}; margin-top:-0.5rem; margin-bottom:1.2rem;">'
                f'Seleziona il tuo ruolo. Ti mostro subito le opportunità più rilevanti per te.</p>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    roles = [
        ("startup", "🚀", "Sono una startup",
         "Trova investitori e aziende partner per raccogliere capitali o avviare un pilot.", c1),
        ("azienda", "🏢", "Sono un'azienda",
         "Trova startup innovative per scouting, pilot, partnership e open innovation.", c2),
        ("investitore", "💰", "Sono un investitore",
         "Trova startup in linea con la tua tesi, filtrate per settore, stadio e geografia.", c3),
    ]
    for role_id, icon, title, desc, col in roles:
        with col:
            st.markdown(f"""
            <div class="nf-role">
                <div class="icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("Inizia →", key=f"role_{role_id}", use_container_width=True, type="primary"):
                st.session_state.role = role_id
                st.rerun()


def render_how_it_works():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="nf-steps">
        <span class="step">1. Scegli chi sei</span>
        <span class="arrow">→</span>
        <span class="step">2. Dicci il tuo obiettivo</span>
        <span class="arrow">→</span>
        <span class="step">3. Ricevi match spiegati</span>
        <span class="arrow">→</span>
        <span class="step">4. Richiedi intro</span>
    </div>""", unsafe_allow_html=True)


def render_compact_header():
    labels = {"startup": "🚀 Startup", "azienda": "🏢 Azienda", "investitore": "💰 Investitore"}
    st.markdown(f"""
    <div class="nf-header">
        <div class="logo">🔗 Nex<span style="color:{ACCENT};">Found</span></div>
        <div class="role-pill">{labels[st.session_state.role]}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SEZIONE: FLUSSO STARTUP
# ─────────────────────────────────────────────────────────────

def render_startup_flow():
    section_title(
        "Trova le connessioni giuste per la tua startup",
        "Seleziona il tuo profilo e dicci cosa cerchi. Ti mostriamo le opportunità più compatibili.",
    )

    startup_name = st.selectbox("Il tuo profilo startup", df_startups["nome"].tolist(), key="sel_startup")
    s = df_startups[df_startups["nome"] == startup_name].iloc[0]

    badges = (
        f'<span class="nf-b nf-b-accent">{s["settore"]}</span>'
        f'<span class="nf-b nf-b-coral">{s["stadio"]}</span>'
        f'<span class="nf-b nf-b-primary">{s["obiettivo"]}</span>'
    )
    if s["verificata"]:
        badges += '<span class="nf-b nf-b-success">Verificata</span>'

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(f'<div class="nf-met"><div class="lbl">Utenti</div><div class="val">{s["users"]:,}</div></div>', unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div class="nf-met"><div class="lbl">MRR</div><div class="val">€{s["mrr"]:,}</div></div>', unsafe_allow_html=True)
    with mc3:
        st.markdown(f'<div class="nf-met"><div class="lbl">Crescita</div><div class="val">{s["growth_pct"]}%</div></div>', unsafe_allow_html=True)
    with mc4:
        st.markdown(f'<div class="nf-met"><div class="lbl">Team</div><div class="val">{s["team_size"]}</div></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nf-profile">
        <div class="name">{s["nome"]}</div>
        <div class="meta">{s["founder"]} · 📍 {s["citta"]} · 💰 {s["funding_need"]}</div>
        <div style="margin-top:0.4rem;">{badges}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"**Cosa stai cercando?**")
    uc = st.radio(
        "Obiettivo", [
            "💰 Cerco investitori",
            "🏢 Cerco una corporate per un pilot",
            "🤝 Cerco partnership strategiche",
        ],
        horizontal=True, label_visibility="collapsed", key="startup_uc",
    )
    st.markdown("---")

    if "investitori" in uc:
        _render_investor_results_for_startup(s)
    else:
        _render_company_results_for_startup(s, filter_pilot="pilot" in uc.lower())


def _render_investor_results_for_startup(s):
    results = find_investors_for_startup(s, df_investors, n=5)
    strong = sum(1 for r in results if r["score"] >= 70)

    st.markdown(f"""
    <div class="nf-info">
        <p><strong>{strong} investitori ad alta compatibilità</strong> trovati per {s["nome"]}.
        Ogni match è calcolato su settore, stadio, ticket e geografia.</p>
    </div>""", unsafe_allow_html=True)

    for i, r in enumerate(results):
        badges = (
            f'<span class="nf-b nf-b-accent">{r["tipo"]}</span>'
            f'<span class="nf-b nf-b-coral">{r["focus_stage"]}</span>'
            f'<span class="nf-b nf-b-primary">{r["ticket"]}</span>'
        )
        meta = f'🎯 {", ".join(r["settori"][:3])} · 🌍 {r["geografia"]}'

        st.markdown(render_match_card(
            i + 1, r["nome"], r["score"], badges, meta,
            r["reasons"], r["sub_scores"],
        ), unsafe_allow_html=True)

        bc1, bc2, _ = st.columns([1, 1, 3])
        with bc1:
            if st.button("📨 Richiedi intro", key=f"intro_i_{i}", use_container_width=True, type="primary"):
                if add_contact_request(s["nome"], r["nome"], "Investitore", r["score"]):
                    st.success(f"Richiesta inviata a {r['nome']}.")
                else:
                    st.info("Richiesta già inviata.")
        with bc2:
            if st.button("⭐ Salva", key=f"save_i_{i}", use_container_width=True):
                rec = {"startup": s["nome"], "target": r["nome"], "tipo": "Investitore", "score": r["score"]}
                if rec not in st.session_state.saved_matches:
                    st.session_state.saved_matches.append(rec)
                st.success("Match salvato.")


def _render_company_results_for_startup(s, filter_pilot=False):
    companies = df_companies
    if filter_pilot:
        filtered = df_companies[df_companies["collaborazione"] == "Pilot"]
        if not filtered.empty:
            companies = filtered

    results = find_companies_for_startup(s, companies, n=5)
    strong = sum(1 for r in results if r["score"] >= 70)

    label = "pilot" if filter_pilot else "partnership e collaborazione"
    st.markdown(f"""
    <div class="nf-info">
        <p><strong>{strong} aziende ad alta compatibilità</strong> trovate per {label}.
        Il matching valuta settore, tipo di collaborazione, stadio e geografia.</p>
    </div>""", unsafe_allow_html=True)

    for i, r in enumerate(results):
        badges = (
            f'<span class="nf-b nf-b-accent">{r["area_innovazione"]}</span>'
            f'<span class="nf-b nf-b-coral">{r["dimensione"]}</span>'
            f'<span class="nf-b nf-b-primary">{r["collaborazione"]}</span>'
        )
        meta = f'📍 {r["citta"]} · 💳 Budget {r["budget_class"]}'

        st.markdown(render_match_card(
            i + 1, r["nome"], r["score"], badges, meta,
            r["reasons"], r["sub_scores"],
        ), unsafe_allow_html=True)

        bc1, bc2, _ = st.columns([1, 1, 3])
        with bc1:
            if st.button("📨 Richiedi intro", key=f"intro_c_{i}", use_container_width=True, type="primary"):
                if add_contact_request(s["nome"], r["nome"], "Azienda", r["score"]):
                    st.success(f"Richiesta inviata a {r['nome']}.")
                else:
                    st.info("Richiesta già inviata.")
        with bc2:
            if st.button("⭐ Salva", key=f"save_c_{i}", use_container_width=True):
                rec = {"startup": s["nome"], "target": r["nome"], "tipo": "Azienda", "score": r["score"]}
                if rec not in st.session_state.saved_matches:
                    st.session_state.saved_matches.append(rec)
                st.success("Match salvato.")


# ─────────────────────────────────────────────────────────────
# SEZIONE: FLUSSO AZIENDA
# ─────────────────────────────────────────────────────────────

def render_company_flow():
    section_title(
        "Trova la startup giusta per il tuo business",
        "Seleziona il tuo profilo aziendale e ti mostriamo le startup più compatibili.",
    )

    company_name = st.selectbox("Il tuo profilo aziendale", df_companies["nome"].tolist(), key="sel_company")
    co = df_companies[df_companies["nome"] == company_name].iloc[0]

    badges = (
        f'<span class="nf-b nf-b-accent">{co["area_innovazione"]}</span>'
        f'<span class="nf-b nf-b-coral">{co["dimensione"]}</span>'
        f'<span class="nf-b nf-b-primary">{co["collaborazione"]}</span>'
    )
    st.markdown(f"""
    <div class="nf-profile">
        <div class="name">{co["nome"]}</div>
        <div class="meta">{co["settore"]} · 📍 {co["citta"]} · 💳 Budget {co["budget_class"]}</div>
        <div style="margin-top:0.4rem;">{badges}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**Cosa stai cercando?**")
    uc = st.radio(
        "Obiettivo", [
            "🔍 Scouting tecnologico",
            "🧪 Pilot con una startup",
            "🤝 Partnership strategica",
            "💡 Open innovation",
        ],
        horizontal=True, label_visibility="collapsed", key="company_uc",
    )

    with st.expander("🔧 Filtra risultati", expanded=False):
        fc1, fc2 = st.columns(2)
        with fc1:
            f_settore = st.multiselect("Settore startup", SETTORI, key="f_co_set")
        with fc2:
            f_stadio = st.multiselect("Stadio startup", STADI, key="f_co_stg")

    st.markdown("---")

    startups = df_startups.copy()
    if f_settore:
        startups = startups[startups["settore"].isin(f_settore)]
    if f_stadio:
        startups = startups[startups["stadio"].isin(f_stadio)]

    results = find_startups_for_company(co, startups, n=6)
    strong = sum(1 for r in results if r["score"] >= 70)

    objective_label = {
        "🔍 Scouting tecnologico": "scouting",
        "🧪 Pilot con una startup": "pilot",
        "🤝 Partnership strategica": "partnership",
        "💡 Open innovation": "open innovation",
    }.get(uc, "collaborazione")

    st.markdown(f"""
    <div class="nf-info">
        <p><strong>{strong} startup ad alta compatibilità</strong> per {objective_label}.
        Ogni match è basato su settore, tipo di collaborazione, maturità e vicinanza.</p>
    </div>""", unsafe_allow_html=True)

    for i, r in enumerate(results):
        badges = (
            f'<span class="nf-b nf-b-accent">{r["settore"]}</span>'
            f'<span class="nf-b nf-b-coral">{r["stadio"]}</span>'
            f'<span class="nf-b nf-b-primary">{r["obiettivo"]}</span>'
        )
        if r["verificata"]:
            badges += '<span class="nf-b nf-b-success">Verificata</span>'
        meta = f'{r["founder"]} · 📍 {r["citta"]} · 👥 {r["team_size"]} · 💰 {r["funding_need"]}'
        extra = ""
        if r["mrr"] > 0 or r["users"] > 0:
            parts = []
            if r["users"] > 0: parts.append(f'{r["users"]:,} utenti')
            if r["mrr"] > 0: parts.append(f'€{r["mrr"]:,} MRR')
            if r["growth_pct"] > 0: parts.append(f'+{r["growth_pct"]}% crescita')
            extra = f'<div style="margin-top:0.3rem; font-size:0.8rem; color:{ACCENT_DK}; font-weight:600;">📊 {" · ".join(parts)}</div>'

        st.markdown(render_match_card(
            i + 1, r["nome"], r["score"], badges, meta,
            r["reasons"], r["sub_scores"], extra,
        ), unsafe_allow_html=True)

        bc1, bc2, _ = st.columns([1, 1, 3])
        with bc1:
            if st.button("📨 Contatta startup", key=f"intro_cs_{i}", use_container_width=True, type="primary"):
                if add_contact_request(r["nome"], co["nome"], "Azienda", r["score"]):
                    st.success(f"Richiesta inviata a {r['nome']}.")
                else:
                    st.info("Richiesta già inviata.")
        with bc2:
            if st.button("⭐ Salva", key=f"save_cs_{i}", use_container_width=True):
                rec = {"startup": r["nome"], "target": co["nome"], "tipo": "Azienda", "score": r["score"]}
                if rec not in st.session_state.saved_matches:
                    st.session_state.saved_matches.append(rec)
                st.success("Match salvato.")


# ─────────────────────────────────────────────────────────────
# SEZIONE: FLUSSO INVESTITORE
# ─────────────────────────────────────────────────────────────

def render_investor_flow():
    section_title(
        "Trova startup in linea con la tua tesi",
        "Seleziona il tuo profilo investitore e ti mostriamo le startup più compatibili.",
    )

    inv_name = st.selectbox("Il tuo profilo investitore", df_investors["nome"].tolist(), key="sel_investor")
    inv = df_investors[df_investors["nome"] == inv_name].iloc[0]

    badges = (
        f'<span class="nf-b nf-b-accent">{inv["tipo"]}</span>'
        f'<span class="nf-b nf-b-coral">{inv["focus_stage"]}</span>'
        f'<span class="nf-b nf-b-primary">{inv["lead_follow"]}</span>'
    )
    st.markdown(f"""
    <div class="nf-profile">
        <div class="name">{inv["nome"]}</div>
        <div class="meta">💰 {inv["ticket"]} · 🌍 {inv["geografia"]} · 🎯 {", ".join(inv["settori_preferiti"][:3])}</div>
        <div style="margin-top:0.3rem; font-size:0.85rem; color:{TEXT_2}; font-style:italic;">
            "{_trunc(inv["thesis"], 200)}"
        </div>
        <div style="margin-top:0.4rem;">{badges}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**Cosa stai cercando?**")
    uc = st.radio(
        "Obiettivo", [
            "🎯 Deal flow per la mia tesi",
            "🔍 Startup per settore",
            "🌱 Discovery early-stage",
        ],
        horizontal=True, label_visibility="collapsed", key="investor_uc",
    )

    with st.expander("🔧 Filtra risultati", expanded=False):
        fi1, fi2 = st.columns(2)
        with fi1:
            f_settore = st.multiselect("Settore", SETTORI, key="f_inv_set")
        with fi2:
            f_stadio = st.multiselect("Stadio", STADI, key="f_inv_stg")

    st.markdown("---")

    startups = df_startups.copy()

    if "early-stage" in uc.lower():
        startups = startups[startups["stadio"].isin(["Idea", "MVP"])]
    if f_settore:
        startups = startups[startups["settore"].isin(f_settore)]
    if f_stadio:
        startups = startups[startups["stadio"].isin(f_stadio)]

    results = find_startups_for_investor(inv, startups, n=6)
    strong = sum(1 for r in results if r["score"] >= 70)

    st.markdown(f"""
    <div class="nf-info">
        <p><strong>{strong} startup ad alta compatibilità</strong> trovate per la tua tesi.
        Ogni match è valutato su settore, stadio, ticket e allineamento geografico.</p>
    </div>""", unsafe_allow_html=True)

    for i, r in enumerate(results):
        badges = (
            f'<span class="nf-b nf-b-accent">{r["settore"]}</span>'
            f'<span class="nf-b nf-b-coral">{r["stadio"]}</span>'
            f'<span class="nf-b nf-b-primary">{r["obiettivo"]}</span>'
        )
        if r["verificata"]:
            badges += '<span class="nf-b nf-b-success">Verificata</span>'
        meta = f'{r["founder"]} · 📍 {r["citta"]} · 👥 {r["team_size"]} · 💰 {r["funding_need"]}'
        extra = ""
        if r["mrr"] > 0 or r["users"] > 0:
            parts = []
            if r["users"] > 0: parts.append(f'{r["users"]:,} utenti')
            if r["mrr"] > 0: parts.append(f'€{r["mrr"]:,} MRR')
            if r["growth_pct"] > 0: parts.append(f'+{r["growth_pct"]}% crescita')
            extra = f'<div style="margin-top:0.3rem; font-size:0.8rem; color:{ACCENT_DK}; font-weight:600;">📊 {" · ".join(parts)}</div>'

        st.markdown(render_match_card(
            i + 1, r["nome"], r["score"], badges, meta,
            r["reasons"], r["sub_scores"], extra,
        ), unsafe_allow_html=True)

        bc1, bc2, _ = st.columns([1, 1, 3])
        with bc1:
            if st.button("📨 Richiedi intro", key=f"intro_is_{i}", use_container_width=True, type="primary"):
                if add_contact_request(r["nome"], inv["nome"], "Investitore", r["score"]):
                    st.success(f"Richiesta inviata per {r['nome']}.")
                else:
                    st.info("Richiesta già inviata.")
        with bc2:
            if st.button("⭐ Salva", key=f"save_is_{i}", use_container_width=True):
                rec = {"startup": r["nome"], "target": inv["nome"], "tipo": "Investitore", "score": r["score"]}
                if rec not in st.session_state.saved_matches:
                    st.session_state.saved_matches.append(rec)
                st.success("Match salvato.")


# ─────────────────────────────────────────────────────────────
# SEZIONE: RICHIESTE E SHORTLIST
# ─────────────────────────────────────────────────────────────

def render_pending_actions():
    has_requests = bool(st.session_state.contact_requests)
    has_saved = bool(st.session_state.saved_matches)

    if not has_requests and not has_saved:
        return

    st.markdown("---")
    section_title("Le tue azioni", "Richieste inviate e match salvati durante questa sessione.")

    if has_requests:
        st.markdown("**Richieste di contatto inviate**")
        status_colors = {
            "Inviata": AMBER, "In revisione": PRIMARY,
            "Accettata": SUCCESS, "Call programmata": ACCENT,
        }
        for i, req in enumerate(st.session_state.contact_requests):
            sc_c = _sc(req["score"])
            st_c = status_colors.get(req["stato"], TEXT_3)
            st.markdown(f"""
            <div class="nf-req">
                <div class="req-info">
                    <div class="req-name">{req["startup"]} → {req["target"]}</div>
                    <div class="req-meta">{req["tipo"]} · {req["data"]}</div>
                </div>
                <span style="font-weight:800; color:{sc_c}; font-size:1rem;">{req["score"]}%</span>
                <span class="nf-b" style="background:rgba(0,0,0,0.05); color:{st_c}; font-weight:700;">{req["stato"]}</span>
            </div>""", unsafe_allow_html=True)

    if has_saved:
        st.markdown("**Match salvati**")
        for i, rec in enumerate(st.session_state.saved_matches):
            sc_c = _sc(rec["score"])
            st.markdown(f"""
            <div class="nf-req">
                <div class="req-info">
                    <div class="req-name">⭐ {rec["startup"]} ↔ {rec["target"]}</div>
                    <div class="req-meta">{rec["tipo"]}</div>
                </div>
                <span style="font-weight:800; color:{sc_c}; font-size:1rem;">{rec["score"]}%</span>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SEZIONE: CTA FINALE
# ─────────────────────────────────────────────────────────────

def render_bottom_cta():
    st.markdown(f"""
    <div class="nf-cta">
        <h2>Vuoi provare NexFound con i tuoi dati?</h2>
        <p>Prenota una demo personalizzata e scopri come accelerare le tue connessioni strategiche.</p>
    </div>""", unsafe_allow_html=True)

    if "show_demo_form" not in st.session_state:
        st.session_state.show_demo_form = False

    _, c, _ = st.columns([2, 1.2, 2])
    with c:
        if st.button("Prenota una demo →", use_container_width=True, type="primary", key="cta_final"):
            st.session_state.show_demo_form = True

    if st.session_state.show_demo_form:
        st.markdown("---")
        st.subheader("📅 Prenota la tua demo")
        with st.form("demo_form"):
            d1, d2 = st.columns(2)
            with d1:
                demo_name = st.text_input("Nome e cognome")
                demo_email = st.text_input("Email aziendale")
            with d2:
                demo_company = st.text_input("Azienda / Startup")
                demo_role = st.selectbox("Ruolo", ["Founder / CEO", "CTO", "Head of Innovation", "Investor", "Altro"])
            demo_msg = st.text_area("Raccontaci brevemente cosa cerchi", height=80)
            submitted = st.form_submit_button("Invia richiesta", use_container_width=True, type="primary")
            if submitted:
                if demo_name and demo_email:
                    st.session_state.show_demo_form = False
                    st.success(f"Grazie {demo_name}! Ti contatteremo a {demo_email} entro 24 ore per fissare la demo.")
                    st.balloons()
                else:
                    st.warning("Per favore compila almeno nome e email.")


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem 0 0.6rem 0;">
            <div style="font-size:1.4rem; font-weight:900; letter-spacing:-0.04em;">
                🔗 <span style="color:{ACCENT};">NexFound</span>
            </div>
            <div style="font-size:0.68rem; color:rgba(214,224,238,0.4);
                 text-transform:uppercase; letter-spacing:0.08em; margin-top:2px;">
                Matching intelligente
            </div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.role:
            labels = {"startup": "🚀 Startup", "azienda": "🏢 Azienda", "investitore": "💰 Investitore"}
            st.markdown("---")
            st.markdown(f"**Ruolo attivo:** {labels[st.session_state.role]}")

            if st.button("← Cambia ruolo", use_container_width=True, key="back_role"):
                st.session_state.role = None
                st.rerun()

            st.markdown("---")

            n_req = len(st.session_state.contact_requests)
            n_saved = len(st.session_state.saved_matches)
            st.markdown(f"""
            <div style="font-size:0.82rem; line-height:1.7;">
                📨 <b>{n_req}</b> richieste inviate<br>
                ⭐ <b>{n_saved}</b> match salvati
            </div>""", unsafe_allow_html=True)

        else:
            st.markdown("---")
            st.markdown(f"""
            <div style="font-size:0.78rem; line-height:1.7;">
                <b>Come funziona</b><br>
                1. Scegli il tuo ruolo<br>
                2. Seleziona il tuo obiettivo<br>
                3. Ricevi match spiegati<br>
                4. Richiedi intro e agisci
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:0.66rem; color:rgba(214,224,238,0.3);
             text-align:center; line-height:1.5;">
            Dati dimostrativi · © 2026 NexFound
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    render_sidebar()

    if not st.session_state.role:
        render_hero()
        render_role_selection()
        render_how_it_works()
        render_bottom_cta()
    else:
        render_compact_header()
        if st.session_state.role == "startup":
            render_startup_flow()
        elif st.session_state.role == "azienda":
            render_company_flow()
        else:
            render_investor_flow()
        render_pending_actions()
        render_bottom_cta()


if __name__ == "__main__":
    main()
