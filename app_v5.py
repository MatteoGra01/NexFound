"""
NexFound V0 — B2B Social Platform connecting Startups, Investors & Corporates
Single-file Streamlit app with mock data, premium UI, and full navigation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# CONFIGURATION & THEME
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="NexFound",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#1B2A4A",
    "primary_light": "#2A4170",
    "accent": "#2EC4B6",
    "accent_dark": "#1A9E92",
    "coral": "#FF6B6B",
    "amber": "#FFB347",
    "light_bg": "#F7F8FB",
    "card_bg": "#FFFFFF",
    "text_primary": "#1B2A4A",
    "text_secondary": "#5B657A",
    "border": "#E6EAF2",
    "success": "#27AE60",
}

def inject_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global */
    .stApp { background-color: #F7F8FB; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #1B2A4A 0%, #2A4170 100%); }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] .stRadio label span { color: #CBD5E1 !important; }
    section[data-testid="stSidebar"] .stRadio label span:hover { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
    
    /* Hide default streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }
    
    /* Cards */
    .nf-card {
        background: #FFFFFF; border: 1px solid #E6EAF2; border-radius: 14px;
        padding: 24px; margin-bottom: 16px;
        transition: box-shadow 0.2s, transform 0.15s;
    }
    .nf-card:hover { box-shadow: 0 8px 25px rgba(27,42,74,0.08); transform: translateY(-1px); }
    
    .nf-card-feed {
        background: #FFFFFF; border: 1px solid #E6EAF2; border-radius: 14px;
        padding: 20px 24px; margin-bottom: 14px;
    }
    
    /* Badges */
    .nf-badge {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600; margin-right: 6px; margin-bottom: 4px;
    }
    .nf-badge-accent { background: rgba(46,196,182,0.12); color: #1A9E92; }
    .nf-badge-coral { background: rgba(255,107,107,0.12); color: #E55555; }
    .nf-badge-amber { background: rgba(255,179,71,0.12); color: #CC8F39; }
    .nf-badge-primary { background: rgba(27,42,74,0.08); color: #1B2A4A; }
    .nf-badge-success { background: rgba(39,174,96,0.12); color: #1E8449; }
    
    /* Match score */
    .nf-match {
        display: inline-flex; align-items: center; gap: 4px;
        background: linear-gradient(135deg, #2EC4B6 0%, #1A9E92 100%);
        color: white; padding: 4px 12px; border-radius: 20px;
        font-size: 13px; font-weight: 700;
    }
    
    /* Section titles */
    .nf-section-title {
        font-size: 22px; font-weight: 700; color: #1B2A4A;
        margin-bottom: 4px; letter-spacing: -0.3px;
    }
    .nf-section-subtitle { font-size: 14px; color: #5B657A; margin-bottom: 20px; }
    
    /* Profile header */
    .nf-profile-header {
        background: linear-gradient(135deg, #1B2A4A 0%, #2A4170 100%);
        border-radius: 16px; padding: 32px; color: white; margin-bottom: 20px;
    }
    .nf-profile-name { font-size: 28px; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
    .nf-profile-tagline { font-size: 15px; opacity: 0.85; margin-top: 4px; }
    
    /* KPI */
    .nf-kpi {
        background: #FFFFFF; border: 1px solid #E6EAF2; border-radius: 12px;
        padding: 18px 20px; text-align: center;
    }
    .nf-kpi-value { font-size: 28px; font-weight: 800; color: #1B2A4A; }
    .nf-kpi-label { font-size: 12px; color: #5B657A; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Buttons */
    .nf-btn {
        display: inline-block; padding: 8px 20px; border-radius: 8px;
        font-size: 13px; font-weight: 600; cursor: pointer; text-decoration: none;
        border: none; transition: all 0.2s;
    }
    .nf-btn-primary { background: #2EC4B6; color: white; }
    .nf-btn-outline { background: transparent; border: 1.5px solid #E6EAF2; color: #1B2A4A; }
    
    /* Message bubble */
    .nf-msg { padding: 12px 16px; border-radius: 12px; margin-bottom: 8px; max-width: 80%; }
    .nf-msg-them { background: #F0F2F5; color: #1B2A4A; }
    .nf-msg-me { background: #2EC4B6; color: white; margin-left: auto; text-align: right; }
    
    /* Landing */
    .nf-hero {
        text-align: center; padding: 60px 20px 40px;
        background: linear-gradient(180deg, #1B2A4A 0%, #2A4170 60%, #F7F8FB 100%);
        border-radius: 0 0 30px 30px; color: white; margin: -1rem -1rem 30px;
    }
    .nf-hero h1 { font-size: 48px; font-weight: 800; letter-spacing: -1px; margin-bottom: 12px; }
    .nf-hero p { font-size: 18px; opacity: 0.85; max-width: 600px; margin: 0 auto 30px; }
    
    /* Tabs override */
    .stTabs [data-baseweb="tab-list"] { gap: 0px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 24px; font-weight: 600; color: #5B657A;
    }
    .stTabs [aria-selected="true"] { color: #1B2A4A !important; border-bottom-color: #2EC4B6 !important; }
    
    /* Opportunity card */
    .nf-opp-card {
        background: #FFFFFF; border-left: 4px solid #2EC4B6;
        border-radius: 0 14px 14px 0; padding: 20px 24px;
        margin-bottom: 14px; border-top: 1px solid #E6EAF2;
        border-right: 1px solid #E6EAF2; border-bottom: 1px solid #E6EAF2;
    }
    
    /* Conversation list item */
    .nf-conv {
        padding: 14px 16px; border-bottom: 1px solid #E6EAF2;
        cursor: pointer; transition: background 0.15s;
    }
    .nf-conv:hover { background: #F7F8FB; }
    .nf-conv-active { background: rgba(46,196,182,0.06); border-left: 3px solid #2EC4B6; }
    
    /* Scrollable area */
    .nf-scroll { max-height: 500px; overflow-y: auto; }
    
    /* Sidebar nav item */
    .nav-item { padding: 8px 0; font-size: 15px; }
    
    /* Landing cards */
    .nf-feature-card {
        background: rgba(255,255,255,0.06); backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 14px;
        padding: 24px; text-align: center; color: white;
    }
    </style>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────────────

RNG = random.Random(42)
np.random.seed(42)

SECTORS = ["AI & Machine Learning", "FinTech", "HealthTech", "CleanTech", "CyberSecurity",
           "HR Tech", "Supply Chain", "Industry 4.0", "FoodTech", "LegalTech",
           "Mobility", "Energy", "DeepTech", "SaaS B2B", "EdTech", "PropTech",
           "InsurTech", "BioTech", "AgriTech", "SpaceTech"]

STAGES = ["Pre-Seed", "Seed", "Series A", "Series B", "Growth"]
CITIES_EU = ["Milano", "Roma", "Berlino", "Parigi", "Amsterdam", "Barcellona",
             "Londra", "Lisbona", "Monaco", "Stoccolma", "Zurigo", "Vienna",
             "Dublino", "Helsinki", "Tallinn", "Bruxelles"]
BIZ_MODELS = ["SaaS", "Marketplace", "Platform", "API-first", "Hardware+Software", "Subscription", "Usage-based"]
INVESTOR_TYPES = ["VC", "Angel", "CVC", "Family Office", "Accelerator"]


def generate_startups(n=24):
    names = ["Aethon AI", "BrightFlow", "CarbonZero", "DataPulse", "EcoSynth", "FinBridge",
             "GreenVolt", "HealthSync", "InnoWave", "JuriBot", "KineticAI", "LogiChain",
             "MediScan", "NeuralPath", "OptiRoute", "PayLoop", "QuantaRisk", "RoboFarm",
             "SecureNet", "TerraTrack", "UrbanFlow", "VoxHealth", "WattGrid", "ZenHR"]
    taglines = [
        "AI-powered predictive maintenance for industrial assets",
        "Workflow automation platform for SMEs",
        "Carbon footprint tracking and offset marketplace",
        "Real-time data analytics for supply chain visibility",
        "Synthetic biology for sustainable materials",
        "Open banking infrastructure for emerging markets",
        "Smart grid optimization using reinforcement learning",
        "Remote patient monitoring with AI diagnostics",
        "Innovation management SaaS for enterprises",
        "AI legal assistant for contract analysis",
        "Computer vision for quality control in manufacturing",
        "Blockchain-based logistics and traceability",
        "AI-powered medical imaging analysis",
        "Neuromorphic computing for edge AI applications",
        "Route optimization platform for last-mile delivery",
        "Embedded finance APIs for B2B payments",
        "Quantum-enhanced risk modeling for finance",
        "Autonomous farming robotics and precision agriculture",
        "Zero-trust cybersecurity mesh for distributed teams",
        "Satellite-based environmental monitoring platform",
        "Smart mobility platform for urban transportation",
        "Voice AI health screening and triage",
        "Energy storage management and trading platform",
        "AI-driven employee experience and retention platform",
    ]
    startups = []
    for i in range(min(n, len(names))):
        sector = SECTORS[i % len(SECTORS)]
        stage = RNG.choice(STAGES[:4])
        city = RNG.choice(CITIES_EU)
        revenue = RNG.choice(["€0-50K MRR", "€50-200K MRR", "€200K-1M MRR", "€1-5M ARR", "Pre-revenue"])
        team_size = RNG.randint(3, 60)
        founded = RNG.randint(2019, 2025)
        raised = RNG.choice(["€150K", "€500K", "€1.2M", "€2.5M", "€4M", "€8M", "€12M", "Bootstrapped"])
        highlights = RNG.sample([
            "YC W24 alumni", "30% MoM growth", "Enterprise pilot with Fortune 500",
            "Patent pending", "200+ B2B customers", "SOC2 certified",
            "Top 10 EU startup 2025", "Microsoft for Startups member",
            "Named in Gartner Cool Vendors", "Revenue positive",
            "20x YoY growth", "Strategic partnership with AWS",
            "Government grant recipient", "Impact-certified B Corp",
        ], k=RNG.randint(1, 3))
        startups.append({
            "id": f"s{i}", "name": names[i], "tagline": taglines[i],
            "sector": sector, "stage": stage, "city": city, "country": "EU",
            "revenue": revenue, "team_size": team_size, "founded": founded,
            "raised": raised, "biz_model": RNG.choice(BIZ_MODELS),
            "highlights": highlights, "type": "Startup",
            "looking_for": RNG.sample(["Investment", "Corporate Pilots", "Partnerships", "Customers", "Advisors"], k=2),
        })
    return startups


def generate_investors(n=14):
    names = ["Northstar Ventures", "Alpine Capital", "Deep Blue VC", "Europa Partners",
             "Fortuna Angels", "Green Horizon Fund", "Impact Ventures EU",
             "Kinetic Capital", "Luminar Partners", "MedTech Angels",
             "Nova Growth Fund", "Orbit Ventures", "Prism Capital", "Quantum Investors"]
    theses = [
        "Early-stage B2B SaaS with strong PLG motion",
        "Climate and sustainability solutions across sectors",
        "Deep tech and frontier technology bets",
        "Pan-European fintech and embedded finance",
        "Angel syndicate focused on Italian tech ecosystem",
        "Sustainability-first fund investing in Series A cleantech",
        "Impact investing across health, education, and climate",
        "Seed to Series A in enterprise AI and automation",
        "Growth equity in European SaaS champions",
        "Specialized in digital health and medtech innovation",
        "Series A/B in high-growth European scale-ups",
        "Space tech, satellite data, and earth observation",
        "Pre-seed to seed in underrepresented founders",
        "Quantum computing, advanced materials, and deep science",
    ]
    investors = []
    for i in range(min(n, len(names))):
        focus = RNG.sample(SECTORS, k=RNG.randint(2, 5))
        stages_pref = RNG.sample(STAGES[:3], k=RNG.randint(1, 2))
        ticket = RNG.choice(["€25-100K", "€100-500K", "€500K-2M", "€2-5M", "€5-15M", "€10-30M"])
        portfolio_size = RNG.randint(8, 80)
        investors.append({
            "id": f"i{i}", "name": names[i], "thesis": theses[i],
            "type_inv": RNG.choice(INVESTOR_TYPES), "focus_sectors": focus,
            "stages_pref": stages_pref, "ticket": ticket,
            "city": RNG.choice(CITIES_EU), "portfolio_size": portfolio_size,
            "portfolio_highlights": RNG.sample(
                ["Aethon AI", "BrightFlow", "DataPulse", "EcoSynth", "FinBridge", "GreenVolt", "MediScan", "SecureNet"],
                k=min(3, RNG.randint(1, 4))
            ),
            "type": "Investor",
            "looking_for": ["Deal flow", "Co-investment", "Startup introductions"],
        })
    return investors


def generate_corporates(n=12):
    names = ["Enel Innovation", "UniCredit Ventures", "Leonardo Tech Hub",
             "Generali Ignite", "Poste Italiane Innovation", "Siemens Energy Lab",
             "BMW i Ventures EU", "Nestlé R&D Connect", "Bosch Industry 4.0",
             "SAP.iO Foundry", "Roche HealthTech Bridge", "Airbus BizLab"]
    descs = [
        "Scouting startups for smart grid, renewables, and energy efficiency",
        "Innovation arm focused on fintech, regtech, and digital banking",
        "Defense & aerospace innovation hub seeking AI, cybersecurity, and autonomy",
        "InsurTech and health innovation accelerator",
        "Digital transformation and logistics innovation",
        "Industrial IoT, digital twins, and decarbonization tech",
        "Mobility, autonomy, and sustainable transport innovation",
        "FoodTech, AgriTech, and sustainable packaging solutions",
        "Manufacturing AI, robotics, and predictive maintenance",
        "Enterprise SaaS, AI, and process automation",
        "Digital health, diagnostics, and personalized medicine",
        "Urban air mobility, drones, and aerospace innovation",
    ]
    corporates = []
    for i in range(min(n, len(names))):
        corporates.append({
            "id": f"c{i}", "name": names[i], "description": descs[i],
            "industry": RNG.choice(["Energy", "Finance", "Aerospace & Defense", "Insurance",
                                     "Logistics", "Industrial", "Automotive", "Food & Beverage",
                                     "Manufacturing", "Software", "Healthcare", "Aerospace"]),
            "size": RNG.choice(["1,000-5,000", "5,000-20,000", "20,000-100,000", "100,000+"]),
            "city": RNG.choice(CITIES_EU[:6]),
            "innovation_areas": RNG.sample(SECTORS, k=RNG.randint(2, 4)),
            "procurement_ready": RNG.choice([True, True, False]),
            "active_challenges": RNG.randint(1, 5),
            "type": "Corporate",
            "looking_for": ["Startup pilots", "Technology partnerships", "Innovation scouting"],
        })
    return corporates


def generate_feed(startups, investors, corporates):
    """Generate 35+ realistic feed items."""
    feed = []
    templates_startup = [
        ("{name} ha chiuso un round {stage} da {amount}", "funding", "coral"),
        ("{name} ha raggiunto {metric} — crescita impressionante!", "traction", "accent"),
        ("{name} ha lanciato un nuovo prodotto nel settore {sector}", "product", "primary"),
        ("{name} è entrata nel programma {program}", "milestone", "amber"),
        ("{name} sta cercando un {role} — il team cresce!", "hiring", "primary"),
        ("{name} ha firmato una partnership con {partner}", "partnership", "accent"),
    ]
    templates_investor = [
        ("{name} ha pubblicato la nuova investment thesis per il 2026", "thesis", "primary"),
        ("{name} è alla ricerca di startup in {sector}", "scouting", "accent"),
        ("{name} ha investito in una nuova startup {sector}", "investment", "coral"),
        ("{name}: 'Il settore {sector} sarà il tema dominante del 2026'", "insight", "amber"),
    ]
    templates_corporate = [
        ("{name} ha lanciato una nuova Innovation Challenge in {sector}", "challenge", "coral"),
        ("{name} cerca startup per un pilot nel settore {sector}", "pilot", "accent"),
        ("{name} ha aperto una call for startups — deadline tra 30 giorni", "open_call", "amber"),
        ("{name} annuncia un nuovo programma di open innovation", "program", "primary"),
    ]
    amounts = ["€500K", "€1.2M", "€2.5M", "€4M", "€8M"]
    metrics = ["1.000 utenti B2B", "€500K ARR", "50 enterprise clients", "30% MoM growth", "100K API calls/day"]
    programs = ["Techstars", "YC", "EIT Digital", "Station F", "Microsoft for Startups"]
    roles = ["CTO", "VP Sales", "Head of Engineering", "Product Lead"]
    partners = ["AWS", "Google Cloud", "Microsoft", "SAP", "Salesforce", "Stripe"]

    for s in startups[:18]:
        tmpl, cat, color = RNG.choice(templates_startup)
        text = tmpl.format(
            name=s["name"], stage=s["stage"], amount=RNG.choice(amounts),
            sector=s["sector"], metric=RNG.choice(metrics),
            program=RNG.choice(programs), role=RNG.choice(roles),
            partner=RNG.choice(partners),
        )
        feed.append({
            "author": s["name"], "author_type": "Startup", "sector": s["sector"],
            "text": text, "category": cat, "color": color,
            "time_ago": f"{RNG.randint(1, 72)}h fa", "likes": RNG.randint(5, 120),
            "comments": RNG.randint(0, 25), "id": f"f{len(feed)}",
        })

    for inv in investors[:10]:
        tmpl, cat, color = RNG.choice(templates_investor)
        text = tmpl.format(name=inv["name"], sector=RNG.choice(inv["focus_sectors"]))
        feed.append({
            "author": inv["name"], "author_type": "Investor", "sector": inv["focus_sectors"][0],
            "text": text, "category": cat, "color": color,
            "time_ago": f"{RNG.randint(1, 48)}h fa", "likes": RNG.randint(10, 200),
            "comments": RNG.randint(2, 40), "id": f"f{len(feed)}",
        })

    for c in corporates[:10]:
        tmpl, cat, color = RNG.choice(templates_corporate)
        text = tmpl.format(name=c["name"], sector=RNG.choice(c["innovation_areas"]))
        feed.append({
            "author": c["name"], "author_type": "Corporate", "sector": c["innovation_areas"][0],
            "text": text, "category": cat, "color": color,
            "time_ago": f"{RNG.randint(1, 96)}h fa", "likes": RNG.randint(8, 150),
            "comments": RNG.randint(1, 30), "id": f"f{len(feed)}",
        })

    RNG.shuffle(feed)
    return feed


def generate_opportunities(corporates, investors):
    opps = []
    corp_opps = [
        ("Smart Grid AI Challenge", "Cerchiamo startup che usano AI/ML per ottimizzare la gestione delle reti elettriche intelligenti. Budget pilota fino a €200K.", "Challenge", "High"),
        ("Digital Identity & KYC Innovation", "Soluzioni innovative per KYC, AML e verifica dell'identità digitale per il settore bancario.", "Pilot", "Medium"),
        ("Autonomous Systems for Inspection", "Droni e robotica autonoma per ispezione infrastrutture critiche — cercasi partner tecnologico.", "Partnership", "High"),
        ("Customer Experience AI", "AI per personalizzazione e automazione della customer experience in ambito assicurativo.", "Pilot", "Medium"),
        ("Last-Mile Logistics Optimization", "Soluzioni per ottimizzare la logistica dell'ultimo miglio con focus su sostenibilità.", "Challenge", "High"),
        ("Predictive Maintenance for Turbines", "Machine learning per manutenzione predittiva di turbine eoliche e asset industriali.", "Partnership", "Critical"),
        ("Sustainable Packaging Innovation", "Soluzioni di packaging sostenibile, biodegradabile o riutilizzabile per il food & beverage.", "Open Call", "Medium"),
        ("Factory of the Future", "Digital twin, computer vision e IoT per la fabbrica intelligente del futuro.", "Challenge", "High"),
        ("Enterprise Workflow Automation", "AI agents e automazione intelligente per processi enterprise complessi.", "Pilot", "Medium"),
        ("Precision Diagnostics Platform", "Piattaforme di diagnostica avanzata con AI per screening rapido e medicina personalizzata.", "Partnership", "High"),
        ("Urban Air Mobility Ecosystem", "Startup che lavorano su eVTOL, droni cargo, e infrastruttura vertiport.", "Open Call", "Medium"),
        ("Cybersecurity Mesh Architecture", "Soluzioni zero-trust e cybersecurity mesh per ambienti enterprise distribuiti.", "Pilot", "Critical"),
    ]
    for i, (title, desc, opp_type, priority) in enumerate(corp_opps):
        c = corporates[i % len(corporates)]
        opps.append({
            "id": f"o{i}", "title": title, "description": desc,
            "owner": c["name"], "owner_type": "Corporate", "type": opp_type,
            "sector": RNG.choice(c["innovation_areas"]),
            "priority": priority, "deadline": f"{RNG.randint(15, 90)} giorni",
            "ideal_fit": RNG.choice(["Pre-Seed / Seed con MVP", "Seed / Series A con traction", "Series A+ con revenue", "Qualsiasi stage con tech validata"]),
            "budget": RNG.choice(["€50-100K", "€100-200K", "€200-500K", "Da definire"]),
        })
    # Investor theses as opportunities
    for j, inv in enumerate(investors[:5]):
        opps.append({
            "id": f"o{len(opps)}", "title": f"Active Thesis: {inv['focus_sectors'][0]}",
            "description": inv["thesis"] + f" Ticket: {inv['ticket']}. Attivamente alla ricerca di deal flow qualificato.",
            "owner": inv["name"], "owner_type": "Investor", "type": "Investment Thesis",
            "sector": inv["focus_sectors"][0], "priority": "Active",
            "deadline": "Ongoing", "ideal_fit": " / ".join(inv["stages_pref"]),
            "budget": inv["ticket"],
        })
    return opps


def generate_conversations():
    return [
        {"id": "conv1", "with": "Northstar Ventures", "with_type": "Investor", "status": "Active",
         "preview": "Ottimo, il vostro deck è molto interessante. Fissiamo una call?",
         "unread": 2, "time": "2h fa",
         "messages": [
             {"from": "me", "text": "Ciao! Siamo Aethon AI, lavoriamo su predictive maintenance con AI. Saremmo interessati a un incontro.", "time": "Ieri 14:30"},
             {"from": "them", "text": "Ciao! Ho visto il vostro profilo, il settore ci interessa molto. Potete inviarmi il deck?", "time": "Ieri 16:45"},
             {"from": "me", "text": "Assolutamente, ecco il link al deck aggiornato. Abbiamo chiuso 3 enterprise pilots nell'ultimo quarter.", "time": "Oggi 09:15"},
             {"from": "them", "text": "Ottimo, il vostro deck è molto interessante. Fissiamo una call?", "time": "Oggi 11:30"},
         ]},
        {"id": "conv2", "with": "Enel Innovation", "with_type": "Corporate", "status": "Intro Pending",
         "preview": "Richiesta di intro inviata tramite NexFound",
         "unread": 0, "time": "1g fa",
         "messages": [
             {"from": "system", "text": "Intro request inviata a Enel Innovation. In attesa di accettazione.", "time": "1g fa"},
         ]},
        {"id": "conv3", "with": "Alpine Capital", "with_type": "Investor", "status": "Active",
         "preview": "Vi aggiorno: abbiamo approvato l'investimento nel nostro comitato.",
         "unread": 1, "time": "3h fa",
         "messages": [
             {"from": "them", "text": "Seguito al nostro incontro — il team ha analizzato i vostri dati di traction.", "time": "2g fa"},
             {"from": "me", "text": "Perfetto, siamo disponibili per qualsiasi approfondimento.", "time": "1g fa"},
             {"from": "them", "text": "Vi aggiorno: abbiamo approvato l'investimento nel nostro comitato.", "time": "3h fa"},
         ]},
        {"id": "conv4", "with": "SAP.iO Foundry", "with_type": "Corporate", "status": "Active",
         "preview": "Il pilot può partire il Q2. Vi mando i dettagli del PoC.",
         "unread": 0, "time": "5h fa",
         "messages": [
             {"from": "them", "text": "Abbiamo rivisto la vostra proposta per il nostro programma di innovazione.", "time": "3g fa"},
             {"from": "me", "text": "Grazie! Siamo entusiasti della possibilità. Quando possiamo iniziare il pilot?", "time": "2g fa"},
             {"from": "them", "text": "Il pilot può partire il Q2. Vi mando i dettagli del PoC.", "time": "5h fa"},
         ]},
        {"id": "conv5", "with": "Deep Blue VC", "with_type": "Investor", "status": "Intro Accepted",
         "preview": "Intro accettata! Potete procedere con la conversazione.",
         "unread": 1, "time": "6h fa",
         "messages": [
             {"from": "system", "text": "Intro accettata da Deep Blue VC. Potete avviare la conversazione.", "time": "6h fa"},
         ]},
        {"id": "conv6", "with": "BrightFlow", "with_type": "Startup", "status": "Active",
         "preview": "Potremmo esplorare un'integrazione tra le nostre piattaforme.",
         "unread": 0, "time": "1g fa",
         "messages": [
             {"from": "them", "text": "Ho visto che lavorate su un settore complementare. Vi andrebbe di esplorare una collaborazione?", "time": "2g fa"},
             {"from": "me", "text": "Certo! Le nostre tecnologie potrebbero essere molto sinergiche.", "time": "1g fa"},
             {"from": "them", "text": "Potremmo esplorare un'integrazione tra le nostre piattaforme.", "time": "1g fa"},
         ]},
        {"id": "conv7", "with": "Generali Ignite", "with_type": "Corporate", "status": "Active",
         "preview": "Vi confermiamo la partecipazione al nostro batch di innovazione Q3.",
         "unread": 3, "time": "30min fa",
         "messages": [
             {"from": "them", "text": "Abbiamo selezionato la vostra soluzione per il nostro programma.", "time": "1g fa"},
             {"from": "me", "text": "Fantastico! Quali sono i prossimi step?", "time": "12h fa"},
             {"from": "them", "text": "Vi confermiamo la partecipazione al nostro batch di innovazione Q3.", "time": "30min fa"},
         ]},
        {"id": "conv8", "with": "GreenVolt", "with_type": "Startup", "status": "Active",
         "preview": "Abbiamo un cliente in comune, potrebbe essere un buon punto di partenza.",
         "unread": 0, "time": "2g fa",
         "messages": [
             {"from": "me", "text": "Ho visto il vostro profilo — lavorate anche con utility europee?", "time": "3g fa"},
             {"from": "them", "text": "Sì, abbiamo 4 utility come clienti. E voi?", "time": "2g fa"},
             {"from": "me", "text": "Anche noi! Potremmo fare cross-selling.", "time": "2g fa"},
             {"from": "them", "text": "Abbiamo un cliente in comune, potrebbe essere un buon punto di partenza.", "time": "2g fa"},
         ]},
        {"id": "conv9", "with": "Leonardo Tech Hub", "with_type": "Corporate", "status": "Intro Pending",
         "preview": "Richiesta di intro in attesa di risposta.",
         "unread": 0, "time": "4g fa",
         "messages": [
             {"from": "system", "text": "Intro request inviata a Leonardo Tech Hub. In attesa di accettazione.", "time": "4g fa"},
         ]},
        {"id": "conv10", "with": "Europa Partners", "with_type": "Investor", "status": "Active",
         "preview": "Possiamo fare un follow-up call la prossima settimana?",
         "unread": 0, "time": "1g fa",
         "messages": [
             {"from": "them", "text": "Ho rivisto i vostri numeri. La growth story è compelling.", "time": "3g fa"},
             {"from": "me", "text": "Grazie! Siamo disponibili per un deep dive sui financials.", "time": "2g fa"},
             {"from": "them", "text": "Possiamo fare un follow-up call la prossima settimana?", "time": "1g fa"},
         ]},
    ]


# ─────────────────────────────────────────────
# INIT SESSION STATE
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "page": "landing",
        "role": None,
        "logged_in": False,
        "saved_profiles": [],
        "saved_opps": [],
        "connections": ["Northstar Ventures", "Alpine Capital", "SAP.iO Foundry", "BrightFlow"],
        "selected_profile": None,
        "selected_conv": "conv1",
        "feed_filter": "Tutti",
        "discover_type": "Startup",
        "discover_sector": "Tutti",
        "discover_stage": "Tutti",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# Load data once
if "startups" not in st.session_state:
    st.session_state.startups = generate_startups()
    st.session_state.investors = generate_investors()
    st.session_state.corporates = generate_corporates()
    st.session_state.feed = generate_feed(st.session_state.startups, st.session_state.investors, st.session_state.corporates)
    st.session_state.opportunities = generate_opportunities(st.session_state.corporates, st.session_state.investors)
    st.session_state.conversations = generate_conversations()


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def badge(text, style="accent"):
    return f'<span class="nf-badge nf-badge-{style}">{text}</span>'

def match_score(entity, role):
    """Deterministic pseudo-random match score based on entity name and role."""
    h = int(hashlib.md5(f"{entity.get('name','')}{role}".encode()).hexdigest()[:8], 16)
    return 65 + (h % 31)  # 65-95

def nav_to(page):
    st.session_state.page = page

def toggle_save_profile(name):
    if name in st.session_state.saved_profiles:
        st.session_state.saved_profiles.remove(name)
    else:
        st.session_state.saved_profiles.append(name)

def toggle_save_opp(oid):
    if oid in st.session_state.saved_opps:
        st.session_state.saved_opps.remove(oid)
    else:
        st.session_state.saved_opps.append(oid)

def author_icon(author_type):
    icons = {"Startup": "🚀", "Investor": "💎", "Corporate": "🏢"}
    return icons.get(author_type, "👤")

def priority_badge(priority):
    m = {"Critical": "coral", "High": "coral", "Medium": "amber", "Active": "accent", "Low": "primary"}
    return badge(priority, m.get(priority, "primary"))

def type_badge(t):
    m = {"Challenge": "coral", "Pilot": "accent", "Partnership": "primary", "Open Call": "amber", "Investment Thesis": "success"}
    return badge(t, m.get(t, "primary"))

def status_badge(status):
    m = {"Active": "accent", "Intro Pending": "amber", "Intro Accepted": "success"}
    return badge(status, m.get(status, "primary"))

def section_title(title, subtitle=""):
    st.markdown(f'<div class="nf-section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="nf-section-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def kpi_card(value, label):
    st.markdown(f"""<div class="nf-kpi">
        <div class="nf-kpi-value">{value}</div>
        <div class="nf-kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def render_entity_card(entity, show_match=True, compact=False):
    """Render a card for any entity type."""
    name = entity["name"]
    etype = entity["type"]
    icon = author_icon(etype)
    ms = match_score(entity, st.session_state.role) if show_match else 0
    saved = name in st.session_state.saved_profiles
    save_icon = "★" if saved else "☆"

    if etype == "Startup":
        sub = f'{entity["sector"]} · {entity["stage"]} · {entity["city"]}'
        detail = entity["tagline"]
        extra_badges = badge(entity["stage"], "primary") + badge(entity["sector"], "accent")
        if "YC W24 alumni" in entity.get("highlights", []):
            extra_badges += badge("YC Alumni", "coral")
    elif etype == "Investor":
        sub = f'{entity["type_inv"]} · {entity["ticket"]} · {entity["city"]}'
        detail = entity["thesis"]
        extra_badges = badge(entity["type_inv"], "primary") + badge(entity["ticket"], "accent")
    else:
        sub = f'{entity["industry"]} · {entity["size"]} employees · {entity["city"]}'
        detail = entity["description"]
        extra_badges = badge(entity["industry"], "primary")
        if entity.get("procurement_ready"):
            extra_badges += badge("Procurement Ready", "success")

    match_html = f'<span class="nf-match">⚡ {ms}% match</span>' if show_match and ms > 0 else ""

    st.markdown(f"""<div class="nf-card">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div style="font-size:11px; color:#5B657A; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">{icon} {etype}</div>
                <div style="font-size:18px; font-weight:700; color:#1B2A4A;">{name}</div>
                <div style="font-size:13px; color:#5B657A; margin:2px 0 8px;">{sub}</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                {match_html}
            </div>
        </div>
        <div style="font-size:14px; color:#3A4560; margin-bottom:10px; line-height:1.5;">{detail}</div>
        <div>{extra_badges}</div>
    </div>""", unsafe_allow_html=True)

    # Action buttons
    if not compact:
        cols = st.columns([1,1,1,3])
        with cols[0]:
            if st.button(f"{'★ Saved' if saved else '☆ Save'}", key=f"save_{name}", type="secondary"):
                toggle_save_profile(name)
                st.rerun()
        with cols[1]:
            if st.button("👤 Profile", key=f"prof_{name}"):
                st.session_state.selected_profile = entity
                nav_to("profile_detail")
                st.rerun()
        with cols[2]:
            if st.button("💬 Connect", key=f"conn_{name}"):
                if name not in st.session_state.connections:
                    st.session_state.connections.append(name)
                st.toast(f"Richiesta di connessione inviata a {name}!")


