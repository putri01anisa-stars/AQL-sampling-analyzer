import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AQL Sampling Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
    
# ─────────────────────────────────────────────
# FRUTIGER AERO CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&family=Exo+2:wght@300;400;600;700&display=swap');

:root {
    --sky-deep:    #0a2540;
    --sky-mid:     #1a5276;
    --sky-light:   #2e86c1;
    --aqua:        #00c9b1;
    --aqua-bright: #00ffdd;
    --aqua-glow:   rgba(0,201,177,0.35);
    --green-fresh: #27ae60;
    --white-glass: rgba(255,255,255,0.12);
    --white-rim:   rgba(255,255,255,0.28);
    --frost:       rgba(255,255,255,0.06);
    --text-bright: #e8f8ff;
    --text-mid:    #a8d8ea;
    --text-soft:   #6ba3be;
    --danger:      #e74c3c;
    --warn:        #f39c12;
    --bg-grad: linear-gradient(160deg, #061728 0%, #0d2f50 35%, #07213a 65%, #041220 100%);
}

/* ── GLOBAL ── */
.stApp {
    background: var(--bg-grad) !important;
    background-attachment: fixed !important;
    color: var(--text-bright) !important;
    font-family: 'Nunito', sans-serif;
}

/* Soft animated background orbs */
.stApp::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(0,180,255,0.07) 0%, transparent 70%);
    animation: drift1 18s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
.stApp { 
  background: var(--bg) !important; 
  color: var(--text) !important; 
  font-family: 'Inter', sans-serif; 
}
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -10%;
    right: -5%;
    width: 50%;
    height: 50%;
    background: radial-gradient(ellipse, rgba(0,201,177,0.06) 0%, transparent 70%);
    animation: drift2 22s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes drift1 { from { transform: translate(0,0); } to { transform: translate(5%,8%); } }
@keyframes drift2 { from { transform: translate(0,0); } to { transform: translate(-6%,-5%); } }

/* ── HEADER ── */
.app-header {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.13) 0%,
        rgba(0,180,255,0.10) 40%,
        rgba(0,201,177,0.08) 100%);
    border: 1px solid var(--white-rim);
    border-radius: 20px;
    padding: 32px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.20),
        0 0 60px rgba(0,201,177,0.08);
}
.app-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
}
.app-header::after {
    content: '';
    position: absolute;
    top: -60%; right: -10%;
    width: 45%; height: 220%;
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 60%);
    transform: rotate(-15deg);
    pointer-events: none;
}
.app-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #a8f0e8 50%, var(--aqua) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    margin: 0;
    text-shadow: none;
    filter: drop-shadow(0 0 20px rgba(0,201,177,0.5));
}
.app-subtitle {
    font-family: 'Nunito', sans-serif;
    font-size: 0.9rem;
    font-weight: 400;
    color: var(--text-mid);
    margin-top: 6px;
    letter-spacing: 1.5px;
    opacity: 0.85;
}
.header-badge {
    display: inline-block;
    background: rgba(0,201,177,0.18);
    border: 1px solid rgba(0,201,177,0.4);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.75rem;
    color: var(--aqua);
    letter-spacing: 1px;
    margin-top: 10px;
    font-weight: 600;
}

/* ── GLASS CARD ── */
.glass-card {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.11) 0%,
        rgba(255,255,255,0.05) 100%);
    border: 1px solid var(--white-rim);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow:
        0 4px 24px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.18),
        inset 0 -1px 0 rgba(0,0,0,0.1);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 12px 40px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.25),
        0 0 30px rgba(0,201,177,0.12);
    border-color: rgba(0,201,177,0.5);
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.4) 50%, transparent 100%);
}
.glass-card::after {
    content: '';
    position: absolute;
    top: -40%; right: -15%;
    width: 40%; height: 150%;
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 60%);
    transform: rotate(-20deg);
    pointer-events: none;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.13) 0%,
        rgba(0,150,200,0.08) 100%);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    box-shadow:
        0 4px 20px rgba(0,0,0,0.22),
        inset 0 1px 0 rgba(255,255,255,0.20);
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: var(--aqua);
    box-shadow:
        0 8px 30px rgba(0,0,0,0.3),
        0 0 25px var(--aqua-glow),
        inset 0 1px 0 rgba(255,255,255,0.25);
    transform: translateY(-2px);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
}
.metric-value {
    font-family: 'Exo 2', sans-serif;
    font-size: 2.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff, var(--aqua));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 8px rgba(0,201,177,0.4));
    line-height: 1.1;
}
.metric-label {
    font-size: 0.72rem;
    color: var(--text-soft);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-weight: 600;
}

