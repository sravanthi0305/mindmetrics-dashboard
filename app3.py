import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import warnings
warnings.filterwarnings("ignore")
 
# ── PAGE CONFIG  ────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindMetrics | Teen Mental Health Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ── GLOBAL CSS  ─────────────────────────────────────────────────────
# Injects a professional dark theme, custom fonts, and polished card styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
 
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
}
.main { background: #080d1a; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1400px; }
 
/* ── Hide Streamlit default header/footer ── */
#MainMenu, footer, header { visibility: hidden; }
 
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1220 !important;
    border-right: 1px solid #1e2d44;
}
[data-testid="stSidebar"] * { color: #a0b4cc !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e2f0ff !important; }
 
/* ── KPI Card ── */
.kpi-card {
    background: linear-gradient(135deg, #0f1a2e 0%, #111f38 100%);
    border: 1px solid #1e2d44;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative; overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, #00c6ff, #0072ff); }
.kpi-card.red::before   { background: linear-gradient(90deg, #ff416c, #ff4b2b); }
.kpi-card.purple::before{ background: linear-gradient(90deg, #a78bfa, #7c3aed); }
.kpi-card.green::before { background: linear-gradient(90deg, #00f260, #0575e6); }
.kpi-card.orange::before{ background: linear-gradient(90deg, #f7971e, #ffd200); }
 
.kpi-value {
    font-size: 2.4rem; font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.1; margin-bottom: 4px;
}
.kpi-label {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: #5a7a99;
}
.kpi-sub {
    font-size: 0.75rem; margin-top: 6px;
    color: #3d5a72;
}
 
/* ── Section Header ── */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 32px 0 18px;
}
.section-header .line {
    width: 4px; height: 22px;
    border-radius: 2px;
}
.section-header h2 {
    font-size: 1.05rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    color: #c8d8e8; margin: 0;
}
 
/* ── Insight Banner ── */
.insight-banner {
    background: linear-gradient(135deg, #0a1628, #0e1f3a);
    border: 1px solid #1e3055;
    border-left: 4px solid #00c6ff;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.85rem;
    color: #a0c4e0;
    line-height: 1.6;
}
.insight-banner b { color: #00d4ff; }
 
/* ── Risk badge ── */
.risk-high   { color: #ff6b8a; font-weight: 800; font-size: 1.1rem; }
.risk-medium { color: #fbbf24; font-weight: 800; font-size: 1.1rem; }
.risk-low    { color: #34d399; font-weight: 800; font-size: 1.1rem; }
 
/* ── Predict result cards ── */
.result-high {
    background: rgba(255,107,138,0.08);
    border: 1px solid rgba(255,107,138,0.3);
    border-radius: 14px; padding: 20px 22px;
    text-align: center;
}
.result-medium {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.3);
    border-radius: 14px; padding: 20px 22px;
    text-align: center;
}
.result-low {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 14px; padding: 20px 22px;
    text-align: center;
}
 
/* ── Plotly chart backgrounds ── */
.js-plotly-plot { border-radius: 14px; }
 
/* ── Page navigation tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid #1e2d44;
    padding-bottom: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 8px 20px;
    font-size: 0.8rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    color: #5a7a99 !important;
    background: transparent;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #0f1a2e !important;
    color: #00c6ff !important;
    border-bottom: 2px solid #00c6ff !important;
}
 
/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080d1a; }
::-webkit-scrollbar-thumb { background: #1e2d44; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)
 
 
# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
 
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora, sans-serif", color="#8a9fc0", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#1a2640", showline=False, zeroline=False),
    yaxis=dict(gridcolor="#1a2640", showline=False, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
)
COLORS = {
    "High":   "#ff6b8a",
    "Medium": "#fbbf24",
    "Low":    "#34d399",
    "accent": "#00c6ff",
    "seq":    ["#0f2b4a","#1a4a7a","#1e6fb5","#2196f3","#64b8f7","#a8d8ff"],
}
 
def kpi(color, value, label, sub=""):
    st.markdown(f"""
    <div class="kpi-card {color}">
        <div class="kpi-value" style="color:{'#00c6ff' if color=='blue' else '#ff6b8a' if color=='red' else '#a78bfa' if color=='purple' else '#34d399' if color=='green' else '#fbbf24'}">
            {value}
        </div>
        <div class="kpi-label">{label}</div>
        {"<div class='kpi-sub'>"+sub+"</div>" if sub else ""}
    </div>""", unsafe_allow_html=True)
 
def section(title, color="#00c6ff"):
    st.markdown(f"""
    <div class="section-header">
        <div class="line" style="background:{color};"></div>
        <h2>{title}</h2>
    </div>""", unsafe_allow_html=True)
 
def insight(text):
    st.markdown(f'<div class="insight-banner">{text}</div>', unsafe_allow_html=True)
 
 
# ══════════════════════════════════════════════════════════════════
# DATA  LOADING
# ══════════════════════════════════════════════════════════════════
 
@st.cache_data               # ← caches so the CSV isn't re-read on every interaction
def load_data():
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
 
    # Risk label formula
    def get_risk(row):
        score = (row['stress_level']  * 0.4 +
                 row['anxiety_level'] * 0.4 +
                 (10 - row['sleep_hours']) * 0.2)
        return 'High' if score > 6 else 'Medium' if score > 4 else 'Low'
 
    df['risk_label']   = df.apply(get_risk, axis=1)
    df['risk_numeric'] = df['risk_label'].map({'High': 3, 'Medium': 2, 'Low': 1})
    return df
 
@st.cache_resource           # ← loads the model only once
def load_model():
    return joblib.load("risk_model.pkl")
 
df    = load_data()
model = load_model()
 
 
# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
 
with st.sidebar:
    st.markdown("## 🧠 MindMetrics")
    st.markdown("<hr style='border-color:#1e2d44;margin:8px 0 18px'/>", unsafe_allow_html=True)
 
    st.markdown("### 🎛️ Filters")
 
    platform_opts = ["All"] + sorted(df["platform_usage"].unique().tolist())
    platform = st.selectbox("📱 Platform", platform_opts)
 
    gender_opts = ["All"] + sorted(df["gender"].unique().tolist())
    gender = st.selectbox("👤 Gender", gender_opts)
 
    age_range = st.slider("🎂 Age Range", 13, 19, (13, 19))
 
    st.markdown("<hr style='border-color:#1e2d44;margin:18px 0'/>", unsafe_allow_html=True)
    st.markdown("### 📌 About")
    st.markdown("""
    <div style='font-size:0.78rem;color:#4a6a88;line-height:1.8;'>
    <b style='color:#6a8aaa;'>Dataset:</b> 2,500 teens<br/>
    <b style='color:#6a8aaa;'>Model:</b> Random Forest (100 trees)<br/>
    <b style='color:#6a8aaa;'>Features:</b> 12 variables<br/>
    <b style='color:#6a8aaa;'>Stack:</b> Python · Streamlit · Plotly<br/>
    <b style='color:#6a8aaa;'>Project:</b> student research and analytic project
    </div>""", unsafe_allow_html=True)
 
    st.markdown("<hr style='border-color:#1e2d44;margin:18px 0'/>", unsafe_allow_html=True)
    # Download filtered data button
    csv_export = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Dataset", csv_export,
                       "teen_mental_health.csv", "text/csv")
 
# ── Apply filters
mask = pd.Series([True] * len(df))
if platform != "All":
    mask &= df["platform_usage"] == platform
if gender != "All":
    mask &= df["gender"] == gender
mask &= (df["age"] >= age_range[0]) & (df["age"] <= age_range[1])
fdf = df[mask].copy()
 
 
# ══════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════
 
st.markdown("""
<div style='margin-bottom:28px;'>
    <div style='font-size:0.7rem;font-weight:700;letter-spacing:2px;
                text-transform:uppercase;color:#00c6ff;margin-bottom:6px;'>
        STUDENT RESEARCH AND ANALYTIC PROJECT · DATA SCIENCE & ML
    </div>
    <h1 style='font-size:2rem;font-weight:800;color:#e2f0ff;
               line-height:1.2;margin:0;'>
        Teen Social Media &amp;
        <span style='color:#00c6ff;'>Mental Health Analytics</span>
    </h1>
    <p style='color:#4a6a88;font-size:0.88rem;margin-top:8px;'>
        Behavioural analysis of 2,500 teenagers · ML-powered risk prediction ·
        Real-time interactive exploration
    </p>
</div>
""", unsafe_allow_html=True)
 
 
# ══════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════
 
section("Key Metrics", "#00c6ff")
k1, k2, k3, k4, k5 = st.columns(5)
 
high_pct = f"{(fdf['risk_label']=='High').mean()*100:.1f}%"
with k1: kpi("blue",   f"{fdf['daily_social_media_hours'].mean():.1f}h",  "Avg Daily Usage",  f"of {len(fdf):,} teens")
with k2: kpi("red",    f"{fdf['stress_level'].mean():.1f}/10",             "Avg Stress",       "out of 10")
with k3: kpi("purple", f"{fdf['anxiety_level'].mean():.1f}/10",            "Avg Anxiety",      "out of 10")
with k4: kpi("green",  f"{fdf['sleep_hours'].mean():.1f}h",                "Avg Sleep",        "per night")
with k5: kpi("orange", high_pct,                                            "High Risk",        f"{(fdf['risk_label']=='High').sum():,} teens")
 
 
# ══════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════
 
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🔬 Deep Analysis",
    "🤖 Risk Predictor",
    "📈 Correlations",
])
 
 
# ──────────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ──────────────────────────────────────────────────────────────────
with tab1:
 
    c1, c2 = st.columns([1.1, 0.9])
 
    # Scatter: screen time vs stress
    with c1:
        section("Screen Time vs Stress Level", "#00c6ff")
        fig = px.scatter(
            fdf, x="daily_social_media_hours", y="stress_level",
            color="risk_label",
            color_discrete_map=COLORS,
            size_max=7, opacity=0.75,
            hover_data=["age", "gender", "platform_usage", "sleep_hours"],
            labels={"daily_social_media_hours": "Daily Hours", "stress_level": "Stress Score"},
            title="",
        )
        fig.update_traces(marker=dict(size=5))
        fig.update_layout(**PLOTLY_LAYOUT, height=340,
                          legend_title_text="Risk Level")
        st.plotly_chart(fig, use_container_width=True)
        insight("<b>Insight:</b> Strong positive correlation (r = +0.91) — each extra hour on social media pushes stress up by ~0.7 points on average.")
 
    # Donut: risk distribution
    with c2:
        section("Risk Distribution", "#a78bfa")
        risk_counts = fdf["risk_label"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]
        fig2 = go.Figure(go.Pie(
            labels=risk_counts["Risk"], values=risk_counts["Count"],
            hole=0.62,
            marker=dict(colors=[COLORS.get(r, "#aaa") for r in risk_counts["Risk"]],
                        line=dict(color="#080d1a", width=3)),
            textinfo="percent+label",
            textfont=dict(size=12, family="Sora"),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=340,
                           annotations=[dict(
                               text=f"<b>{len(fdf):,}</b><br><span style='font-size:10px'>Teens</span>",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=16, color="#c8d8e8", family="Sora"))])
        st.plotly_chart(fig2, use_container_width=True)
 
    st.markdown("---")
 
    c3, c4 = st.columns(2)
 
    # Bar: avg stress by platform
    with c3:
        section("Avg Stress & Anxiety by Platform", "#ff6b8a")
        plat = fdf.groupby("platform_usage")[["stress_level","anxiety_level"]].mean().reset_index()
        plat = plat.sort_values("stress_level", ascending=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=plat["platform_usage"], x=plat["stress_level"],
            name="Stress", orientation="h",
            marker_color="#ff6b8a",
            marker_line_width=0,
        ))
        fig3.add_trace(go.Bar(
            y=plat["platform_usage"], x=plat["anxiety_level"],
            name="Anxiety", orientation="h",
            marker_color="#a78bfa",
            marker_line_width=0,
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=280,
                           barmode="group", xaxis_title="Score /10")
        st.plotly_chart(fig3, use_container_width=True)
 
    # Line: avg stress by age
    with c4:
        section("Mental Health Trends by Age", "#34d399")
        age_df = fdf.groupby("age")[["stress_level","anxiety_level","sleep_hours"]].mean().reset_index()
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=age_df["age"], y=age_df["stress_level"],
            name="Stress", line=dict(color="#ff6b8a", width=2.5), mode="lines+markers",
            marker=dict(size=7)))
        fig4.add_trace(go.Scatter(x=age_df["age"], y=age_df["anxiety_level"],
            name="Anxiety", line=dict(color="#a78bfa", width=2.5), mode="lines+markers",
            marker=dict(size=7)))
        fig4.add_trace(go.Scatter(x=age_df["age"], y=age_df["sleep_hours"],
            name="Sleep (hrs)", line=dict(color="#34d399", width=2.5, dash="dot"),
            mode="lines+markers", marker=dict(size=7)))
        fig4.update_layout(**PLOTLY_LAYOUT, height=280,
                           xaxis_title="Age", yaxis_title="Score / Hours")
        st.plotly_chart(fig4, use_container_width=True)
 
 
# ──────────────────────────────────────────────────────────────────
# TAB 2 — DEEP ANALYSIS
# ──────────────────────────────────────────────────────────────────
with tab2:
 
    c1, c2 = st.columns(2)
 
    # Box plot: daily hours by risk
    with c1:
        section("Social Media Usage Distribution by Risk", "#fbbf24")
        fig = px.box(
            fdf, x="risk_label", y="daily_social_media_hours",
            color="risk_label", color_discrete_map=COLORS,
            labels={"daily_social_media_hours": "Hours/Day", "risk_label": "Risk Level"},
            category_orders={"risk_label": ["Low", "Medium", "High"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight("<b>Insight:</b> High-risk teens average <b>6.2h/day</b> vs only <b>2.4h</b> for low-risk teens.")
 
    # Violin: sleep by platform
    with c2:
        section("Sleep Hours Distribution by Platform", "#00c6ff")
        fig2 = px.violin(
            fdf, x="platform_usage", y="sleep_hours",
            color="platform_usage",
            box=True, points=False,
            labels={"sleep_hours": "Sleep (hrs)", "platform_usage": "Platform"},
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        insight("<b>Insight:</b> TikTok users show the widest sleep variance and lowest median sleep.")
 
    # Grouped bar: risk by gender
    section("Risk Level Breakdown by Gender", "#ff6b8a")
    gender_risk = fdf.groupby(["gender","risk_label"]).size().reset_index(name="count")
    fig3 = px.bar(
        gender_risk, x="gender", y="count", color="risk_label",
        color_discrete_map=COLORS, barmode="group",
        labels={"count": "Number of Teens", "gender": "Gender"},
    )
    fig3.update_layout(**PLOTLY_LAYOUT, height=300)
    st.plotly_chart(fig3, use_container_width=True)
 
    # Sunburst: platform → risk
    section("Platform → Risk Hierarchy (Sunburst)", "#a78bfa")
    sun = fdf.groupby(["platform_usage","risk_label"]).size().reset_index(name="count")
    fig4 = px.sunburst(
        sun, path=["platform_usage","risk_label"], values="count",
        color="risk_label", color_discrete_map=COLORS,
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), height=380)
    st.plotly_chart(fig4, use_container_width=True)
 
 
# ──────────────────────────────────────────────────────────────────
# TAB 3 — ML RISK PREDICTOR
# ──────────────────────────────────────────────────────────────────
with tab3:
 
    section("🤖 Real-Time Mental Health Risk Predictor", "#00c6ff")
    st.markdown("""
    <p style='color:#4a6a88;font-size:0.85rem;margin-bottom:20px;'>
    Adjust the sliders below to describe a teen's profile.
    The Random Forest model (100 trees, trained on 2,500 teens)
    will instantly predict their mental health risk category.
    </p>""", unsafe_allow_html=True)
 
    pc1, pc2, pc3 = st.columns([1, 1, 1])
 
    with pc1:
        st.markdown("#### 📱 Usage Profile")
        hours   = st.slider("Daily Social Media Hours", 0.0, 12.0, 4.0, 0.5)
        screen_b= st.slider("Screen Time Before Sleep (hrs)", 0.0, 3.0, 1.5, 0.1)
 
    with pc2:
        st.markdown("#### 🧠 Mental State")
        stress  = st.slider("Stress Level", 1, 10, 5)
        anxiety = st.slider("Anxiety Level", 1, 10, 5)
 
    with pc3:
        st.markdown("#### 💤 Lifestyle")
        sleep   = st.slider("Sleep Hours / Night", 3.0, 10.0, 7.0, 0.5)
        age     = st.slider("Age", 13, 19, 16)
 
    st.markdown("<br/>", unsafe_allow_html=True)
    btn_col = st.columns([1, 2, 1])[1]
    predict_clicked = btn_col.button("🔮 Predict Risk Level", use_container_width=True)
 
    if predict_clicked:
        prediction = model.predict([[hours, stress, anxiety, sleep, age]])[0]
 
        # ── Result display
        r1, r2, r3 = st.columns([1, 2, 1])
        with r2:
            if prediction == "High":
                st.markdown("""
                <div class="result-high">
                    <div style='font-size:2.5rem;'>⚠️</div>
                    <div class='risk-high'>HIGH RISK</div>
                    <div style='color:#cc4466;font-size:0.85rem;margin-top:8px;'>
                    Immediate counselling evaluation recommended.<br/>
                    Reduce screen time below 2h/day urgently.
                    </div>
                </div>""", unsafe_allow_html=True)
            elif prediction == "Medium":
                st.markdown("""
                <div class="result-medium">
                    <div style='font-size:2.5rem;'>🟡</div>
                    <div class='risk-medium'>MEDIUM RISK</div>
                    <div style='color:#aa8822;font-size:0.85rem;margin-top:8px;'>
                    Monitor weekly. Encourage offline activities.<br/>
                    Aim for 8+ hours sleep and reduce usage by 30%.
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-low">
                    <div style='font-size:2.5rem;'>✅</div>
                    <div class='risk-low'>LOW RISK</div>
                    <div style='color:#228866;font-size:0.85rem;margin-top:8px;'>
                    Current habits appear healthy.<br/>
                    Maintain sleep schedule and balanced usage.
                    </div>
                </div>""", unsafe_allow_html=True)
 
        # ── Risk factor gauge bars
        st.markdown("<br/>", unsafe_allow_html=True)
        section("Risk Factor Breakdown", "#fbbf24")
        factors = {
            "📱 Usage Impact":   min(100, hours / 12 * 100),
            "😤 Stress Load":    stress / 10 * 100,
            "😰 Anxiety Load":   anxiety / 10 * 100,
            "😴 Sleep Deficit":  max(0, (8.5 - sleep) / 5 * 100),
        }
        fig_gauge = go.Figure()
        for label, val in factors.items():
            color = "#ff6b8a" if val > 66 else "#fbbf24" if val > 40 else "#34d399"
            fig_gauge.add_trace(go.Bar(
                x=[val], y=[label], orientation="h",
                marker_color=color, text=f"{val:.0f}%",
                textposition="outside", marker_line_width=0,
            ))
        layout = PLOTLY_LAYOUT.copy()
        layout.pop("xaxis", None)
        fig_gauge.update_layout(
       **layout,
        height=220,
        xaxis=dict(range=[0,110], gridcolor="#1a2640"),
        showlegend=False,
        xaxis_title="Risk Contribution (%)"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
 
 
# ──────────────────────────────────────────────────────────────────
# TAB 4 — CORRELATIONS
# ──────────────────────────────────────────────────────────────────
with tab4:
 
    section("Correlation Matrix — All Variables", "#00c6ff")
 
    num_cols = ["daily_social_media_hours","sleep_hours","stress_level",
                "anxiety_level","screen_time_before_sleep",
                "academic_performance","physical_activity"]
    nice_labels = ["Daily Hours","Sleep","Stress","Anxiety",
                   "Screen@Bedtime","Academics","Exercise"]
 
    corr = fdf[num_cols].corr()
    fig_heat = go.Figure(go.Heatmap(
        z=corr.values,
        x=nice_labels, y=nice_labels,
        colorscale=[
            [0.0, "#1a4a7a"], [0.5, "#0a0f1a"], [1.0, "#8b1a2a"]
        ],
        zmid=0,
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}",
        textfont=dict(size=11),
        hoverongaps=False,
    ))
    fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#8a9fc0", family="Sora"),
                           margin=dict(l=10,r=10,t=20,b=10), height=430)
    st.plotly_chart(fig_heat, use_container_width=True)
 
    insight("<b>Key finding:</b> Social media usage vs stress = <b>+0.91</b> (very strong). "
            "Academics vs stress = <b>–0.94</b> (strongest protective factor). "
            "Sleep vs daily hours = <b>–0.77</b> (more social media = less sleep).")
 
    # Scatter matrix
    section("Pairplot — Usage, Sleep, Stress, Anxiety", "#a78bfa")
    sample = fdf.sample(min(400, len(fdf)), random_state=42)
    fig_pair = px.scatter_matrix(
        sample,
        dimensions=["daily_social_media_hours","sleep_hours","stress_level","anxiety_level"],
        color="risk_label", color_discrete_map=COLORS,
        labels={
            "daily_social_media_hours": "Hours",
            "sleep_hours": "Sleep",
            "stress_level": "Stress",
            "anxiety_level": "Anxiety",
        },
        opacity=0.6,
    )
    fig_pair.update_traces(marker=dict(size=3))
    fig_pair.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#8a9fc0", family="Sora"),
                           height=500,
                           margin=dict(l=10,r=10,t=30,b=10))
    st.plotly_chart(fig_pair, use_container_width=True)
 
 
# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("<br/><br/>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:20px 0;border-top:1px solid #1e2d44;
            color:#2a3a4a;font-size:0.75rem;letter-spacing:0.5px;'>
    MindMetrics · Teen Mental Health Analytics Dashboard ·
    Built with Python, Streamlit &amp; Plotly ·
    student research and analytic  Project
</div>""", unsafe_allow_html=True)
