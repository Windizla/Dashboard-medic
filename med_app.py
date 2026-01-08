from __future__ import annotations

import base64

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# ---------------- Page ----------------
st.set_page_config(
    page_title="Future Medical Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Futuristic CSS ----------------
CSS = """
<style>
:root{
  --bg0:#060a16;
  --bg1:#0b1020;
  --panel: rgba(18,26,51,0.78);
  --stroke: rgba(255,255,255,0.08);
  --text: rgba(235,240,255,0.95);
  --muted: rgba(235,240,255,0.62);

  --cyan:#18e0ff;
  --violet:#b256ff;
  --pink:#ff4fd8;
  --green:#3dffb8;
  --red:#ff3c50;
}

header[data-testid="stHeader"] { display: none; }
div[data-testid="stToolbar"] { display: none; }
div[data-testid="stDecoration"] { display: none; }
footer { display: none; }

.stApp{
  background:
    radial-gradient(circle at 12% 12%, rgba(178,86,255,0.18), transparent 42%),
    radial-gradient(circle at 78% 22%, rgba(24,224,255,0.14), transparent 48%),
    linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 55%, var(--bg0) 100%);
  color: var(--text);
}

div.block-container{
  padding-top: 0.7rem !important;
  padding-bottom: 1.0rem !important;
  padding-left: 1.1rem !important;
  padding-right: 1.1rem !important;
  max-width: 1650px;
}

section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, rgba(18,26,51,0.95), rgba(10,14,28,0.95));
  border-right: 1px solid var(--stroke);
}
section[data-testid="stSidebar"] > div{ padding-top: 0.8rem !important; }

h1,h2,h3,h4, p, span, div { color: var(--text); }
small, .muted { color: var(--muted); }

.card{
  background: var(--panel);
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 12px 12px 10px 12px;
  box-shadow: 0 18px 60px rgba(0,0,0,0.45);
}

.metric{
  border-radius: 16px;
  padding: 12px;
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 18px 60px rgba(0,0,0,0.30);
}
.metric.a{
  background: linear-gradient(135deg, rgba(212,99,255,0.95), rgba(145,74,255,0.55));
}
.metric.b{
  background: linear-gradient(135deg, rgba(35,255,228,0.85), rgba(54,138,255,0.55));
}
.metric.c{
  background: linear-gradient(135deg, rgba(58,160,255,0.90), rgba(24,224,255,0.35));
}
.metric .title{
  font-size: 0.82rem;
  color: rgba(255,255,255,0.88);
  margin-bottom: 6px;
}
.metric .value{
  font-size: 1.85rem;
  font-weight: 850;
  letter-spacing: 0.3px;
}
.metric .value span{
  font-size: 0.95rem;
  font-weight: 700;
  opacity: 0.9;
  margin-left: 6px;
}

.kpi{
  background: rgba(18,26,51,0.72);
  border: 1px solid var(--stroke);
  border-radius: 14px;
  padding: 10px 10px 8px 10px;
  margin-bottom: 10px;
}
.kpi-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 10px;
}
.kpi .label{ font-weight: 650; }
.chip{
  font-size: 0.78rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.9);
}
.chip.pos{ background: rgba(61,255,184,0.12); border-color: rgba(61,255,184,0.25); }
.chip.neg{ background: rgba(255,60,80,0.12); border-color: rgba(255,60,80,0.25); }

div[data-testid="stVerticalBlock"] { gap: 0.75rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------- Helpers ----------------
def card_open() -> None:
    st.markdown('<div class="card">', unsafe_allow_html=True)


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def metric_html(title: str, value: str, variant: str) -> str:
    return f"""
    <div class="metric {variant}">
      <div class="title">{title}</div>
      <div class="value">{value}</div>
    </div>
    """


def kpi_html(label: str, chip: str, chip_class: str) -> str:
    return f"""
    <div class="kpi">
      <div class="kpi-row">
        <div class="label">{label}</div>
        <div class="chip {chip_class}">{chip}</div>
      </div>
    </div>
    """


def fig_style(fig: go.Figure, title: str, height: int) -> go.Figure:
    fig.update_layout(
        height=height,
        title=dict(text=title, x=0.02, y=0.96, font=dict(size=13, color="rgba(235,240,255,0.95)")),
        paper_bgcolor="rgba(18,26,51,0.0)",
        plot_bgcolor="rgba(18,26,51,0.0)",
        margin=dict(l=8, r=8, t=42, b=8),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.98,
            font=dict(size=11, color="rgba(235,240,255,0.75)"),
        ),
        font=dict(color="rgba(235,240,255,0.85)"),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        zeroline=False,
        linecolor="rgba(255,255,255,0.10)",
        tickfont=dict(size=10, color="rgba(235,240,255,0.70)"),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        zeroline=False,
        linecolor="rgba(255,255,255,0.10)",
        tickfont=dict(size=10, color="rgba(235,240,255,0.70)"),
    )
    return fig


def bytes_to_data_uri(data: bytes, mime: str) -> str:
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def synthetic_ecg(
    hr_bpm: float,
    duration_s: float = 10.0,
    fs: int = 500,
    noise: float = 0.012,
) -> tuple[np.ndarray, np.ndarray]:
    """Synthetic ECG (P-QRS-T) as sum of Gaussians per beat. Demo visualization."""
    hr_bpm = float(max(30.0, min(180.0, hr_bpm)))
    period = 60.0 / hr_bpm

    t = np.arange(0.0, duration_s, 1.0 / fs)
    y = np.zeros_like(t)

    def gauss(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
        return np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    beat0 = 0.6
    n_beats = int(np.ceil((duration_s - beat0) / period)) + 2

    for k in range(n_beats):
        c = beat0 + k * period
        y += 0.12 * gauss(t, c - 0.20, 0.025)  # P
        y += -0.15 * gauss(t, c - 0.045, 0.010)  # Q
        y += 1.00 * gauss(t, c + 0.00, 0.012)  # R
        y += -0.25 * gauss(t, c + 0.040, 0.012)  # S
        y += 0.35 * gauss(t, c + 0.26, 0.055)  # T

    y += 0.03 * np.sin(2 * np.pi * 0.33 * t) + 0.015 * np.sin(2 * np.pi * 0.10 * t)
    y += np.random.normal(0.0, noise, size=len(t))
    return t, y


def condition_from_status(status: dict[str, str]) -> tuple[str, str, str]:
    """
    Demo-only card that labels a 'condition' from inflamed organs.
    Returns: (chip_text, chip_class, description)
    """
    inflamed = [o for o, v in status.items() if str(v).lower() == "inflamed"]

    if not inflamed:
        return (
            "stable",
            "pos",
            "No active organ flags. Demo visualization (not a diagnosis).",
        )

    if len(inflamed) == 1:
        o = inflamed[0]
        mapping: dict[str, tuple[str, str, str]] = {
            "brain": ("neuro", "neg", "Flag: brain. Example: neuro-inflammatory / stress load. Demo (not a diagnosis)."),
            "lungs": ("resp", "neg", "Flag: lungs. Example: respiratory inflammation/irritation. Demo (not a diagnosis)."),
            "heart": ("cardio", "neg", "Flag: heart. Example: cardiac load/inflammation. Demo (not a diagnosis)."),
            "abdomen": ("abd", "neg", "Flag: abdomen. Example: abdominal symptom cluster. Demo (not a diagnosis)."),
            "kidneys": ("renal", "neg", "Flag: kidneys. Example: renal / urinary system inflammation. Demo (not a diagnosis)."),
        }
        return mapping.get(o, ("alert", "neg", f"Flag: {o}. Demo (not a diagnosis)."))

    organs_txt = ", ".join([o.capitalize() for o in inflamed])
    return (
        "multi",
        "neg",
        f"Flag: multi-organ state. Affected: {organs_txt}. Demo (not a diagnosis).",
    )


def doctor_orders_from_status(status: dict[str, str]) -> tuple[str, str, str, str]:
    """
    Returns: (chip_text, chip_class, description, note)
    Target format: title -> chip -> description -> note
    """
    inflamed = [o for o, v in status.items() if str(v).lower() == "inflamed"]

    if not inflamed:
        return (
            "routine follow-up",
            "pos",
            "No inflamed organs flagged. Maintain sleep, hydration, and regular activity. "
            "If symptoms exist, contact a clinician.",
            "Demo card: generated from sidebar organ statuses (not medical advice).",
        )

    if len(inflamed) == 1:
        o = inflamed[0]
        plans: dict[str, tuple[str, str, str, str]] = {
            "brain": (
                "neuro / stress",
                "neg",
                "Consider stress & sleep assessment. Screen for headache or neurologic symptoms. "
                "Discuss recovery routines and cognitive load.",
                "Example checks: symptom diary, sleep tracking; clinician decides if neuro consult is needed.",
            ),
            "heart": (
                "cardio check",
                "neg",
                "Consider ECG review and blood pressure trend review. Evaluate chest pain, palpitations, and exercise tolerance.",
                "Example checks: ECG; clinician decides labs/imaging based on symptoms and risk factors.",
            ),
            "lungs": (
                "respiratory check",
                "neg",
                "Consider respiratory evaluation: cough, wheeze, shortness of breath. Monitor SpO₂ if symptomatic.",
                "Example checks: SpO₂, spirometry; imaging only if clinically indicated.",
            ),
            "abdomen": (
                "GI evaluation",
                "neg",
                "Consider GI-focused review: pain pattern, appetite, nausea, stool changes, hydration.",
                "Example checks: clinician may order CBC/CRP; ultrasound if indicated.",
            ),
            "kidneys": (
                "renal evaluation",
                "neg",
                "Consider renal/urinary evaluation: hydration, flank pain, urinary symptoms, edema, and blood pressure.",
                "Example checks: urinalysis, creatinine/eGFR; clinician decides ultrasound if needed.",
            ),
        }
        return plans.get(
            o,
            ("clinical review", "neg", f"Flagged organ: {o}. Consider clinician review.", "Demo card (not medical advice)."),
        )

    organs_txt = ", ".join([o.capitalize() for o in inflamed])
    return (
        "multi-organ review",
        "neg",
        f"Multiple organs flagged ({organs_txt}). Prioritize clinician review and basic labs; "
        "watch for red flags (severe pain, fainting, breathing issues).",
        "Demo card: generated from sidebar organ statuses (not medical advice).",
    )


# ---------------- Body Map ----------------
ORGANS = ["brain", "lungs", "heart", "abdomen", "kidneys"]
COLOR_HEALTHY = "#18e0ff"
COLOR_INFLAMED = "#ff3c50"


def body_scene_html(
    status: dict[str, str],
    tuning: dict[str, dict[str, float]],
    height_px: int,
    bg_data_uri: str | None,
    bg_opacity: float,
    bg_blend: str,
    bg_fit: str,
    bg_pos_x: float,
    bg_pos_y: float,
) -> str:
    def state(o: str) -> str:
        return "inflamed" if str(status.get(o, "healthy")).lower() == "inflamed" else "healthy"

    def col(o: str) -> str:
        return COLOR_INFLAMED if state(o) == "inflamed" else COLOR_HEALTHY

    def flt(o: str) -> str:
        return "url(#glowRed)" if state(o) == "inflamed" else "url(#glowCyan)"

    def t(o: str, key: str, default: float) -> float:
        try:
            return float(tuning.get(o, {}).get(key, default))
        except Exception:
            return float(default)

    heart_dur = "0.70s" if state("heart") == "inflamed" else "1.15s"

    default_bg_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 980" preserveAspectRatio="xMidYMid meet">
  <defs>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 36 0 L 0 0 0 36" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
      <path d="M 18 0 L 18 36 M 0 18 L 36 18" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect x="0" y="0" width="520" height="980" fill="url(#grid)" opacity="0.90"/>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M260 110
             C225 110 198 140 198 178
             C198 210 212 238 216 252
             C222 274 206 312 194 360
             C176 432 182 580 206 690
             C216 740 214 810 206 940
             M260 110
             C295 110 322 140 322 178
             C322 210 308 238 304 252
             C298 274 314 312 326 360
             C344 432 338 580 314 690
             C304 740 306 810 314 940"
          stroke="rgba(24,224,255,0.28)" stroke-width="1.4"/>
    <ellipse cx="260" cy="162" rx="44" ry="56" stroke="rgba(24,224,255,0.50)" stroke-width="1.6"/>
    <path d="M260 226 C260 320 260 420 260 520 C260 620 260 700 260 760"
          stroke="rgba(24,224,255,0.55)" stroke-width="1.8"/>
    <path d="M216 278 C212 324 224 366 260 386 C296 366 308 324 304 278"
          stroke="rgba(24,224,255,0.42)" stroke-width="1.6"/>
    <path d="M222 520 C238 496 246 486 260 486 C274 486 282 496 298 520"
          stroke="rgba(24,224,255,0.40)" stroke-width="1.6"/>
  </g>
</svg>
"""

    if bg_data_uri:
        bg_layer = f"""<img class="bg" src="{bg_data_uri}" alt="body-bg"/>"""
    else:
        bg_layer = f"""<div class="bgsvg">{default_bg_svg}</div>"""

    bg_fit = bg_fit if bg_fit in {"cover", "contain"} else "cover"
    bg_blend = bg_blend if bg_blend in {"screen", "lighten", "normal"} else "screen"

    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  html,body {{
    margin:0; padding:0; background:transparent;
    font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  }}
  .frame {{
    position: relative;
    width: 100%;
    height: {height_px}px;
    overflow: hidden;
    border-radius: 16px;
    background: rgba(0,0,0,0.10);
  }}

  .bg {{
    position:absolute; inset:0;
    width:100%; height:100%;
    object-fit: {bg_fit};
    object-position: {bg_pos_x}% {bg_pos_y}%;
    opacity: {bg_opacity};
    mix-blend-mode: {bg_blend};
    filter: contrast(1.08) saturate(1.12);
  }}
  .bgsvg {{
    position:absolute; inset:0;
    width:100%; height:100%;
    opacity: 1;
  }}
  .bgsvg svg {{ width:100%; height:100%; display:block; }}

  svg.overlay {{
    position:absolute; inset:0;
    width:100%; height:100%;
    display:block;
  }}

  .hudTitle {{
    font-weight: 800; font-size: 12px;
    letter-spacing: 0.22em;
    fill: rgba(235,240,255,0.72);
  }}
  .hudSub {{
    font-weight: 650; font-size: 12px;
    fill: rgba(235,240,255,0.60);
  }}

  .organ {{
    stroke: rgba(255,255,255,0.16);
    stroke-width: 1.0;
  }}
  .organWrap:hover .organ {{
    stroke: rgba(255,255,255,0.40);
    filter: brightness(1.10);
  }}

  .heart {{
    stroke: rgba(255,255,255,0.30);
    stroke-width: 1.8;
  }}

  .abdomen {{
    fill: none;
    stroke: rgba(255,255,255,0.18);
    stroke-width: 1.4;
    stroke-dasharray: 7 8;
  }}

  .scan {{
    position:absolute;
    left:-10%;
    width:120%;
    height: 150px;
    top: -160px;
    background: linear-gradient(
      to bottom,
      rgba(24,224,255,0.00),
      rgba(24,224,255,0.10),
      rgba(24,224,255,0.18),
      rgba(24,224,255,0.08),
      rgba(24,224,255,0.00)
    );
    animation: scanMove 3.2s linear infinite;
    mix-blend-mode: screen;
    opacity: 0.85;
    pointer-events:none;
  }}
  @keyframes scanMove {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY({height_px + 260}px); }}
  }}
