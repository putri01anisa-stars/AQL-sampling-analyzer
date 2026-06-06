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
    page_title="Penganalisis Sampling AQL",
    page_icon="⚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS STYLING — ADAPTIVE DARK/LIGHT
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── LIGHT MODE (default) ── */
:root {
    --primary: #1a5f4a;
    --primary-light: #2d8c6e;
    --accent: #c0392b;
    --bg: #f5f2ec;
    --surface: #ffffff;
    --card: #faf8f4;
    --border: #d6cfc3;
    --border-strong: #b8ae9e;
    --text: #1a1714;
    --text-secondary: #4a4540;
    --muted: #7a726a;
    --shadow: rgba(0,0,0,0.08);
    --primary-bg: rgba(26,95,74,0.07);
    --accent-bg: rgba(192,57,43,0.08);
    --highlight-row: rgba(26,95,74,0.08);
}

/* ── DARK MODE ── */
@media (prefers-color-scheme: dark) {
    :root {
        --primary: #3dba90;
        --primary-light: #5acfa6;
        --accent: #e05c4a;
        --bg: #111410;
        --surface: #1a1f18;
        --card: #1e241c;
        --border: #2c3628;
        --border-strong: #3d4a36;
        --text: #e8ede2;
        --text-secondary: #b0bba8;
        --muted: #6e7c68;
        --shadow: rgba(0,0,0,0.3);
        --primary-bg: rgba(61,186,144,0.08);
        --accent-bg: rgba(224,92,74,0.1);
        --highlight-row: rgba(61,186,144,0.12);
    }
}

/* ── BASE ── */
.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

/* ── HEADER ── */
.app-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--primary);
    border-radius: 4px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px var(--shadow);
}
.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.5px;
    margin: 0;
}
.app-title span {
    color: var(--text);
    font-weight: 600;
}
.app-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 6px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.header-badge {
    display: inline-block;
    background: var(--primary-bg);
    color: var(--primary);
    border: 1px solid var(--primary);
    border-radius: 2px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 2px 8px;
    margin-top: 10px;
    letter-spacing: 1px;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--primary);
    border-radius: 4px;
    padding: 16px 18px;
    text-align: left;
    box-shadow: 0 1px 6px var(--shadow);
    transition: border-color 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    border-color: var(--primary-light);
    box-shadow: 0 3px 12px var(--shadow);
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    line-height: 1;
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 5px;
}

/* ── RESULT BADGES ── */
.result-pass {
    background: var(--primary-bg);
    border: 1.5px solid var(--primary);
    border-left: 5px solid var(--primary);
    border-radius: 4px;
    padding: 20px 24px;
    text-align: left;
    margin: 12px 0;
}
.result-pass .result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: 0.5px;
}
.result-fail {
    background: var(--accent-bg);
    border: 1.5px solid var(--accent);
    border-left: 5px solid var(--accent);
    border-radius: 4px;
    padding: 20px 24px;
    text-align: left;
    margin: 12px 0;
}
.result-fail .result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.5px;
}
.result-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-top: 6px;
    font-style: italic;
}

/* ── SECTION TITLES ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 1px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin: 24px 0 14px 0;
    text-transform: uppercase;
}
.section-title::before {
    content: '// ';
    color: var(--primary);
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}

/* ── SIDEBAR ── */
div[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
div[data-testid="stSidebar"] * {
    color: var(--text) !important;
}
div[data-testid="stSidebar"] .stMarkdown p {
    color: var(--muted) !important;
}

/* ── INPUTS ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 4px !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px var(--primary-bg) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: var(--primary) !important;
    color: var(--bg) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 10px 28px !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: var(--primary-light) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px var(--shadow) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--border) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.5px !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
    border-bottom: 2px solid var(--primary) !important;
}

/* ── TEXT ── */
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }
p, span, li { color: var(--text); }
.stMarkdown p { color: var(--text-secondary) !important; }
.stCaption p, .stCaption { color: var(--muted) !important; }

