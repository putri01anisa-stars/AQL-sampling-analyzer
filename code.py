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

# CSS STYLING

# ─────────────────────────────────────────────

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Source+Code+Pro:wght@400;600&family=Inter:wght@300;400;500&display=swap');



:root {

    --primary: #00d4aa;

    --secondary: #0a1628;

    --accent: #ff6b35;

    --bg: #060d1a;

    --card: #0d1f35;

    --border: #1a3a5c;

    --text: #e0f0ff;

    --muted: #7899bb;

}



.stApp { background: var(--bg) !important; color: var(--text) !important; font-family: 'Inter', sans-serif; }



.opening-card {

    background: var(--card);

    padding: 25px;

    border-radius: 15px;

    border-left: 5px solid var(--primary);

    margin-bottom: 25px;

    box-shadow: 0 4px 15px rgba(0,0,0,0.3);

}



.app-title { font-family: 'Rajdhani', sans-serif; font-size: 2.6rem; font-weight: 700; color: var(--primary); margin: 0; }

.section-title { font-family: 'Rajdhani', sans-serif; font-size: 1.3rem; font-weight: 600; color: var(--primary); border-left: 3px solid var(--primary); padding-left: 12px; margin: 20px 0 12px 0; text-transform: uppercase; }

.metric-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 18px 22px; text-align: center; }

.metric-value { font-family: 'Rajdhani', sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--primary); }