</style>
</head>
<body>
  <div class="frame">
    {bg_layer}
    <div class="scan"></div>

    <svg class="overlay" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 980" preserveAspectRatio="xMidYMid meet">
      <defs>
        <filter id="glowCyan" x="-70%" y="-70%" width="240%" height="240%">
          <feGaussianBlur stdDeviation="7" result="b"/>
          <feColorMatrix in="b" type="matrix"
            values="0 0 0 0 0
                    0 1 0 0 0
                    0 1 1 0 0
                    0 0 0 0.70 0" result="c"/>
          <feMerge>
            <feMergeNode in="c"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>

        <filter id="glowRed" x="-80%" y="-80%" width="260%" height="260%">
          <feGaussianBlur stdDeviation="8" result="b"/>
          <feColorMatrix in="b" type="matrix"
            values="1 0 0 0 0
                    0 0.16 0 0 0
                    0 0 0.16 0 0
                    0 0 0 0.86 0" result="r"/>
          <feMerge>
            <feMergeNode in="r"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      <text x="26" y="44" class="hudTitle">INTERNAL SCAN</text>
      <text x="26" y="70" class="hudSub">Healthy = cyan • Inflamed = red</text>

      <!-- BRAIN -->
      <g transform="translate({t('brain','dx',0.0)} {t('brain','dy',0.0)}) scale({t('brain','scale',1.0)})">
        <g class="organWrap" filter="{flt('brain')}">
          <title>Brain: {state('brain')}</title>
          <path class="organ"
            d="M230 165
               C230 142 248 132 260 132
               C272 132 290 142 290 165
               C290 190 274 202 260 202
               C246 202 230 190 230 165 Z"
            fill="{col('brain')}" opacity="{t('brain','alpha',0.62)}"/>
        </g>
      </g>

      <!-- LUNGS -->
      <g transform="translate({t('lungs','dx',0.0)} {t('lungs','dy',0.0)}) scale({t('lungs','scale',1.0)})">
        <g class="organWrap" filter="{flt('lungs')}">
          <title>Lungs: {state('lungs')}</title>
          <path class="organ"
            d="M232 292
               C214 302 206 330 210 360
               C214 392 232 412 254 416
               C258 382 258 330 254 302
               C252 290 242 288 232 292 Z"
            fill="{col('lungs')}" opacity="{t('lungs','alpha',0.62)}"/>
          <path class="organ"
            d="M288 292
               C306 302 314 330 310 360
               C306 392 288 412 266 416
               C262 382 262 330 266 302
               C268 290 278 288 288 292 Z"
            fill="{col('lungs')}" opacity="{t('lungs','alpha',0.62)}"/>
        </g>
      </g>

      <!-- HEART -->
      <g transform="translate({t('heart','dx',0.0)} {t('heart','dy',0.0)}) scale({t('heart','scale',1.0)})">
        <g class="organWrap" filter="{flt('heart')}">
          <title>Heart: {state('heart')}</title>

          <g transform="translate(252 368) scale(1.35)">
            <g>
              <path class="organ heart"
                d="M0 -10
                   C -10 -26 -34 -22 -34 -4
                   C -34 14 -10 28 0 40
                   C 10 28 34 14 34 -4
                   C 34 -22 10 -26 0 -10 Z"
                fill="{col('heart')}" opacity="{min(1.0, t('heart','alpha',0.62) + 0.14)}">
                <animate attributeName="opacity"
                  values="{max(0.40, t('heart','alpha',0.62)-0.10)};{min(1.0, t('heart','alpha',0.62)+0.22)};{max(0.40, t('heart','alpha',0.62)-0.10)}"
                  dur="{heart_dur}" repeatCount="indefinite"/>
              </path>

              <animateTransform
                attributeName="transform"
                type="scale"
                values="1;1.14;1;1.07;1"
                keyTimes="0;0.18;0.42;0.62;1"
                dur="{heart_dur}"
                repeatCount="indefinite"/>
            </g>
          </g>
        </g>
      </g>

      <!-- ABDOMEN -->
      <g transform="translate({t('abdomen','dx',0.0)} {t('abdomen','dy',0.0)}) scale({t('abdomen','scale',1.0)})">
        <g class="organWrap" filter="{flt('abdomen')}">
          <title>Abdomen: {state('abdomen')}</title>
          <path class="organ abdomen"
            d="M205 530
               C190 590 190 660 210 720
               C232 780 288 780 310 720
               C330 660 330 590 315 530
               C300 500 220 500 205 530 Z"
            stroke="{col('abdomen')}"
            opacity="{max(0.20, min(0.80, t('abdomen','alpha',0.62)))}"/>
        </g>
      </g>

      <!-- KIDNEYS -->
      <g transform="translate({t('kidneys','dx',0.0)} {t('kidneys','dy',0.0)}) scale({t('kidneys','scale',1.0)})">
        <g class="organWrap" filter="{flt('kidneys')}">
          <title>Kidneys: {state('kidneys')}</title>

          <path class="organ"
            d="M208 610
               C190 610 184 632 190 654
               C198 686 232 692 248 674
               C260 660 258 636 250 624
               C242 612 228 610 208 610 Z"
            fill="{col('kidneys')}" opacity="{t('kidneys','alpha',0.62)}"/>

          <path class="organ"
            d="M312 610
               C330 610 336 632 330 654
               C322 686 288 692 272 674
               C260 660 262 636 270 624
               C278 612 292 610 312 610 Z"
            fill="{col('kidneys')}" opacity="{t('kidneys','alpha',0.62)}"/>
        </g>
      </g>

    </svg>
  </div>