/* ── INFO/WARNING BOXES ── */
.stInfo {
    background: var(--primary-bg) !important;
    border: 1px solid var(--primary) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
}
.stWarning {
    background: rgba(180,120,0,0.08) !important;
    border: 1px solid rgba(180,120,0,0.4) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--primary) !important;
    border: 1.5px solid var(--primary) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 4px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.stDownloadButton > button:hover {
    background: var(--primary-bg) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AQL DATA TABLES (ISO 2859-1)
# ─────────────────────────────────────────────

LOT_SIZE_TABLE = [
    (2, 8, 'A'),
    (9, 15, 'B'),
    (16, 25, 'C'),
    (26, 50, 'D'),
    (51, 90, 'E'),
    (91, 150, 'F'),
    (151, 280, 'G'),
    (281, 500, 'H'),
    (501, 1200, 'J'),
    (1201, 3200, 'K'),
    (3201, 10000, 'L'),
    (10001, 35000, 'M'),
    (35001, 150000, 'N'),
    (150001, 500000, 'P'),
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

def get_defect_rate(n_cacatan, sample_size):
    return (n_cacatan / sample_size) * 100 if sample_size > 0 else 0

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">⚗ Penganalisis <span>Sampling AQL</span></div>
    <div class="app-subtitle">Pengolahan Data Sampling &amp; Batas Mutu Penerimaan &nbsp;·&nbsp; ISO 2859-1 &nbsp;·&nbsp; Kelompok 7</div>
    <div class="header-badge">ISO 2859-1 · Inspeksi Atribut Tunggal Normal · Tingkat Pemeriksaan Umum II</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Pengaturan Sampling")
    st.markdown("---")

    lot_size = st.number_input("Ukuran Lot (Tumpak)", min_value=2, max_value=999999, value=1000, step=50)
    aql_level = st.selectbox("Tingkat AQL (%)", options=AQL_LEVELS, index=6, format_func=lambda x: f"{x}%")
    inspection_type = st.selectbox("Jenis Pemeriksaan", ["Normal", "Ketat", "Longgar"])

    st.markdown("---")
    st.markdown("### Data Kecacatan")
    n_cacatan = st.number_input("Jumlah Cacat Ditemukan", min_value=0, max_value=9999, value=3)

    st.markdown("---")
    st.markdown("### Informasi Lot")
    product_name = st.text_input("Nama Produk / Lot", value="Sampel Kimia A")
    lot_number   = st.text_input("Nomor Lot", value="LOT-2026-001")
    inspector    = st.text_input("Nama Pemeriksa", value="Kelompok 7")

    analyze_btn = st.button("ANALISIS SEKARANG", use_container_width=True)

# ─────────────────────────────────────────────
# KALKULASI
# ─────────────────────────────────────────────
code_letter = get_code_letter(lot_size)
sample_size = SAMPLE_SIZE.get(code_letter, 2)
criteria    = get_aql_criteria(code_letter, aql_level)

if criteria:
    ac, re = criteria
else:
    ac, re = 0, 1

tingkat_cacat = get_defect_rate(n_cacatan, sample_size)
diterima      = n_cacatan <= ac

# Plotly template sesuai tema — gunakan plotly_white agar terbaca di kedua mode
PLOT_BG    = 'rgba(0,0,0,0)'   # transparan, ikuti CSS
PAPER_BG   = 'rgba(0,0,0,0)'
GRID_COLOR = 'rgba(128,128,128,0.15)'
TEXT_COLOR = '#555555'          # abu netral, terbaca di keduanya
PRIMARY_CLR = '#2d8c6e'
ACCENT_CLR  = '#c0392b'

def plotly_base_layout(height=300):
    return dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COLOR, family='DM Sans'),
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
    )

# ─────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Hasil Analisis",
    "Visualisasi",
    "Tabel AQL",
    "Laporan"
])