# ─────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────

def render_landing():
    st.markdown("""<div class="nf-hero">
        <div style="font-size:14px; font-weight:600; letter-spacing:2px; opacity:0.7; margin-bottom:8px;">◆ NEXFOUND</div>
        <h1>Where Innovation<br>Meets Opportunity</h1>
        <p>La piattaforma B2B che connette startup, investitori e corporate.<br>
        Scopri opportunità, crea connessioni di valore, accelera la crescita.</p>
    </div>""", unsafe_allow_html=True)

    # Value props
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="nf-card" style="text-align:center; padding:30px;">
            <div style="font-size:36px; margin-bottom:12px;">🚀</div>
            <div style="font-size:17px; font-weight:700; color:#1B2A4A; margin-bottom:8px;">Per le Startup</div>
            <div style="font-size:13px; color:#5B657A; line-height:1.6;">Fatti scoprire da investitori e corporate. Mostra la tua traction, trova partner e accelera il tuo funding.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="nf-card" style="text-align:center; padding:30px;">
            <div style="font-size:36px; margin-bottom:12px;">💎</div>
            <div style="font-size:17px; font-weight:700; color:#1B2A4A; margin-bottom:8px;">Per gli Investitori</div>
            <div style="font-size:13px; color:#5B657A; line-height:1.6;">Scouting intelligente, deal flow qualificato, filtri avanzati. Trova le startup giuste per la tua thesis.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="nf-card" style="text-align:center; padding:30px;">
            <div style="font-size:36px; margin-bottom:12px;">🏢</div>
            <div style="font-size:17px; font-weight:700; color:#1B2A4A; margin-bottom:8px;">Per le Corporate</div>
            <div style="font-size:13px; color:#5B657A; line-height:1.6;">Pubblica challenge, trova startup rilevanti, gestisci il tuo innovation scouting in un unico posto.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Social proof
    st.markdown("""<div style="text-align:center; padding:20px 0;">
        <div style="font-size:13px; color:#5B657A; letter-spacing:1px; text-transform:uppercase; margin-bottom:16px;">Trusted by the European innovation ecosystem</div>
        <div style="display:flex; justify-content:center; gap:40px; flex-wrap:wrap; color:#5B657A; font-size:18px; font-weight:600; opacity:0.5;">
            <span>240+ Startup</span> <span>·</span>
            <span>80+ Investitori</span> <span>·</span>
            <span>45+ Corporate</span> <span>·</span>
            <span>€120M+ Deal Flow</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="text-align:center; margin:20px 0;"><span style="font-size:20px; font-weight:700; color:#1B2A4A;">Scegli il tuo ruolo per entrare</span></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀  Sono una Startup", use_container_width=True, type="primary"):
            st.session_state.role = "Startup"
            st.session_state.logged_in = True
            nav_to("home")
            st.rerun()
    with c2:
        if st.button("💎  Sono un Investitore", use_container_width=True, type="primary"):
            st.session_state.role = "Investor"
            st.session_state.logged_in = True
            nav_to("home")
            st.rerun()
    with c3:
        if st.button("🏢  Sono una Corporate", use_container_width=True, type="primary"):
            st.session_state.role = "Corporate"
            st.session_state.logged_in = True
            nav_to("home")
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: HOME FEED
# ─────────────────────────────────────────────

def render_home():
    role = st.session_state.role
    section_title(f"Home", f"Il tuo feed personalizzato · Ruolo: {role}")

    # Top KPIs row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("12", "Nuovi Match")
    with k2:
        kpi_card("5", "Opportunità Rilevanti")
    with k3:
        kpi_card("3", "Messaggi Non Letti")
    with k4:
        kpi_card("87%", "Profilo Completo")

    st.markdown("<br>", unsafe_allow_html=True)

    # Feed content
    left, right = st.columns([2, 1])

    with left:
        # Filter tabs
        feed_cats = ["Tutti", "Startup", "Investor", "Corporate"]
        filter_col = st.columns(len(feed_cats))
        for i, cat in enumerate(feed_cats):
            with filter_col[i]:
                if st.button(cat, key=f"ffilt_{cat}", use_container_width=True,
                             type="primary" if st.session_state.feed_filter == cat else "secondary"):
                    st.session_state.feed_filter = cat
                    st.rerun()

        # Filtered feed
        feed = st.session_state.feed
        if st.session_state.feed_filter != "Tutti":
            feed = [f for f in feed if f["author_type"] == st.session_state.feed_filter]

        # Role-based sorting: bring relevant content to top
        def relevance(item):
            if role == "Startup" and item["author_type"] in ["Investor", "Corporate"]:
                return 0
            elif role == "Investor" and item["author_type"] == "Startup":
                return 0
            elif role == "Corporate" and item["author_type"] == "Startup":
                return 0
            return 1

        feed_sorted = sorted(feed, key=relevance)

        for item in feed_sorted[:15]:
            icon = author_icon(item["author_type"])
            color_badge = badge(item["category"], item["color"])
            type_b = badge(item["author_type"], "primary")

            st.markdown(f"""<div class="nf-card-feed">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <span style="font-weight:700; color:#1B2A4A;">{icon} {item['author']}</span>
                        {type_b}
                    </div>
                    <span style="font-size:12px; color:#5B657A;">{item['time_ago']}</span>
                </div>
                <div style="font-size:14px; color:#2A3550; line-height:1.6; margin-bottom:10px;">{item['text']}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>{color_badge} {badge(item['sector'], 'primary')}</div>
                    <div style="font-size:12px; color:#5B657A;">♥ {item['likes']} · 💬 {item['comments']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with right:
        # Suggested for you
        st.markdown(f"""<div class="nf-card" style="border-left:3px solid #2EC4B6;">
            <div style="font-size:15px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">⚡ Suggeriti per te</div>""", unsafe_allow_html=True)

        if role == "Investor":
            suggestions = st.session_state.startups[:5]
        elif role == "Startup":
            suggestions = st.session_state.investors[:3] + st.session_state.corporates[:2]
        else:
            suggestions = st.session_state.startups[:5]

        for s in suggestions:
            ms = match_score(s, role)
            st.markdown(f"""<div style="padding:8px 0; border-bottom:1px solid #E6EAF2;">
                <div style="font-weight:600; font-size:13px; color:#1B2A4A;">{author_icon(s['type'])} {s['name']}</div>
                <div style="font-size:11px; color:#5B657A;">{s.get('sector', s.get('focus_sectors',[''])[0] if 'focus_sectors' in s else s.get('industry',''))}</div>
                <span class="nf-match" style="font-size:11px; padding:2px 8px; margin-top:4px;">⚡ {ms}%</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Trending topics
        st.markdown(f"""<div class="nf-card" style="margin-top:16px;">
            <div style="font-size:15px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">🔥 Trending</div>
            <div style="font-size:13px; color:#3A4560; line-height:2;">
                {''.join([f'{badge(s, "accent")}' for s in ["AI Agents", "Climate Tech", "GenAI Enterprise", "Open Innovation", "Embedded Finance"]])}
            </div>
        </div>""", unsafe_allow_html=True)

        # Quick actions
        st.markdown(f"""<div class="nf-card" style="margin-top:16px;">
            <div style="font-size:15px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">🎯 Azioni Rapide</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔍 Esplora Opportunità", use_container_width=True):
            nav_to("opportunities")
            st.rerun()
        if st.button("👥 Discover Profili", use_container_width=True):
            nav_to("discover")
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: DISCOVER
# ─────────────────────────────────────────────

def render_discover():
    role = st.session_state.role
    section_title("Discover", "Trova startup, investitori e corporate rilevanti per te")

    # Filters
    with st.container():
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            disc_type = st.selectbox("Tipo", ["Startup", "Investor", "Corporate"],
                                      index=["Startup", "Investor", "Corporate"].index(st.session_state.discover_type),
                                      key="dt_sel")
            st.session_state.discover_type = disc_type
        with f2:
            all_sectors = ["Tutti"] + SECTORS
            sector = st.selectbox("Settore", all_sectors, key="ds_sel")
            st.session_state.discover_sector = sector
        with f3:
            if disc_type == "Startup":
                all_stages = ["Tutti"] + STAGES
                stage = st.selectbox("Stage", all_stages, key="dstg_sel")
                st.session_state.discover_stage = stage
            else:
                st.selectbox("Stage", ["N/A"], disabled=True, key="dstg_dis")
        with f4:
            search_q = st.text_input("🔍 Cerca", placeholder="Nome, keyword...", key="disc_search")

    st.markdown("---")

    # Get entities
    if disc_type == "Startup":
        entities = st.session_state.startups
        if st.session_state.discover_sector != "Tutti":
            entities = [e for e in entities if e["sector"] == st.session_state.discover_sector]
        if st.session_state.discover_stage != "Tutti":
            entities = [e for e in entities if e["stage"] == st.session_state.discover_stage]
    elif disc_type == "Investor":
        entities = st.session_state.investors
        if st.session_state.discover_sector != "Tutti":
            entities = [e for e in entities if st.session_state.discover_sector in e["focus_sectors"]]
    else:
        entities = st.session_state.corporates
        if st.session_state.discover_sector != "Tutti":
            entities = [e for e in entities if st.session_state.discover_sector in e["innovation_areas"]]

    if search_q:
        q = search_q.lower()
        entities = [e for e in entities if q in e["name"].lower() or q in e.get("tagline", e.get("thesis", e.get("description", ""))).lower()]

    # Sort by match score
    entities_scored = [(e, match_score(e, role)) for e in entities]
    entities_scored.sort(key=lambda x: x[1], reverse=True)

    st.markdown(f"**{len(entities_scored)}** risultati trovati", unsafe_allow_html=True)

    for entity, score in entities_scored:
        render_entity_card(entity, show_match=True)


# ─────────────────────────────────────────────
# PAGE: PROFILE DETAIL
# ─────────────────────────────────────────────

def render_profile_detail():
    entity = st.session_state.selected_profile
    if not entity:
        st.warning("Nessun profilo selezionato.")
        if st.button("← Torna a Discover"):
            nav_to("discover")
            st.rerun()
        return

    name = entity["name"]
    etype = entity["type"]
    icon = author_icon(etype)
    ms = match_score(entity, st.session_state.role)
    saved = name in st.session_state.saved_profiles

    # Header
    st.markdown(f"""<div class="nf-profile-header">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div style="font-size:12px; opacity:0.7; text-transform:uppercase; letter-spacing:1px;">{icon} {etype}</div>
                <div class="nf-profile-name">{name}</div>
                <div class="nf-profile-tagline">{entity.get('tagline', entity.get('thesis', entity.get('description', '')))}</div>
            </div>
            <div><span class="nf-match" style="font-size:16px; padding:8px 18px;">⚡ {ms}% match</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Action bar
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        if st.button(f"{'★ Salvato' if saved else '☆ Salva Profilo'}", key="prof_save", use_container_width=True, type="primary" if saved else "secondary"):
            toggle_save_profile(name)
            st.rerun()
    with ac2:
        connected = name in st.session_state.connections
        if st.button(f"{'✓ Connesso' if connected else '💬 Connetti'}", key="prof_conn", use_container_width=True, type="primary" if not connected else "secondary"):
            if not connected:
                st.session_state.connections.append(name)
            st.toast(f"Connesso con {name}!" if not connected else f"Già connesso con {name}")
            st.rerun()
    with ac3:
        if st.button("📨 Richiedi Intro", key="prof_intro", use_container_width=True):
            st.toast(f"Richiesta di intro inviata a {name}!")
    with ac4:
        if st.button("← Indietro", key="prof_back", use_container_width=True):
            nav_to("discover")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Profile body based on type
    if etype == "Startup":
        left, right = st.columns([2, 1])
        with left:
            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Overview</div>
                <div style="font-size:14px; color:#3A4560; line-height:1.7;">{entity['tagline']}</div>
                <div style="margin-top:16px;">
                    {badge(entity['sector'], 'accent')} {badge(entity['stage'], 'primary')} {badge(entity['biz_model'], 'amber')}
                </div>
                <div style="margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div><span style="font-size:12px; color:#5B657A;">📍 Location</span><br><span style="font-weight:600;">{entity['city']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">👥 Team</span><br><span style="font-weight:600;">{entity['team_size']} persone</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">📅 Fondazione</span><br><span style="font-weight:600;">{entity['founded']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">💰 Raised</span><br><span style="font-weight:600;">{entity['raised']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">📊 Revenue</span><br><span style="font-weight:600;">{entity['revenue']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">🏷️ Model</span><br><span style="font-weight:600;">{entity['biz_model']}</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Highlights & Traction</div>
                {''.join([f'<div style="padding:6px 0; border-bottom:1px solid #F0F2F5; font-size:14px;">✓ {h}</div>' for h in entity['highlights']])}
            </div>""", unsafe_allow_html=True)

        with right:
            st.markdown(f"""<div class="nf-card" style="border-left:3px solid #2EC4B6;">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Cercano</div>
                {''.join([f'{badge(lf, "accent")}' for lf in entity['looking_for']])}
            </div>""", unsafe_allow_html=True)

            # Fake recent activity
            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Attività Recente</div>
                <div style="font-size:13px; color:#5B657A; line-height:1.8;">
                    <div>📈 Revenue +32% YoY</div>
                    <div>🤝 Nuovo partner enterprise</div>
                    <div>👥 3 nuove assunzioni tech</div>
                    <div>🏆 Selezionata per EU Innovation Radar</div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif etype == "Investor":
        left, right = st.columns([2, 1])
        with left:
            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Investment Thesis</div>
                <div style="font-size:14px; color:#3A4560; line-height:1.7;">{entity['thesis']}</div>
                <div style="margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div><span style="font-size:12px; color:#5B657A;">📍 Base</span><br><span style="font-weight:600;">{entity['city']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">🏷️ Tipo</span><br><span style="font-weight:600;">{entity['type_inv']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">💰 Ticket</span><br><span style="font-weight:600;">{entity['ticket']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">📊 Portfolio</span><br><span style="font-weight:600;">{entity['portfolio_size']} aziende</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Focus Sectors</div>
                <div>{''.join([badge(s, 'accent') for s in entity['focus_sectors']])}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Portfolio Highlights</div>
                {''.join([f'<div style="padding:4px 0; font-size:14px;">🚀 {p}</div>' for p in entity['portfolio_highlights']])}
            </div>""", unsafe_allow_html=True)

        with right:
            st.markdown(f"""<div class="nf-card" style="border-left:3px solid #2EC4B6;">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Stage Preferiti</div>
                {''.join([badge(s, 'primary') for s in entity['stages_pref']])}
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Attività Recente</div>
                <div style="font-size:13px; color:#5B657A; line-height:1.8;">
                    <div>💰 Nuovo investimento nel Q1 2026</div>
                    <div>📝 Thesis aggiornata</div>
                    <div>🤝 3 nuovi deal in pipeline</div>
                </div>
            </div>""", unsafe_allow_html=True)

    else:  # Corporate
        left, right = st.columns([2, 1])
        with left:
            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Overview</div>
                <div style="font-size:14px; color:#3A4560; line-height:1.7;">{entity['description']}</div>
                <div style="margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div><span style="font-size:12px; color:#5B657A;">🏭 Industry</span><br><span style="font-weight:600;">{entity['industry']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">📍 HQ</span><br><span style="font-weight:600;">{entity['city']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">👥 Size</span><br><span style="font-weight:600;">{entity['size']}</span></div>
                    <div><span style="font-size:12px; color:#5B657A;">🎯 Challenges</span><br><span style="font-weight:600;">{entity['active_challenges']} attive</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Innovation Areas</div>
                <div>{''.join([badge(a, 'accent') for a in entity['innovation_areas']])}</div>
            </div>""", unsafe_allow_html=True)

        with right:
            pr = "✅ Sì" if entity.get('procurement_ready') else "⏳ In valutazione"
            st.markdown(f"""<div class="nf-card" style="border-left:3px solid #2EC4B6;">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Procurement Ready</div>
                <div style="font-size:15px; font-weight:600;">{pr}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="nf-card">
                <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:12px;">Attività Recente</div>
                <div style="font-size:13px; color:#5B657A; line-height:1.8;">
                    <div>🎯 Nuova challenge pubblicata</div>
                    <div>🤝 2 pilot avviati nel Q1</div>
                    <div>🚀 Partnership con 3 startup</div>
                </div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: OPPORTUNITIES
# ─────────────────────────────────────────────

def render_opportunities():
    section_title("Opportunità", "Challenge, pilot, partnership e investment thesis attive")

    opps = st.session_state.opportunities

    f1, f2, f3 = st.columns(3)
    with f1:
        opp_type_filter = st.selectbox("Tipo", ["Tutti", "Challenge", "Pilot", "Partnership", "Open Call", "Investment Thesis"], key="opp_type")
    with f2:
        opp_sector_filter = st.selectbox("Settore", ["Tutti"] + SECTORS, key="opp_sector")
    with f3:
        opp_priority_filter = st.selectbox("Priorità", ["Tutte", "Critical", "High", "Medium", "Active"], key="opp_prio")

    if opp_type_filter != "Tutti":
        opps = [o for o in opps if o["type"] == opp_type_filter]
    if opp_sector_filter != "Tutti":
        opps = [o for o in opps if o["sector"] == opp_sector_filter]
    if opp_priority_filter != "Tutte":
        opps = [o for o in opps if o["priority"] == opp_priority_filter]

    st.markdown(f"**{len(opps)}** opportunità trovate")
    st.markdown("---")

    for opp in opps:
        saved = opp["id"] in st.session_state.saved_opps
        owner_icon = "🏢" if opp["owner_type"] == "Corporate" else "💎"

        st.markdown(f"""<div class="nf-opp-card">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div>
                    <div style="margin-bottom:6px;">{type_badge(opp['type'])} {priority_badge(opp['priority'])}</div>
                    <div style="font-size:17px; font-weight:700; color:#1B2A4A;">{opp['title']}</div>
                    <div style="font-size:13px; color:#5B657A; margin-top:2px;">{owner_icon} {opp['owner']} · {badge(opp['sector'], 'accent')}</div>
                </div>
            </div>
            <div style="font-size:14px; color:#3A4560; margin:12px 0; line-height:1.6;">{opp['description']}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; font-size:12px; color:#5B657A;">
                <div>⏰ <strong>Deadline:</strong> {opp['deadline']}</div>
                <div>🎯 <strong>Fit ideale:</strong> {opp['ideal_fit']}</div>
                <div>💰 <strong>Budget:</strong> {opp['budget']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        oc1, oc2, oc3, _ = st.columns([1, 1, 1, 3])
        with oc1:
            if st.button("✋ Express Interest", key=f"ei_{opp['id']}", type="primary"):
                st.toast(f"Interesse espresso per: {opp['title']}")
        with oc2:
            if st.button(f"{'★' if saved else '☆'} Salva", key=f"so_{opp['id']}"):
                toggle_save_opp(opp["id"])
                st.rerun()
        with oc3:
            if st.button("📨 Contatta", key=f"co_{opp['id']}"):
                st.toast(f"Messaggio inviato a {opp['owner']}")


# ─────────────────────────────────────────────
# PAGE: MESSAGES
# ─────────────────────────────────────────────

def _conv_card_html(conv, is_active):
    """Build a single self-contained HTML string for a conversation list item."""
    border_left = "border-left:3px solid #2EC4B6;" if is_active else ""
    bg = "background:rgba(46,196,182,0.04);" if is_active else ""
    icon = author_icon(conv["with_type"])
    unread_dot = ""
    if conv["unread"] > 0:
        unread_dot = (
            f'<span style="background:#FF6B6B;color:white;border-radius:50%;'
            f'width:20px;height:20px;display:inline-flex;align-items:center;'
            f'justify-content:center;font-size:11px;font-weight:700;">'
            f'{conv["unread"]}</span>'
        )
    s_badge = status_badge(conv["status"])
    return (
        f'<div style="padding:12px 20px;border-bottom:1px solid #E6EAF2;{border_left}{bg}">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<div style="font-weight:600;font-size:14px;color:#1B2A4A;">{icon} {conv["with"]}</div>'
        f'<div style="display:flex;align-items:center;gap:6px;">'
        f'<span style="font-size:11px;color:#5B657A;">{conv["time"]}</span>{unread_dot}</div></div>'
        f'<div style="font-size:12px;color:#5B657A;margin-top:2px;">{s_badge}</div>'
        f'<div style="font-size:12px;color:#5B657A;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{conv["preview"]}</div>'
        f'</div>'
    )


def _thread_header_html(conv):
    icon = author_icon(conv["with_type"])
    s_badge = status_badge(conv["status"])
    return (
        f'<div class="nf-card">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid #E6EAF2;">'
        f'<div>'
        f'<div style="font-size:17px;font-weight:700;color:#1B2A4A;">{icon} {conv["with"]}</div>'
        f'<div style="font-size:12px;color:#5B657A;">{conv["with_type"]} · {s_badge}</div>'
        f'</div></div></div>'
    )


def _msg_html(msg):
    if msg["from"] == "system":
        return (
            f'<div style="text-align:center;padding:12px;margin:8px 0;">'
            f'<div style="font-size:12px;color:#5B657A;background:#F7F8FB;display:inline-block;padding:6px 16px;border-radius:20px;">'
            f'🔗 {msg["text"]}<br><span style="font-size:11px;">{msg["time"]}</span>'
            f'</div></div>'
        )
    elif msg["from"] == "me":
        return (
            f'<div style="display:flex;justify-content:flex-end;margin-bottom:8px;">'
            f'<div class="nf-msg nf-msg-me">'
            f'<div style="font-size:13px;">{msg["text"]}</div>'
            f'<div style="font-size:10px;opacity:0.8;margin-top:4px;">{msg["time"]}</div>'
            f'</div></div>'
        )
    else:
        return (
            f'<div style="display:flex;justify-content:flex-start;margin-bottom:8px;">'
            f'<div class="nf-msg nf-msg-them">'
            f'<div style="font-size:13px;">{msg["text"]}</div>'
            f'<div style="font-size:10px;color:#5B657A;margin-top:4px;">{msg["time"]}</div>'
            f'</div></div>'
        )


def render_messages():
    section_title("Messaggi & Intro", "Le tue conversazioni e richieste di introduzione")

    convs = st.session_state.conversations

    left, right = st.columns([1, 2])

    with left:
        st.markdown('<div class="nf-card" style="padding:16px 20px;border-bottom:1px solid #E6EAF2;"><div style="font-size:15px;font-weight:700;color:#1B2A4A;">Conversazioni</div></div>', unsafe_allow_html=True)

        for conv in convs:
            is_active = st.session_state.selected_conv == conv["id"]
            st.markdown(_conv_card_html(conv, is_active), unsafe_allow_html=True)
            if st.button("Apri", key=f"open_{conv['id']}", use_container_width=True):
                st.session_state.selected_conv = conv["id"]
                st.rerun()

    with right:
        active_conv = next((c for c in convs if c["id"] == st.session_state.selected_conv), convs[0])

        st.markdown(_thread_header_html(active_conv), unsafe_allow_html=True)

        all_msgs = "".join(_msg_html(m) for m in active_conv["messages"])
        st.markdown(f'<div class="nf-card">{all_msgs}</div>', unsafe_allow_html=True)

        # Reply box
        reply_col1, reply_col2 = st.columns([5, 1])
        with reply_col1:
            st.text_input("Scrivi un messaggio...", key="msg_input", label_visibility="collapsed", placeholder="Scrivi un messaggio...")
        with reply_col2:
            if st.button("📤 Invia", key="send_msg", use_container_width=True, type="primary"):
                st.toast("Messaggio inviato!")


# ─────────────────────────────────────────────
# PAGE: NETWORK
# ─────────────────────────────────────────────

def render_network():
    section_title("Il Tuo Network", "Connessioni, profili salvati e pipeline")

    tabs = st.tabs(["🤝 Connessioni", "★ Profili Salvati", "🎯 Opportunità Salvate", "📊 Pipeline"])

    with tabs[0]:
        conns = st.session_state.connections
        if not conns:
            st.info("Non hai ancora connessioni. Vai su Discover per trovare e connetterti con profili rilevanti!")
        else:
            st.markdown(f"**{len(conns)}** connessioni attive")
            for cname in conns:
                # Find entity
                entity = None
                for lst in [st.session_state.startups, st.session_state.investors, st.session_state.corporates]:
                    for e in lst:
                        if e["name"] == cname:
                            entity = e
                            break

                if entity:
                    icon = author_icon(entity["type"])
                    ms = match_score(entity, st.session_state.role)
                    desc = entity.get("tagline", entity.get("thesis", entity.get("description", "")))[:80]
                    st.markdown(f"""<div class="nf-card" style="padding:16px 20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-weight:700; color:#1B2A4A;">{icon} {cname}</span>
                                {badge(entity['type'], 'primary')}
                                <div style="font-size:12px; color:#5B657A; margin-top:2px;">{desc}...</div>
                            </div>
                            <div><span class="nf-match" style="font-size:11px;">⚡ {ms}%</span></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    c1, c2, _ = st.columns([1, 1, 4])
                    with c1:
                        if st.button("👤 Profilo", key=f"net_prof_{cname}"):
                            st.session_state.selected_profile = entity
                            nav_to("profile_detail")
                            st.rerun()
                    with c2:
                        if st.button("💬 Messaggio", key=f"net_msg_{cname}"):
                            nav_to("messages")
                            st.rerun()
                else:
                    st.markdown(f"""<div class="nf-card" style="padding:14px 20px;">
                        <span style="font-weight:600;">{cname}</span> {badge('Connected', 'success')}
                    </div>""", unsafe_allow_html=True)

    with tabs[1]:
        saved = st.session_state.saved_profiles
        if not saved:
            st.info("Non hai ancora salvato profili. Usa il pulsante ☆ Save sui profili che ti interessano!")
        else:
            st.markdown(f"**{len(saved)}** profili salvati")
            for sname in saved:
                entity = None
                for lst in [st.session_state.startups, st.session_state.investors, st.session_state.corporates]:
                    for e in lst:
                        if e["name"] == sname:
                            entity = e
                            break
                if entity:
                    render_entity_card(entity, show_match=True, compact=False)

    with tabs[2]:
        saved_opps = st.session_state.saved_opps
        if not saved_opps:
            st.info("Non hai ancora salvato opportunità. Esplora la sezione Opportunità per trovarne di rilevanti!")
        else:
            st.markdown(f"**{len(saved_opps)}** opportunità salvate")
            for oid in saved_opps:
                opp = next((o for o in st.session_state.opportunities if o["id"] == oid), None)
                if opp:
                    st.markdown(f"""<div class="nf-opp-card">
                        <div>{type_badge(opp['type'])} {priority_badge(opp['priority'])}</div>
                        <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-top:6px;">{opp['title']}</div>
                        <div style="font-size:13px; color:#5B657A;">{opp['owner']}</div>
                    </div>""", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("""<div class="nf-card">
            <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:16px;">📊 La Tua Pipeline</div>
        </div>""", unsafe_allow_html=True)

        pipeline_stages = [
            ("Discovered", 8, "#E6EAF2"),
            ("Contacted", 4, "#FFB347"),
            ("In Conversation", 3, "#2EC4B6"),
            ("Evaluating", 2, "#2A4170"),
            ("Closed / Won", 1, "#27AE60"),
        ]
        for stage_name, count, color in pipeline_stages:
            pct = count / 8 * 100
            st.markdown(f"""<div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;">
                    <span style="font-weight:600; color:#1B2A4A;">{stage_name}</span>
                    <span style="color:#5B657A;">{count}</span>
                </div>
                <div style="background:#F0F2F5; border-radius:6px; height:8px; overflow:hidden;">
                    <div style="background:{color}; width:{pct}%; height:100%; border-radius:6px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Suggested intros
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="nf-card" style="border-left:3px solid #FFB347;">
            <div style="font-size:15px; font-weight:700; color:#1B2A4A; margin-bottom:10px;">💡 Intro Suggerite</div>
            <div style="font-size:13px; color:#3A4560; line-height:1.8;">
                <div>🤝 <strong>Northstar Ventures</strong> → <strong>DataPulse</strong> — Forte allineamento su AI & Supply Chain</div>
                <div>🤝 <strong>Enel Innovation</strong> → <strong>GreenVolt</strong> — Match su Smart Grid & Energy</div>
                <div>🤝 <strong>Alpine Capital</strong> → <strong>FinBridge</strong> — Focus condiviso su FinTech Seed</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: INSIGHTS
# ─────────────────────────────────────────────

def render_insights():
    section_title("Insights", "Il tuo riepilogo settimanale e i trend dell'ecosistema")

    # Weekly summary
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        kpi_card("47", "Profili Visti")
    with k2:
        kpi_card("12", "Nuovi Match")
    with k3:
        kpi_card("5", "Opportunità Nuove")
    with k4:
        kpi_card("8", "Connessioni")
    with k5:
        kpi_card("92", "Activity Score")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        st.markdown("""<div class="nf-card">
            <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:16px;">🔥 Settori in Trend</div>
        </div>""", unsafe_allow_html=True)
        trending = [
            ("AI & Machine Learning", 94, "+12%"),
            ("CleanTech", 87, "+18%"),
            ("CyberSecurity", 82, "+8%"),
            ("FinTech", 78, "+5%"),
            ("HealthTech", 75, "+9%"),
            ("Industry 4.0", 71, "+15%"),
        ]
        for sector, score, growth in trending:
            st.markdown(f"""<div style="display:flex; align-items:center; justify-content:space-between; padding:10px 0; border-bottom:1px solid #F0F2F5;">
                <div>
                    <span style="font-weight:600; font-size:14px; color:#1B2A4A;">{sector}</span>
                </div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:12px; color:#27AE60; font-weight:600;">{growth}</span>
                    <div style="background:#F0F2F5; border-radius:6px; height:6px; width:100px; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #2EC4B6, #1A9E92); width:{score}%; height:100%; border-radius:6px;"></div>
                    </div>
                    <span style="font-size:12px; color:#5B657A; font-weight:600;">{score}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown("""<div class="nf-card">
            <div style="font-size:16px; font-weight:700; color:#1B2A4A; margin-bottom:16px;">📈 High-Fit Matches Recenti</div>
        </div>""", unsafe_allow_html=True)

        role = st.session_state.role
        if role == "Investor":
            recs = st.session_state.startups[:6]
        elif role == "Startup":
            recs = st.session_state.investors[:4] + st.session_state.corporates[:2]
        else:
            recs = st.session_state.startups[:6]

        for e in recs:
            ms = match_score(e, role)
            if ms >= 75:
                icon = author_icon(e["type"])
                st.markdown(f"""<div style="display:flex; align-items:center; justify-content:space-between; padding:8px 0; border-bottom:1px solid #F0F2F5;">
                    <div>
                        <span style="font-weight:600; font-size:13px; color:#1B2A4A;">{icon} {e['name']}</span>
                        <div style="font-size:11px; color:#5B657A;">{e.get('sector', e.get('focus_sectors',[''])[0] if 'focus_sectors' in e else e.get('industry',''))}</div>
                    </div>
                    <span class="nf-match" style="font-size:11px; padding:2px 10px;">⚡ {ms}%</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="nf-card" style="border-left:3px solid #FFB347;">
            <div style="font-size:15px; font-weight:700; color:#1B2A4A; margin-bottom:8px;">💡 Weekly Digest</div>
            <div style="font-size:13px; color:#3A4560; line-height:1.8;">
                <div>• 3 nuove startup nel tuo settore di interesse</div>
                <div>• 2 challenge corporate con deadline entro 30gg</div>
                <div>• Il tuo profilo è stato visto 23 volte questa settimana</div>
                <div>• 1 investitore ha salvato il tuo profilo</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: MY PROFILE
# ─────────────────────────────────────────────

def render_my_profile():
    role = st.session_state.role
    section_title("Il Tuo Profilo", "Gestisci le informazioni del tuo profilo")

    if role == "Startup":
        mock = st.session_state.startups[0]  # Use first startup as "my" profile
    elif role == "Investor":
        mock = st.session_state.investors[0]
    else:
        mock = st.session_state.corporates[0]

    st.session_state.selected_profile = mock
    render_profile_detail()


# ─────────────────────────────────────────────
# SIDEBAR & NAVIGATION
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""<div style="text-align:center; padding:20px 0 10px;">
            <div style="font-size:24px; font-weight:800; color:white; letter-spacing:-0.5px;">◆ NexFound</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.5); letter-spacing:1px; margin-top:2px;">B2B INNOVATION NETWORK</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        role = st.session_state.role
        role_icons = {"Startup": "🚀", "Investor": "💎", "Corporate": "🏢"}
        st.markdown(f"""<div style="padding:8px 12px; background:rgba(255,255,255,0.08); border-radius:10px; margin-bottom:16px;">
            <div style="font-size:12px; color:rgba(255,255,255,0.5);">Logged in as</div>
            <div style="font-size:15px; font-weight:700; color:white;">{role_icons.get(role, '👤')} {role}</div>
        </div>""", unsafe_allow_html=True)

        # Navigation
        pages = [
            ("home", "🏠", "Home"),
            ("discover", "🔍", "Discover"),
            ("opportunities", "🎯", "Opportunità"),
            ("messages", "💬", "Messaggi"),
            ("network", "🤝", "Network"),
            ("insights", "📊", "Insights"),
            ("my_profile", "👤", "Profilo"),
        ]

        for page_id, icon, label in pages:
            is_current = st.session_state.page == page_id
            marker = "▸ " if is_current else "  "
            if st.button(f"{marker}{icon}  {label}", key=f"nav_{page_id}", use_container_width=True):
                nav_to(page_id)
                st.rerun()

        st.markdown("---")

        # Switch role
        st.markdown('<div style="font-size:12px; color:rgba(255,255,255,0.5); margin-bottom:8px;">CAMBIA RUOLO</div>', unsafe_allow_html=True)
        new_role = st.radio("", ["Startup", "Investor", "Corporate"], index=["Startup", "Investor", "Corporate"].index(role), key="role_switch", label_visibility="collapsed")
        if new_role != role:
            st.session_state.role = new_role
            st.rerun()

        st.markdown("---")

        # Quick stats
        st.markdown(f"""<div style="font-size:12px; color:rgba(255,255,255,0.4); line-height:2;">
            <div>🤝 {len(st.session_state.connections)} Connessioni</div>
            <div>★ {len(st.session_state.saved_profiles)} Salvati</div>
            <div>🎯 {len(st.session_state.saved_opps)} Opp. Salvate</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = None
            nav_to("landing")
            st.rerun()


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────

def main():
    inject_css()

    if not st.session_state.logged_in:
        render_landing()
        return

    render_sidebar()

    page = st.session_state.page
    routes = {
        "home": render_home,
        "discover": render_discover,
        "opportunities": render_opportunities,
        "messages": render_messages,
        "network": render_network,
        "insights": render_insights,
        "my_profile": render_my_profile,
        "profile_detail": render_profile_detail,
    }

    renderer = routes.get(page, render_home)
    renderer()


if __name__ == "__main__":
    main()