/* ── RESULT BADGES ── */
.result-pass {
    background: linear-gradient(135deg,
        rgba(39,174,96,0.18) 0%,
        rgba(0,201,177,0.12) 100%);
    border: 1.5px solid rgba(39,174,96,0.6);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    box-shadow:
        0 8px 32px rgba(39,174,96,0.15),
        inset 0 1px 0 rgba(255,255,255,0.15);
}
.result-pass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(39,174,96,0.7), transparent);
}
.result-pass-text {
    font-family: 'Exo 2', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a8f5c8, #27ae60);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    filter: drop-shadow(0 0 12px rgba(39,174,96,0.5));
}
.result-fail {
    background: linear-gradient(135deg,
        rgba(231,76,60,0.18) 0%,
        rgba(192,57,43,0.10) 100%);
    border: 1.5px solid rgba(231,76,60,0.6);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    box-shadow:
        0 8px 32px rgba(231,76,60,0.15),
        inset 0 1px 0 rgba(255,255,255,0.12);
}
.result-fail::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(231,76,60,0.7), transparent);
}
.result-fail-text {
    font-family: 'Exo 2', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f5a8a8, #e74c3c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    filter: drop-shadow(0 0 12px rgba(231,76,60,0.5));
}
.result-sub {
    font-size: 0.95rem;
    color: var(--text-mid);
    margin-top: 8px;
    font-weight: 400;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-bright);
    letter-spacing: 2px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 20px;
    border-radius: 2px;
    background: linear-gradient(180deg, var(--aqua-bright), var(--aqua));
    box-shadow: 0 0 8px var(--aqua-glow);
    flex-shrink: 0;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,201,177,0.3), transparent);
    margin-left: 4px;
}

/* ── SIDEBAR ── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        rgba(6,23,40,0.97) 0%,
        rgba(10,37,64,0.97) 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.10) !important;
    backdrop-filter: blur(20px) !important;
}
div[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 1px;
    height: 100%;
    background: linear-gradient(180deg, transparent, rgba(0,201,177,0.3), transparent);
}
div[data-testid="stSidebar"] * { color: var(--text-bright) !important; }
div[data-testid="stSidebar"] h3 {
    font-family: 'Exo 2', sans-serif !important;
    letter-spacing: 1px !important;
    color: var(--aqua) !important;
}

/* ── FORM INPUTS ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.08) 0%,
        rgba(0,100,160,0.06) 100%) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: var(--text-bright) !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--aqua) !important;
    box-shadow: 0 0 0 3px rgba(0,201,177,0.15) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg,
        rgba(0,201,177,0.9) 0%,
        rgba(0,150,210,0.85) 100%) !important;
    color: #ffffff !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 2px !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease !important;
    box-shadow:
        0 4px 15px rgba(0,201,177,0.25),
        inset 0 1px 0 rgba(255,255,255,0.25) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 10px 30px rgba(0,201,177,0.4),
        inset 0 1px 0 rgba(255,255,255,0.35) !important;
    background: linear-gradient(135deg,
        rgba(0,230,200,0.95) 0%,
        rgba(0,170,230,0.9) 100%) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    color: var(--text-soft) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.08) !important;
    color: var(--text-bright) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,
        rgba(0,201,177,0.22) 0%,
        rgba(0,150,210,0.15) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(0,201,177,0.35) !important;
    box-shadow: 0 2px 10px rgba(0,201,177,0.15) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── ALERTS / INFO ── */
.stInfo, .stWarning, .stSuccess, .stError {
    border-radius: 12px !important;
    backdrop-filter: blur(8px) !important;
}

/* ── MISC OVERRIDES ── */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-bright) !important;
    font-family: 'Exo 2', sans-serif !important;
}
p, span { color: var(--text-bright); }
.stMarkdown p { color: var(--text-mid) !important; }