# ── TAB 1: HASIL ──────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Parameter Lot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{lot_size:,}</div><div class="metric-label">Ukuran Lot</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{code_letter}</div><div class="metric-label">Kode Sampel</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{sample_size}</div><div class="metric-label">Ukuran Sampel (n)</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{aql_level}%</div><div class="metric-label">Tingkat AQL</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Kriteria Penerimaan</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{ac}</div><div class="metric-label">Bilangan Terima (Ac)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{re}</div><div class="metric-label">Bilangan Tolak (Re)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{n_cacatan}</div><div class="metric-label">Cacat Ditemukan</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{tingkat_cacat:.2f}%</div><div class="metric-label">Tingkat Kecacatan</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Keputusan Sampling</div>', unsafe_allow_html=True)
    if diterima:
        st.markdown(f"""
        <div class="result-pass">
            <div class="result-label">LOT DITERIMA</div>
            <div class="result-sub">Jumlah cacat ({n_cacatan}) &le; Bilangan Terima ({ac}) &mdash; Lot memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-fail">
            <div class="result-label">LOT DITOLAK</div>
            <div class="result-sub">Jumlah cacat ({n_cacatan}) &ge; Bilangan Tolak ({re}) &mdash; Lot tidak memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">Keterangan &amp; Rekomendasi</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"""
**Identitas Lot**
- **Produk:** {product_name}
- **Nomor Lot:** {lot_number}
- **Pemeriksa:** {inspector}
- **Jenis Pemeriksaan:** {inspection_type}
        """)
    with col_b:
        rasio_sampling = (sample_size / lot_size) * 100
        if diterima:
            rekomendasi = "Lot dapat dikirim atau digunakan. Lanjutkan proses produksi secara normal."
        else:
            rekomendasi = "Lakukan pemeriksaan 100% atau kembalikan kepada pemasok. Tinjau ulang proses produksi."
        st.warning(f"""
**Rekomendasi Tindakan**

{rekomendasi}

- Rasio pengambilan sampel: **{rasio_sampling:.1f}%** dari lot
- Tingkat kepercayaan: **~95%** (Tingkat Pemeriksaan Umum II)
        """)

# ── TAB 2: VISUALISASI ────────────────────────
with tab2:
    st.markdown('<div class="section-title">Visualisasi Data Sampling</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        batas_maks = max(re * 2, n_cacatan * 1.5, 5)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=n_cacatan,
            delta={
                'reference': ac,
                'increasing': {'color': ACCENT_CLR},
                'decreasing': {'color': PRIMARY_CLR}
            },
            title={
                'text': "Cacat vs Bilangan Terima",
                'font': {'color': TEXT_COLOR, 'family': 'Syne', 'size': 14}
            },
            gauge={
                'axis': {'range': [0, batas_maks], 'tickcolor': TEXT_COLOR},
                'bar': {'color': PRIMARY_CLR if diterima else ACCENT_CLR},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 1,
                'bordercolor': GRID_COLOR,
                'steps': [
                    {'range': [0, ac], 'color': 'rgba(45,140,110,0.12)'},
                    {'range': [ac, re], 'color': 'rgba(255,165,0,0.1)'},
                    {'range': [re, batas_maks], 'color': 'rgba(192,57,43,0.1)'},
                ],
                'threshold': {
                    'line': {'color': ACCENT_CLR, 'width': 3},
                    'thickness': 0.75,
                    'value': re,
                }
            },
            number={'font': {'color': PRIMARY_CLR if diterima else ACCENT_CLR, 'family': 'Syne', 'size': 36}}
        ))
        fig_gauge.update_layout(**plotly_base_layout(320))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        baik = max(sample_size - n_cacatan, 0)
        fig_pie = go.Figure(go.Pie(
            labels=['Baik', 'Cacat'],
            values=[baik, n_cacatan],
            hole=0.55,
            marker=dict(
                colors=[PRIMARY_CLR, ACCENT_CLR],
                line=dict(color='white', width=2)
            ),
            textfont=dict(family='DM Mono', size=13),
        ))
        fig_pie.update_layout(
            **plotly_base_layout(320),
            title=dict(text='Komposisi Sampel', font=dict(family='Syne', color=TEXT_COLOR, size=14)),
            legend=dict(font=dict(color=TEXT_COLOR))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="section-title">Analisis Kepekaan — Keputusan per Jumlah Cacat</div>', unsafe_allow_html=True)
    maks_cacat  = max(re * 3, 10)
    rentang_cacat = list(range(0, maks_cacat + 1))
    warna_bar   = [PRIMARY_CLR if d <= ac else ACCENT_CLR for d in rentang_cacat]
    fig_bar = go.Figure(go.Bar(
        x=rentang_cacat,
        y=rentang_cacat,
        marker=dict(color=warna_bar),
        text=['Terima' if d <= ac else 'Tolak' for d in rentang_cacat],
        textposition='auto',
        textfont=dict(family='DM Mono', size=10, color='white'),
    ))
    fig_bar.add_vline(x=ac + 0.5, line_color='#b8860b', line_dash='dash', line_width=2,
                      annotation_text=f'Batas Ac={ac}',
                      annotation_font_color='#b8860b')
    fig_bar.update_layout(
        **plotly_base_layout(280),
        xaxis=dict(title='Jumlah Cacat', gridcolor=GRID_COLOR, color=TEXT_COLOR),
        yaxis=dict(title='Jumlah Cacat', gridcolor=GRID_COLOR, color=TEXT_COLOR),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="section-title">Kurva OC — Kurva Karakteristik Operasi</div>', unsafe_allow_html=True)
    p_values = np.linspace(0, 0.3, 200)
    pa_values = []
    for p in p_values:
        pa = sum(
            math.comb(sample_size, k) * (p**k) * ((1-p)**(sample_size-k))
            for k in range(ac + 1)
        )
        pa_values.append(pa * 100)

    fig_oc = go.Figure()
    fig_oc.add_trace(go.Scatter(
        x=p_values * 100, y=pa_values,
        mode='lines', name='P(Diterima)',
        line=dict(color=PRIMARY_CLR, width=2.5),
        fill='tozeroy', fillcolor='rgba(45,140,110,0.08)'
    ))
    fig_oc.add_vline(x=aql_level, line_color='#b8860b', line_dash='dot',
                     annotation_text=f'AQL={aql_level}%',
                     annotation_font_color='#b8860b')
    fig_oc.add_hline(y=95, line_color=TEXT_COLOR, line_dash='dot',
                     annotation_text='95% Diterima',
                     annotation_font_color=TEXT_COLOR)
    fig_oc.update_layout(
        **plotly_base_layout(300),
        xaxis=dict(title='Tingkat Kecacatan (%)', gridcolor=GRID_COLOR, color=TEXT_COLOR),
        yaxis=dict(title='P(Diterima) %', gridcolor=GRID_COLOR, color=TEXT_COLOR, range=[0, 105]),
        legend=dict(font=dict(color=TEXT_COLOR))
    )
    st.plotly_chart(fig_oc, use_container_width=True)

# ── TAB 3: TABEL AQL ─────────────────────────
with tab3:
    st.markdown('<div class="section-title">Tabel Acuan AQL (ISO 2859-1 — Pemeriksaan Normal)</div>', unsafe_allow_html=True)

    baris = []
    for low, high, code in LOT_SIZE_TABLE:
        n = SAMPLE_SIZE[code]
        baris_data = {
            'Ukuran Lot': f"{low:,} – {high:,}" if high != float('inf') else f"≥ {low:,}",
            'Kode': code,
            'n Sampel': n
        }
        for aql_v in [0.65, 1.0, 1.5, 2.5, 4.0, 6.5]:
            crit = AQL_TABLE[code].get(aql_v, (0, 1))
            baris_data[f'AQL {aql_v}%'] = f"Ac={crit[0]} Re={crit[1]}"
        baris.append(baris_data)

    df_table = pd.DataFrame(baris)

    def sorot_baris(row):
        if row['Kode'] == code_letter:
            return ['background-color: rgba(45,140,110,0.15); font-weight: 600'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_table.style.apply(sorot_baris, axis=1),
        use_container_width=True, height=420
    )
    st.caption(f"Baris yang disorot = kode {code_letter} sesuai ukuran lot {lot_size:,}")

    st.markdown('<div class="section-title">Tabel Ukuran Lot ke Kode Sampel</div>', unsafe_allow_html=True)
    st.markdown("""
| Ukuran Lot | Kode | n Sampel | Ukuran Lot | Kode | n Sampel |
|---|:---:|:---:|---|:---:|:---:|
| 2 – 8 | A | 2 | 501 – 1.200 | J | 80 |
| 9 – 15 | B | 3 | 1.201 – 3.200 | K | 125 |
| 16 – 25 | C | 5 | 3.201 – 10.000 | L | 200 |
| 26 – 50 | D | 8 | 10.001 – 35.000 | M | 315 |
| 51 – 90 | E | 13 | 35.001 – 150.000 | N | 500 |
| 91 – 150 | F | 20 | 150.001 – 500.000 | P | 800 |
| 151 – 280 | G | 32 | ≥ 500.001 | Q | 1.250 |
| 281 – 500 | H | 50 | | | |
""")

# ── TAB 4: LAPORAN ────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Laporan Hasil Pemeriksaan</div>', unsafe_allow_html=True)

    from datetime import datetime
    sekarang = datetime.now().strftime("%d %B %Y, %H:%M")

    teks_laporan = f"""
## LAPORAN HASIL SAMPLING AQL
**Tanggal:** {sekarang}

---

### Identifikasi Lot
| Parameter | Nilai |
|---|---|
| Nama Produk | {product_name} |
| Nomor Lot | {lot_number} |
| Pemeriksa | {inspector} |
| Jenis Pemeriksaan | {inspection_type} |

### Parameter Sampling (ISO 2859-1)
| Parameter | Nilai |
|---|---|
| Ukuran Lot | {lot_size:,} unit |
| Kode Sampel | {code_letter} |
| Ukuran Sampel (n) | {sample_size} unit |
| Tingkat AQL | {aql_level}% |
| Bilangan Terima (Ac) | {ac} |
| Bilangan Tolak (Re) | {re} |

### Hasil Pemeriksaan
| Parameter | Nilai |
|---|---|
| Jumlah Cacat Ditemukan | {n_cacatan} unit |
| Tingkat Kecacatan | {tingkat_cacat:.3f}% |
| Keputusan | **{"DITERIMA" if diterima else "DITOLAK"}** |

### Dasar Keputusan
{"Lot **DITERIMA** karena jumlah cacat (" + str(n_cacatan) + ") tidak melebihi Bilangan Terima (" + str(ac) + ") sesuai standar AQL " + str(aql_level) + "%." if diterima else "Lot **DITOLAK** karena jumlah cacat (" + str(n_cacatan) + ") mencapai atau melebihi Bilangan Tolak (" + str(re) + ") sesuai standar AQL " + str(aql_level) + "%."}

### Rekomendasi Tindakan
{"Lot dapat diterima dan diteruskan ke proses selanjutnya. Pertahankan standar produksi saat ini." if diterima else "Lot ditolak. Lakukan salah satu tindakan berikut:\\n1. Pemeriksaan 100% atas seluruh lot\\n2. Pengembalian kepada pemasok (jika bahan dari luar)\\n3. Analisis akar penyebab masalah (root cause analysis)\\n4. Peninjauan dan perbaikan proses produksi"}

---
*Laporan ini dibuat secara otomatis menggunakan Penganalisis Sampling AQL — Kelompok 7 LPK 2026*
*Standar Acuan: ISO 2859-1 (Prosedur Pengambilan Sampel untuk Pemeriksaan Atribut)*
"""

    st.markdown(teks_laporan)

    st.download_button(
        label="Unduh Laporan (.txt)",
        data=teks_laporan,
        file_name=f"laporan_aql_{lot_number.replace('-','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("""
<div style="text-align:center; color:var(--muted); font-family:'DM Mono',monospace; letter-spacing:1px; font-size:0.78rem; margin-top:10px;">
    PENGANALISIS SAMPLING AQL &nbsp;·&nbsp; KELOMPOK 7 &nbsp;·&nbsp; LPK 2026<br>
    Standar: ISO 2859-1 &nbsp;·&nbsp; Tingkat Pemeriksaan Umum II &nbsp;·&nbsp; Pengambilan Sampel Tunggal Normal
</div>
""", unsafe_allow_html=True)