.metric-label { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

.result-pass { background: rgba(0,212,170,0.12); border: 2px solid var(--primary); border-radius: 12px; padding: 20px; text-align: center; font-family: 'Rajdhani'; font-size: 1.8rem; color: var(--primary); }

.result-fail { background: rgba(255,107,53,0.12); border: 2px solid var(--accent); border-radius: 12px; padding: 20px; text-align: center; font-family: 'Rajdhani'; font-size: 1.8rem; color: var(--accent); }



.stButton > button { background: linear-gradient(135deg, #00d4aa, #00a882) !important; color: #060d1a !important; font-weight: 700 !important; border-radius: 8px !important; }

</style>

""", unsafe_allow_html=True)

	
# ─────────────────────────────────────────────
# AQL DATA TABLES (ISO 2859-1)
# ─────────────────────────────────────────────

# Lot size → Sample Size Code Letter (General Inspection Level II)
LOT_SIZE_TABLE = [
    (2, 8, 'A'), (9, 15, 'B'), (16, 25, 'C'), (26, 50, 'D'),
    (51, 90, 'E'), (91, 150, 'F'), (151, 280, 'G'), (281, 500, 'H'),
    (501, 1200, 'J'), (1201, 3200, 'K'), (3201, 10000, 'L'),
    (10001, 35000, 'M'), (35001, 150000, 'N'), (150001, 500000, 'P'),
    (500001, float('inf'), 'Q'),
]

# Sample size per code letter
SAMPLE_SIZE = {
    'A': 2, 'B': 3, 'C': 5, 'D': 8, 'E': 13,
    'F': 20, 'G': 32, 'H': 50, 'J': 80, 'K': 125,
    'L': 200, 'M': 315, 'N': 500, 'P': 800, 'Q': 1250,
}

# AQL Single Normal Inspection: {code_letter: {aql: (Ac, Re)}}
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
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">🔬 AQL SAMPLING ANALYZER</div>
    <div class="app-subtitle">Pengolahan Data Sampling & Acceptance Quality Limit · ISO 2859-1 · Kelompok 7</div>
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
    lot_number = st.text_input("Nomor Lot", value="LOT-2026-001")
    inspector = st.text_input("Nama Inspektor", value="Kelompok 7")

    analyze_btn = st.button("🔍 ANALISIS SEKARANG", use_container_width=True)

# ─────────────────────────────────────────────
# CALCULATION
# ─────────────────────────────────────────────
code_letter = get_code_letter(lot_size)
sample_size = SAMPLE_SIZE.get(code_letter, 2)
criteria = get_aql_criteria(code_letter, aql_level)

if criteria:
    ac, re = criteria
else:
    ac, re = 0, 1

defect_rate = get_defect_rate(n_defects, sample_size)
decision = "ACCEPT ✅" if n_defects <= ac else "REJECT ❌"
decision_pass = n_defects <= ac

# ─────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Hasil Analisis", "📈 Visualisasi", "📋 Tabel AQL", "📄 Laporan"])

# ── TAB 1: HASIL ──────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Parameter Lot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{lot_size:,}</div><div class="metric-label">Ukuran Lot</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{code_letter}</div><div class="metric-label">Kode Sampel</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{sample_size}</div><div class="metric-label">Ukuran Sampel</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{aql_level}%</div><div class="metric-label">AQL Level</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Kriteria Penerimaan</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{ac}</div><div class="metric-label">Accept Number (Ac)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{re}</div><div class="metric-label">Reject Number (Re)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{n_defects}</div><div class="metric-label">Defek Ditemukan</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{defect_rate:.2f}%</div><div class="metric-label">Defect Rate</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Keputusan Sampling</div>', unsafe_allow_html=True)
    if decision_pass:
        st.markdown(f'<div class="result-pass">✅ LOT DITERIMA (ACCEPT)<br><span style="font-size:1rem;font-weight:400;color:var(--muted)">Defek ({n_defects}) ≤ Ac ({ac}) — Lot memenuhi standar AQL {aql_level}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-fail">❌ LOT DITOLAK (REJECT)<br><span style="font-size:1rem;font-weight:400;color:var(--muted)">Defek ({n_defects}) ≥ Re ({re}) — Lot tidak memenuhi standar AQL {aql_level}%</span></div>', unsafe_allow_html=True)

    st.markdown("")

    # Interpretation
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
        if decision_pass:
            rekomendasi = "✅ Lot dapat dikirim/digunakan. Lanjutkan proses produksi normal."
        else:
            rekomendasi = "❌ Lakukan inspeksi 100% atau kembalikan ke supplier. Tinjau proses produksi."
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

    # Gauge chart - defect vs limit
    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=n_defects,
            delta={'reference': ac, 'increasing': {'color': "#ff6b35"}, 'decreasing': {'color': "#00d4aa"}},
            title={'text': "Jumlah Defek vs Accept Number", 'font': {'color': '#e0f0ff', 'family': 'Rajdhani', 'size': 15}},
            gauge={
                'axis': {'range': [0, max(re * 2, n_defects * 1.5, 5)], 'tickcolor': '#7899bb'},
                'bar': {'color': '#00d4aa' if decision_pass else '#ff6b35'},
                'bgcolor': '#0d1f35',
                'borderwidth': 1,
                'bordercolor': '#1a3a5c',
                'steps': [
                    {'range': [0, ac], 'color': 'rgba(0,212,170,0.15)'},
                    {'range': [ac, re], 'color': 'rgba(255,165,0,0.15)'},
                    {'range': [re, max(re * 2, n_defects * 1.5, 5)], 'color': 'rgba(255,107,53,0.15)'},
                ],
                'threshold': {
                    'line': {'color': "#ff6b35", 'width': 3},
                    'thickness': 0.75,
                    'value': re,
                }
            },
            number={'font': {'color': '#00d4aa' if decision_pass else '#ff6b35', 'family': 'Rajdhani', 'size': 36}}
        ))
        fig_gauge.update_layout(
            paper_bgcolor='#0d1f35', plot_bgcolor='#0d1f35',
            font_color='#e0f0ff', height=320,
            margin=dict(l=20, r=20, t=40, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Pie chart - defect vs good
    with col2:
        good = sample_size - n_defects
        fig_pie = go.Figure(go.Pie(
            labels=['Baik', 'Defek'],
            values=[max(good, 0), n_defects],
            hole=0.55,
            marker=dict(colors=['#00d4aa', '#ff6b35'], line=dict(color='#060d1a', width=2)),
            textfont=dict(family='Rajdhani', size=14, color='#e0f0ff'),
        ))
        fig_pie.update_layout(
            paper_bgcolor='#0d1f35', plot_bgcolor='#0d1f35',
            font_color='#e0f0ff', height=320,
            title=dict(text='Komposisi Sampel', font=dict(family='Rajdhani', color='#e0f0ff', size=15)),
            margin=dict(l=20, r=20, t=40, b=10),
            legend=dict(font=dict(color='#e0f0ff'))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart - sensitivity analysis (vary defects)
    st.markdown('<div class="section-title">Analisis Sensitivitas — Keputusan per Jumlah Defek</div>', unsafe_allow_html=True)
    max_def = max(re * 3, 10)
    defect_range = list(range(0, max_def + 1))
    colors_bar = ['#00d4aa' if d <= ac else '#ff6b35' for d in defect_range]
    fig_bar = go.Figure(go.Bar(
        x=defect_range,
        y=defect_range,
        marker=dict(color=colors_bar),
        text=['ACCEPT' if d <= ac else 'REJECT' for d in defect_range],
        textposition='auto',
        textfont=dict(family='Rajdhani', size=10, color='#060d1a'),
    ))
    fig_bar.add_vline(x=ac + 0.5, line_color='#ffd700', line_dash='dash', line_width=2,
                      annotation_text=f'Batas Ac={ac}', annotation_font_color='#ffd700')
    fig_bar.update_layout(
        paper_bgcolor='#0d1f35', plot_bgcolor='#0a1628',
        font_color='#e0f0ff', height=280,
        xaxis=dict(title='Jumlah Defek', gridcolor='#1a3a5c', color='#7899bb'),
        yaxis=dict(title='Jumlah Defek', gridcolor='#1a3a5c', color='#7899bb'),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # OC Curve (Operating Characteristic)
    st.markdown('<div class="section-title">OC Curve — Kurva Karakteristik Operasi</div>', unsafe_allow_html=True)
    p_values = np.linspace(0, 0.3, 200)
    pa_values = []
    for p in p_values:
        # Binomial probability P(X <= Ac) where X ~ Binomial(n, p)
        pa = sum(math.comb(sample_size, k) * (p**k) * ((1-p)**(sample_size-k))
                 for k in range(ac + 1))
        pa_values.append(pa * 100)

    fig_oc = go.Figure()
    fig_oc.add_trace(go.Scatter(
        x=p_values * 100, y=pa_values,
        mode='lines', name='P(Accept)',
        line=dict(color='#00d4aa', width=2.5),
        fill='tozeroy', fillcolor='rgba(0,212,170,0.07)'
    ))
    fig_oc.add_vline(x=aql_level, line_color='#ffd700', line_dash='dot',
                     annotation_text=f'AQL={aql_level}%', annotation_font_color='#ffd700')
    fig_oc.add_hline(y=95, line_color='#7899bb', line_dash='dot',
                     annotation_text='95% Accept', annotation_font_color='#7899bb')
    fig_oc.update_layout(
        paper_bgcolor='#0d1f35', plot_bgcolor='#0a1628',
        font_color='#e0f0ff', height=300,
        xaxis=dict(title='Defect Rate (%)', gridcolor='#1a3a5c', color='#7899bb'),
        yaxis=dict(title='P(Accept) %', gridcolor='#1a3a5c', color='#7899bb', range=[0, 105]),
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(font=dict(color='#e0f0ff'))
    )
    st.plotly_chart(fig_oc, use_container_width=True)

# ── TAB 3: TABEL AQL ─────────────────────────
with tab3:
    st.markdown('<div class="section-title">Tabel Referensi AQL (ISO 2859-1 — Normal Inspection)</div>', unsafe_allow_html=True)

    # Build summary table
    rows = []
    for low, high, code in LOT_SIZE_TABLE:
        n = SAMPLE_SIZE[code]
        row = {'Ukuran Lot': f"{low:,} – {high:,}" if high != float('inf') else f"≥ {low:,}",
               'Kode': code, 'n Sampel': n}
        for aql_v in [0.65, 1.0, 1.5, 2.5, 4.0, 6.5]:
            crit = AQL_TABLE[code].get(aql_v, (0, 1))
            row[f'AQL {aql_v}%'] = f"Ac={crit[0]} Re={crit[1]}"
        rows.append(row)

    df_table = pd.DataFrame(rows)
    # Highlight current row
    def highlight_current(row):
        if row['Kode'] == code_letter:
            return ['background-color: rgba(0,212,170,0.15); color: #00d4aa'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_table.style.apply(highlight_current, axis=1),
        use_container_width=True, height=400
    )
    st.caption(f"🟢 Baris yang di-highlight = kode **{code_letter}** sesuai lot size **{lot_size:,}**")

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
    now = datetime.now().strftime("%d %B %Y, %H:%M")

    report_text = f"""
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

    st.markdown(report_text)

    # Download button
    st.download_button(
        label="📥 Unduh Laporan (.txt)",
        data=report_text,
        file_name=f"laporan_aql_{lot_number.replace('-','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("""
<div style="text-align:center; color:var(--muted); font-family:Rajdhani; letter-spacing:1px; font-size:0.85rem; margin-top:10px;">
    AQL SAMPLING ANALYZER · KELOMPOK 7 · LPK 2026<br>
    Standar: ISO 2859-1 · General Inspection Level II · Single Sampling Normal
</div>
""", unsafe_allow_html=True)