/* Divider */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(0,201,177,0.3), transparent) !important;
    margin: 16px 0 !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.12) 0%,
        rgba(0,150,210,0.10) 100%) !important;
    border: 1px solid rgba(0,201,177,0.4) !important;
    color: var(--aqua) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
    transition: all 0.25s !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg,
        rgba(0,201,177,0.18) 0%,
        rgba(0,150,210,0.15) 100%) !important;
    box-shadow: 0 0 20px rgba(0,201,177,0.25) !important;
    transform: translateY(-2px) !important;
}

/* Caption */
.stCaption {
    color: var(--text-soft) !important;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AQL DATA TABLES (ISO 2859-1)
# ─────────────────────────────────────────────

LOT_SIZE_TABLE = [
    (2, 8, 'A'), (9, 15, 'B'), (16, 25, 'C'), (26, 50, 'D'),
    (51, 90, 'E'), (91, 150, 'F'), (151, 280, 'G'), (281, 500, 'H'),
    (501, 1200, 'J'), (1201, 3200, 'K'), (3201, 10000, 'L'),
    (10001, 35000, 'M'), (35001, 150000, 'N'), (150001, 500000, 'P'),
    (500001, float('inf'), 'Q'),
]

SAMPLE_SIZE = {
    'A': 2, 'B': 3, 'C': 5, 'D': 8, 'E': 13,
    'F': 20, 'G': 32, 'H': 50, 'J': 80, 'K': 125,
    'L': 200, 'M': 315, 'N': 500, 'P': 800, 'Q': 1250,
}

AQL_TABLE = {
    'A': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(0,1),6.5:(0,1),10:(0,1)},
    'B': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(0,1),6.5:(0,1),10:(0,1)},
    'C': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(0,1),6.5:(1,2),10:(1,2)},
    'D': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(1,2),6.5:(1,2),10:(2,3)},
    'E': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(1,2),4.0:(1,2),6.5:(2,3),10:(3,4)},
    'F': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(1,2),2.5:(1,2),4.0:(2,3),6.5:(3,4),10:(5,6)},
    'G': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(1,2),1.0:(1,2),1.5:(1,2),2.5:(2,3),4.0:(3,4),6.5:(5,6),10:(7,8)},
    'H': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(1,2),0.65:(1,2),1.0:(1,2),1.5:(2,3),2.5:(3,4),4.0:(5,6),6.5:(7,8),10:(10,11)},
    'J': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(1,2),0.40:(1,2),0.65:(2,3),1.0:(2,3),1.5:(3,4),2.5:(5,6),4.0:(7,8),6.5:(10,11),10:(14,15)},
    'K': {0.065:(0,1),0.1:(0,1),0.15:(1,2),0.25:(1,2),0.40:(2,3),0.65:(3,4),1.0:(3,4),1.5:(5,6),2.5:(7,8),4.0:(10,11),6.5:(14,15),10:(21,22)},
    'L': {0.065:(0,1),0.1:(1,2),0.15:(1,2),0.25:(2,3),0.40:(3,4),0.65:(5,6),1.0:(5,6),1.5:(7,8),2.5:(10,11),4.0:(14,15),6.5:(21,22),10:(21,22)},
    'M': {0.065:(1,2),0.1:(1,2),0.15:(2,3),0.25:(3,4),0.40:(5,6),0.65:(7,8),1.0:(7,8),1.5:(10,11),2.5:(14,15),4.0:(21,22),6.5:(21,22),10:(21,22)},
    'N': {0.065:(1,2),0.1:(2,3),0.15:(3,4),0.25:(5,6),0.40:(7,8),0.65:(10,11),1.0:(10,11),1.5:(14,15),2.5:(21,22),4.0:(21,22),6.5:(21,22),10:(21,22)},
    'P': {0.065:(2,3),0.1:(3,4),0.15:(5,6),0.25:(7,8),0.40:(10,11),0.65:(14,15),1.0:(14,15),1.5:(21,22),2.5:(21,22),4.0:(21,22),6.5:(21,22),10:(21,22)},
    'Q': {0.065:(3,4),0.1:(5,6),0.15:(7,8),0.25:(10,11),0.40:(14,15),0.65:(21,22),1.0:(21,22),1.5:(21,22),2.5:(21,22),4.0:(21,22),6.5:(21,22),10:(21,22)},
}

AQL_LEVELS = [0.065, 0.1, 0.15, 0.25, 0.40, 0.65, 1.0, 1.5, 2.5, 4.0, 6.5, 10]

def get_code_letter(lot_size):
    for low, high, code in LOT_SIZE_TABLE:
        if low <= lot_size <= high:
            return code
    return 'Q'

