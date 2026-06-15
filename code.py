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
# FRUTIGER AERO CSS (MENDUKUNG LIGHT & DARK MODE)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&family=Exo+2:wght@300;400;600;700&display=swap');

/* VARIABEL GLOBAL KEDUA TEMA */
:root {
    --green-fresh: #27ae60;
    --danger:      #e74c3c;
    --warn:        #f39c12;
}

/* ── TEMA GELAP (DARK MODE) ── */
@media (prefers-color-scheme: dark) {
    :root {
        --aqua:        #00c9b1;
        --aqua-bright: #00ffdd;
        --aqua-glow:   rgba(0,201,177,0.35);
        --white-rim:   rgba(255,255,255,0.28);
        --text-bright: #e8f8ff;
        --text-mid:    #a8d8ea;
        --text-soft:   #6ba3be;
        --bg-grad: linear-gradient(160deg, #061728 0%, #0d2f50 35%, #07213a 65%, #041220 100%);
        --card-bg: linear-gradient(145deg, rgba(255,255,255,0.13) 0%, rgba(0,150,200,0.08) 100%);
        --sidebar-bg: linear-gradient(180deg, rgba(6,23,40,0.97) 0%, rgba(10,37,64,0.97) 100%);
        --input-bg: linear-gradient(145deg, rgba(255,255,255,0.08) 0%, rgba(0,100,160,0.06) 100%);
        --header-bg: linear-gradient(135deg, rgba(255,255,255,0.13) 0%, rgba(0,180,255,0.10) 40%, rgba(0,201,177,0.08) 100%);
        --metric-val-color: linear-gradient(135deg, #ffffff, #00c9b1);
    }
}

/* ── TEMA TERANG (LIGHT MODE) ── */
@media (prefers-color-scheme: light) {
    :root {
        --aqua:        #009988;
        --aqua-bright: #00c9b1;
        --aqua-glow:   rgba(0,153,136,0.35);
        --white-rim:   rgba(255,255,255,0.9);
        --text-bright: #0f172a;
        --text-mid:    #334155;
        --text-soft:   #475569;
        --bg-grad: linear-gradient(160deg, #e0f2fe 0%, #bae6fd 35%, #e0f2fe 65%, #f0f9ff 100%);
        --card-bg: linear-gradient(145deg, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0.4) 100%);
        --sidebar-bg: linear-gradient(180deg, rgba(224,242,254,0.97) 0%, rgba(186,230,253,0.97) 100%);
        --input-bg: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        --header-bg: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(186,230,253,0.5) 40%, rgba(153,246,228,0.5) 100%);
        --metric-val-color: linear-gradient(135deg, #0f172a, #009988);
    }
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
    background: var(--header-bg);
    border: 1px solid var(--white-rim);
    border-radius: 20px;
    padding: 32px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.1),
        inset 0 1px 0 rgba(255,255,255,0.4);
}
.app-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
}
.app-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: var(--metric-val-color);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    margin: 0;
    text-shadow: none;
}
.app-subtitle {
    font-family: 'Nunito', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-mid);
    margin-top: 6px;
    letter-spacing: 1.5px;
}
.header-badge {
    display: inline-block;
    background: rgba(0,201,177,0.18);
    border: 1px solid var(--aqua);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.75rem;
    color: var(--aqua);
    letter-spacing: 1px;
    margin-top: 10px;
    font-weight: 700;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--white-rim);
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: var(--aqua);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12), 0 0 25px var(--aqua-glow);
    transform: translateY(-2px);
}
.metric-value {
    font-family: 'Exo 2', sans-serif;
    font-size: 2.3rem;
    font-weight: 700;
    background: var(--metric-val-color);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.72rem;
    color: var(--text-soft);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-weight: 700;
}

/* ── RESULT BADGES ── */
.result-pass {
    background: linear-gradient(135deg, rgba(39,174,96,0.15) 0%, rgba(0,201,177,0.1) 100%);
    border: 1.5px solid rgba(39,174,96,0.6);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    backdrop-filter: blur(12px);
}
.result-pass-text {
    font-family: 'Exo 2', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--green-fresh);
    letter-spacing: 2px;
}
.result-fail {
    background: linear-gradient(135deg, rgba(231,76,60,0.15) 0%, rgba(192,57,43,0.08) 100%);
    border: 1.5px solid rgba(231,76,60,0.6);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    backdrop-filter: blur(12px);
}
.result-fail-text {
    font-family: 'Exo 2', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--danger);
    letter-spacing: 2px;
}
.result-sub {
    font-size: 0.95rem;
    color: var(--text-mid);
    margin-top: 8px;
    font-weight: 600;
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

/* ── SIDEBAR ── */
div[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--white-rim) !important;
    backdrop-filter: blur(20px) !important;
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
    background: var(--input-bg) !important;
    border: 1px solid var(--white-rim) !important;
    color: var(--text-bright) !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--aqua) !important;
    box-shadow: 0 0 0 3px var(--aqua-glow) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,201,177,0.9) 0%, rgba(0,150,210,0.85) 100%) !important;
    color: #ffffff !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
    text-transform: uppercase !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border: 1px solid var(--white-rim) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── ALERTS / INFO ── */