</body>
</html>
"""


# ---------------- Demo data for charts ----------------
np.random.seed(7)
days = pd.date_range(end=pd.Timestamp.today().normalize(), periods=30, freq="D")
sys = 120 + np.cumsum(np.random.normal(0, 1.6, len(days)))
dia = 78 + np.cumsum(np.random.normal(0, 1.1, len(days)))
pulse = 72 + np.cumsum(np.random.normal(0, 0.35, len(days)))
glucose = 4.8 + np.cumsum(np.random.normal(0, 0.05, len(days)))
vitals = pd.DataFrame({"date": days, "systolic": sys, "diastolic": dia, "pulse": pulse, "glucose": glucose})


# ---------------- Sidebar ----------------
st.sidebar.markdown("### 🧬 Medical Dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown("**Patient (demo)**")
st.sidebar.markdown("<div class='muted'>Demo data. Not medical advice.</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Body map — background**")
bg_file = st.sidebar.file_uploader(
    "Upload PNG/JPG (X-ray/HUD)",
    type=["png", "jpg", "jpeg"],
    help="Use your own/licensed image without watermarks.",
)
bg_opacity = st.sidebar.slider("Background opacity", 0.10, 1.00, 0.70, 0.05)
bg_blend = st.sidebar.selectbox("Blend mode", ["screen", "lighten", "normal"], index=0)

bg_fit = st.sidebar.selectbox(
    "Background fit",
    ["cover", "contain"],
    index=0,
    help="cover = larger (cropping expected). contain = shows everything but may look smaller.",
)

bg_pos_x = st.sidebar.slider("Position X (%)", 0.0, 100.0, 50.0, 1.0)
bg_pos_y = st.sidebar.slider("Position Y (%)", 0.0, 100.0, 42.0, 1.0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Organ status**")
status: dict[str, str] = {}
for o in ORGANS:
    status[o] = st.sidebar.selectbox(o.capitalize(), ["healthy", "inflamed"], index=0, key=f"organ_{o}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Organ alignment tuning (per organ)**")

# Defaults for first run (tuned for the provided layout)
DEFAULTS: dict[str, dict[str, float]] = {
    "brain": {"scale": 0.94, "dx": 12.0, "dy": -48.0, "alpha": 0.55},
    "lungs": {"scale": 0.98, "dx": -1.0, "dy": -60.0, "alpha": 0.62},
    "heart": {"scale": 1.14, "dx": -215.0, "dy": 0.0, "alpha": 0.62},
    "abdomen": {"scale": 0.98, "dx": 0.0, "dy": 0.0, "alpha": 0.62},
    "kidneys": {"scale": 0.66, "dx": 79.0, "dy": -51.0, "alpha": 0.62},
}

tuning: dict[str, dict[str, float]] = {}
for o in ORGANS:
    d = DEFAULTS.get(o, {"scale": 1.0, "dx": 0.0, "dy": 0.0, "alpha": 0.62})
    with st.sidebar.expander(f"{o.capitalize()} tuning", expanded=False):
        tuning[o] = {
            "scale": st.slider(
                "Scale",
                0.60,
                1.80,
                float(d["scale"]),
                0.02,
                key=f"t_{o}_scale",
            ),
            "dx": st.slider(
                "Offset X",
                -250.0,
                250.0,
                float(d["dx"]),
                1.0,
                key=f"t_{o}_dx",
            ),
            "dy": st.slider(
                "Offset Y",
                -260.0,
                260.0,
                float(d["dy"]),
                1.0,
                key=f"t_{o}_dy",
            ),
            "alpha": st.slider(
                "Opacity",
                0.20,
                0.95,
                float(d["alpha"]),
                0.01,
                key=f"t_{o}_alpha",
            ),
        }

st.sidebar.markdown("---")
map_height = st.sidebar.slider("Body map height", min_value=520, max_value=980, value=760, step=20)

bg_data_uri: str | None = None
if bg_file is not None:
    mime = bg_file.type or "image/png"
    bg_data_uri = bytes_to_data_uri(bg_file.getvalue(), mime)


# ---------------- Layout ----------------
outer_left, outer_right = st.columns([3.6, 2.2], gap="large")

# ===== LEFT =====
with outer_left:
    st.markdown("## Patient: Demo Patient")
    st.markdown("<div class='muted'>ID: P-001 • Sex: Angel • Age: 29</div>", unsafe_allow_html=True)

    top1, top2, top3 = st.columns([1.2, 1.2, 1.0], gap="large")
    last = vitals.iloc[-1]

    with top1:
        st.markdown(
            metric_html(
                "Blood pressure (latest)",
                f"{int(last['systolic'])}/{int(last['diastolic'])} <span>mmHg</span>",
                "a",
            ),
            unsafe_allow_html=True,
        )
    with top2:
        st.markdown(
            metric_html("Pulse (latest)", f"{int(last['pulse'])} <span>bpm</span>", "b"),
            unsafe_allow_html=True,
        )
    with top3:
        inflamed_count = sum(1 for v in status.values() if v == "inflamed")
        st.markdown(
            kpi_html("Inflamed organs", f"{inflamed_count}", "neg" if inflamed_count else "pos"),
            unsafe_allow_html=True,
        )
        st.markdown(
            kpi_html("Glucose (latest)", f"{last['glucose']:.1f}", "pos"),
            unsafe_allow_html=True,
        )

    # --- ECG card ---
    card_open()
    hr = float(last["pulse"])
    t_ecg, y_ecg = synthetic_ecg(hr_bpm=hr, duration_s=10.0, fs=500)

    fig_ecg = go.Figure()
    fig_ecg.add_trace(
        go.Scatter(
            x=t_ecg,
            y=y_ecg,
            mode="lines",
            name="ECG",
            line=dict(color="rgba(61,255,184,0.95)", width=2.6),
            hovertemplate="t=%{x:.3f}s<br>mV=%{y:.3f}<extra></extra>",
        )
    )
    fig_style(fig_ecg, "ECG waveform (10 seconds)", height=300)
    fig_ecg.update_layout(showlegend=False)
    fig_ecg.update_xaxes(title_text="Seconds", dtick=1.0)
    fig_ecg.update_yaxes(title_text="mV")
    st.plotly_chart(fig_ecg, use_container_width=True, config={"displayModeBar": False})
    card_close()

    b1, b2 = st.columns(2, gap="large")

    # --- Condition card ---
    with b1:
        card_open()

        chip_text, chip_class, desc = condition_from_status(status)
        inflamed_organs = [o for o, v in status.items() if v == "inflamed"]

        st.markdown("#### Condition")
        st.markdown(kpi_html("Condition", chip_text, chip_class), unsafe_allow_html=True)

        if inflamed_organs:
            st.markdown(
                "<div class='muted' style='margin-top:6px;'>"
                f"Organs flagged: <b>{', '.join([o.capitalize() for o in inflamed_organs])}</b>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='muted' style='margin-top:6px;'>Organs flagged: —</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"<div class='muted' style='margin-top:10px; line-height:1.35'>{desc}</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='muted' style='margin-top:10px; font-size:0.85rem;'>"
            "This card is generated from organ statuses in the sidebar (demo)."
            "</div>",
            unsafe_allow_html=True,
        )
        card_close()

    # --- Doctor's Orders card (replaces Glucose last 10 days chart) ---
    with b2:
        card_open()

        st.markdown("#### Doctor's Orders")

        chip_text, chip_class, desc, note = doctor_orders_from_status(status)
        st.markdown(kpi_html("Plan", chip_text, chip_class), unsafe_allow_html=True)

        st.markdown(
            f"<div class='muted' style='margin-top:10px; line-height:1.35'>{desc}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='muted' style='margin-top:10px; font-size:0.85rem;'>{note}</div>",
            unsafe_allow_html=True,
        )

        card_close()

# ===== RIGHT =====
with outer_right:
    card_open()
    st.markdown(
        "<div class='muted' style='font-weight:800;margin-bottom:6px;'>Body map (HUD background + organ highlights)</div>",
        unsafe_allow_html=True,
    )

    scene = body_scene_html(
        status=status,
        tuning=tuning,
        height_px=map_height,
        bg_data_uri=bg_data_uri,
        bg_opacity=bg_opacity,
        bg_blend=bg_blend,
        bg_fit=bg_fit,
        bg_pos_x=bg_pos_x,
        bg_pos_y=bg_pos_y,
    )
    components.html(scene, height=map_height + 10, scrolling=False)
    card_close()

    st.markdown("### Alerts")
    inflamed = [o for o, v in status.items() if v == "inflamed"]
    if inflamed:
        for o in inflamed:
            st.markdown(kpi_html(o.capitalize(), "inflamed", "neg"), unsafe_allow_html=True)
    else:
        st.markdown(kpi_html("All organs", "healthy", "pos"), unsafe_allow_html=True)

    st.markdown(
        "<div class='muted' style='margin-top:6px;'>This is a visualization of statuses, not an automatic diagnosis.</div>",
        unsafe_allow_html=True,
    )
### streamlit run med_app.py