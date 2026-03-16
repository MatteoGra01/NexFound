import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math

# ══════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

st.set_page_config(
    page_title="NexFound – Connetti Startup, Aziende e Investitori",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Brand palette
PRIMARY = "#1B2A4A"
PRIMARY_LIGHT = "#2a4170"
ACCENT = "#2EC4B6"
ACCENT_DARK = "#1a9e92"
CORAL = "#FF6B6B"
AMBER = "#FFB347"
LIGHT_BG = "#F7F8FB"
CARD_BG = "#FFFFFF"
TEXT_PRIMARY = "#1B2A4A"
TEXT_SECONDARY = "#5A6B87"
TEXT_MUTED = "#97A3B6"
BORDER = "#E8ECF1"

# ══════════════════════════════════════════════════════════════
# CUSTOM CSS — Premium design system
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* ── Global ────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    h1, h2, h3, h4, h5 {{
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }}

    /* ── Sidebar ───────────────────────────── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {PRIMARY} 0%, #0f1b33 100%);
        border-right: 1px solid rgba(46,196,182,0.15);
    }}
    section[data-testid="stSidebar"] * {{
        color: #C8D4E6 !important;
    }}
    section[data-testid="stSidebar"] .stRadio label {{
        padding: 6px 8px;
        border-radius: 8px;
        transition: all 0.15s ease;
        margin-bottom: 1px;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(46,196,182,0.1);
    }}
    section[data-testid="stSidebar"] .stRadio label span {{
        font-size: 0.88rem;
        font-weight: 500;
    }}
    section[data-testid="stSidebar"] .stRadio [data-checked="true"] label {{
        background: rgba(46,196,182,0.15);
        border-left: 3px solid {ACCENT};
    }}
    section[data-testid="stSidebar"] .stRadio [data-checked="true"] label span {{
        color: #fff !important;
        font-weight: 600;
    }}

    /* ── Section titles ────────────────────── */
    .nx-section-header {{
        margin-bottom: 0.3rem;
    }}
    .nx-section-header h2 {{
        font-size: 1.85rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        margin: 0;
        letter-spacing: -0.03em;
    }}
    .nx-section-header .accent-line {{
        width: 48px; height: 4px;
        background: {ACCENT};
        border-radius: 2px;
        margin-top: 8px;
    }}
    .nx-section-sub {{
        font-size: 1rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 1.8rem;
        line-height: 1.5;
    }}

    /* ── Metric card — premium ─────────────── */
    .nx-metric {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.3rem 1.4rem 1.1rem;
        box-shadow: 0 1px 3px rgba(27,42,74,0.04), 0 4px 14px rgba(27,42,74,0.06);
        border: 1px solid {BORDER};
        margin-bottom: 0.8rem;
        position: relative;
        overflow: hidden;
    }}
    .nx-metric::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {ACCENT}, {ACCENT_DARK});
    }}
    .nx-metric .metric-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.4rem;
    }}
    .nx-metric .metric-value {{
        font-size: 1.9rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        margin: 0.15rem 0;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }}
    .nx-metric .metric-label {{
        font-size: 0.8rem;
        font-weight: 500;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin: 0;
    }}
    .nx-metric .metric-delta {{
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.35rem;
    }}
    .nx-metric .metric-delta.up {{ color: #22c55e; }}
    .nx-metric .metric-delta.neutral {{ color: {TEXT_MUTED}; }}
    .nx-metric-accent::before {{
        background: linear-gradient(90deg, {CORAL}, {AMBER});
    }}

    /* ── Profile card ──────────────────────── */
    .nx-card {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.35rem 1.4rem;
        box-shadow: 0 1px 3px rgba(27,42,74,0.04), 0 4px 14px rgba(27,42,74,0.06);
        border: 1px solid {BORDER};
        margin-bottom: 1rem;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .nx-card:hover {{
        box-shadow: 0 4px 8px rgba(27,42,74,0.06), 0 8px 24px rgba(27,42,74,0.10);
        transform: translateY(-2px);
    }}
    .nx-card .card-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 0.7rem;
    }}
    .nx-card .card-avatar {{
        width: 42px; height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        color: #fff;
        flex-shrink: 0;
    }}
    .nx-card .card-avatar.avatar-startup {{ background: linear-gradient(135deg, {ACCENT}, {ACCENT_DARK}); }}
    .nx-card .card-avatar.avatar-company {{ background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_LIGHT}); }}
    .nx-card .card-avatar.avatar-investor {{ background: linear-gradient(135deg, {CORAL}, #e05555); }}
    .nx-card .card-name {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin: 0;
        line-height: 1.2;
    }}
    .nx-card .card-subtitle {{
        font-size: 0.8rem;
        color: {TEXT_MUTED};
        margin: 0;
    }}
    .nx-card .card-body {{
        font-size: 0.87rem;
        color: {TEXT_SECONDARY};
        line-height: 1.55;
        margin-bottom: 0.6rem;
    }}
    .nx-card .card-meta {{
        font-size: 0.8rem;
        color: {TEXT_MUTED};
    }}

    /* ── Badges ─────────────────────────────── */
    .nx-badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-right: 5px;
        margin-bottom: 5px;
    }}
    .nx-badge-accent {{ background: rgba(46,196,182,0.12); color: {ACCENT_DARK}; }}
    .nx-badge-coral {{ background: rgba(255,107,107,0.12); color: #d94f4f; }}
    .nx-badge-primary {{ background: rgba(27,42,74,0.08); color: {PRIMARY}; }}
    .nx-badge-amber {{ background: rgba(255,179,71,0.15); color: #c77f20; }}
    .nx-badge-success {{ background: rgba(34,197,94,0.12); color: #16803c; }}
    .nx-badge-gray {{ background: {LIGHT_BG}; color: {TEXT_MUTED}; }}

    /* ── Hero section ──────────────────────── */
    .nx-hero {{
        background: linear-gradient(135deg, {PRIMARY} 0%, #0f1b33 60%, #162847 100%);
        border-radius: 20px;
        padding: 3.5rem 3rem;
        color: #fff;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }}
    .nx-hero::before {{
        content: '';
        position: absolute;
        top: -60%; right: -20%;
        width: 500px; height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(46,196,182,0.15) 0%, transparent 70%);
    }}
    .nx-hero::after {{
        content: '';
        position: absolute;
        bottom: -40%; left: -10%;
        width: 400px; height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,107,107,0.08) 0%, transparent 70%);
    }}
    .nx-hero h1 {{
        font-size: 3rem;
        font-weight: 900;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.04em;
        position: relative;
    }}
    .nx-hero .hero-accent {{
        color: {ACCENT};
    }}
    .nx-hero .hero-tagline {{
        font-size: 1.2rem;
        color: rgba(255,255,255,0.75);
        max-width: 600px;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        position: relative;
    }}
    .nx-hero .hero-stats {{
        display: flex;
        gap: 2.5rem;
        position: relative;
    }}
    .nx-hero .hero-stat {{
        text-align: left;
    }}
    .nx-hero .hero-stat-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {ACCENT};
        line-height: 1;
    }}
    .nx-hero .hero-stat-label {{
        font-size: 0.78rem;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
    }}

    /* ── Ecosystem / value card ──────────── */
    .nx-eco {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_LIGHT} 100%);
        border-radius: 16px;
        padding: 1.8rem 1.5rem;
        color: #fff;
        text-align: center;
        min-height: 210px;
        border: 1px solid rgba(46,196,182,0.15);
    }}
    .nx-eco .eco-icon {{
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
    }}
    .nx-eco h3 {{
        color: {ACCENT};
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0.3rem 0 0.8rem 0;
    }}
    .nx-eco p {{
        font-size: 0.88rem;
        color: rgba(255,255,255,0.7);
        line-height: 1.55;
    }}
    .nx-eco-center {{
        background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DARK} 100%);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .nx-eco-center h3 {{
        color: #fff;
    }}
    .nx-eco-center p {{
        color: rgba(255,255,255,0.85);
    }}

    /* ── Pain card ─────────────────────────── */
    .nx-pain {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(27,42,74,0.04), 0 4px 14px rgba(27,42,74,0.06);
        border: 1px solid {BORDER};
        min-height: 220px;
        transition: transform 0.2s ease;
    }}
    .nx-pain:hover {{
        transform: translateY(-2px);
    }}
    .nx-pain .pain-icon {{
        width: 44px; height: 44px;
        border-radius: 12px;
        background: rgba(255,107,107,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
    }}
    .nx-pain h4 {{
        color: {TEXT_PRIMARY};
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }}
    .nx-pain p {{
        color: {TEXT_SECONDARY};
        font-size: 0.87rem;
        line-height: 1.55;
        margin: 0;
    }}

    /* ── Match card ─────────────────────────── */
    .nx-match {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        border: 1px solid {BORDER};
        box-shadow: 0 1px 3px rgba(27,42,74,0.04), 0 4px 14px rgba(27,42,74,0.06);
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }}
    .nx-match::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, {ACCENT}, {ACCENT_DARK});
    }}
    .nx-match .match-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }}
    .nx-match .match-rank {{
        font-size: 0.7rem;
        font-weight: 700;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .nx-match .match-name {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin: 2px 0 6px 0;
    }}
    .nx-match .match-score-box {{
        text-align: center;
        min-width: 72px;
    }}
    .nx-match .match-score-value {{
        font-size: 2rem;
        font-weight: 900;
        line-height: 1;
        letter-spacing: -0.04em;
    }}
    .nx-match .match-score-label {{
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {TEXT_MUTED};
        font-weight: 600;
    }}
    .nx-match .match-reasons {{
        margin-top: 0.7rem;
        padding-top: 0.7rem;
        border-top: 1px solid {BORDER};
        font-size: 0.85rem;
        color: {TEXT_SECONDARY};
        line-height: 1.6;
    }}

    /* ── CTA box ────────────────────────────── */
    .nx-cta {{
        background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DARK} 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    .nx-cta::before {{
        content: '';
        position: absolute;
        top: -50%; right: -20%;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }}
    .nx-cta h2 {{
        color: #fff;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        position: relative;
    }}
    .nx-cta p {{
        color: rgba(255,255,255,0.8);
        font-size: 1.02rem;
        position: relative;
        max-width: 550px;
        margin: 0 auto;
        line-height: 1.55;
    }}

    /* ── Feed item ──────────────────────────── */
    .nx-feed {{
        background: {CARD_BG};
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.6rem;
        border: 1px solid {BORDER};
        display: flex;
        align-items: flex-start;
        gap: 12px;
        transition: background 0.15s ease;
    }}
    .nx-feed:hover {{
        background: {LIGHT_BG};
    }}
    .nx-feed .feed-icon {{
        width: 38px; height: 38px;
        border-radius: 10px;
        background: {LIGHT_BG};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }}
    .nx-feed .feed-content {{
        flex: 1;
    }}
    .nx-feed .feed-type {{
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {ACCENT_DARK};
    }}
    .nx-feed .feed-text {{
        font-size: 0.88rem;
        color: {TEXT_PRIMARY};
        margin: 2px 0 0 0;
        line-height: 1.45;
    }}
    .nx-feed .feed-time {{
        font-size: 0.75rem;
        color: {TEXT_MUTED};
        white-space: nowrap;
        margin-top: 2px;
    }}

    /* ── Conclusion / info box ──────────────── */
    .nx-info {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        border: 1px solid {BORDER};
        box-shadow: 0 1px 3px rgba(27,42,74,0.04), 0 4px 14px rgba(27,42,74,0.06);
        margin-bottom: 1rem;
    }}
    .nx-info.nx-info-accent {{
        border-left: 4px solid {ACCENT};
    }}
    .nx-info h4 {{
        color: {TEXT_PRIMARY};
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 0.6rem 0;
    }}
    .nx-info p, .nx-info li {{
        color: {TEXT_SECONDARY};
        line-height: 1.7;
        font-size: 0.92rem;
    }}
    .nx-info ul, .nx-info ol {{
        padding-left: 1.2rem;
        margin: 0.5rem 0 0 0;
    }}

    /* ── Value flow strip ───────────────────── */
    .nx-flow {{
        background: {LIGHT_BG};
        border-radius: 14px;
        padding: 1.5rem 2rem;
        border: 1px solid {BORDER};
    }}
    .nx-flow h4 {{
        color: {TEXT_PRIMARY};
        font-weight: 700;
        text-align: center;
        margin: 0 0 0.8rem 0;
    }}
    .nx-flow-steps {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.3rem;
        font-size: 0.95rem;
        color: {TEXT_SECONDARY};
    }}
    .nx-flow-steps .step {{
        padding: 6px 14px;
        background: {CARD_BG};
        border-radius: 8px;
        border: 1px solid {BORDER};
        font-weight: 500;
        font-size: 0.85rem;
    }}
    .nx-flow-steps .arrow {{
        color: {ACCENT};
        font-weight: 700;
        font-size: 1.1rem;
    }}

    /* ── Detail card (expanded profile) ──── */
    .nx-detail {{
        background: {CARD_BG};
        border-radius: 16px;
        padding: 1.8rem 2rem;
        border: 1px solid {BORDER};
        box-shadow: 0 1px 3px rgba(27,42,74,0.04), 0 8px 24px rgba(27,42,74,0.08);
        position: relative;
        overflow: hidden;
    }}
    .nx-detail::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 5px;
        background: linear-gradient(180deg, {ACCENT}, {ACCENT_DARK});
    }}
    .nx-detail .detail-name {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        letter-spacing: -0.02em;
        margin: 0 0 0.5rem 0;
    }}
    .nx-detail .detail-desc {{
        color: {TEXT_SECONDARY};
        font-size: 0.92rem;
        line-height: 1.65;
        margin-bottom: 1rem;
    }}
    .nx-detail .detail-meta {{
        font-size: 0.9rem;
        color: {TEXT_SECONDARY};
        line-height: 1.8;
    }}
    .nx-detail .detail-meta b {{
        color: {TEXT_PRIMARY};
    }}

    /* ── Status pills ──────────────────────── */
    .nx-status {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }}
    .nx-status-sent {{ background: rgba(255,179,71,0.15); color: #b8860b; }}
    .nx-status-review {{ background: rgba(59,130,246,0.12); color: #2563eb; }}
    .nx-status-accepted {{ background: rgba(34,197,94,0.12); color: #16803c; }}
    .nx-status-call {{ background: rgba(46,196,182,0.15); color: {ACCENT_DARK}; }}

    /* ── Progress bar ──────────────────────── */
    .nx-progress {{
        height: 6px;
        background: {LIGHT_BG};
        border-radius: 3px;
        overflow: hidden;
        margin-top: 0.4rem;
    }}
    .nx-progress-fill {{
        height: 100%;
        border-radius: 3px;
        transition: width 0.3s ease;
    }}

    /* ── Divider ────────────────────────────── */
    .nx-divider {{
        height: 1px;
        background: {BORDER};
        margin: 1.8rem 0;
        border: none;
    }}

    /* Streamlit overrides */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.85rem;
    }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SYNTHETIC DATA (unchanged logic, same deterministic output)
# ══════════════════════════════════════════════════════════════

SETTORI = ["AI", "Fintech", "Climate Tech", "HealthTech", "SaaS B2B",
           "HR Tech", "PropTech", "Cybersecurity", "Mobility", "EdTech"]

STADI = ["Idea", "MVP", "Traction", "Revenue"]

CITTA_IT = ["Milano", "Roma", "Torino", "Bologna", "Firenze", "Napoli",
            "Padova", "Bergamo", "Genova", "Verona", "Bari", "Catania",
            "Palermo", "Trieste", "Brescia", "Modena"]

OBIETTIVI = ["Fundraising", "Pilot aziendale", "Partnership", "Mentorship", "Co-founder"]

# Sector colors
SECTOR_COLORS = {
    "AI": "#6366f1", "Fintech": "#2EC4B6", "Climate Tech": "#22c55e",
    "HealthTech": "#ef4444", "SaaS B2B": "#3b82f6", "HR Tech": "#a855f7",
    "PropTech": "#f59e0b", "Cybersecurity": "#1B2A4A", "Mobility": "#06b6d4",
    "EdTech": "#ec4899",
}


@st.cache_data
def generate_startups(n=40):
    names = [
        "Nexara", "FinSmart", "GreenPulse", "MedIntel", "DataForge",
        "TalentUp", "SpaceNest", "CyberNext", "MoveFlow", "LearnHub",
        "Visionary AI", "PayLoop", "SolarMind", "VitaLink", "CloudMetrics",
        "SkillMatch", "CasaClick", "SecureNet", "RideSmart", "ClassForward",
        "DeepVision", "WealthPath", "EcoTrace", "PharmaFlow", "SyncBoard",
        "PeopleFirst", "UrbanKey", "ThreatMap", "LogiRoute", "MentorAI",
        "Predictiva", "TransactIO", "CarbonLess", "NurseBot", "APILayer",
        "HireWise", "BuildView", "VaultEdge", "FleetPulse", "StudyVerse",
    ]
    founders = [
        "Alice Colombo", "Marco Fontana", "Giulia Bianchi", "Luca Moretti",
        "Sara Ricci", "Andrea Conti", "Francesca De Luca", "Davide Galli",
        "Elena Marchetti", "Tommaso Barbieri", "Chiara Ferro", "Lorenzo Mancini",
        "Valentina Rossetti", "Matteo Pellegrini", "Silvia Caruso", "Federico Villa",
        "Martina Fabbri", "Giorgio Testa", "Eleonora Grasso", "Alessandro Vitale",
        "Beatrice Amato", "Simone Lombardi", "Anna Leone", "Nicola Parisi",
        "Laura Santoro", "Roberto Marini", "Irene Costa", "Pietro Benedetti",
        "Sofia Serra", "Giacomo Bassi", "Claudia Monti", "Filippo Greco",
        "Arianna Rizzi", "Daniele Cattaneo", "Camilla Orlando", "Enrico Palumbo",
        "Giulia Ferrara", "Paolo Sartori", "Teresa Mazza", "Riccardo Gatti",
    ]
    descriptions = [
        "Piattaforma di intelligenza artificiale per ottimizzare processi aziendali nel retail.",
        "Soluzione fintech per micropagamenti e gestione finanziaria per freelance.",
        "Monitoraggio e riduzione delle emissioni di CO2 per PMI tramite IoT.",
        "Sistema di triage medico basato su AI per pronto soccorso e cliniche.",
        "Suite SaaS per analytics predittive e reportistica automatizzata B2B.",
        "Piattaforma di talent matching basata su competenze e cultura aziendale.",
        "Marketplace digitale per affitti a breve termine di spazi commerciali.",
        "Soluzioni di cybersecurity avanzata per PMI e startup in cloud.",
        "App per la mobilità multimodale integrata nelle aree metropolitane.",
        "Piattaforma di microlearning personalizzato per formazione aziendale continua.",
        "Motore di visione artificiale per il controllo qualità industriale.",
        "Gateway di pagamento istantaneo con riconciliazione automatica per e-commerce.",
        "Software per la gestione e ottimizzazione di impianti fotovoltaici distribuiti.",
        "Piattaforma di telemedicina con monitoraggio remoto per pazienti cronici.",
        "Dashboard di business intelligence cloud-native per team distribuiti.",
        "AI matching engine per processi di selezione del personale.",
        "Piattaforma di valutazione immobiliare automatizzata con dati satellitari.",
        "Threat intelligence platform per la protezione proattiva delle reti aziendali.",
        "Ottimizzazione di flotte di veicoli condivisi tramite algoritmi predittivi.",
        "Piattaforma gamificata per l'apprendimento STEM nelle scuole superiori.",
        "Modelli di deep learning per la personalizzazione dell'esperienza utente.",
        "Robo-advisor di nuova generazione per investitori retail europei.",
        "Soluzione di tracciabilità della supply chain per la sostenibilità.",
        "Automazione dei processi farmaceutici con robotica e AI.",
        "Piattaforma collaborativa per la gestione di progetti enterprise.",
        "HR analytics per migliorare retention e benessere dei dipendenti.",
        "Piattaforma di gestione smart building con integrazione IoT.",
        "Soluzione di threat detection in tempo reale per infrastrutture critiche.",
        "Ottimizzazione logistica last-mile con intelligenza artificiale.",
        "Tutor AI personalizzato per percorsi di upskilling professionale.",
        "Piattaforma predittiva per manutenzione industriale basata su sensori.",
        "Infrastruttura blockchain per transazioni finanziarie cross-border.",
        "Marketplace per crediti di carbonio verificati e trasparenti.",
        "Assistente virtuale AI per infermieri e personale sanitario.",
        "API management platform per microservizi enterprise.",
        "Piattaforma di recruiting automation con screening AI-driven.",
        "Digital twin per cantieri edili e monitoraggio costruzioni.",
        "Piattaforma di gestione delle vulnerabilità e compliance automatizzata.",
        "Gestione intelligente di flotte aziendali e ottimizzazione consumi.",
        "Ambiente di apprendimento immersivo VR per università e corporate.",
    ]
    rng = np.random.RandomState(SEED)
    data = []
    for i in range(n):
        settore = SETTORI[i % len(SETTORI)]
        stadio = STADI[rng.randint(0, len(STADI))]
        citta = CITTA_IT[rng.randint(0, len(CITTA_IT))]
        obiettivo = OBIETTIVI[rng.randint(0, len(OBIETTIVI))]
        team = int(rng.choice([1, 2, 3, 4, 5, 7, 10, 12, 15, 20, 25, 30, 40]))
        mrr = 0
        users = 0
        growth = 0.0
        if stadio == "Idea":
            users = int(rng.randint(0, 50))
        elif stadio == "MVP":
            users = int(rng.randint(50, 500))
            mrr = int(rng.randint(0, 2000))
            growth = round(rng.uniform(0, 15), 1)
        elif stadio == "Traction":
            users = int(rng.randint(500, 10000))
            mrr = int(rng.randint(2000, 20000))
            growth = round(rng.uniform(5, 30), 1)
        elif stadio == "Revenue":
            users = int(rng.randint(5000, 100000))
            mrr = int(rng.randint(10000, 100000))
            growth = round(rng.uniform(3, 25), 1)
        score_profilo = int(rng.randint(55, 100))
        verificata = bool(rng.choice([True, False], p=[0.4, 0.6]))
        funding_need = {
            "Idea": "Pre-seed €50K–€150K",
            "MVP": "Seed €150K–€500K",
            "Traction": "Seed / Series A €500K–€2M",
            "Revenue": "Series A+ €1M–€5M",
        }[stadio]
        data.append({
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
            "score_profilo": score_profilo,
            "verificata": verificata,
            "funding_need": funding_need,
        })
    return pd.DataFrame(data)


@st.cache_data
def generate_companies(n=18):
    names = [
        "Gruppo Rinaldi", "Banca Meridiana", "EnerVita", "FarmaItalia",
        "TechnoMedia", "Costruzioni Lombarde", "AutoItalia", "AssicuraPlus",
        "RetailMax", "FoodCorp Italia", "LogiTrans", "TeleNova",
        "AeroSpace Solutions", "MedDevice Pro", "Stile Moda Group",
        "ChemTech Industries", "AgriSmart Italia", "InfoServices Group",
    ]
    settori = [
        "Manifattura", "Banking & Finance", "Energia", "Farmaceutico",
        "Media & Tech", "Real Estate", "Automotive", "Assicurazioni",
        "Retail", "Food & Beverage", "Logistica", "Telecomunicazioni",
        "Aerospace", "Medical Devices", "Fashion & Luxury",
        "Chimica", "Agricoltura", "IT & Servizi",
    ]
    aree_innovazione = [
        "AI", "Fintech", "Climate Tech", "HealthTech", "SaaS B2B",
        "HR Tech", "PropTech", "Cybersecurity", "Mobility", "EdTech",
        "AI", "SaaS B2B", "AI", "HealthTech", "AI",
        "Climate Tech", "Climate Tech", "Cybersecurity",
    ]
    dimensioni = [
        "Enterprise", "Enterprise", "Enterprise", "Enterprise",
        "Mid-market", "Mid-market", "Enterprise", "Enterprise",
        "Mid-market", "Mid-market", "Mid-market", "Enterprise",
        "Enterprise", "Mid-market", "Mid-market",
        "Enterprise", "PMI", "Mid-market",
    ]
    collaborazioni = [
        "Pilot", "Investimento", "Partnership", "Pilot",
        "Scouting", "Pilot", "Partnership", "Scouting",
        "Pilot", "Partnership", "Pilot", "Scouting",
        "Partnership", "Pilot", "Scouting",
        "Pilot", "Partnership", "Pilot",
    ]
    citta = [
        "Milano", "Roma", "Milano", "Roma", "Milano",
        "Bergamo", "Torino", "Trieste", "Bologna", "Parma",
        "Verona", "Roma", "Torino", "Padova", "Milano",
        "Brescia", "Bologna", "Roma",
    ]
    budget_classes = [
        "Alto", "Alto", "Alto", "Medio",
        "Medio", "Medio", "Alto", "Alto",
        "Medio", "Medio", "Basso", "Alto",
        "Alto", "Medio", "Medio",
        "Medio", "Basso", "Medio",
    ]
    descriptions = [
        "Gruppo industriale leader nel manifatturiero avanzato, cerca innovazione di processo.",
        "Istituto bancario con focus su digital transformation e open banking.",
        "Utility energetica impegnata nella transizione verde e smart grid.",
        "Azienda farmaceutica alla ricerca di soluzioni digitali per la R&D.",
        "Gruppo media-tech interessato a nuove piattaforme di contenuto e AI.",
        "Impresa edile che investe in digitalizzazione dei cantieri.",
        "Gruppo automotive in transizione verso l'elettrico e la connettività.",
        "Compagnia assicurativa che esplora insurtech e automazione sinistri.",
        "Catena retail che cerca soluzioni omnichannel e personalizzazione AI.",
        "Azienda alimentare interessata a supply chain tech e sostenibilità.",
        "Operatore logistico alla ricerca di ottimizzazione last-mile.",
        "Operatore telecom che investe in 5G, IoT e piattaforme cloud.",
        "Azienda aerospaziale interessata a materiali avanzati e AI per manutenzione.",
        "Produttore di dispositivi medici alla ricerca di digitalizzazione clinica.",
        "Gruppo moda che esplora AI per trend forecasting e sostenibilità.",
        "Industria chimica alla ricerca di soluzioni per riduzione impatto ambientale.",
        "Azienda agricola innovativa interessata a precision farming e IoT.",
        "Società di servizi IT che cerca partnership con startup SaaS.",
    ]
    rng = np.random.RandomState(SEED + 1)
    data = []
    for i in range(n):
        data.append({
            "nome": names[i],
            "settore": settori[i],
            "dimensione": dimensioni[i],
            "area_innovazione": aree_innovazione[i],
            "collaborazione": collaborazioni[i],
            "citta": citta[i],
            "budget_class": budget_classes[i],
            "tempo_valutazione_gg": int(rng.randint(14, 90)),
            "descrizione": descriptions[i],
            "premium": bool(rng.choice([True, False], p=[0.5, 0.5])),
        })
    return pd.DataFrame(data)


@st.cache_data
def generate_investors(n=18):
    names = [
        "Mediterraneo Ventures", "Italian Angels Network", "Primo Capital",
        "TechSeed Fund", "Innovation Bay Capital", "Alps Ventures",
        "Futuro Fund", "Digital Growth Partners", "EcoInvest",
        "HealthVentures Italia", "StartUp Factory Fund", "Valore Capital",
        "European Founders Fund", "Rinascimento Ventures", "Blue Horizon Partners",
        "Catalyst Angels", "NordEst Investimenti", "Meridione Growth Capital",
    ]
    tipi = [
        "VC", "Angel", "VC", "Micro-VC", "VC", "Micro-VC",
        "VC", "VC", "VC", "VC", "Micro-VC", "VC",
        "VC", "VC", "VC", "Angel", "Corporate VC", "VC",
    ]
    tickets = [
        "€500K–€3M", "€20K–€100K", "€1M–€5M", "€100K–€500K",
        "€500K–€2M", "€100K–€500K", "€1M–€5M", "€500K–€3M",
        "€300K–€2M", "€500K–€3M", "€100K–€500K", "€1M–€5M",
        "€2M–€10M", "€500K–€3M", "€1M–€5M", "€10K–€80K",
        "€300K–€2M", "€500K–€3M",
    ]
    ticket_min = [
        500, 20, 1000, 100, 500, 100, 1000, 500,
        300, 500, 100, 1000, 2000, 500, 1000, 10,
        300, 500,
    ]
    ticket_max = [
        3000, 100, 5000, 500, 2000, 500, 5000, 3000,
        2000, 3000, 500, 5000, 10000, 3000, 5000, 80,
        2000, 3000,
    ]
    focus_stages = [
        "Seed", "Pre-seed", "Series A", "Pre-seed", "Seed",
        "Pre-seed", "Series A", "Seed", "Seed", "Seed",
        "Pre-seed", "Series A", "Series A", "Seed", "Series A",
        "Pre-seed", "Seed", "Seed",
    ]
    settori_pref = [
        ["AI", "SaaS B2B", "Fintech"],
        ["AI", "HealthTech", "EdTech", "Climate Tech"],
        ["Fintech", "SaaS B2B", "Cybersecurity"],
        ["AI", "SaaS B2B", "HR Tech"],
        ["Climate Tech", "Mobility", "AI"],
        ["PropTech", "SaaS B2B", "Fintech"],
        ["AI", "HealthTech", "Cybersecurity"],
        ["SaaS B2B", "Fintech", "HR Tech"],
        ["Climate Tech", "Mobility", "PropTech"],
        ["HealthTech", "AI"],
        ["EdTech", "HR Tech", "SaaS B2B"],
        ["Fintech", "Cybersecurity", "AI"],
        ["AI", "SaaS B2B", "Climate Tech", "HealthTech"],
        ["AI", "Fintech", "Mobility"],
        ["SaaS B2B", "Cybersecurity", "Fintech"],
        ["AI", "EdTech", "HealthTech", "Climate Tech"],
        ["Mobility", "AI", "PropTech"],
        ["HealthTech", "Fintech", "Climate Tech"],
    ]
    geografie = [
        "Italia", "Italia", "Europa", "Italia", "Italia & Europa",
        "Nord Italia", "Europa", "Italia & Europa", "Europa",
        "Italia", "Italia", "Europa", "Europa", "Italia",
        "Europa", "Italia", "Nord-Est Italia", "Sud Italia & Isole",
    ]
    lead_follow = [
        "Lead", "Follow", "Lead", "Follow", "Lead", "Follow",
        "Lead", "Lead", "Lead", "Lead", "Follow", "Lead",
        "Lead", "Lead", "Lead", "Follow", "Follow", "Lead",
    ]
    rng = np.random.RandomState(SEED + 2)
    theses = [
        "Investiamo in startup tech italiane con forte potenziale di scalabilità internazionale.",
        "Supportiamo founder visionari con piccoli ticket e grande mentorship nella fase iniziale.",
        "Focus su round Serie A per aziende con traction dimostrata e mercato europeo.",
        "Primo capitale per team tecnici brillanti che risolvono problemi reali.",
        "Cerchiamo innovazione che genera impatto positivo su clima e mobilità.",
        "Investiamo in startup PropTech e SaaS che digitalizzano il real estate.",
        "Puntiamo su AI e cybersecurity per un futuro digitale più sicuro.",
        "Supportiamo la crescita di piattaforme SaaS con metriche solide.",
        "Investiamo esclusivamente in startup a impatto ambientale positivo.",
        "Focus verticale su HealthTech e digital health con team multidisciplinari.",
        "Acceleriamo startup EdTech e HR Tech con go-to-market B2B.",
        "Cerchiamo fintech e cybersecurity con modelli ricorrenti e difendibili.",
        "Fondo europeo generalista con preferenza per round Seed-Series A.",
        "Rinascimento dell'innovazione italiana: investiamo in eccellenze tecnologiche.",
        "Focus su infrastruttura software e sicurezza per enterprise.",
        "Angel investing con forte coinvolgimento operativo e rete di contatti.",
        "Corporate VC che connette startup alla rete industriale del Nord-Est.",
        "Valorizziamo il talento imprenditoriale del Mezzogiorno con capitale paziente.",
    ]
    data = []
    for i in range(n):
        data.append({
            "nome": names[i],
            "tipo": tipi[i],
            "ticket": tickets[i],
            "ticket_min_k": ticket_min[i],
            "ticket_max_k": ticket_max[i],
            "focus_stage": focus_stages[i],
            "settori_preferiti": settori_pref[i],
            "geografia": geografie[i],
            "lead_follow": lead_follow[i],
            "velocita_risposta_gg": int(rng.randint(3, 30)),
            "portfolio_size": int(rng.randint(5, 60)),
            "thesis": theses[i],
        })
    return pd.DataFrame(data)


@st.cache_data
def generate_feed():
    return [
        {"icona": "🚀", "tipo": "Milestone", "testo": "Nexara ha raggiunto 5.000 utenti attivi sulla piattaforma.", "tempo": "2 ore fa"},
        {"icona": "💰", "tipo": "Round aperto", "testo": "FinSmart ha aperto un round Seed da €400K su NexFound.", "tempo": "4 ore fa"},
        {"icona": "🏢", "tipo": "Challenge", "testo": "Banca Meridiana ha lanciato una innovation challenge su Open Banking.", "tempo": "6 ore fa"},
        {"icona": "📋", "tipo": "Thesis aggiornata", "testo": "Mediterraneo Ventures ha aggiornato la propria investment thesis.", "tempo": "8 ore fa"},
        {"icona": "🤝", "tipo": "Pilot avviato", "testo": "GreenPulse ha avviato un pilot con EnerVita per il monitoraggio emissioni.", "tempo": "1 giorno fa"},
        {"icona": "✅", "tipo": "Verifica", "testo": "MedIntel ha completato la verifica del profilo ed è ora verificata.", "tempo": "1 giorno fa"},
        {"icona": "🏢", "tipo": "Nuova azienda", "testo": "AutoItalia si è registrata su NexFound per scouting di startup Mobility.", "tempo": "2 giorni fa"},
        {"icona": "📊", "tipo": "Report", "testo": "Nuovo report settimanale: +12% match generati rispetto alla settimana precedente.", "tempo": "2 giorni fa"},
        {"icona": "🔔", "tipo": "Opportunità", "testo": "RetailMax cerca startup AI per personalizzazione in-store. Candidature aperte.", "tempo": "3 giorni fa"},
        {"icona": "🚀", "tipo": "Milestone", "testo": "DataForge ha superato €15K di MRR, in crescita del 22% mese su mese.", "tempo": "3 giorni fa"},
        {"icona": "💰", "tipo": "Investimento", "testo": "Primo Capital ha completato un investimento in una startup Fintech tramite NexFound.", "tempo": "4 giorni fa"},
        {"icona": "🤝", "tipo": "Partnership", "testo": "TalentUp ha siglato una partnership con InfoServices Group per HR analytics.", "tempo": "5 giorni fa"},
    ]


# ══════════════════════════════════════════════════════════════
# MATCHING ENGINE (unchanged)
# ══════════════════════════════════════════════════════════════

STAGE_COMPAT_INV = {
    "Pre-seed": {"Idea": 95, "MVP": 70, "Traction": 30, "Revenue": 10},
    "Seed": {"Idea": 40, "MVP": 90, "Traction": 85, "Revenue": 40},
    "Series A": {"Idea": 5, "MVP": 30, "Traction": 90, "Revenue": 95},
    "Growth": {"Idea": 0, "MVP": 5, "Traction": 40, "Revenue": 90},
}
STAGE_COMPAT_CORP = {
    "PMI": {"Idea": 50, "MVP": 80, "Traction": 70, "Revenue": 60},
    "Mid-market": {"Idea": 20, "MVP": 60, "Traction": 90, "Revenue": 85},
    "Enterprise": {"Idea": 5, "MVP": 30, "Traction": 80, "Revenue": 95},
}
OBJ_COLLAB_MAP = {
    "Fundraising": {"Investimento": 90, "Scouting": 40, "Pilot": 20, "Partnership": 30},
    "Pilot aziendale": {"Pilot": 95, "Scouting": 70, "Partnership": 60, "Investimento": 15},
    "Partnership": {"Partnership": 95, "Pilot": 70, "Scouting": 60, "Investimento": 20},
    "Mentorship": {"Partnership": 50, "Pilot": 40, "Scouting": 60, "Investimento": 20},
    "Co-founder": {"Partnership": 40, "Pilot": 20, "Scouting": 30, "Investimento": 10},
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
GEO_NORTH = {"Milano", "Torino", "Bergamo", "Padova", "Genova", "Verona", "Brescia", "Trieste", "Modena"}
GEO_CENTER = {"Roma", "Bologna", "Firenze"}
GEO_SOUTH = {"Napoli", "Bari", "Catania", "Palermo"}


def _geo_region(citta):
    if citta in GEO_NORTH:
        return "Nord"
    elif citta in GEO_CENTER:
        return "Centro"
    return "Sud"


def compute_investor_match(startup, investor):
    scores = {}
    explanations = []
    s_sec = startup["settore"]
    inv_secs = investor["settori_preferiti"]
    if s_sec in inv_secs:
        scores["Settore"] = 95
        explanations.append(f"Il settore {s_sec} è tra i focus dell'investitore.")
    elif any(r in inv_secs for r in RELATED_SECTORS.get(s_sec, [])):
        scores["Settore"] = 60
        explanations.append(f"Il settore {s_sec} è affine ai focus dell'investitore.")
    else:
        scores["Settore"] = 15
    stage_scores = STAGE_COMPAT_INV.get(investor["focus_stage"], {})
    scores["Stadio"] = stage_scores.get(startup["stadio"], 30)
    if scores["Stadio"] >= 80:
        explanations.append(f"Lo stadio {startup['stadio']} è in linea con il focus {investor['focus_stage']}.")
    inv_geo = investor["geografia"]
    s_region = _geo_region(startup["citta"])
    if "Europa" in inv_geo or "Italia" == inv_geo:
        scores["Geografia"] = 85
    elif "Nord" in inv_geo and s_region == "Nord":
        scores["Geografia"] = 95
        explanations.append("Match geografico: entrambi nel Nord Italia.")
    elif "Sud" in inv_geo and s_region == "Sud":
        scores["Geografia"] = 95
        explanations.append("Match geografico nel Sud Italia e Isole.")
    elif "Nord-Est" in inv_geo and startup["citta"] in {"Padova", "Trieste", "Verona"}:
        scores["Geografia"] = 95
    else:
        scores["Geografia"] = 50
    funding_stage_need_k = {"Idea": 100, "MVP": 350, "Traction": 1000, "Revenue": 3000}
    need = funding_stage_need_k[startup["stadio"]]
    if investor["ticket_min_k"] <= need <= investor["ticket_max_k"]:
        scores["Ticket"] = 95
        explanations.append("Il ticket dell'investitore copre il fabbisogno stimato della startup.")
    elif investor["ticket_min_k"] <= need * 1.5 and need * 0.5 <= investor["ticket_max_k"]:
        scores["Ticket"] = 65
    else:
        scores["Ticket"] = 20
    weights = {"Settore": 0.30, "Stadio": 0.25, "Geografia": 0.15, "Ticket": 0.30}
    overall = sum(scores[k] * weights[k] for k in weights)
    return round(overall), scores, explanations


def compute_company_match(startup, company):
    scores = {}
    explanations = []
    if startup["settore"] == company["area_innovazione"]:
        scores["Settore"] = 95
        explanations.append(f"L'area di innovazione {company['area_innovazione']} corrisponde al settore della startup.")
    elif startup["settore"] in RELATED_SECTORS.get(company["area_innovazione"], []):
        scores["Settore"] = 60
        explanations.append("Il settore della startup è affine all'area di innovazione dell'azienda.")
    else:
        scores["Settore"] = 15
    obj_scores = OBJ_COLLAB_MAP.get(startup["obiettivo"], {})
    scores["Collaborazione"] = obj_scores.get(company["collaborazione"], 25)
    if scores["Collaborazione"] >= 70:
        explanations.append(f"L'obiettivo '{startup['obiettivo']}' è compatibile con '{company['collaborazione']}'.")
    stage_scores = STAGE_COMPAT_CORP.get(company["dimensione"], {})
    scores["Stadio"] = stage_scores.get(startup["stadio"], 40)
    if scores["Stadio"] >= 75:
        explanations.append(f"La maturità della startup è adatta a una {company['dimensione']}.")
    s_region = _geo_region(startup["citta"])
    c_region = _geo_region(company["citta"])
    if s_region == c_region:
        scores["Geografia"] = 90
        explanations.append("Vicinanza geografica favorevole alla collaborazione.")
    else:
        scores["Geografia"] = 55
    weights = {"Settore": 0.35, "Collaborazione": 0.30, "Stadio": 0.20, "Geografia": 0.15}
    overall = sum(scores[k] * weights[k] for k in weights)
    return round(overall), scores, explanations


# ══════════════════════════════════════════════════════════════
# UI HELPERS — Premium components
# ══════════════════════════════════════════════════════════════

def _initials(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def _truncate_text(text, max_len=110):
    """Truncate testo intelligentemente: aggiungi '...' solo se troncs realmente."""
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "..."


def nx_metric(label, value, icon="", delta="", accent=False):
    cls = "nx-metric nx-metric-accent" if accent else "nx-metric"
    delta_html = ""
    if delta:
        arrow = "↑" if delta.startswith("+") else ("↓" if delta.startswith("-") else "")
        dcls = "up" if arrow == "↑" else "neutral"
        delta_html = f'<div class="metric-delta {dcls}">{arrow} {delta}</div>'
    st.markdown(f"""
    <div class="{cls}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)


def nx_section(title, subtitle=""):
    st.markdown(f"""
    <div class="nx-section-header">
        <h2>{title}</h2>
        <div class="accent-line"></div>
    </div>""", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="nx-section-sub">{subtitle}</div>', unsafe_allow_html=True)


def nx_divider():
    st.markdown('<div class="nx-divider"></div>', unsafe_allow_html=True)


def render_radar(scores_dict, title=""):
    cats = list(scores_dict.keys())
    vals = list(scores_dict.values())
    cats.append(cats[0])
    vals.append(vals[0])
    fig = go.Figure(data=go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        fillcolor='rgba(46,196,182,0.18)',
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=5, color=ACCENT),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(0,0,0,0.06)"),
            angularaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        margin=dict(l=50, r=50, t=35, b=35),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=title, font=dict(size=13, color=TEXT_SECONDARY)) if title else None,
    )
    return fig


def score_color(score):
    if score >= 75:
        return ACCENT
    if score >= 55:
        return AMBER
    return CORAL


def score_bar_html(score, label="Profilo"):
    c = score_color(score)
    return f"""
    <div style="font-size:0.78rem; color:{TEXT_MUTED}; display:flex; justify-content:space-between;">
        <span>{label}</span><span style="font-weight:600; color:{c};">{score}%</span>
    </div>
    <div class="nx-progress"><div class="nx-progress-fill" style="width:{score}%; background:{c};"></div></div>
    """


# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════

if "contact_requests" not in st.session_state:
    st.session_state.contact_requests = []
if "saved_matches" not in st.session_state:
    st.session_state.saved_matches = []

# ══════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════

df_startups = generate_startups()
df_companies = generate_companies()
df_investors = generate_investors()
feed_items = generate_feed()


# ══════════════════════════════════════════════════════════════
# SECTIONS
# ══════════════════════════════════════════════════════════════

# ─── 1. HOME ─────────────────────────────────────────────────

def section_home():
    # Hero
    st.markdown(f"""
    <div class="nx-hero">
        <h1>🔗 Nex<span class="hero-accent">Found</span></h1>
        <div class="hero-tagline">
            La piattaforma intelligente che connette <b>startup</b>, <b>aziende</b> e <b>investitori</b>
            per accelerare l'innovazione in Italia e in Europa.
        </div>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-value">247</div>
                <div class="hero-stat-label">Startup</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">68</div>
                <div class="hero-stat-label">Aziende</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">42</div>
                <div class="hero-stat-label">Investitori</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">1.247</div>
                <div class="hero-stat-label">Match generati</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Three pillars
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="nx-eco">
            <div class="eco-icon">🚀</div>
            <h3>Startup</h3>
            <p>Visibilità qualificata, accesso diretto a investitori e corporate, match intelligenti per crescere.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="nx-eco nx-eco-center">
            <div class="eco-icon">🏢</div>
            <h3>Aziende</h3>
            <p>Scouting strutturato, accesso a startup verificate, open innovation semplificata.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="nx-eco">
            <div class="eco-icon">💰</div>
            <h3>Investitori</h3>
            <p>Deal flow curato, segnali strutturati, filtraggio efficiente per investire meglio.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPI row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        nx_metric("Startup registrate", "247", "🚀", "+18 questo mese")
    with m2:
        nx_metric("Aziende attive", "68", "🏢", "+5 questo mese")
    with m3:
        nx_metric("Investitori", "42", "💰", "+3 questo mese")
    with m4:
        nx_metric("Match generati", "1.247", "🎯", "+12% vs mese prec.")
    with m5:
        nx_metric("Intro completate", "328", "🤝", "+8% vs mese prec.", accent=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Scenario demo
    st.markdown(f"""
    <div class="nx-info nx-info-accent">
        <h4>📖 Scenario demo — Il percorso di Alice</h4>
        <p>
            <b>Alice Colombo</b>, founder di <b>Nexara</b> (startup AI per il retail), si registra su NexFound e completa il profilo.
            La piattaforma genera automaticamente <b>3 match rilevanti</b>: 2 aziende (RetailMax e Gruppo Rinaldi)
            e 1 investitore (Mediterraneo Ventures). Alice invia una richiesta di contatto a RetailMax,
            che viene accettata in 3 giorni. Un pilot viene avviato entro il mese.
        </p>
        <p style="color:{TEXT_MUTED}; font-size:0.85rem; margin-top:0.6rem;">
            👉 Naviga tra le sezioni nel menu laterale per vedere ogni passaggio in azione.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ Come leggere questa demo"):
        st.markdown(f"""
        Questa è una **demo interattiva** di NexFound, costruita con dati sintetici ma realistici.

        **Come navigare:** usa il **menu laterale** per passare tra le sezioni.

        **Momenti chiave della presentazione:**
        1. **Matching Intelligente** — il cuore della piattaforma, con score spiegabili
        2. **Flusso di Contatto** — come avviene una richiesta di intro
        3. **Dashboard KPI** — metriche di piattaforma per investitori e stakeholder

        *Tutti i nomi, i dati e le metriche sono fittizi e generati a scopo dimostrativo.*
        """)


# ─── 2. PROBLEMA DI MERCATO ──────────────────────────────────

def section_problema():
    nx_section("Il problema di mercato",
               "Tre attori dell'ecosistema innovazione, tre insiemi di pain point irrisolti.")

    t1, t2, t3 = st.tabs(["🚀 Startup", "🏢 Aziende", "💰 Investitori"])

    pains = {
        "startup": [
            ("😶‍🌫️", "Poca visibilità qualificata", "Le startup faticano a farsi notare da investitori e corporate rilevanti, affidandosi a contatti informali e eventi casuali."),
            ("🚪", "Accesso limitato", "Raggiungere decision-maker in aziende e fondi è complesso senza un network preesistente."),
            ("🎯", "Contatti irrilevanti", "Il tempo speso a generare lead spesso produce contatti non in target, riducendo l'efficacia del business development."),
        ],
        "aziende": [
            ("🔍", "Scouting dispersivo", "Le aziende dedicano molto tempo allo scouting di startup senza un canale strutturato, con risultati inconsistenti."),
            ("📊", "Filtraggio inefficiente", "Valutare centinaia di startup senza segnali strutturati richiede risorse sproporzionate."),
            ("🔗", "Canale mancante", "Manca una piattaforma dedicata per l'open innovation che connetta direttamente con startup qualificate."),
        ],
        "investitori": [
            ("📢", "Deal flow rumoroso", "Gli investitori ricevono deal non filtrati e non strutturati, rendendo difficile identificare le opportunità migliori."),
            ("📉", "Segnali deboli", "Mancano metriche standardizzate e segnali strutturati per valutare rapidamente il potenziale di una startup."),
            ("⏳", "Tempo sprecato", "Il processo di filtraggio manuale sottrae tempo all'attività di valore: analisi approfondita e supporto ai founder."),
        ],
    }

    for tab, key in zip([t1, t2, t3], ["startup", "aziende", "investitori"]):
        with tab:
            cols = st.columns(3)
            for col, (icon, title, desc) in zip(cols, pains[key]):
                with col:
                    st.markdown(f"""
                    <div class="nx-pain">
                        <div class="pain-icon">{icon}</div>
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="nx-cta">
        <h2>NexFound risolve questi problemi</h2>
        <p>Un'unica piattaforma che connette i tre attori con matching intelligente, profili strutturati e flussi di contatto semplificati.</p>
    </div>
    """, unsafe_allow_html=True)


# ─── 3. ECOSISTEMA NEXFOUND ──────────────────────────────────

def section_ecosistema():
    nx_section("L'ecosistema NexFound",
               "Tre attori, una piattaforma, valore condiviso.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="nx-eco">
            <div class="eco-icon">🚀</div>
            <h3>Startup</h3>
            <p style="text-align:left;">
                ✅ Profilo strutturato e verificabile<br>
                ✅ Match automatici con investor e corporate<br>
                ✅ Visibilità presso decision-maker<br>
                ✅ Pipeline di contatti organizzata<br>
                ✅ Credibilità tramite badge di verifica
            </p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="nx-eco nx-eco-center">
            <div class="eco-icon">🔗</div>
            <h3>NexFound</h3>
            <p style="text-align:left;">
                🎯 Matching intelligente e spiegabile<br>
                📊 Profili standardizzati e comparabili<br>
                📨 Flussi di contatto gestiti end-to-end<br>
                ✅ Verifica e trust layer integrato<br>
                📈 Analytics e insight per tutti
            </p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="nx-eco">
            <div class="eco-icon">🏢 💰</div>
            <h3>Aziende & Investitori</h3>
            <p style="text-align:left;">
                ✅ Scouting efficiente e mirato<br>
                ✅ Deal flow qualificato e curato<br>
                ✅ Filtri avanzati per settore, stadio, geo<br>
                ✅ Richieste di contatto semplificate<br>
                ✅ Metriche e segnali strutturati
            </p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nx-flow">
        <h4>Flusso di valore sulla piattaforma</h4>
        <div class="nx-flow-steps">
            <span class="step">🚀 Startup pubblica profilo</span>
            <span class="arrow">→</span>
            <span class="step">🎯 NexFound genera match</span>
            <span class="arrow">→</span>
            <span class="step">🏢💰 Scoperta opportunità</span>
            <span class="arrow">→</span>
            <span class="step">📨 Intro request</span>
            <span class="arrow">→</span>
            <span class="step">🤝 Collaborazione / Investimento</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── 4. DIRECTORY STARTUP ────────────────────────────────────

def _startup_card(s):
    initials = _initials(s["nome"])
    badges = (
        f'<span class="nx-badge nx-badge-accent">{s["settore"]}</span>'
        f'<span class="nx-badge nx-badge-coral">{s["stadio"]}</span>'
        f'<span class="nx-badge nx-badge-primary">{s["obiettivo"]}</span>'
    )
    if s["verificata"]:
        badges += '<span class="nx-badge nx-badge-success">✅ Verificata</span>'
    desc = _truncate_text(s['descrizione'])
    bar = score_bar_html(s['score_profilo'])
    return (
        '<div class="nx-card">'
        '<div class="card-header">'
        f'<div class="card-avatar avatar-startup">{initials}</div>'
        f'<div><div class="card-name">{s["nome"]}</div>'
        f'<div class="card-subtitle">{s["founder"]} · 📍 {s["citta"]}</div></div>'
        '</div>'
        f'<div>{badges}</div>'
        f'<div class="card-body">{desc}</div>'
        f'<div class="card-meta">👥 {s["team_size"]} persone</div>'
        f'{bar}'
        '</div>'
    )


def section_startups():
    nx_section("Directory Startup",
               f"{len(df_startups)} startup registrate sulla piattaforma.")

    with st.sidebar:
        st.markdown("#### 🔍 Filtri Startup")
        f_settore = st.multiselect("Settore", SETTORI, key="f_s_settore")
        f_stadio = st.multiselect("Stadio", STADI, key="f_s_stadio")
        f_citta = st.multiselect("Città", sorted(df_startups["citta"].unique()), key="f_s_citta")
        f_obiettivo = st.multiselect("Obiettivo", OBIETTIVI, key="f_s_obj")
        f_verificata = st.selectbox("Verificata", ["Tutte", "Sì", "No"], key="f_s_ver")

    filtered = df_startups.copy()
    if f_settore:
        filtered = filtered[filtered["settore"].isin(f_settore)]
    if f_stadio:
        filtered = filtered[filtered["stadio"].isin(f_stadio)]
    if f_citta:
        filtered = filtered[filtered["citta"].isin(f_citta)]
    if f_obiettivo:
        filtered = filtered[filtered["obiettivo"].isin(f_obiettivo)]
    if f_verificata == "Sì":
        filtered = filtered[filtered["verificata"]]
    elif f_verificata == "No":
        filtered = filtered[~filtered["verificata"]]

    st.markdown(f"**{len(filtered)}** startup trovate")

    cols_per_row = 3
    for row_start in range(0, min(len(filtered), 12), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = row_start + j
            if idx < len(filtered):
                with col:
                    st.markdown(_startup_card(filtered.iloc[idx]), unsafe_allow_html=True)

    if len(filtered) > 12:
        st.info(f"Mostrate 12 di {len(filtered)} startup. Usa i filtri per restringere la ricerca.")

    nx_divider()
    st.markdown("#### 🔎 Dettaglio Startup")
    selected_name = st.selectbox("Seleziona una startup", filtered["nome"].tolist(), key="startup_detail")
    s = filtered[filtered["nome"] == selected_name].iloc[0]

    dc1, dc2 = st.columns([5, 2])
    with dc1:
        ver_label = "✅ Verificata" if s["verificata"] else "Non verificata"
        st.markdown(f"""
        <div class="nx-detail">
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:0.8rem;">
                <div class="card-avatar avatar-startup" style="width:52px;height:52px;font-size:1.2rem;border-radius:12px;">{_initials(s['nome'])}</div>
                <div>
                    <div class="detail-name">{s['nome']}</div>
                    <span class="nx-badge nx-badge-accent">{s['settore']}</span>
                    <span class="nx-badge nx-badge-coral">{s['stadio']}</span>
                    <span class="nx-badge nx-badge-primary">{s['obiettivo']}</span>
                    <span class="nx-badge nx-badge-gray">{ver_label}</span>
                </div>
            </div>
            <div class="detail-desc">{_truncate_text(s['descrizione'], max_len=500)}</div>
            <div class="detail-meta">
                👤 <b>Founder:</b> {s['founder']}<br>
                📍 <b>Città:</b> {s['citta']}<br>
                👥 <b>Team:</b> {s['team_size']} persone<br>
                💰 <b>Fabbisogno:</b> {s['funding_need']}<br>
                🎯 <b>Obiettivo attuale:</b> {s['obiettivo']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with dc2:
        nx_metric("Utenti", f"{s['users']:,}", "👥")
        nx_metric("MRR", f"€{s['mrr']:,}", "💰")
        nx_metric("Crescita mese", f"{s['growth_pct']}%", "📈")
        nx_metric("Score profilo", f"{s['score_profilo']}/100", "⭐")

    with st.expander("📊 Anteprima match per questa startup"):
        top_inv = []
        for _, inv in df_investors.iterrows():
            sc, _, _ = compute_investor_match(s, inv)
            top_inv.append((inv["nome"], sc, inv["tipo"]))
        top_inv.sort(key=lambda x: x[1], reverse=True)
        st.markdown("**Top 3 investitori compatibili:**")
        for name, sc, tipo in top_inv[:3]:
            c = score_color(sc)
            st.markdown(f"- **{name}** ({tipo}) — <span style='color:{c}; font-weight:700;'>{sc}%</span>", unsafe_allow_html=True)


# ─── 5. DIRECTORY AZIENDE ────────────────────────────────────

def _company_card(c):
    initials = _initials(c["nome"])
    badges = (
        f'<span class="nx-badge nx-badge-accent">{c["area_innovazione"]}</span>'
        f'<span class="nx-badge nx-badge-coral">{c["dimensione"]}</span>'
        f'<span class="nx-badge nx-badge-primary">{c["collaborazione"]}</span>'
    )
    if c["premium"]:
        badges += '<span class="nx-badge nx-badge-amber">⭐ Premium</span>'
    desc = _truncate_text(c['descrizione'])
    return (
        '<div class="nx-card">'
        '<div class="card-header">'
        f'<div class="card-avatar avatar-company">{initials}</div>'
        f'<div><div class="card-name">{c["nome"]}</div>'
        f'<div class="card-subtitle">{c["settore"]} · 📍 {c["citta"]}</div></div>'
        '</div>'
        f'<div>{badges}</div>'
        f'<div class="card-body">{desc}</div>'
        f'<div class="card-meta">💳 Budget: {c["budget_class"]} · ⏱️ {c["tempo_valutazione_gg"]}gg valutazione</div>'
        '</div>'
    )


def section_aziende():
    nx_section("Directory Aziende",
               f"{len(df_companies)} aziende attive sulla piattaforma.")

    with st.sidebar:
        st.markdown("#### 🔍 Filtri Aziende")
        f_dim = st.multiselect("Dimensione", ["PMI", "Mid-market", "Enterprise"], key="f_c_dim")
        f_area = st.multiselect("Area innovazione", SETTORI, key="f_c_area")
        f_collab = st.multiselect("Collaborazione cercata", ["Pilot", "Partnership", "Investimento", "Scouting"], key="f_c_collab")

    filtered = df_companies.copy()
    if f_dim:
        filtered = filtered[filtered["dimensione"].isin(f_dim)]
    if f_area:
        filtered = filtered[filtered["area_innovazione"].isin(f_area)]
    if f_collab:
        filtered = filtered[filtered["collaborazione"].isin(f_collab)]

    st.markdown(f"**{len(filtered)}** aziende trovate")

    cols_per_row = 3
    for row_start in range(0, min(len(filtered), 12), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = row_start + j
            if idx < len(filtered):
                with col:
                    st.markdown(_company_card(filtered.iloc[idx]), unsafe_allow_html=True)

    nx_divider()
    st.markdown("#### 🔎 Dettaglio Azienda")
    sel = st.selectbox("Seleziona un'azienda", filtered["nome"].tolist(), key="az_detail")
    c = filtered[filtered["nome"] == sel].iloc[0]

    cc1, cc2 = st.columns([5, 2])
    with cc1:
        prem_label = "⭐ Premium" if c["premium"] else "Standard"
        st.markdown(f"""
        <div class="nx-detail">
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:0.8rem;">
                <div class="card-avatar avatar-company" style="width:52px;height:52px;font-size:1.2rem;border-radius:12px;">{_initials(c['nome'])}</div>
                <div>
                    <div class="detail-name">{c['nome']}</div>
                    <span class="nx-badge nx-badge-accent">{c['area_innovazione']}</span>
                    <span class="nx-badge nx-badge-coral">{c['dimensione']}</span>
                    <span class="nx-badge nx-badge-primary">{c['collaborazione']}</span>
                    <span class="nx-badge nx-badge-gray">{prem_label}</span>
                </div>
            </div>
            <div class="detail-desc">{_truncate_text(c['descrizione'], max_len=500)}</div>
            <div class="detail-meta">
                📍 <b>Città:</b> {c['citta']}<br>
                🏭 <b>Settore:</b> {c['settore']}<br>
                🤝 <b>Collaborazione cercata:</b> {c['collaborazione']}<br>
                💳 <b>Budget innovazione:</b> {c['budget_class']}<br>
                ⏱️ <b>Tempo medio valutazione:</b> {c['tempo_valutazione_gg']} giorni
            </div>
        </div>
        """, unsafe_allow_html=True)
    with cc2:
        nx_metric("Budget innovazione", c["budget_class"], "💳")
        nx_metric("Tempo valutazione", f"{c['tempo_valutazione_gg']}gg", "⏱️")
        nx_metric("Area focus", c["area_innovazione"], "🎯")


# ─── 6. DIRECTORY INVESTITORI ─────────────────────────────────

def _investor_card(inv):
    secs = ", ".join(inv["settori_preferiti"][:3])
    initials = _initials(inv["nome"])
    desc = _truncate_text(inv['thesis'])
    badges = (
        f'<span class="nx-badge nx-badge-accent">{inv["tipo"]}</span>'
        f'<span class="nx-badge nx-badge-coral">{inv["focus_stage"]}</span>'
        f'<span class="nx-badge nx-badge-primary">{inv["lead_follow"]}</span>'
    )
    return (
        '<div class="nx-card">'
        '<div class="card-header">'
        f'<div class="card-avatar avatar-investor">{initials}</div>'
        f'<div><div class="card-name">{inv["nome"]}</div>'
        f'<div class="card-subtitle">{inv["tipo"]} · {inv["geografia"]}</div></div>'
        '</div>'
        f'<div>{badges}</div>'
        f'<div class="card-body">{desc}</div>'
        f'<div class="card-meta">🎯 {secs} · 💰 {inv["ticket"]}</div>'
        '</div>'
    )


def section_investitori():
    nx_section("Directory Investitori",
               f"{len(df_investors)} investitori attivi sulla piattaforma.")

    with st.sidebar:
        st.markdown("#### 🔍 Filtri Investitori")
        f_tipo = st.multiselect("Tipo", ["Angel", "Micro-VC", "VC", "Corporate VC"], key="f_i_tipo")
        f_stage = st.multiselect("Focus stage", ["Pre-seed", "Seed", "Series A", "Growth"], key="f_i_stage")
        f_sec_inv = st.multiselect("Settori preferiti", SETTORI, key="f_i_sec")

    filtered = df_investors.copy()
    if f_tipo:
        filtered = filtered[filtered["tipo"].isin(f_tipo)]
    if f_stage:
        filtered = filtered[filtered["focus_stage"].isin(f_stage)]
    if f_sec_inv:
        filtered = filtered[filtered["settori_preferiti"].apply(lambda x: any(s in x for s in f_sec_inv))]

    st.markdown(f"**{len(filtered)}** investitori trovati")

    cols_per_row = 3
    for row_start in range(0, min(len(filtered), 12), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = row_start + j
            if idx < len(filtered):
                with col:
                    st.markdown(_investor_card(filtered.iloc[idx]), unsafe_allow_html=True)

    nx_divider()
    st.markdown("#### 🔎 Dettaglio Investitore")
    sel = st.selectbox("Seleziona un investitore", filtered["nome"].tolist(), key="inv_detail")
    inv = filtered[filtered["nome"] == sel].iloc[0]

    ic1, ic2 = st.columns([5, 2])
    with ic1:
        secs_all = ", ".join(inv["settori_preferiti"])
        st.markdown(f"""
        <div class="nx-detail">
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:0.8rem;">
                <div class="card-avatar avatar-investor" style="width:52px;height:52px;font-size:1.2rem;border-radius:12px;">{_initials(inv['nome'])}</div>
                <div>
                    <div class="detail-name">{inv['nome']}</div>
                    <span class="nx-badge nx-badge-accent">{inv['tipo']}</span>
                    <span class="nx-badge nx-badge-coral">{inv['focus_stage']}</span>
                    <span class="nx-badge nx-badge-primary">{inv['lead_follow']}</span>
                </div>
            </div>
            <div class="detail-desc" style="font-style:italic;">"{_truncate_text(inv['thesis'], max_len=500)}"</div>
            <div class="detail-meta">
                💰 <b>Ticket:</b> {inv['ticket']}<br>
                🎯 <b>Settori:</b> {secs_all}<br>
                🌍 <b>Geografia:</b> {inv['geografia']}<br>
                📂 <b>Portfolio:</b> {inv['portfolio_size']} startup<br>
                ⏱️ <b>Velocità risposta:</b> ~{inv['velocita_risposta_gg']} giorni
            </div>
        </div>
        """, unsafe_allow_html=True)
    with ic2:
        nx_metric("Ticket medio", inv["ticket"], "💰")
        nx_metric("Portfolio", f"{inv['portfolio_size']} startup", "📂")
        nx_metric("Risposta media", f"{inv['velocita_risposta_gg']}gg", "⏱️")
        nx_metric("Preferenza", inv["lead_follow"], "🎯")


# ─── 7. MATCHING INTELLIGENTE ─────────────────────────────────

def section_matching():
    nx_section("Matching Intelligente",
               "Il cuore di NexFound: connessioni rilevanti basate su criteri strutturati e spiegabili.")

    st.markdown(f"""
    <div class="nx-info nx-info-accent">
        <p style="margin:0;">
            Il motore di matching analizza <b>settore</b>, <b>stadio</b>, <b>geografia</b>,
            <b>ticket/budget</b> e <b>obiettivi</b> per generare raccomandazioni.
            Ogni match è accompagnato da un punteggio percentuale e una spiegazione.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    selected_startup = st.selectbox("🚀 Seleziona una startup", df_startups["nome"].tolist(), key="match_startup")
    s = df_startups[df_startups["nome"] == selected_startup].iloc[0]

    # Compact selected startup summary
    st.markdown(f"""
    <div class="nx-card" style="border-left:4px solid {ACCENT}; margin-bottom:1.2rem;">
        <div class="card-header">
            <div class="card-avatar avatar-startup">{_initials(s['nome'])}</div>
            <div>
                <div class="card-name">{s['nome']}</div>
                <div class="card-subtitle">
                    {s['settore']} · {s['stadio']} · 📍 {s['citta']} · 🎯 {s['obiettivo']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    match_type = st.radio("Tipo di ricerca", ["🔍 Ricerca Investitori", "🔍 Ricerca Corporate"], horizontal=True, key="match_type")

    if "Investitori" in match_type:
        results = []
        for _, inv in df_investors.iterrows():
            sc, sub_scores, explanations = compute_investor_match(s, inv)
            results.append({
                "nome": inv["nome"], "tipo": inv["tipo"], "ticket": inv["ticket"],
                "score": sc, "sub_scores": sub_scores, "explanations": explanations,
                "focus_stage": inv["focus_stage"],
                "settori": ", ".join(inv["settori_preferiti"][:3]),
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        top_n = st.slider("Numero di match da mostrare", 3, 10, 5, key="match_n_inv")

        for i, r in enumerate(results[:top_n]):
            sc_col = score_color(r["score"])
            expl_html = "<br>".join(f"✅ {e}" for e in r["explanations"]) if r["explanations"] else "⚠️ Compatibilità limitata su alcuni criteri."
            mc1, mc2 = st.columns([3, 2])
            with mc1:
                st.markdown(f"""
                <div class="nx-match">
                    <div class="match-header">
                        <div>
                            <div class="match-rank">Match #{i+1}</div>
                            <div class="match-name">{r['nome']}</div>
                            <span class="nx-badge nx-badge-accent">{r['tipo']}</span>
                            <span class="nx-badge nx-badge-coral">{r['focus_stage']}</span>
                            <span style="font-size:0.82rem; color:{TEXT_MUTED};"> · 🎯 {r['settori']} · 💰 {r['ticket']}</span>
                        </div>
                        <div class="match-score-box">
                            <div class="match-score-value" style="color:{sc_col};">{r['score']}%</div>
                            <div class="match-score-label">Compatibilità</div>
                        </div>
                    </div>
                    <div class="match-reasons">{expl_html}</div>
                </div>
                """, unsafe_allow_html=True)
            with mc2:
                fig = render_radar(r["sub_scores"])
                st.plotly_chart(fig, use_container_width=True, key=f"radar_inv_{i}")

    else:
        results = []
        for _, co in df_companies.iterrows():
            sc, sub_scores, explanations = compute_company_match(s, co)
            results.append({
                "nome": co["nome"], "dimensione": co["dimensione"],
                "collaborazione": co["collaborazione"], "score": sc,
                "sub_scores": sub_scores, "explanations": explanations,
                "area": co["area_innovazione"], "citta": co["citta"],
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        top_n = st.slider("Numero di match da mostrare", 3, 10, 5, key="match_n_corp")

        for i, r in enumerate(results[:top_n]):
            sc_col = score_color(r["score"])
            expl_html = "<br>".join(f"✅ {e}" for e in r["explanations"]) if r["explanations"] else "⚠️ Compatibilità limitata su alcuni criteri."
            mc1, mc2 = st.columns([3, 2])
            with mc1:
                st.markdown(f"""
                <div class="nx-match">
                    <div class="match-header">
                        <div>
                            <div class="match-rank">Match #{i+1}</div>
                            <div class="match-name">{r['nome']}</div>
                            <span class="nx-badge nx-badge-accent">{r['dimensione']}</span>
                            <span class="nx-badge nx-badge-coral">{r['area']}</span>
                            <span style="font-size:0.82rem; color:{TEXT_MUTED};"> · 🤝 {r['collaborazione']} · 📍 {r['citta']}</span>
                        </div>
                        <div class="match-score-box">
                            <div class="match-score-value" style="color:{sc_col};">{r['score']}%</div>
                            <div class="match-score-label">Compatibilità</div>
                        </div>
                    </div>
                    <div class="match-reasons">{expl_html}</div>
                </div>
                """, unsafe_allow_html=True)
            with mc2:
                fig = render_radar(r["sub_scores"])
                st.plotly_chart(fig, use_container_width=True, key=f"radar_corp_{i}")

    nx_divider()
    st.markdown("#### 📊 Distribuzione punteggi di match")
    all_scores = [r["score"] for r in results]
    bins = ["0–30", "31–50", "51–70", "71–85", "86–100"]
    counts = [
        sum(1 for s_ in all_scores if s_ <= 30),
        sum(1 for s_ in all_scores if 31 <= s_ <= 50),
        sum(1 for s_ in all_scores if 51 <= s_ <= 70),
        sum(1 for s_ in all_scores if 71 <= s_ <= 85),
        sum(1 for s_ in all_scores if 86 <= s_ <= 100),
    ]
    fig_bar = px.bar(x=bins, y=counts, labels={"x": "Fascia di punteggio", "y": "Numero match"}, color_discrete_sequence=[ACCENT])
    fig_bar.update_layout(showlegend=False, height=280, margin=dict(l=20, r=20, t=20, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          yaxis=dict(gridcolor="rgba(0,0,0,0.06)"))
    st.plotly_chart(fig_bar, use_container_width=True)


# ─── 8. FLUSSO DI CONTATTO ───────────────────────────────────

def section_contatto():
    nx_section("Flusso di Contatto",
               "Come funziona una richiesta di intro su NexFound.")

    st.markdown(f"""
    <div class="nx-info nx-info-accent">
        <p style="margin:0;">
            Una startup può inviare una <b>richiesta di contatto</b> a un investitore o un'azienda.
            NexFound facilita l'introduzione, genera un messaggio personalizzato e monitora il processo end-to-end.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 🔄 Pipeline di conversione")
    funnel_data = {
        "Fase": ["Profili visualizzati", "Match salvati", "Richieste inviate", "Intro accettate", "Call fissate"],
        "Numero": [4200, 1247, 583, 328, 156],
    }
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data["Fase"], x=funnel_data["Numero"],
        textinfo="value+percent initial",
        marker=dict(color=[PRIMARY, PRIMARY_LIGHT, ACCENT, ACCENT_DARK, CORAL]),
        connector=dict(line=dict(color=BORDER)),
    ))
    fig_funnel.update_layout(height=320, margin=dict(l=20, r=20, t=10, b=10),
                             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_funnel, use_container_width=True)

    nx_divider()
    st.markdown("#### ✉️ Simula una richiesta di contatto")

    rc1, rc2 = st.columns(2)
    with rc1:
        sel_startup = st.selectbox("🚀 Startup richiedente", df_startups["nome"].tolist(), key="contact_startup")
    with rc2:
        target_type = st.radio("Destinatario", ["Investitore", "Azienda"], horizontal=True, key="contact_target_type")

    target_list = df_investors["nome"].tolist() if target_type == "Investitore" else df_companies["nome"].tolist()
    sel_target = st.selectbox(f"🎯 Seleziona {target_type.lower()}", target_list, key="contact_target")

    s = df_startups[df_startups["nome"] == sel_startup].iloc[0]

    if target_type == "Investitore":
        inv = df_investors[df_investors["nome"] == sel_target].iloc[0]
        match_score, _, _ = compute_investor_match(s, inv)
        message = (
            f"Gentile team di {sel_target},\n\n"
            f"mi chiamo {s['founder']}, founder di {s['nome']}, una startup nel settore {s['settore']} "
            f"attualmente in fase di {s['stadio']}.\n\n"
            f"Stiamo cercando {s['obiettivo'].lower()} e il vostro focus su {', '.join(inv['settori_preferiti'][:2])} "
            f"ci sembra particolarmente in linea con il nostro progetto.\n\n"
            f"{s['descrizione']}\n\n"
            f"Mi piacerebbe avere l'opportunità di presentarvi il nostro progetto in una breve call.\n\n"
            f"Cordiali saluti,\n{s['founder']}\n{s['nome']}"
        )
    else:
        co = df_companies[df_companies["nome"] == sel_target].iloc[0]
        match_score, _, _ = compute_company_match(s, co)
        message = (
            f"Gentile team Innovazione di {sel_target},\n\n"
            f"mi chiamo {s['founder']}, founder di {s['nome']}, una startup nel settore {s['settore']} "
            f"attualmente in fase di {s['stadio']}.\n\n"
            f"Abbiamo notato il vostro interesse per l'innovazione nell'area {co['area_innovazione']} "
            f"e crediamo che la nostra soluzione possa creare valore per la vostra organizzazione.\n\n"
            f"{s['descrizione']}\n\n"
            f"Saremmo lieti di esplorare un'opportunità di {co['collaborazione'].lower()} insieme.\n\n"
            f"Cordiali saluti,\n{s['founder']}\n{s['nome']}"
        )

    with st.expander("📝 Anteprima messaggio generato", expanded=True):
        st.text_area("", message, height=200, disabled=True, key="preview_msg")
        sc_col = score_color(match_score)
        st.markdown(f"**Match score:** <span style='color:{sc_col}; font-weight:800; font-size:1.3rem;'>{match_score}%</span>", unsafe_allow_html=True)

    if st.button("📨 Invia richiesta di contatto", type="primary", key="send_contact"):
        st.session_state.contact_requests.append({
            "startup": sel_startup, "target": sel_target, "tipo": target_type,
            "score": match_score, "stato": "Inviata",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        })
        st.success(f"✅ Richiesta di contatto inviata a **{sel_target}**! La piattaforma gestirà l'introduzione.")

    if st.session_state.contact_requests:
        nx_divider()
        st.markdown("#### 📋 Richieste di contatto inviate")
        status_options = ["Inviata", "In revisione", "Accettata", "Call programmata"]
        status_cls = {"Inviata": "nx-status-sent", "In revisione": "nx-status-review",
                      "Accettata": "nx-status-accepted", "Call programmata": "nx-status-call"}

        for i, req in enumerate(st.session_state.contact_requests):
            r1, r2, r3, r4, r5 = st.columns([2, 2, 1, 2, 1])
            with r1:
                st.markdown(f"**{req['startup']}**")
            with r2:
                st.markdown(f"→ {req['target']}")
            with r3:
                st.markdown(f"<span style='font-weight:700; color:{score_color(req['score'])};'>{req['score']}%</span>", unsafe_allow_html=True)
            with r4:
                new_status = st.selectbox("Stato", status_options,
                                          index=status_options.index(req["stato"]),
                                          key=f"status_{i}", label_visibility="collapsed")
                st.session_state.contact_requests[i]["stato"] = new_status
            with r5:
                st.markdown(f'<span class="nx-status {status_cls.get(new_status, "")}">{new_status}</span>', unsafe_allow_html=True)


# ─── 9. FEED PIATTAFORMA ─────────────────────────────────────

def section_feed():
    nx_section("Feed Piattaforma",
               "Aggiornamenti in tempo reale dall'ecosistema NexFound.")

    for item in feed_items:
        st.markdown(f"""
        <div class="nx-feed">
            <div class="feed-icon">{item['icona']}</div>
            <div class="feed-content">
                <div class="feed-type">{item['tipo']}</div>
                <div class="feed-text">{item['testo']}</div>
            </div>
            <div class="feed-time">{item['tempo']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; color:{TEXT_MUTED}; font-size:0.82rem;">
        Questo feed mostra attività sintetiche a scopo dimostrativo.
        Nella piattaforma reale, ogni utente vedrebbe un feed personalizzato.
    </div>
    """, unsafe_allow_html=True)


# ─── 10. DASHBOARD KPI ───────────────────────────────────────

def section_dashboard():
    nx_section("Dashboard KPI",
               "Metriche di piattaforma per stakeholder e investitori.")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        nx_metric("Startup registrate", "247", "🚀", "+18 questo mese")
    with m2:
        nx_metric("Aziende attive", "68", "🏢", "+5 questo mese")
    with m3:
        nx_metric("Investitori attivi", "42", "💰", "+3 questo mese")
    with m4:
        nx_metric("Startup verificate", "112", "✅", "45% del totale")

    m5, m6, m7, m8 = st.columns(4)
    with m5:
        nx_metric("Match generati", "1.247", "🎯", "+12% vs mese prec.", accent=True)
    with m6:
        nx_metric("Richieste inviate", "583", "📨", "+8% vs mese prec.")
    with m7:
        nx_metric("Tasso risposta", "56%", "📊", "+3pp vs mese prec.")
    with m8:
        nx_metric("Call fissate", "156", "📞", "+11% vs mese prec.")

    st.markdown("<br>", unsafe_allow_html=True)

    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"), margin=dict(l=20, r=20, t=40, b=20),
    )

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuzione settori", "📈 Trend temporale", "🔄 Funnel conversione", "🌍 Geografia"])

    with tab1:
        sector_counts = df_startups["settore"].value_counts().reset_index()
        sector_counts.columns = ["Settore", "Startup"]
        fig = px.bar(sector_counts, x="Settore", y="Startup", color="Startup",
                     color_continuous_scale=["#e0f7f5", ACCENT, PRIMARY])
        fig.update_layout(height=380, showlegend=False, **CHART_LAYOUT,
                          yaxis=dict(gridcolor="rgba(0,0,0,0.06)"))
        st.plotly_chart(fig, use_container_width=True)

        cst1, cst2 = st.columns(2)
        with cst1:
            stage_counts = df_startups["stadio"].value_counts().reset_index()
            stage_counts.columns = ["Stadio", "Numero"]
            fig_stage = px.pie(stage_counts, values="Numero", names="Stadio", hole=0.45,
                               color_discrete_sequence=[PRIMARY, ACCENT, CORAL, AMBER])
            fig_stage.update_layout(height=330, title="Distribuzione per stadio", **CHART_LAYOUT)
            st.plotly_chart(fig_stage, use_container_width=True)
        with cst2:
            obj_counts = df_startups["obiettivo"].value_counts().reset_index()
            obj_counts.columns = ["Obiettivo", "Numero"]
            fig_obj = px.pie(obj_counts, values="Numero", names="Obiettivo", hole=0.45,
                             color_discrete_sequence=[ACCENT, PRIMARY, CORAL, AMBER, TEXT_MUTED])
            fig_obj.update_layout(height=330, title="Distribuzione per obiettivo", **CHART_LAYOUT)
            st.plotly_chart(fig_obj, use_container_width=True)

    with tab2:
        months = pd.date_range("2025-01-01", periods=15, freq="MS")
        np.random.seed(SEED)
        base_startups = np.cumsum(np.random.randint(8, 22, size=15)) + 50
        base_matches = np.cumsum(np.random.randint(30, 90, size=15)) + 100
        base_requests = np.cumsum(np.random.randint(15, 45, size=15)) + 40
        df_trend = pd.DataFrame({"Mese": months, "Startup registrate": base_startups,
                                  "Match generati": base_matches, "Richieste inviate": base_requests})
        fig_trend = go.Figure()
        for col_name, color, dash in [("Startup registrate", PRIMARY, "solid"),
                                       ("Match generati", ACCENT, "solid"),
                                       ("Richieste inviate", CORAL, "dot")]:
            fig_trend.add_trace(go.Scatter(
                x=df_trend["Mese"], y=df_trend[col_name], mode="lines+markers", name=col_name,
                line=dict(color=color, width=2.5, dash=dash), marker=dict(size=5),
            ))
        fig_trend.update_layout(height=400, legend=dict(orientation="h", y=-0.15),
                                yaxis_title="Cumulativo", **CHART_LAYOUT,
                                yaxis=dict(gridcolor="rgba(0,0,0,0.06)"))
        st.plotly_chart(fig_trend, use_container_width=True)

    with tab3:
        funnel_data = {
            "Fase": ["Profili visualizzati", "Match generati", "Match salvati", "Richieste inviate",
                     "Intro accettate", "Call fissate", "Deal / Pilot chiusi"],
            "Numero": [8400, 1247, 890, 583, 328, 156, 47],
        }
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data["Fase"], x=funnel_data["Numero"],
            textinfo="value+percent initial",
            marker=dict(color=[PRIMARY, PRIMARY_LIGHT, "#3a6a9f", ACCENT, ACCENT_DARK, "#ff8c8c", CORAL]),
            connector=dict(line=dict(color=BORDER)),
        ))
        fig_funnel.update_layout(height=400, **CHART_LAYOUT)
        st.plotly_chart(fig_funnel, use_container_width=True)

    with tab4:
        city_counts = df_startups["citta"].value_counts().reset_index()
        city_counts.columns = ["Città", "Startup"]
        fig_geo = px.bar(city_counts.head(10), x="Startup", y="Città", orientation="h",
                         color="Startup", color_continuous_scale=["#e0f7f5", ACCENT, PRIMARY])
        fig_geo.update_layout(height=380, showlegend=False, **CHART_LAYOUT,
                              yaxis=dict(autorange="reversed"),
                              xaxis=dict(gridcolor="rgba(0,0,0,0.06)"))
        st.plotly_chart(fig_geo, use_container_width=True)

        inv_type_counts = df_investors["tipo"].value_counts().reset_index()
        inv_type_counts.columns = ["Tipo", "Numero"]
        fig_inv_type = px.pie(inv_type_counts, values="Numero", names="Tipo", hole=0.45,
                              color_discrete_sequence=[PRIMARY, ACCENT, CORAL, AMBER])
        fig_inv_type.update_layout(height=330, title="Investitori per tipologia", **CHART_LAYOUT)
        st.plotly_chart(fig_inv_type, use_container_width=True)


# ─── 11. CONCLUSIONE ─────────────────────────────────────────

def section_conclusione():
    nx_section("NexFound — Il valore del prodotto",
               "Perché NexFound è la risposta giusta al momento giusto.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="nx-info nx-info-accent">
            <h4>🎯 Il problema che risolviamo</h4>
            <p>
                L'ecosistema innovazione italiano è frammentato. Startup, aziende e investitori
                operano in silos, affidandosi a contatti informali, eventi casuali e processi
                non strutturati. Il risultato: opportunità perse, tempo sprecato, valore non catturato.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="nx-info nx-info-accent">
            <h4>🔗 Perché NexFound è diverso</h4>
            <p>NexFound non è un social network generico né un semplice database.
            È una <b>piattaforma di matching intelligente</b> che:</p>
            <ul>
                <li>Struttura profili e metriche in modo standardizzato</li>
                <li>Genera match spiegabili su criteri oggettivi</li>
                <li>Gestisce il flusso di contatto da intro a collaborazione</li>
                <li>Crea un trust layer con verifica e badge</li>
                <li>Offre analytics per tutti gli attori dell'ecosistema</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="nx-info nx-info-accent">
            <h4>📊 Cosa dimostra questo MVP</h4>
            <p>Questa demo dimostra che il concept di NexFound è:</p>
            <ul>
                <li><b>Chiaro</b> — il valore per ogni attore è immediato</li>
                <li><b>Strutturato</b> — profili, matching e flussi sono ben definiti</li>
                <li><b>Presentabile</b> — l'esperienza è comprensibile e professionale</li>
                <li><b>Realizzabile</b> — le feature core sono implementabili con tecnologie standard</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="nx-info nx-info-accent">
            <h4>🚀 Prossimi passi</h4>
            <ol>
                <li>Validazione con 20 startup e 10 corporate pilota</li>
                <li>Sviluppo MVP web con autenticazione e profili reali</li>
                <li>Integrazione di scoring ML per match più sofisticati</li>
                <li>Partnership con acceleratori e incubatori italiani</li>
                <li>Lancio beta su mercato italiano, poi espansione europea</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nx-cta">
        <h2>NexFound — Dove l'innovazione incontra l'opportunità</h2>
        <p>Connetti startup, aziende e investitori in modo intelligente.<br>
        Un ecosistema. Una piattaforma. Infinite possibilità.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        nx_metric("Startup nel network", "247+", "🚀", "+74% anno su anno", accent=True)
    with mc2:
        nx_metric("Match rate medio", "73%", "🎯", "+8pp vs Q1")
    with mc3:
        nx_metric("Tempo medio primo contatto", "4.2 gg", "⚡", "-1.3gg vs Q1")


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding: 1.2rem 0 0.8rem 0;">
            <div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.04em;">
                🔗 <span style="color:{ACCENT};">NexFound</span>
            </div>
            <div style="font-size:0.72rem; color:rgba(200,212,230,0.5); letter-spacing:0.08em; text-transform:uppercase; margin-top:2px;">
                Demo Interattiva v2.0
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        pagina = st.radio(
            "Navigazione",
            [
                "🏠  Home",
                "⚡  Problema di Mercato",
                "🔗  Ecosistema",
                "🚀  Directory Startup",
                "🏢  Directory Aziende",
                "💰  Directory Investitori",
                "🎯  Matching Intelligente",
                "📨  Flusso di Contatto",
                "📰  Feed Piattaforma",
                "📊  Dashboard KPI",
                "✨  Conclusione",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:0.7rem; color:rgba(200,212,230,0.35); text-align:center; line-height:1.6;">
            Demo con dati sintetici<br>
            Streamlit · Plotly · Python<br>
            © 2026 NexFound
        </div>
        """, unsafe_allow_html=True)

    sections = {
        "🏠  Home": section_home,
        "⚡  Problema di Mercato": section_problema,
        "🔗  Ecosistema": section_ecosistema,
        "🚀  Directory Startup": section_startups,
        "🏢  Directory Aziende": section_aziende,
        "💰  Directory Investitori": section_investitori,
        "🎯  Matching Intelligente": section_matching,
        "📨  Flusso di Contatto": section_contatto,
        "📰  Feed Piattaforma": section_feed,
        "📊  Dashboard KPI": section_dashboard,
        "✨  Conclusione": section_conclusione,
    }

    sections[pagina]()


if __name__ == "__main__":
    main()