def get_aql_criteria(code_letter, aql):
    table = AQL_TABLE.get(code_letter, {})
    return table.get(aql, None)

def get_defect_rate(n_defects, sample_size):
    return (n_defects / sample_size) * 100 if sample_size > 0 else 0

# ─────────────────────────────────────────────
# PLOTLY THEME (Frutiger Aero)
# ─────────────────────────────────────────────
PLOT_BG      = 'rgba(10,30,55,0.0)'
PAPER_BG     = 'rgba(14,35,65,0.75)'
GRID_COLOR   = 'rgba(255,255,255,0.07)'
TICK_COLOR   = '#6ba3be'
AQUA         = '#00c9b1'
AQUA_BRIGHT  = '#00ffdd'
DANGER_COLOR = '#e74c3c'
GOLD_COLOR   = '#f5d76e'
FONT_FAMILY  = 'Nunito, sans-serif'

def aero_layout(**kwargs):
    base = dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color='#c8e8f8', family=FONT_FAMILY, size=12),
        margin=dict(l=24, r=24, t=40, b=24),
        xaxis=dict(gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, linecolor='rgba(255,255,255,0.1)', color=TICK_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, linecolor='rgba(255,255,255,0.1)', color=TICK_COLOR),
    )
    base.update(kwargs)
    return base

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">🔬 AQL SAMPLING ANALYZER</div>
    <div class="app-subtitle">Pengolahan Data Sampling &amp; Acceptance Quality Limit · ISO 2859-1</div>
    <div class="header-badge">✦ KELOMPOK 7 · LPK 2026 ✦</div>
</div>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# OPENING / INTRODUCTION (FITUR TAMBAHAN)
# ─────────────────────────────────────────────
with st.expander("ℹ️ TENTANG APLIKASI & KELOMPOK 7", expanded=True):
    st.markdown("""
    **Selamat Datang di AQL Sampling Analyzer!**
    
    Aplikasi ini dirancang sebagai alat bantu interaktif untuk mempermudah proses *Quality Control* (QC) dan pengambilan keputusan dalam penerimaan lot produk. 
    
    **Tujuan & Kegunaan:**
    - Menentukan ukuran sampel (*Sample Size*) secara otomatis berdasarkan jumlah produksi lot/batch.
    - Menetapkan kriteria batas penerimaan (*Acceptance Number/Ac*) dan penolakan (*Rejection Number/Re*).
    - Meminimalisir kesalahan interpretasi tabel manual dan menyediakan laporan serta visualisasi inspeksi atribut yang efisien.
    
    **Sumber Data (Standar Referensi):**
    Seluruh logika kalkulasi dan tabel acuan dalam aplikasi ini merujuk pada **Standar Internasional ISO 2859-1** *(Sampling procedures for inspection by attributes)* untuk inspeksi umum level II (Single Sampling Normal).
    
    **Dikembangkan Oleh Kelompok 7:**
    1. **Iren Nethania Rifai** (2560644)
    2. **Mayang Devani Dwi Nanda** (2560669)
    3. **Putri Anisa** (2560737)
    4. **Shally Ardhany** (2560778)
    5. **Shiela Feriska Demayanti** (2560779)
    """)
	
# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Parameter Sampling")
    st.markdown("---")
    lot_size = st.number_input("Ukuran Lot (Batch)", min_value=2, max_value=999999, value=1000, step=50)
    aql_level = st.selectbox("AQL Level (%)", options=AQL_LEVELS, index=6, format_func=lambda x: f"{x}%")
    inspection_type = st.selectbox("Tipe Inspeksi", ["Normal", "Ketat (Tightened)", "Longgar (Reduced)"])
    st.markdown("---")
    st.markdown("### 📥 Data Defek")
    n_defects = st.number_input("Jumlah Defek Ditemukan", min_value=0, max_value=9999, value=3)
    st.markdown("---")
    st.markdown("### 📋 Info Lot")
    product_name = st.text_input("Nama Produk/Lot", value="Sampel Kimia A")
    lot_number   = st.text_input("Nomor Lot", value="LOT-2026-001")
    inspector    = st.text_input("Nama Inspektor", value="Kelompok 7")
    analyze_btn  = st.button("🔍 ANALISIS SEKARANG", use_container_width=True)