.stInfo, .stWarning, .stSuccess, .stError {
    border-radius: 12px !important;
    backdrop-filter: blur(8px) !important;
    background: var(--card-bg) !important;
    color: var(--text-bright) !important;
    border: 1px solid var(--white-rim) !important;
}

/* ── MISC OVERRIDES ── */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-bright) !important;
    font-family: 'Exo 2', sans-serif !important;
}
p, span, li { color: var(--text-bright) !important; font-weight: 500; }
.stMarkdown p { color: var(--text-mid) !important; }

/* Download button */
.stDownloadButton > button {
    background: var(--card-bg) !important;
    border: 1px solid var(--aqua) !important;
    color: var(--aqua) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
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
# PLOTLY THEME (TRANSPARENT BACKGROUND)
# ─────────────────────────────────────────────
# Kita membuat background plotly menjadi transparan (rgba(0,0,0,0))
# sehingga ia otomatis mengikuti warna tema terang/gelap dari CSS Streamlit
def aero_layout(**kwargs):
    base = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Nunito, sans-serif', size=12),
        margin=dict(l=24, r=24, t=40, b=24),
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
# OPENING / INTRODUCTION
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
    st.markdown("### 📥 Data kecacatan")
    n_defects = st.number_input("Jumlah kecacatan Ditemukan", min_value=0, max_value=9999, value=3)
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
        (str(n_defects),         "kecacatan Ditemukan"),
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
            <div class="result-sub">kecacatan ({n_defects}) ≤ Ac ({ac}) — Lot memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-fail">
            <div class="result-fail-text">❌ LOT DITOLAK (REJECT)</div>
            <div class="result-sub">kecacatan ({n_defects}) ≥ Re ({re}) — Lot tidak memenuhi standar AQL {aql_level}%</div>
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
    
    AQUA = '#00c9b1'
    DANGER_COLOR = '#e74c3c'
    GOLD_COLOR = '#f5d76e'

    # Gauge
    with col1:
        gauge_color = AQUA if decision_pass else DANGER_COLOR
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=n_defects,
            delta={'reference': ac, 'increasing': {'color': DANGER_COLOR}, 'decreasing': {'color': AQUA}},
            title={'text': "Jumlah kecacatan vs Accept Number", 'font': {'family': 'Nunito, sans-serif', 'size': 14}},
            gauge={
                'axis': {'range': [0, max(re*2, n_defects*1.5, 5)]},
                'bar': {'color': gauge_color, 'thickness': 0.25},
                'bgcolor': 'rgba(128,128,128,0.2)',
                'borderwidth': 1,
                'bordercolor': 'rgba(128,128,128,0.2)',
                'steps': [
                    {'range': [0, ac],                              'color': 'rgba(0,201,177,0.15)'},
                    {'range': [ac, re],                             'color': 'rgba(243,156,18,0.15)'},
                    {'range': [re, max(re*2, n_defects*1.5, 5)],   'color': 'rgba(231,76,60,0.15)'},
                ],
                'threshold': {'line': {'color': DANGER_COLOR, 'width': 2.5}, 'thickness': 0.75, 'value': re}
            },
            number={'font': {'color': gauge_color, 'family': 'Exo 2, sans-serif', 'size': 38}}
        ))
        fig_gauge.update_layout(**aero_layout(height=320))
        # Penambahan theme="streamlit" memastikan text label otomatis beradaptasi dengan mode terang/gelap
        st.plotly_chart(fig_gauge, use_container_width=True, theme="streamlit")

    # Donut
    with col2:
        good = max(sample_size - n_defects, 0)
        fig_pie = go.Figure(go.Pie(
            labels=['Baik', 'kecacatan'],
            values=[good, n_defects],
            hole=0.6,
            marker=dict(
                colors=[AQUA, DANGER_COLOR],
                line=dict(color='rgba(128,128,128,0.2)', width=1)
            ),
            textfont=dict(family='Nunito, sans-serif', size=13),
        ))
        fig_pie.update_layout(
            **aero_layout(
                height=320,
                title=dict(text='Komposisi Sampel', font=dict(family='Exo 2', size=14))
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit")

    # Sensitivity bar
    st.markdown('<div class="section-title">Analisis Sensitivitas — Keputusan per Jumlah kecacatan</div>', unsafe_allow_html=True)
    max_def = max(re * 3, 10)
    defect_range = list(range(0, max_def + 1))
    colors_bar   = [AQUA if d <= ac else DANGER_COLOR for d in defect_range]
    fig_bar = go.Figure(go.Bar(
        x=defect_range,
        y=defect_range,
        marker=dict(color=colors_bar, line=dict(color='rgba(128,128,128,0.2)', width=1)),
        text=['ACCEPT' if d <= ac else 'REJECT' for d in defect_range],
        textposition='auto',
        textfont=dict(family='Exo 2, sans-serif', size=10, color='#ffffff'),
    ))
    fig_bar.add_vline(x=ac+0.5, line_color=GOLD_COLOR, line_dash='dash', line_width=1.5,
                      annotation_text=f'Batas Ac={ac}', annotation_font_color=GOLD_COLOR)
    fig_bar.update_layout(
        **aero_layout(
            height=280,
            xaxis=dict(title='Jumlah kecacatan'),
            yaxis=dict(title='Jumlah kecacatan'),
            showlegend=False
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit")

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
        fill='tozeroy', fillcolor='rgba(0,201,177,0.1)'
    ))
    fig_oc.add_vline(x=aql_level, line_color=GOLD_COLOR, line_dash='dot',
                     annotation_text=f'AQL={aql_level}%', annotation_font_color=GOLD_COLOR)
    fig_oc.add_hline(y=95, line_color='rgba(128,128,128,0.5)', line_dash='dot',
                     annotation_text='95%')
    fig_oc.update_layout(
        **aero_layout(
            height=300,
            xaxis=dict(title='Defect Rate (%)'),
            yaxis=dict(title='P(Accept) %', range=[0,105])
        )
    )
    st.plotly_chart(fig_oc, use_container_width=True, theme="streamlit")

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
            return ['background-color: rgba(0,201,177,0.3); font-weight: bold;'] * len(row)
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
| Jumlah kecacatan Ditemukan | {n_defects} unit |
| Defect Rate | {defect_rate:.3f}% |
| Keputusan | **{"ACCEPT ✅" if decision_pass else "REJECT ❌"}** |

### Dasar Keputusan
{"Lot **DITERIMA** karena jumlah kecacatan ditemukan (" + str(n_defects) + ") tidak melebihi Accept Number (" + str(ac) + ") sesuai standar AQL " + str(aql_level) + "%." if decision_pass else "Lot **DITOLAK** karena jumlah kecacatan ditemukan (" + str(n_defects) + ") mencapai atau melebihi Reject Number (" + str(re) + ") sesuai standar AQL " + str(aql_level) + "%."}

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
        tambah_baris("Jumlah kecacatan Ditemukan", f"{n_defects} unit")
        tambah_baris("Defect Rate", f"{defect_rate:.3f}%")
        
        # Status Keputusan Berwarna / Bold teks biasa (Tanpa emoji)
        status_keputusan = "ACCEPT" if decision_pass else "REJECT"
        tambah_baris("Keputusan Akhir", status_keputusan)
        pdf.ln(4)

        # Dasar Keputusan & Rekomendasi (Menggunakan multi_cell agar teks panjang otomatis turun ke bawah)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(200, 6, txt="Dasar Keputusan:", ln=True)
        pdf.set_font("Helvetica", size=11)
        txt_dasar = f"Lot DITERIMA karena jumlah kecacatan ditemukan ({n_defects}) tidak melebihi Accept Number ({ac}) sesuai standar AQL {aql_level}%." if decision_pass else f"Lot DITOLAK karena jumlah kecacatan ditemukan ({n_defects}) mencapai atau melebihi Reject Number ({re}) sesuai standar AQL {aql_level}%."
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
<div style="text-align:center; font-family:'Nunito'; letter-spacing:1px; font-size:0.85rem; margin-top:10px; opacity:0.7;">
    AQL SAMPLING ANALYZER · KELOMPOK 7 · LPK 2026<br>
    Standar: ISO 2859-1 · General Inspection Level II · Single Sampling Normal
</div>
""", unsafe_allow_html=True)