# ─────────────────────────────────────────────
# CALCULATION
# ─────────────────────────────────────────────
code_letter = get_code_letter(lot_size)
sample_size = SAMPLE_SIZE.get(code_letter, 2)
criteria    = get_aql_criteria(code_letter, aql_level)
ac, re      = criteria if criteria else (0, 1)
defect_rate = get_defect_rate(n_defects, sample_size)
decision_pass = n_defects <= ac

# ─────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Hasil Analisis", "📈 Visualisasi", "📋 Tabel AQL", "📄 Laporan"])

# ── TAB 1: HASIL ──────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Parameter Lot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics_row1 = [
        (f"{lot_size:,}", "Ukuran Lot"),
        (code_letter,     "Kode Sampel"),
        (str(sample_size),"Ukuran Sampel"),
        (f"{aql_level}%", "AQL Level"),
    ]
    for col, (val, lbl) in zip([c1,c2,c3,c4], metrics_row1):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Kriteria Penerimaan</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics_row2 = [
        (str(ac),                "Accept Number (Ac)"),
        (str(re),                "Reject Number (Re)"),
        (str(n_defects),         "Defek Ditemukan"),
        (f"{defect_rate:.2f}%",  "Defect Rate"),
    ]
    for col, (val, lbl) in zip([c1,c2,c3,c4], metrics_row2):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Keputusan Sampling</div>', unsafe_allow_html=True)
    if decision_pass:
        st.markdown(f"""
        <div class="result-pass">
            <div class="result-pass-text">✅ LOT DITERIMA (ACCEPT)</div>
            <div class="result-sub">Defek ({n_defects}) ≤ Ac ({ac}) — Lot memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-fail">
            <div class="result-fail-text">❌ LOT DITOLAK (REJECT)</div>
            <div class="result-sub">Defek ({n_defects}) ≥ Re ({re}) — Lot tidak memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">Interpretasi</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"""
**📌 Tentang Lot Ini**
- **Produk:** {product_name}
- **Nomor Lot:** {lot_number}
- **Inspektor:** {inspector}
- **Tipe Inspeksi:** {inspection_type}
        """)
    with col_b:
        sampling_ratio = (sample_size / lot_size) * 100
        rekomendasi = (
            "✅ Lot dapat dikirim/digunakan. Lanjutkan proses produksi normal."
            if decision_pass else
            "❌ Lakukan inspeksi 100% atau kembalikan ke supplier. Tinjau proses produksi."
        )
        st.warning(f"""
**💡 Rekomendasi Tindakan**

{rekomendasi}

- Rasio sampling: **{sampling_ratio:.1f}%** dari lot
- Confidence level: **~95%** (General Inspection Level II)
        """)

# ── TAB 2: VISUALISASI ────────────────────────
with tab2:
    st.markdown('<div class="section-title">Visualisasi Data Sampling</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Gauge
    with col1:
        gauge_color = AQUA if decision_pass else DANGER_COLOR
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=n_defects,
            delta={'reference': ac, 'increasing': {'color': DANGER_COLOR}, 'decreasing': {'color': AQUA}},
            title={'text': "Jumlah Defek vs Accept Number", 'font': {'color': '#c8e8f8', 'family': FONT_FAMILY, 'size': 14}},
            gauge={
                'axis': {'range': [0, max(re*2, n_defects*1.5, 5)], 'tickcolor': TICK_COLOR},
                'bar': {'color': gauge_color, 'thickness': 0.25},
                'bgcolor': 'rgba(10,30,60,0.5)',
                'borderwidth': 1,
                'bordercolor': 'rgba(255,255,255,0.15)',
                'steps': [
                    {'range': [0, ac],                              'color': 'rgba(0,201,177,0.12)'},
                    {'range': [ac, re],                             'color': 'rgba(243,156,18,0.12)'},
                    {'range': [re, max(re*2, n_defects*1.5, 5)],   'color': 'rgba(231,76,60,0.12)'},
                ],
                'threshold': {'line': {'color': DANGER_COLOR, 'width': 2.5}, 'thickness': 0.75, 'value': re}
            },
            number={'font': {'color': gauge_color, 'family': 'Exo 2, sans-serif', 'size': 38}}
        ))
        fig_gauge.update_layout(**aero_layout(height=320))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Donut
    with col2:
        good = max(sample_size - n_defects, 0)
        fig_pie = go.Figure(go.Pie(
            labels=['Baik', 'Defek'],
            values=[good, n_defects],
            hole=0.6,
            marker=dict(
                colors=[AQUA, DANGER_COLOR],
                line=dict(color='rgba(10,25,50,0.8)', width=2)
            ),
            textfont=dict(family=FONT_FAMILY, size=13, color='#e8f8ff'),
        ))
        fig_pie.update_layout(
            **aero_layout(
                height=320,
                title=dict(text='Komposisi Sampel', font=dict(family='Exo 2', color='#c8e8f8', size=14)),
                legend=dict(font=dict(color='#c8e8f8'))
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Sensitivity bar
    st.markdown('<div class="section-title">Analisis Sensitivitas — Keputusan per Jumlah Defek</div>', unsafe_allow_html=True)
    max_def = max(re * 3, 10)
    defect_range = list(range(0, max_def + 1))
    colors_bar   = [AQUA if d <= ac else DANGER_COLOR for d in defect_range]
    fig_bar = go.Figure(go.Bar(
        x=defect_range,
        y=defect_range,
        marker=dict(color=colors_bar, line=dict(color='rgba(255,255,255,0.08)', width=1)),
        text=['ACCEPT' if d <= ac else 'REJECT' for d in defect_range],
        textposition='auto',
        textfont=dict(family='Exo 2, sans-serif', size=10, color='#ffffff'),
    ))
    fig_bar.add_vline(x=ac+0.5, line_color=GOLD_COLOR, line_dash='dash', line_width=1.5,
                      annotation_text=f'Batas Ac={ac}', annotation_font_color=GOLD_COLOR)
    fig_bar.update_layout(
        **aero_layout(
            height=280,
            xaxis=dict(title='Jumlah Defek', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR),
            yaxis=dict(title='Jumlah Defek', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR),
            showlegend=False
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # OC Curve
    st.markdown('<div class="section-title">OC Curve — Kurva Karakteristik Operasi</div>', unsafe_allow_html=True)
    p_values  = np.linspace(0, 0.3, 200)
    pa_values = []
    for p in p_values:
        pa = sum(math.comb(sample_size, k) * (p**k) * ((1-p)**(sample_size-k)) for k in range(ac+1))
        pa_values.append(pa * 100)

    fig_oc = go.Figure()
    fig_oc.add_trace(go.Scatter(
        x=p_values*100, y=pa_values,
        mode='lines', name='P(Accept)',
        line=dict(color=AQUA, width=2.5),
        fill='tozeroy', fillcolor='rgba(0,201,177,0.07)'
    ))
    fig_oc.add_vline(x=aql_level, line_color=GOLD_COLOR, line_dash='dot',
                     annotation_text=f'AQL={aql_level}%', annotation_font_color=GOLD_COLOR)
    fig_oc.add_hline(y=95, line_color='rgba(255,255,255,0.3)', line_dash='dot',
                     annotation_text='95%', annotation_font_color=TICK_COLOR)
    fig_oc.update_layout(
        **aero_layout(
            height=300,
            xaxis=dict(title='Defect Rate (%)', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR),
            yaxis=dict(title='P(Accept) %', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR, range=[0,105]),
            legend=dict(font=dict(color='#c8e8f8'))
        )
    )
    st.plotly_chart(fig_oc, use_container_width=True)

# ── TAB 3: TABEL AQL ─────────────────────────
with tab3:
    st.markdown('<div class="section-title">Tabel Referensi AQL (ISO 2859-1 — Normal Inspection)</div>', unsafe_allow_html=True)

    rows = []
    for low, high, code in LOT_SIZE_TABLE:
        n   = SAMPLE_SIZE[code]
        row = {
            'Ukuran Lot': f"{low:,} – {high:,}" if high != float('inf') else f"≥ {low:,}",
            'Kode': code,
            'n Sampel': n,
        }
        for aql_v in [0.65, 1.0, 1.5, 2.5, 4.0, 6.5]:
            crit = AQL_TABLE[code].get(aql_v, (0, 1))
            row[f'AQL {aql_v}%'] = f"Ac={crit[0]}  Re={crit[1]}"
        rows.append(row)

    df_table = pd.DataFrame(rows)

    def highlight_current(row):
        if row['Kode'] == code_letter:
            return ['background-color: rgba(0,201,177,0.15); color: #00ffdd'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_table.style.apply(highlight_current, axis=1),
        use_container_width=True, height=420
    )
    st.caption(f"🟢 Baris yang di-highlight = kode {code_letter} sesuai lot size {lot_size:,}")

    st.markdown('<div class="section-title">Tabel Ukuran Lot → Kode Sampel</div>', unsafe_allow_html=True)
    st.markdown("""
| Ukuran Lot | Kode | n Sampel | Ukuran Lot | Kode | n Sampel |
|---|---|---|---|---|---|
| 2–8 | A | 2 | 501–1,200 | J | 80 |
| 9–15 | B | 3 | 1,201–3,200 | K | 125 |
| 16–25 | C | 5 | 3,201–10,000 | L | 200 |
| 26–50 | D | 8 | 10,001–35,000 | M | 315 |
| 51–90 | E | 13 | 35,001–150,000 | N | 500 |
| 91–150 | F | 20 | 150,001–500,000 | P | 800 |
| 151–280 | G | 32 | ≥ 500,001 | Q | 1,250 |
| 281–500 | H | 50 | | | |
""")

# ── TAB 4: LAPORAN ────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Laporan Hasil Sampling</div>', unsafe_allow_html=True)

    from datetime import datetime
    from zoneinfo import ZoneInfo
    from fpdf import FPDF
    import io

    # Mengunci waktu ke WIB
    waktu_jakarta = ZoneInfo("Asia/Jakarta")
    now = datetime.now(waktu_jakarta).strftime("%d %B %Y, %H:%M WIB")

    # 1. Teks Markdown untuk ditampilkan di layar Streamlit (Tetap menggunakan Emoji)
    report_text_markdown = f"""
## 📄 LAPORAN HASIL SAMPLING AQL
**Tanggal:** {now}

---

### Identifikasi Lot
| Parameter | Nilai |
|---|---|
| Nama Produk | {product_name} |
| Nomor Lot | {lot_number} |
| Inspektor | {inspector} |
| Tipe Inspeksi | {inspection_type} |

### Parameter Sampling (ISO 2859-1)
| Parameter | Nilai |
|---|---|
| Ukuran Lot | {lot_size:,} unit |
| Kode Sampel | {code_letter} |
| Ukuran Sampel (n) | {sample_size} unit |
| AQL Level | {aql_level}% |
| Accept Number (Ac) | {ac} |
| Reject Number (Re) | {re} |

### Hasil Pemeriksaan
| Parameter | Nilai |
|---|---|
| Jumlah Defek Ditemukan | {n_defects} unit |
| Defect Rate | {defect_rate:.3f}% |
| Keputusan | **{"ACCEPT ✅" if decision_pass else "REJECT ❌"}** |

### Dasar Keputusan
{"Lot **DITERIMA** karena jumlah defek ditemukan (" + str(n_defects) + ") tidak melebihi Accept Number (" + str(ac) + ") sesuai standar AQL " + str(aql_level) + "%." if decision_pass else "Lot **DITOLAK** karena jumlah defek ditemukan (" + str(n_defects) + ") mencapai atau melebihi Reject Number (" + str(re) + ") sesuai standar AQL " + str(aql_level) + "%."}

### Rekomendasi Tindakan
{"✅ Lot dapat diterima dan diteruskan ke proses selanjutnya. Pertahankan standar produksi saat ini." if decision_pass else "❌ Lot ditolak. Lakukan salah satu:\n1. Inspeksi 100% seluruh lot\n2. Kembalikan ke supplier (jika material dari luar)\n3. Lakukan analisis akar masalah (root cause analysis)\n4. Review dan perbaiki proses produksi"}

---
*Laporan ini dibuat otomatis menggunakan AQL Sampling Analyzer — Kelompok 7 LPK 2026*
*Standar Referensi: ISO 2859-1 (Sampling procedures for inspection by attributes)*
    """
    
    # Tampilkan laporan dalam bentuk Markdown di Tab 4 Streamlit
    st.markdown(report_text_markdown)

    # 2. PROSES GENERATE REKAYASA PDF (Membersihkan emoji agar PDF tidak error/corrupt)
    def buat_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        # Judul Laporan
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(200, 10, txt="LAPORAN HASIL SAMPLING AQL", ln=True, align='C')
        pdf.set_font("Helvetica", size=10)
        pdf.cell(200, 10, txt=f"Tanggal Cetak: {now}", ln=True, align='C')
        pdf.ln(10)
        
        # Helper untuk buat baris tebal-tipis (key-value)
        def tambah_baris(label, nilai):
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.cell(60, 8, txt=f"{label}:", border=0)
            pdf.set_font("Helvetica", size=11)
            pdf.cell(130, 8, txt=str(nilai), border=0, ln=True)

        # Bagian Identifikasi
        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(200, 8, txt="I. IDENTIFIKASI LOT", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        tambah_baris("Nama Produk", product_name)
        tambah_baris("Nomor Lot", lot_number)
        tambah_baris("Inspektor", inspector)
        tambah_baris("Tipe Inspeksi", inspection_type)
        pdf.ln(5)

        # Bagian Parameter
        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(200, 8, txt="II. PARAMETER SAMPLING (ISO 2859-1)", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        tambah_baris("Ukuran Lot", f"{lot_size:,} unit")
        tambah_baris("Kode Sampel", code_letter)
        tambah_baris("Ukuran Sampel (n)", f"{sample_size} unit")
        tambah_baris("AQL Level", f"{aql_level}%")
        tambah_baris("Accept Number (Ac)", ac)
        tambah_baris("Reject Number (Re)", re)
        pdf.ln(5)

        # Bagian Hasil
        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(200, 8, txt="III. HASIL PEMERIKSAAN & KEPUTUSAN", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        tambah_baris("Jumlah Defek Ditemukan", f"{n_defects} unit")
        tambah_baris("Defect Rate", f"{defect_rate:.3f}%")
        
        # Status Keputusan Berwarna / Bold teks biasa (Tanpa emoji)
        status_keputusan = "ACCEPT" if decision_pass else "REJECT"
        tambah_baris("Keputusan Akhir", status_keputusan)
        pdf.ln(4)

        # Dasar Keputusan & Rekomendasi (Menggunakan multi_cell agar teks panjang otomatis turun ke bawah)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(200, 6, txt="Dasar Keputusan:", ln=True)
        pdf.set_font("Helvetica", size=11)
        txt_dasar = f"Lot DITERIMA karena jumlah defek ditemukan ({n_defects}) tidak melebihi Accept Number ({ac}) sesuai standar AQL {aql_level}%." if decision_pass else f"Lot DITOLAK karena jumlah defek ditemukan ({n_defects}) mencapai atau melebihi Reject Number ({re}) sesuai standar AQL {aql_level}%."
        pdf.multi_cell(190, 6, txt=txt_dasar)
        pdf.ln(4)

        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(200, 6, txt="Rekomendasi Tindakan:", ln=True)
        pdf.set_font("Helvetica", size=11)
        txt_rekomendasi = "Lot dapat diterima dan diteruskan ke proses selanjutnya. Pertahankan standar produksi saat ini." if decision_pass else "Lot ditolak. Lakukan salah satu:\n1. Inspeksi 100% seluruh lot\n2. Kembalikan ke supplier\n3. Lakukan analisis akar masalah (root cause analysis)\n4. Review dan perbaiki proses produksi"
        pdf.multi_cell(190, 6, txt=txt_rekomendasi)
        
        pdf.ln(15)
        pdf.set_font("Helvetica", style="I", size=9)
        pdf.cell(200, 5, txt="Laporan ini dibuat otomatis menggunakan AQL Sampling Analyzer - Kelompok 7 LPK 2026", ln=True, align='C')
        pdf.cell(200, 5, txt="Standar Referensi: ISO 2859-1", ln=True, align='C')
        
        # Mengembalikan data sebagai bytes buffer agar bisa langsung didownload Streamlit
        return pdf.output()

    # Generate file PDF ke dalam memori buffer RAM
    pdf_data = buat_pdf()

    # 3. BUTTON DOWNLOAD (Ubah dari .txt menjadi .pdf)
    st.download_button(
        label="📥 Unduh Laporan Resmi (.pdf)",
        data=bytes(pdf_data),
        file_name=f"laporan_aql_{lot_number.replace('-','_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("""
<div style="text-align:center; color:var(--muted); font-family:Rajdhani; letter-spacing:1px; font-size:0.85rem; margin-top:10px;">
    AQL SAMPLING ANALYZER · KELOMPOK 7 · LPK 2026<br>
    Standar: ISO 2859-1 · General Inspection Level II · Single Sampling Normal
</div>
""", unsafe_allow_html=True)
