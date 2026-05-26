import math
from datetime import datetime

import pandas as pd
import streamlit as st


# =========================================================
# SISTEM PENILAIAN TERNAK PRO
# Fitur:
# - Form ruminansia dan ayam dipisah
# - Evaluasi kuantitatif dan kualitatif
# - Pembanding SNI/acuan minimum yang bisa diedit
# - Mode pengguna: peternak, jagal, blantik, pembibit, ayam lokal
# - Rekomendasi akhir
# - Analisis ekonomi lanjutan
# - Riwayat evaluasi, grafik, CSV, dan laporan HTML
# =========================================================


st.set_page_config(
    page_title="Sistem Penilaian Ternak Pro",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS LIGHT / DARK
# =========================================================

CUSTOM_CSS = """
<style>
:root {
    color-scheme: light dark;
    --bg1: #f8fafc;
    --bg2: #eef2ff;
    --surface: rgba(255,255,255,0.88);
    --surface2: rgba(255,255,255,0.68);
    --text: #0f172a;
    --muted: #475569;
    --soft: #64748b;
    --border: rgba(15, 23, 42, .14);
    --shadow: 0 12px 34px rgba(15, 23, 42, .10);
    --primary: #2563eb;
    --primary-soft: rgba(37,99,235,.12);
    --good: #16a34a;
    --good-soft: rgba(22,163,74,.12);
    --warn: #d97706;
    --warn-soft: rgba(217,119,6,.14);
    --bad: #dc2626;
    --bad-soft: rgba(220,38,38,.12);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg1: #020617;
        --bg2: #0f172a;
        --surface: rgba(15,23,42,.84);
        --surface2: rgba(30,41,59,.64);
        --text: #e5e7eb;
        --muted: #cbd5e1;
        --soft: #94a3b8;
        --border: rgba(226,232,240,.16);
        --shadow: 0 14px 42px rgba(0,0,0,.35);
        --primary: #60a5fa;
        --primary-soft: rgba(96,165,250,.16);
        --good: #4ade80;
        --good-soft: rgba(74,222,128,.15);
        --warn: #fbbf24;
        --warn-soft: rgba(251,191,36,.16);
        --bad: #f87171;
        --bad-soft: rgba(248,113,113,.15);
    }
}

.stApp {
    background:
        radial-gradient(circle at top left, var(--bg2), transparent 34%),
        linear-gradient(135deg, var(--bg1), var(--bg2));
    color: var(--text);
}

.main .block-container {
    max-width: 1320px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

.hero {
    border: 1px solid var(--border);
    border-radius: 28px;
    background: linear-gradient(135deg, var(--surface), var(--surface2));
    box-shadow: var(--shadow);
    padding: 28px 30px;
    margin-bottom: 18px;
    backdrop-filter: blur(16px);
}

.hero-title {
    font-size: clamp(1.7rem, 3vw, 2.7rem);
    font-weight: 900;
    line-height: 1.08;
    letter-spacing: -0.04em;
    margin-bottom: 8px;
    color: var(--text);
}

.hero-subtitle {
    color: var(--muted);
    max-width: 960px;
    line-height: 1.6;
}

.card {
    border: 1px solid var(--border);
    border-radius: 20px;
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 18px 20px;
    margin-bottom: 14px;
}

.metric-card {
    border: 1px solid var(--border);
    border-radius: 20px;
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 18px 20px;
    min-height: 118px;
}

.big-score {
    font-size: clamp(2.4rem, 5vw, 3.5rem);
    font-weight: 900;
    color: var(--primary);
    letter-spacing: -0.06em;
    line-height: 1;
}

.muted {
    color: var(--muted);
}

.badge {
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 7px 13px;
    margin: 4px 6px 4px 0;
    background: var(--surface2);
    color: var(--muted);
    font-weight: 700;
    font-size: .88rem;
}

.badge-primary {
    color: var(--primary);
    background: var(--primary-soft);
}

.badge-good {
    color: var(--good);
    background: var(--good-soft);
}

.badge-warn {
    color: var(--warn);
    background: var(--warn-soft);
}

.badge-bad {
    color: var(--bad);
    background: var(--bad-soft);
}

.insight {
    border: 1px solid var(--border);
    border-left: 7px solid var(--primary);
    border-radius: 18px;
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 16px 18px;
    margin-bottom: 12px;
    line-height: 1.58;
}

.insight.good {
    border-left-color: var(--good);
    background: linear-gradient(90deg, var(--good-soft), transparent 40%), var(--surface);
}

.insight.warn {
    border-left-color: var(--warn);
    background: linear-gradient(90deg, var(--warn-soft), transparent 40%), var(--surface);
}

.insight.bad {
    border-left-color: var(--bad);
    background: linear-gradient(90deg, var(--bad-soft), transparent 40%), var(--surface);
}

div[data-testid="stMetric"] {
    border: 1px solid var(--border);
    border-radius: 18px;
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 12px 14px;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border-color: var(--border) !important;
    background-color: var(--surface) !important;
    color: var(--text) !important;
}

.stButton button,
.stDownloadButton button {
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
    font-weight: 800 !important;
}

.stButton button:hover,
.stDownloadButton button:hover {
    border-color: var(--primary) !important;
    color: var(--primary) !important;
}

button[data-baseweb="tab"] {
    border-radius: 999px !important;
    color: var(--muted) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: var(--primary-soft) !important;
    color: var(--primary) !important;
    font-weight: 900 !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--surface), var(--surface2)) !important;
    border-right: 1px solid var(--border);
}

hr {
    border-color: var(--border);
    margin: 1.2rem 0;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

BREED_DATA = {
    "Sapi Potong": {
        "Bali": {
            "kind": "ruminant",
            "target_min": 280,
            "target_ideal": 350,
            "height_min": 115,
            "height_max": 130,
            "adg": 0.55,
            "dressing": 50,
            "colors": ["Merah bata", "Cokelat kemerahan", "Hitam pada jantan dewasa"],
            "face": ["Lurus", "Pendek agak lebar"],
            "horn_or_comb": ["Bertanduk", "Tanduk kecil"],
            "ear_or_leg": ["Telinga sedang", "Telinga tegak sedang"],
            "build": ["Kompak", "Padat", "Rangka sedang"],
            "features": ["Kaki kuat", "Punggung lurus", "Paha berisi", "Bulu bersih"],
            "sni": {
                "name": "SNI 7651-4:2023 - Bibit sapi potong Bali",
                "coverage": "bibit",
                "min_weight": 280,
                "min_height": 115,
                "min_length": 110,
                "min_girth": 145,
                "min_bcs": 2.5,
            },
        },
        "Peranakan Ongole / PO": {
            "kind": "ruminant",
            "target_min": 320,
            "target_ideal": 450,
            "height_min": 125,
            "height_max": 145,
            "adg": 0.65,
            "dressing": 49,
            "colors": ["Putih", "Abu-abu muda", "Abu-abu tua"],
            "face": ["Panjang", "Lurus", "Cembung ringan"],
            "horn_or_comb": ["Bertanduk", "Tanduk kecil"],
            "ear_or_leg": ["Telinga sedang", "Telinga agak menggantung"],
            "build": ["Rangka besar", "Tinggi", "Panjang"],
            "features": ["Punuk terlihat", "Gelambir berkembang", "Dada dalam", "Kaki kuat"],
            "sni": {
                "name": "SNI 7651-5:2022 - Bibit sapi potong PO",
                "coverage": "bibit",
                "min_weight": 320,
                "min_height": 125,
                "min_length": 120,
                "min_girth": 150,
                "min_bcs": 2.5,
            },
        },
        "Simmental Cross": {
            "kind": "ruminant",
            "target_min": 450,
            "target_ideal": 650,
            "height_min": 135,
            "height_max": 155,
            "adg": 0.95,
            "dressing": 53,
            "colors": ["Cokelat putih", "Merah putih", "Krem putih"],
            "face": ["Lebar", "Lurus"],
            "horn_or_comb": ["Bertanduk", "Tidak bertanduk/polled"],
            "ear_or_leg": ["Telinga sedang", "Telinga tegak sedang"],
            "build": ["Rangka besar", "Berotot", "Panjang dan dalam"],
            "features": ["Dada dalam", "Punggung lebar", "Paha penuh", "Kaki kokoh"],
            "sni": {
                "name": "SNI 7651-8:2022 - Bibit sapi potong Simmental Indonesia",
                "coverage": "bibit",
                "min_weight": 450,
                "min_height": 135,
                "min_length": 130,
                "min_girth": 165,
                "min_bcs": 2.5,
            },
        },
        "Limousin Cross": {
            "kind": "ruminant",
            "target_min": 450,
            "target_ideal": 650,
            "height_min": 135,
            "height_max": 155,
            "adg": 0.95,
            "dressing": 54,
            "colors": ["Cokelat keemasan", "Merah kecokelatan", "Cokelat muda"],
            "face": ["Panjang", "Lurus"],
            "horn_or_comb": ["Bertanduk", "Tidak bertanduk/polled"],
            "ear_or_leg": ["Telinga sedang", "Telinga tegak sedang"],
            "build": ["Berotot", "Rangka besar", "Punggung panjang"],
            "features": ["Paha sangat berisi", "Punggung lebar", "Dada dalam", "Kaki kokoh"],
            "sni": {
                "name": "SNI 7651-9:2022 - Bibit sapi potong Limousin Indonesia",
                "coverage": "bibit",
                "min_weight": 450,
                "min_height": 135,
                "min_length": 130,
                "min_girth": 165,
                "min_bcs": 2.5,
            },
        },
        "Brahman Cross": {
            "kind": "ruminant",
            "target_min": 400,
            "target_ideal": 550,
            "height_min": 130,
            "height_max": 150,
            "adg": 0.85,
            "dressing": 51,
            "colors": ["Abu-abu", "Putih keabu-abuan", "Merah kecokelatan"],
            "face": ["Panjang", "Cembung ringan"],
            "horn_or_comb": ["Bertanduk", "Tanduk kecil", "Tidak bertanduk/polled"],
            "ear_or_leg": ["Telinga menggantung", "Telinga panjang menggantung"],
            "build": ["Rangka besar", "Panjang", "Berotot sedang"],
            "features": ["Punuk jelas", "Gelambir berkembang", "Kulit longgar", "Dada dalam"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 400,
                "min_height": 130,
                "min_length": 125,
                "min_girth": 160,
                "min_bcs": 2.5,
            },
        },
    },
    "Sapi Perah": {
        "Friesian Holstein / FH": {
            "kind": "ruminant",
            "target_min": 400,
            "target_ideal": 550,
            "height_min": 130,
            "height_max": 150,
            "adg": 0.70,
            "dressing": 47,
            "colors": ["Hitam putih", "Putih hitam", "Belang hitam putih"],
            "face": ["Panjang", "Lurus"],
            "horn_or_comb": ["Tidak bertanduk/polled", "Bertanduk", "Tanduk kecil"],
            "ear_or_leg": ["Telinga sedang", "Telinga tegak sedang"],
            "build": ["Tinggi", "Panjang", "Bentuk tubuh perah"],
            "features": ["Ambing proporsional", "Kaki kuat", "Punggung lurus", "Rangka panjang"],
            "sni": {
                "name": "SNI 2735:2022 - Bibit sapi perah FH Indonesia",
                "coverage": "bibit",
                "min_weight": 400,
                "min_height": 130,
                "min_length": 125,
                "min_girth": 160,
                "min_bcs": 2.5,
            },
        },
    },
    "Kerbau": {
        "Kerbau Lumpur / Rawa": {
            "kind": "ruminant",
            "target_min": 350,
            "target_ideal": 500,
            "height_min": 125,
            "height_max": 145,
            "adg": 0.55,
            "dressing": 45,
            "colors": ["Abu-abu gelap", "Hitam keabu-abuan", "Cokelat kehitaman"],
            "face": ["Panjang", "Lebar"],
            "horn_or_comb": ["Tanduk besar", "Tanduk melengkung", "Bertanduk"],
            "ear_or_leg": ["Telinga sedang", "Telinga agak menggantung"],
            "build": ["Rangka besar", "Dada dalam", "Kuat"],
            "features": ["Kulit tebal", "Kaki kuat", "Tubuh lebar", "Tanduk melengkung"],
            "sni": {
                "name": "SNI 7706:2023 - Bibit kerbau lumpur",
                "coverage": "bibit",
                "min_weight": 350,
                "min_height": 125,
                "min_length": 120,
                "min_girth": 160,
                "min_bcs": 2.5,
            },
        },
    },
    "Kambing": {
        "Kacang": {
            "kind": "ruminant",
            "target_min": 18,
            "target_ideal": 28,
            "height_min": 45,
            "height_max": 60,
            "adg": 0.06,
            "dressing": 43,
            "colors": ["Cokelat", "Hitam", "Putih", "Belang"],
            "face": ["Pendek", "Lurus"],
            "horn_or_comb": ["Bertanduk", "Tanduk kecil"],
            "ear_or_leg": ["Telinga kecil", "Telinga tegak"],
            "build": ["Kompak", "Kecil", "Lincah"],
            "features": ["Tubuh kompak", "Kaki kuat", "Bulu bersih", "Gerak lincah"],
            "sni": {
                "name": "SNI 7352-2:2018 - Bibit kambing Kacang",
                "coverage": "bibit",
                "min_weight": 18,
                "min_height": 45,
                "min_length": 42,
                "min_girth": 50,
                "min_bcs": 2.5,
            },
        },
        "Peranakan Etawa / PE": {
            "kind": "ruminant",
            "target_min": 35,
            "target_ideal": 60,
            "height_min": 65,
            "height_max": 90,
            "adg": 0.10,
            "dressing": 44,
            "colors": ["Putih hitam", "Putih cokelat", "Belang", "Cokelat putih"],
            "face": ["Cembung", "Roman nose", "Panjang"],
            "horn_or_comb": ["Bertanduk", "Tanduk kecil"],
            "ear_or_leg": ["Telinga panjang menggantung", "Telinga menggantung"],
            "build": ["Tinggi", "Panjang", "Dwiguna"],
            "features": ["Telinga panjang menggantung", "Profil wajah cembung", "Ambing proporsional", "Kaki tinggi"],
            "sni": {
                "name": "SNI 7352-1:2022 - Bibit kambing PE",
                "coverage": "bibit",
                "min_weight": 35,
                "min_height": 65,
                "min_length": 62,
                "min_girth": 70,
                "min_bcs": 2.5,
            },
        },
        "Boer": {
            "kind": "ruminant",
            "target_min": 35,
            "target_ideal": 70,
            "height_min": 60,
            "height_max": 80,
            "adg": 0.15,
            "dressing": 48,
            "colors": ["Putih kepala cokelat", "Putih cokelat", "Cokelat putih"],
            "face": ["Cembung ringan", "Lebar", "Roman nose"],
            "horn_or_comb": ["Bertanduk", "Tanduk kecil", "Melengkung ke belakang"],
            "ear_or_leg": ["Telinga menggantung", "Telinga sedang menggantung"],
            "build": ["Berotot", "Dada lebar", "Paha penuh"],
            "features": ["Kepala cokelat", "Badan putih dominan", "Paha penuh", "Dada lebar"],
            "sni": {
                "name": "SNI 7352-8:2024 - Bibit kambing Boer",
                "coverage": "bibit",
                "min_weight": 35,
                "min_height": 60,
                "min_length": 58,
                "min_girth": 70,
                "min_bcs": 2.5,
            },
        },
    },
    "Domba": {
        "Domba Garut": {
            "kind": "ruminant",
            "target_min": 30,
            "target_ideal": 55,
            "height_min": 55,
            "height_max": 75,
            "adg": 0.12,
            "dressing": 47,
            "colors": ["Putih", "Hitam", "Cokelat", "Belang"],
            "face": ["Sedang", "Lurus"],
            "horn_or_comb": ["Tanduk besar", "Tanduk melingkar", "Bertanduk"],
            "ear_or_leg": ["Telinga kecil", "Telinga sedang"],
            "build": ["Berotot", "Kompak", "Dada lebar"],
            "features": ["Tanduk kuat", "Dada lebar", "Punggung kuat", "Paha berisi"],
            "sni": {
                "name": "SNI 7532.1:2015 - Bibit domba Garut",
                "coverage": "bibit",
                "min_weight": 30,
                "min_height": 55,
                "min_length": 50,
                "min_girth": 65,
                "min_bcs": 2.5,
            },
        },
    },
    "Ayam Lokal Indonesia": {
        "Ayam Kampung": {
            "kind": "poultry",
            "target_min": 0.9,
            "target_ideal": 1.5,
            "height_min": 30,
            "height_max": 45,
            "adg": 0.010,
            "dressing": 62,
            "colors": ["Campuran/liar", "Hitam merah", "Cokelat merah", "Wiring", "Belang"],
            "face": ["Kepala sedang", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki putih", "Kaki hitam", "Kaki kehijauan"],
            "build": ["Tubuh sedang", "Lincah", "Tipe dwiguna lokal"],
            "features": ["Gerak lincah", "Bulu rapat dan mengilap", "Dada cukup berisi", "Kaki kuat", "Mata cerah"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 0.9,
                "min_height": 30,
                "min_length": 25,
                "min_girth": 25,
                "min_bcs": 2.5,
            },
        },
        "Ayam KUB-1": {
            "kind": "poultry",
            "target_min": 1.0,
            "target_ideal": 1.6,
            "height_min": 30,
            "height_max": 45,
            "adg": 0.012,
            "dressing": 62,
            "colors": ["Campuran/liar", "Hitam merah", "Cokelat merah", "Wiring", "Belang"],
            "face": ["Kepala sedang", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki putih", "Kaki hitam"],
            "build": ["Tipe petelur lokal", "Tubuh sedang", "Lincah"],
            "features": ["Gerak lincah", "Bulu rapat dan mengilap", "Produksi telur relatif baik", "Dada cukup berisi", "Mata cerah"],
            "sni": {
                "name": "SNI 8405-1:2017 - Bibit ayam umur sehari/kuri KUB-1",
                "coverage": "DOC/kuri",
                "min_weight": 0.035,
                "min_height": 8,
                "min_length": 6,
                "min_girth": 5,
                "min_bcs": 2.5,
            },
        },
        "Ayam KUB Janaka Agrinak": {
            "kind": "poultry",
            "target_min": 1.0,
            "target_ideal": 1.7,
            "height_min": 30,
            "height_max": 45,
            "adg": 0.012,
            "dressing": 62,
            "colors": ["Campuran/liar", "Cokelat merah", "Hitam merah", "Wiring"],
            "face": ["Kepala sedang", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki putih", "Kaki hitam"],
            "build": ["Tipe petelur lokal", "Tubuh sedang", "Lincah"],
            "features": ["Gerak lincah", "Bulu rapat dan mengilap", "Produksi telur relatif baik", "Dada cukup berisi", "Mata cerah"],
            "sni": {
                "name": "SNI 8405-2:2023 - Bibit ayam umur sehari/kuri KUB Janaka Agrinak",
                "coverage": "DOC/kuri",
                "min_weight": 0.035,
                "min_height": 8,
                "min_length": 6,
                "min_girth": 5,
                "min_bcs": 2.5,
            },
        },
        "Ayam Sentul": {
            "kind": "poultry",
            "target_min": 1.0,
            "target_ideal": 1.7,
            "height_min": 32,
            "height_max": 48,
            "adg": 0.011,
            "dressing": 62,
            "colors": ["Abu-abu", "Kelabu", "Sentul batu", "Sentul kelabu", "Sentul mas"],
            "face": ["Kepala sedang", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki putih", "Kaki hitam"],
            "build": ["Tubuh sedang", "Tipe dwiguna lokal", "Lincah"],
            "features": ["Warna kelabu/sentul khas", "Gerak lincah", "Dada cukup berisi", "Bulu rapat dan mengilap", "Kaki kuat"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.0,
                "min_height": 32,
                "min_length": 26,
                "min_girth": 26,
                "min_bcs": 2.5,
            },
        },
        "Ayam Pelung": {
            "kind": "poultry",
            "target_min": 2.0,
            "target_ideal": 3.5,
            "height_min": 45,
            "height_max": 70,
            "adg": 0.014,
            "dressing": 60,
            "colors": ["Hitam merah", "Wiring", "Cokelat merah", "Campuran/liar"],
            "face": ["Kepala besar", "Postur kepala tegap", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger besar"],
            "ear_or_leg": ["Kaki panjang", "Kaki kuning", "Kaki hitam"],
            "build": ["Postur tegap", "Tubuh besar", "Panjang"],
            "features": ["Postur tinggi dan tegap", "Suara panjang/merdu pada jantan", "Leher panjang", "Kaki panjang dan kuat", "Dada cukup dalam"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 2.0,
                "min_height": 45,
                "min_length": 35,
                "min_girth": 32,
                "min_bcs": 2.5,
            },
        },
        "Ayam Kedu Hitam": {
            "kind": "poultry",
            "target_min": 1.2,
            "target_ideal": 2.0,
            "height_min": 35,
            "height_max": 55,
            "adg": 0.011,
            "dressing": 61,
            "colors": ["Hitam", "Hitam mengilap"],
            "face": ["Kepala sedang", "Paruh gelap"],
            "horn_or_comb": ["Jengger tunggal", "Jengger gelap", "Jengger kecil"],
            "ear_or_leg": ["Kaki hitam", "Kaki gelap"],
            "build": ["Tubuh sedang", "Postur tegap", "Tipe dwiguna lokal"],
            "features": ["Bulu hitam dominan", "Paruh/kaki cenderung gelap", "Bulu rapat dan mengilap", "Kaki kuat", "Mata cerah"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.2,
                "min_height": 35,
                "min_length": 28,
                "min_girth": 28,
                "min_bcs": 2.5,
            },
        },
        "Ayam Cemani": {
            "kind": "poultry",
            "target_min": 1.2,
            "target_ideal": 2.0,
            "height_min": 35,
            "height_max": 55,
            "adg": 0.010,
            "dressing": 60,
            "colors": ["Hitam total", "Hitam mengilap"],
            "face": ["Kepala sedang", "Paruh gelap"],
            "horn_or_comb": ["Jengger gelap", "Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki hitam", "Kaki gelap"],
            "build": ["Tubuh sedang", "Postur tegap"],
            "features": ["Bulu hitam total", "Kulit/jengger/paruh/kaki hitam", "Bulu rapat dan mengilap", "Kaki kuat", "Mata cerah"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.2,
                "min_height": 35,
                "min_length": 28,
                "min_girth": 28,
                "min_bcs": 2.5,
            },
        },
        "Ayam Nunukan": {
            "kind": "poultry",
            "target_min": 1.4,
            "target_ideal": 2.2,
            "height_min": 35,
            "height_max": 55,
            "adg": 0.012,
            "dressing": 62,
            "colors": ["Cokelat kemerahan", "Buff/kuning kecokelatan", "Columbian"],
            "face": ["Kepala sedang", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki putih"],
            "build": ["Tubuh sedang", "Tipe dwiguna lokal"],
            "features": ["Warna cokelat kemerahan/buff", "Ujung sayap atau ekor cenderung gelap", "Pertumbuhan bulu relatif lambat", "Dada cukup berisi", "Kaki kuat"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.4,
                "min_height": 35,
                "min_length": 28,
                "min_girth": 28,
                "min_bcs": 2.5,
            },
        },
        "Ayam Merawang": {
            "kind": "poultry",
            "target_min": 1.2,
            "target_ideal": 2.0,
            "height_min": 35,
            "height_max": 55,
            "adg": 0.011,
            "dressing": 62,
            "colors": ["Kuning keemasan", "Cokelat keemasan", "Cokelat merah"],
            "face": ["Kepala sedang", "Paruh sedang"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki putih"],
            "build": ["Tubuh sedang", "Tipe dwiguna lokal"],
            "features": ["Warna kuning/cokelat keemasan", "Bulu rapat dan mengilap", "Dada cukup berisi", "Kaki kuat", "Gerak lincah"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.2,
                "min_height": 35,
                "min_length": 28,
                "min_girth": 28,
                "min_bcs": 2.5,
            },
        },
        "Ayam Gaok": {
            "kind": "poultry",
            "target_min": 1.5,
            "target_ideal": 2.8,
            "height_min": 40,
            "height_max": 65,
            "adg": 0.012,
            "dressing": 61,
            "colors": ["Hitam merah", "Wiring", "Cokelat merah", "Campuran/liar"],
            "face": ["Kepala besar", "Postur kepala tegap"],
            "horn_or_comb": ["Jengger tunggal", "Jengger besar"],
            "ear_or_leg": ["Kaki panjang", "Kaki kuning", "Kaki hitam"],
            "build": ["Postur tegap", "Tubuh besar", "Panjang"],
            "features": ["Postur tinggi", "Suara panjang pada jantan", "Leher relatif panjang", "Kaki kuat", "Dada cukup dalam"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.5,
                "min_height": 40,
                "min_length": 32,
                "min_girth": 30,
                "min_bcs": 2.5,
            },
        },
        "Ayam Kokok Balenggek": {
            "kind": "poultry",
            "target_min": 1.2,
            "target_ideal": 2.0,
            "height_min": 35,
            "height_max": 55,
            "adg": 0.010,
            "dressing": 60,
            "colors": ["Hitam merah", "Wiring", "Cokelat merah", "Campuran/liar"],
            "face": ["Kepala sedang", "Postur kepala tegap"],
            "horn_or_comb": ["Jengger tunggal", "Jengger kecil"],
            "ear_or_leg": ["Kaki kuning", "Kaki hitam", "Kaki putih"],
            "build": ["Postur tegap", "Tubuh sedang", "Lincah"],
            "features": ["Kokok bertingkat/balenggek pada jantan", "Postur tegap", "Bulu rapat dan mengilap", "Kaki kuat", "Mata cerah"],
            "sni": {
                "name": "Acuan internal - belum dipetakan SNI langsung",
                "coverage": "internal",
                "min_weight": 1.2,
                "min_height": 35,
                "min_length": 28,
                "min_girth": 28,
                "min_bcs": 2.5,
            },
        },
    },
}


USER_MODES = [
    "Peternak",
    "Jagal",
    "Blantik / Jual Beli",
    "Pembibit",
    "Evaluasi SNI",
    "Ayam Lokal",
]


PURPOSE_OPTIONS = [
    "Penggemukan / Potong",
    "Bibit / Breeding",
    "Perah",
    "Jagal",
    "Blantik / Jual Beli",
    "Pedaging",
    "Petelur",
    "Hias / Kontes",
    "Pelestarian Rumpun",
]


# =========================================================
# FUNCTIONS
# =========================================================

def rupiah(value):
    return f"Rp{value:,.0f}".replace(",", ".")


def clamp(value, low, high):
    return max(low, min(high, value))


def get_age_stage(kind, age_months):
    if kind == "poultry":
        if age_months < 1:
            return "DOC/kuri"
        if age_months < 2:
            return "Starter"
        if age_months < 4:
            return "Grower"
        if age_months < 7:
            return "Dara/pullet atau jantan muda"
        return "Dewasa/produksi"

    if age_months < 8:
        return "Anak/pedet/cempe"
    if age_months < 18:
        return "Muda/tumbuh"
    if age_months < 36:
        return "Dewasa muda/siap produksi"
    return "Dewasa"


def estimate_ruminant_weight(girth_cm, length_cm, species):
    if species in ["Sapi Potong", "Sapi Perah", "Kerbau"]:
        return round((girth_cm ** 2 * length_cm) / 10840, 2)
    return round((girth_cm ** 2 * length_cm) / 10000, 2)


def score_weight(weight, target_min, target_ideal):
    if weight <= 0:
        return 0
    if weight < target_min:
        return round(clamp((weight / target_min) * 15, 0, 15), 1)
    if weight <= target_ideal:
        return round(15 + ((weight - target_min) / max(target_ideal - target_min, 1)) * 5, 1)
    excess = (weight - target_ideal) / max(target_ideal, 1)
    return round(clamp(20 - min(excess * 8, 4), 0, 20), 1)


def score_bcs(bcs, kind, purpose):
    low, high = (2.5, 3.5) if kind == "poultry" else (2.75, 4.0)
    if low <= bcs <= high:
        score = 15
    else:
        distance = min(abs(bcs - low), abs(bcs - high))
        score = 15 - distance * 5
    if purpose in ["Bibit / Breeding", "Petelur"] and bcs > 4:
        score -= 2
    return round(clamp(score, 0, 15), 1)


def score_range(value, low, high, max_score):
    if low <= value <= high:
        return max_score
    if value < low:
        ratio = value / max(low, 1)
        return round(clamp(ratio * max_score * 0.9, 0, max_score), 1)
    excess = (value - high) / max(high, 1)
    return round(clamp(max_score - min(excess * max_score, max_score * 0.35), 0, max_score), 1)


def score_body_proportion(girth_cm, length_cm, kind):
    ratio = length_cm / max(girth_cm, 1)
    low, high = (0.75, 1.35) if kind == "poultry" else (0.80, 1.20)
    score = score_range(ratio, low, high, 8)
    return score, round(ratio, 3)


def score_quant_extra(height_cm, chest_depth_cm, rump_width_cm, cannon_cm, kind):
    if height_cm <= 0:
        return 0, {}

    chest_ratio = chest_depth_cm / height_cm
    rump_ratio = rump_width_cm / height_cm
    cannon_ratio = cannon_cm / height_cm

    if kind == "poultry":
        chest_range = (0.25, 0.40)
        rump_range = (0.12, 0.24)
        cannon_range = (0.035, 0.090)
    else:
        chest_range = (0.36, 0.56)
        rump_range = (0.17, 0.34)
        cannon_range = (0.07, 0.18)

    chest_score = score_range(chest_ratio, *chest_range, 4)
    rump_score = score_range(rump_ratio, *rump_range, 3)
    cannon_score = score_range(cannon_ratio, *cannon_range, 3)

    details = {
        "Rasio kedalaman dada": round(chest_ratio, 3),
        "Rasio lebar pinggul/panggul": round(rump_ratio, 3),
        "Rasio lingkar kaki/tulang kering": round(cannon_ratio, 3),
        "Skor kedalaman dada": chest_score,
        "Skor lebar pinggul/panggul": rump_score,
        "Skor kaki/tulang kering": cannon_score,
    }

    return round(chest_score + rump_score + cannon_score, 1), details


def score_health(checks):
    if not checks:
        return 0
    return round((sum(1 for value in checks.values() if value) / len(checks)) * 15, 1)


def match_score(value, expected, max_score):
    if value in expected:
        return max_score, "Sesuai"
    if value in ["Tidak yakin", "Lainnya / tidak sesuai"]:
        return round(max_score * 0.35, 1), "Belum yakin"
    return round(max_score * 0.45, 1), "Kurang sesuai"


def score_phenotype(data, color, face, horn_or_comb, ear_or_leg, build, features):
    s_color, st_color = match_score(color, data["colors"], 3)
    s_face, st_face = match_score(face, data["face"], 2)
    s_horn, st_horn = match_score(horn_or_comb, data["horn_or_comb"], 2)
    s_ear, st_ear = match_score(ear_or_leg, data["ear_or_leg"], 2)
    s_build, st_build = match_score(build, data["build"], 2.5)

    expected_features = data["features"]
    feature_match = len([x for x in features if x in expected_features])
    s_feature = 3.5 * feature_match / max(len(expected_features), 1)

    total = round(s_color + s_face + s_horn + s_ear + s_build + s_feature, 1)

    details = pd.DataFrame(
        [
            ["Warna bulu", color, ", ".join(data["colors"]), st_color, s_color],
            ["Kepala/wajah/paruh", face, ", ".join(data["face"]), st_face, s_face],
            ["Tanduk/jengger", horn_or_comb, ", ".join(data["horn_or_comb"]), st_horn, s_horn],
            ["Telinga/kaki", ear_or_leg, ", ".join(data["ear_or_leg"]), st_ear, s_ear],
            ["Bentuk tubuh", build, ", ".join(data["build"]), st_build, s_build],
            ["Ciri khas", ", ".join(features) if features else "-", ", ".join(expected_features), f"{feature_match}/{len(expected_features)} cocok", round(s_feature, 1)],
        ],
        columns=["Ciri", "Input", "Acuan", "Status", "Skor"],
    )

    return clamp(total, 0, 15), details


def classify_score(score):
    if score >= 85:
        return "Sangat Layak", "good"
    if score >= 70:
        return "Layak", "good"
    if score >= 55:
        return "Perlu Perbaikan", "warn"
    return "Risiko Tinggi", "bad"


def final_decision(score, sni_percent, health_score, purpose, mode, kind):
    if health_score < 9:
        return "❌ Tunda keputusan. Kesehatan lapangan belum aman."

    if score >= 85 and sni_percent >= 85:
        if mode == "Jagal":
            return "✅ Layak dibeli untuk potong, cek harga akhir dan kondisi karkas."
        if mode == "Blantik / Jual Beli":
            return "✅ Layak untuk transaksi, masih aman untuk dijual sebagai ternak berkualitas."
        if mode == "Pembibit":
            return "✅ Potensial untuk bibit, lanjutkan cek reproduksi dan asal-usul."
        if kind == "poultry":
            return "✅ Layak dipertahankan/dibeli sesuai tujuan ayam lokal."
        return "✅ Layak dipelihara atau dibeli."

    if score >= 70:
        return "⚠️ Layak bersyarat. Bisa dipilih, tetapi harga dan risiko perlu dinegosiasikan."

    if score >= 55:
        return "⚠️ Perlu perbaikan 7–30 hari sebelum dijadikan pilihan utama."

    return "❌ Tidak disarankan untuk keputusan besar atau harga premium."


def sni_compare(thresholds, weight, height, length, girth, bcs, pheno_score, health_score):
    rows = [
        ["Bobot hidup", weight, thresholds["min_weight"], "kg", weight >= thresholds["min_weight"]],
        ["Tinggi", height, thresholds["min_height"], "cm", height >= thresholds["min_height"]],
        ["Panjang badan", length, thresholds["min_length"], "cm", length >= thresholds["min_length"]],
        ["Lingkar dada", girth, thresholds["min_girth"], "cm", girth >= thresholds["min_girth"]],
        ["BCS", bcs, thresholds["min_bcs"], "skor", bcs >= thresholds["min_bcs"]],
        ["Kesesuaian fenotipe", round(pheno_score / 15 * 100, 1), 70, "%", pheno_score >= 10.5],
        ["Kesehatan lapangan", round(health_score / 15 * 100, 1), 80, "%", health_score >= 12],
    ]

    df = pd.DataFrame(rows, columns=["Parameter", "Nilai", "Acuan minimum", "Satuan", "Lolos"])
    df["Status"] = df["Lolos"].apply(lambda x: "Memenuhi" if x else "Belum memenuhi")
    percent = round(df["Lolos"].mean() * 100, 1)

    if percent >= 100:
        status = "Sesuai acuan"
    elif percent >= 70:
        status = "Mendekati acuan"
    else:
        status = "Belum sesuai acuan"

    return df, percent, status


def make_insights(
    kind,
    species,
    breed,
    mode,
    purpose,
    weight,
    target_min,
    target_ideal,
    bcs,
    health_score,
    pheno_score,
    quant_score,
    sni_percent,
    profit,
    max_buy_price,
):
    insights = []

    if weight < target_min:
        insights.append(("warn", "Bobot belum optimal", f"Bobot masih di bawah target minimum {target_min} kg. Prioritaskan pakan, kesehatan, dan evaluasi parasit."))
    elif weight <= target_ideal:
        insights.append(("good", "Bobot berada pada rentang target", f"Bobot {weight:.2f} kg berada pada rentang ekonomis untuk {breed}."))
    else:
        insights.append(("warn", "Bobot di atas target ideal", "Pastikan harga beli masih sebanding dengan tambahan bobot/karkas."))

    if pheno_score >= 12:
        insights.append(("good", "Ciri bangsa kuat", f"Fenotipe cukup sesuai dengan karakter {breed}."))
    elif pheno_score >= 8:
        insights.append(("warn", "Ciri bangsa sedang", "Ada ciri yang belum kuat. Untuk harga premium, minta bukti asal atau riwayat keturunan."))
    else:
        insights.append(("bad", "Ciri bangsa lemah", "Jangan membeli dengan harga premium hanya berdasarkan klaim bangsa/rumpun."))

    if health_score < 10:
        insights.append(("bad", "Kesehatan perlu dicek", "Nafsu makan, mata, napas, feses, kaki, bulu/kulit, dan luka perlu diperiksa ulang."))
    elif health_score < 13:
        insights.append(("warn", "Kesehatan cukup", "Masih bisa dipertimbangkan, tetapi tetap perlu pemeriksaan lapangan sebelum transaksi."))
    else:
        insights.append(("good", "Kesehatan baik", "Kondisi lapangan mendukung keputusan pemeliharaan atau pembelian."))

    if mode == "Jagal":
        insights.append(("info", "Insight jagal", "Fokus pada karkas, dada, paha, punggung, BCS, dan tidak pincang. Bobot besar belum tentu untung jika lemak berlebihan."))
    elif mode == "Blantik / Jual Beli":
        insights.append(("info", "Insight blantik", f"Harga maksimal beli berbasis simulasi: {rupiah(max_buy_price)}. Gunakan kekurangan SNI/fenotipe sebagai bahan negosiasi."))
    elif mode == "Pembibit":
        insights.append(("info", "Insight pembibit", "Prioritaskan asal-usul, reproduksi, kaki, kesehatan, kemurnian ciri bangsa, dan kesesuaian acuan."))
    elif kind == "poultry":
        insights.append(("info", "Insight ayam lokal", "Untuk ayam penyanyi nilai suara penting; untuk petelur nilai produksi telur penting; untuk Cemani/Kedu warna menjadi faktor harga."))
    else:
        insights.append(("info", "Insight peternak", "Pantau ADG, biaya pakan, BCS, dan target panen. Jangan hanya mengejar bobot tanpa kesehatan."))

    if profit >= 0:
        insights.append(("good", "Ekonomi positif", f"Simulasi menunjukkan potensi laba kasar {rupiah(profit)}."))
    else:
        insights.append(("warn", "Ekonomi belum aman", f"Simulasi menunjukkan potensi rugi kasar {rupiah(abs(profit))}. Tekan harga beli atau biaya pemeliharaan."))

    if sni_percent < 70:
        insights.append(("warn", "Acuan SNI belum kuat", "Beberapa parameter belum memenuhi acuan aplikasi. Aktifkan edit manual jika memakai dokumen SNI resmi."))
    else:
        insights.append(("good", "Acuan SNI cukup baik", f"Kesesuaian acuan mencapai {sni_percent}%."))

    return insights


def make_report_html(record, insights):
    insight_html = "".join(
        f"<li><strong>{title}:</strong> {body}</li>"
        for _, title, body in insights
    )

    rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in record.items()
    )

    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Laporan Evaluasi Ternak</title>
<style>
body {{
    font-family: Arial, sans-serif;
    line-height: 1.5;
    color: #111827;
    margin: 32px;
}}
h1, h2 {{ color: #0f172a; }}
table {{
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 20px;
}}
td, th {{
    border: 1px solid #d1d5db;
    padding: 8px 10px;
}}
th {{
    background: #f3f4f6;
}}
.badge {{
    display: inline-block;
    padding: 6px 10px;
    background: #e0f2fe;
    border-radius: 999px;
    font-weight: bold;
}}
</style>
</head>
<body>
<h1>Laporan Evaluasi Ternak</h1>
<p class="badge">{record.get("Kategori", "-")}</p>
<h2>Data Ringkas</h2>
<table>{rows}</table>
<h2>Insight</h2>
<ul>{insight_html}</ul>
<p><em>Laporan ini adalah alat bantu evaluasi, bukan sertifikat resmi.</em></p>
</body>
</html>
"""


# =========================================================
# SESSION
# =========================================================

if "records" not in st.session_state:
    st.session_state.records = []


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-title">🐄 Sistem Penilaian Ternak Pro</div>
    <div class="hero-subtitle">
        Evaluasi sapi, kerbau, kambing, domba, dan ayam lokal Indonesia berdasarkan faktor kuantitatif,
        kualitatif, kesehatan, ekonomi, mode pengguna, serta pembanding SNI/acuan minimum yang bisa diedit.
    </div>
    <div style="margin-top:14px;">
        <span class="badge badge-primary">📊 Skor 100</span>
        <span class="badge badge-good">🧬 Fenotipe bangsa/rumpun</span>
        <span class="badge badge-warn">🇮🇩 Pembanding SNI</span>
        <span class="badge">🌗 Light/Dark</span>
        <span class="badge">📈 Riwayat & grafik</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


st.sidebar.title("🐄 Evaluasi Ternak Pro")
st.sidebar.caption("Form adaptif, insight otomatis, ekonomi, SNI, dan riwayat evaluasi.")

with st.sidebar.expander("Cara pakai", expanded=True):
    st.write(
        """
1. Pilih jenis, bangsa/rumpun, mode pengguna, dan tujuan.
2. Isi data ukuran tubuh, BCS, kesehatan, dan ciri fenotipe.
3. Cek hasil, SNI, ekonomi, rekomendasi akhir, dan insight.
4. Simpan ke riwayat bila ingin membandingkan beberapa ternak.
"""
    )

st.sidebar.warning("Hasil adalah alat bantu. Untuk sertifikasi resmi, gunakan dokumen SNI dan petugas berwenang.")


tab_input, tab_result, tab_sni, tab_economy, tab_history, tab_report, tab_guide = st.tabs(
    [
        "📝 Input",
        "📊 Hasil",
        "🇮🇩 SNI/Acuan",
        "💰 Ekonomi",
        "📈 Riwayat",
        "📄 Laporan",
        "📘 Panduan",
    ]
)


# =========================================================
# INPUT
# =========================================================

with tab_input:
    st.subheader("Input Identitas dan Tujuan")

    c1, c2, c3 = st.columns(3)

    with c1:
        species = st.selectbox("Jenis ternak", list(BREED_DATA.keys()))
        breed = st.selectbox("Bangsa / rumpun", list(BREED_DATA[species].keys()))

    data = BREED_DATA[species][breed]
    kind = data["kind"]

    with c2:
        mode = st.selectbox(
            "Mode pengguna",
            USER_MODES,
            index=5 if species == "Ayam Lokal Indonesia" else 0,
        )

        purpose = st.selectbox(
            "Tujuan penilaian",
            PURPOSE_OPTIONS,
            index=5 if kind == "poultry" else 0,
        )

    with c3:
        animal_id = st.text_input("Kode / nama ternak", value=f"{breed}-{datetime.now().strftime('%H%M%S')}")
        sex = st.selectbox("Jenis kelamin", ["Jantan", "Betina", "Kebiri / tidak diketahui"])
        location = st.text_input("Lokasi / kandang", value="")

    st.markdown("---")
    st.subheader("Data Kuantitatif")

    if kind == "poultry":
        st.info("Form ayam memakai bobot aktual/estimasi timbang. Rumus bobot ruminansia tidak dipakai untuk ayam.")
        age_months = st.number_input("Umur ayam (bulan)", min_value=0.0, max_value=120.0, value=5.0, step=0.25)
        live_weight = st.number_input("Bobot hidup aktual / estimasi timbang (kg)", min_value=0.01, max_value=10.0, value=float(data["target_ideal"]), step=0.01)
        girth = st.number_input("Lingkar dada ayam (cm)", min_value=1.0, max_value=80.0, value=28.0, step=0.5)
        length = st.number_input("Panjang badan ayam (cm)", min_value=1.0, max_value=100.0, value=30.0, step=0.5)
        height = st.number_input("Tinggi ayam (cm)", min_value=1.0, max_value=100.0, value=float((data["height_min"] + data["height_max"]) / 2), step=0.5)
        chest_depth = st.number_input("Kedalaman dada (cm)", min_value=1.0, max_value=50.0, value=10.0, step=0.5)
        rump_width = st.number_input("Lebar panggul / badan belakang (cm)", min_value=1.0, max_value=50.0, value=8.0, step=0.5)
        cannon = st.number_input("Lingkar shank/kaki (cm)", min_value=0.1, max_value=20.0, value=2.5, step=0.1)
        weight = live_weight
    else:
        age_months = st.number_input("Umur ternak (bulan)", min_value=0.0, max_value=240.0, value=24.0, step=1.0)
        girth = st.number_input("Lingkar dada (cm)", min_value=10.0, max_value=300.0, value=150.0, step=0.5)
        length = st.number_input("Panjang badan (cm)", min_value=10.0, max_value=300.0, value=130.0, step=0.5)
        height = st.number_input("Tinggi pundak/gumba (cm)", min_value=10.0, max_value=250.0, value=float((data["height_min"] + data["height_max"]) / 2), step=0.5)
        chest_depth = st.number_input("Kedalaman dada (cm)", min_value=1.0, max_value=150.0, value=60.0, step=0.5)
        rump_width = st.number_input("Lebar pinggul/panggul (cm)", min_value=1.0, max_value=150.0, value=35.0, step=0.5)
        cannon = st.number_input("Lingkar tulang kering/kaki depan (cm)", min_value=1.0, max_value=80.0, value=18.0, step=0.5)
        weight = estimate_ruminant_weight(girth, length, species)

    bcs = st.slider("BCS / Body Condition Score", 1.0, 5.0, 3.0, 0.1)

    st.markdown("---")
    st.subheader("Data Kualitatif / Fenotipe")

    q1, q2, q3 = st.columns(3)

    with q1:
        color = st.selectbox("Warna bulu dominan", data["colors"] + ["Tidak yakin", "Lainnya / tidak sesuai"])
        face = st.selectbox("Kepala/wajah/paruh", data["face"] + ["Tidak yakin", "Lainnya / tidak sesuai"])

    with q2:
        horn_label = "Jengger" if kind == "poultry" else "Tanduk"
        leg_label = "Warna/bentuk kaki" if kind == "poultry" else "Telinga"
        horn_or_comb = st.selectbox(horn_label, data["horn_or_comb"] + ["Tidak yakin", "Lainnya / tidak sesuai"])
        ear_or_leg = st.selectbox(leg_label, data["ear_or_leg"] + ["Tidak yakin", "Lainnya / tidak sesuai"])

    with q3:
        build = st.selectbox("Bentuk tubuh", data["build"] + ["Tidak yakin", "Lainnya / tidak sesuai"])
        features = st.multiselect("Ciri khas yang tampak", data["features"], default=data["features"][:2])

    st.markdown("---")
    st.subheader("Kesehatan Lapangan")

    h1, h2, h3 = st.columns(3)

    with h1:
        check_appetite = st.checkbox("Nafsu makan baik", True)
        check_active = st.checkbox("Aktif/responsif", True)
        check_eye = st.checkbox("Mata cerah/normal", True)

    with h2:
        check_feces = st.checkbox("Feses normal", True)
        check_limp = st.checkbox("Tidak pincang", True)
        check_skin = st.checkbox("Bulu/kulit baik", True)

    with h3:
        check_breath = st.checkbox("Napas normal", True)
        check_wound = st.checkbox("Tidak ada luka serius", True)
        check_parasite = st.checkbox("Tidak tampak parasit berat", True)

    health_checks = {
        "Nafsu makan": check_appetite,
        "Aktif": check_active,
        "Mata": check_eye,
        "Feses": check_feces,
        "Tidak pincang": check_limp,
        "Bulu/kulit": check_skin,
        "Napas": check_breath,
        "Luka": check_wound,
        "Parasit": check_parasite,
    }

    st.success("Input selesai. Buka tab Hasil, SNI/Acuan, dan Ekonomi.")


# =========================================================
# CALCULATION
# =========================================================

age_stage = get_age_stage(kind, age_months)
weight_score = score_weight(weight, data["target_min"], data["target_ideal"])
bcs_score = score_bcs(bcs, kind, purpose)
height_score = score_range(height, data["height_min"], data["height_max"], 10)
prop_score, prop_ratio = score_body_proportion(girth, length, kind)
quant_score, quant_details = score_quant_extra(height, chest_depth, rump_width, cannon, kind)
health_score = score_health(health_checks)
pheno_score, pheno_df = score_phenotype(data, color, face, horn_or_comb, ear_or_leg, build, features)

market_score = 7
if weight < data["target_min"]:
    market_score -= 2
if health_score < 12:
    market_score -= 1.5
if pheno_score < 10:
    market_score -= 1
market_score = round(clamp(market_score, 0, 7), 1)

total_score = round(
    weight_score + bcs_score + height_score + prop_score + quant_score + health_score + pheno_score + market_score,
    1,
)
total_score = clamp(total_score, 0, 100)
category, cat_style = classify_score(total_score)

# SNI thresholds default
sni_default = data["sni"].copy()


# =========================================================
# SNI / ACUAN
# =========================================================

with tab_sni:
    st.subheader("Pembanding SNI / Acuan Minimum")

    st.markdown(
        f"""
<div class="card">
<strong>Acuan saat ini:</strong> {sni_default["name"]}<br>
<span class="muted">Cakupan: {sni_default["coverage"]}. Untuk dokumen SNI resmi, edit ambang sesuai umur, jenis kelamin, dan kelas mutu.</span>
</div>
""",
        unsafe_allow_html=True,
    )

    edit_sni = st.toggle("Ubah ambang SNI/acuan secara manual", value=False)

    if edit_sni:
        s1, s2, s3 = st.columns(3)
        with s1:
            min_weight = st.number_input("Bobot minimum", min_value=0.0, value=float(sni_default["min_weight"]), step=0.1)
            min_height = st.number_input("Tinggi minimum", min_value=0.0, value=float(sni_default["min_height"]), step=0.5)
        with s2:
            min_length = st.number_input("Panjang badan minimum", min_value=0.0, value=float(sni_default["min_length"]), step=0.5)
            min_girth = st.number_input("Lingkar dada minimum", min_value=0.0, value=float(sni_default["min_girth"]), step=0.5)
        with s3:
            min_bcs = st.number_input("BCS minimum", min_value=1.0, max_value=5.0, value=float(sni_default["min_bcs"]), step=0.1)
    else:
        min_weight = float(sni_default["min_weight"])
        min_height = float(sni_default["min_height"])
        min_length = float(sni_default["min_length"])
        min_girth = float(sni_default["min_girth"])
        min_bcs = float(sni_default["min_bcs"])

    sni_thresholds = {
        "min_weight": min_weight,
        "min_height": min_height,
        "min_length": min_length,
        "min_girth": min_girth,
        "min_bcs": min_bcs,
    }

    sni_df, sni_percent, sni_status = sni_compare(
        sni_thresholds,
        weight,
        height,
        length,
        girth,
        bcs,
        pheno_score,
        health_score,
    )

    a, b, c = st.columns(3)
    a.metric("Status acuan", sni_status)
    b.metric("Kesesuaian", f"{sni_percent:.1f}%")
    c.metric("Parameter lolos", f"{int(sni_df['Lolos'].sum())}/{len(sni_df)}")

    st.dataframe(sni_df.drop(columns=["Lolos"]), use_container_width=True, hide_index=True)

    failed = sni_df[sni_df["Status"] == "Belum memenuhi"]
    if failed.empty:
        st.success("Semua parameter pembanding memenuhi ambang yang digunakan.")
    else:
        notes = []
        for _, row in failed.iterrows():
            diff = row["Acuan minimum"] - row["Nilai"]
            if diff > 0:
                notes.append(f"{row['Parameter']} kurang {diff:.2f} {row['Satuan']}")
            else:
                notes.append(f"{row['Parameter']} belum memenuhi")
        st.warning("; ".join(notes))


# =========================================================
# EKONOMI
# =========================================================

with tab_economy:
    st.subheader("Analisis Ekonomi Lanjutan")

    e1, e2, e3 = st.columns(3)

    with e1:
        buy_price = st.number_input("Harga beli total (Rp)", min_value=0, value=0, step=5000)
        sell_price_per_kg = st.number_input("Estimasi harga jual per kg bobot hidup (Rp)", min_value=0, value=0, step=1000)

    with e2:
        feed_cost_day = st.number_input("Biaya pakan per hari (Rp)", min_value=0, value=0, step=1000)
        other_cost_day = st.number_input("Biaya lain per hari (Rp)", min_value=0, value=0, step=1000)

    with e3:
        target_weight = st.number_input("Target bobot jual (kg)", min_value=0.0, value=float(data["target_ideal"]), step=0.1)
        desired_margin = st.number_input("Target margin/laba minimal (Rp)", min_value=0, value=0, step=5000)

    days_to_target = math.ceil(max(target_weight - weight, 0) / max(data["adg"], 0.0001))
    total_operational_cost = days_to_target * (feed_cost_day + other_cost_day)
    estimated_sell_value = target_weight * sell_price_per_kg if sell_price_per_kg > 0 else 0
    profit = estimated_sell_value - buy_price - total_operational_cost
    bep_price_per_kg = (buy_price + total_operational_cost) / max(target_weight, 0.01)
    max_buy_price = max(estimated_sell_value - total_operational_cost - desired_margin, 0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Estimasi hari ke target", f"{days_to_target} hari")
    c2.metric("Biaya operasional", rupiah(total_operational_cost))
    c3.metric("Laba/rugi kasar", rupiah(profit))
    c4.metric("Harga BEP/kg", rupiah(bep_price_per_kg))

    st.info(
        f"Harga maksimal beli agar mencapai margin target: **{rupiah(max_buy_price)}**. "
        "Gunakan angka ini untuk batas negosiasi, bukan harga mutlak."
    )


# =========================================================
# RESULT
# =========================================================

sni_df_calc, sni_percent_calc, sni_status_calc = sni_compare(
    sni_default,
    weight,
    height,
    length,
    girth,
    bcs,
    pheno_score,
    health_score,
)

# These ekonomi variables might not exist before tab render in some cases,
# so define safe defaults.
if "buy_price" not in locals():
    buy_price = 0
if "sell_price_per_kg" not in locals():
    sell_price_per_kg = 0
if "feed_cost_day" not in locals():
    feed_cost_day = 0
if "other_cost_day" not in locals():
    other_cost_day = 0
if "target_weight" not in locals():
    target_weight = float(data["target_ideal"])
if "days_to_target" not in locals():
    days_to_target = math.ceil(max(target_weight - weight, 0) / max(data["adg"], 0.0001))
if "total_operational_cost" not in locals():
    total_operational_cost = days_to_target * (feed_cost_day + other_cost_day)
if "estimated_sell_value" not in locals():
    estimated_sell_value = target_weight * sell_price_per_kg if sell_price_per_kg > 0 else 0
if "profit" not in locals():
    profit = estimated_sell_value - buy_price - total_operational_cost
if "bep_price_per_kg" not in locals():
    bep_price_per_kg = (buy_price + total_operational_cost) / max(target_weight, 0.01)
if "max_buy_price" not in locals():
    max_buy_price = max(estimated_sell_value - total_operational_cost, 0)

decision = final_decision(total_score, sni_percent_calc, health_score, purpose, mode, kind)

insights = make_insights(
    kind,
    species,
    breed,
    mode,
    purpose,
    weight,
    data["target_min"],
    data["target_ideal"],
    bcs,
    health_score,
    pheno_score,
    quant_score,
    sni_percent_calc,
    profit,
    max_buy_price,
)

with tab_result:
    st.subheader("Ringkasan Hasil")

    badge_class = "badge-good" if cat_style == "good" else ("badge-warn" if cat_style == "warn" else "badge-bad")
    st.markdown(
        f"""
<span class="badge {badge_class}">Kategori: {category}</span>
<span class="badge badge-primary">Jenis: {species}</span>
<span class="badge">Bangsa/Rumpun: {breed}</span>
<span class="badge">Mode: {mode}</span>
<span class="badge">Fase: {age_stage}</span>
""",
        unsafe_allow_html=True,
    )

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.markdown(
            f"""
<div class="metric-card">
<div class="muted">Skor Total</div>
<div class="big-score">{total_score:.1f}</div>
<div class="muted">dari 100</div>
</div>
""",
            unsafe_allow_html=True,
        )

    r2.metric("Estimasi/aktual bobot", f"{weight:.2f} kg")
    r3.metric("Kesesuaian SNI/acuan", f"{sni_percent_calc:.1f}%")
    r4.metric("Estimasi karkas", f"{weight * data['dressing'] / 100:.2f} kg")

    st.markdown(
        f"""
<div class="card">
<strong>Rekomendasi akhir:</strong><br>{decision}
</div>
""",
        unsafe_allow_html=True,
    )

    score_df = pd.DataFrame(
        [
            ["Bobot", weight_score, 20],
            ["BCS", bcs_score, 15],
            ["Tinggi/rangka", height_score, 10],
            ["Proporsi tubuh", prop_score, 8],
            ["Kuantitatif tambahan", quant_score, 10],
            ["Kesehatan", health_score, 15],
            ["Kualitatif/fenotipe", pheno_score, 15],
            ["Kesiapan pasar", market_score, 7],
        ],
        columns=["Komponen", "Skor", "Maksimum"],
    )

    st.dataframe(score_df, use_container_width=True, hide_index=True)
    st.progress(int(clamp(total_score, 0, 100)))

    st.subheader("Detail Fenotipe")
    st.dataframe(pheno_df, use_container_width=True, hide_index=True)

    st.subheader("Insight Otomatis")
    for kind_insight, title, body in insights:
        css_class = kind_insight if kind_insight in ["good", "warn", "bad"] else ""
        st.markdown(
            f"""
<div class="insight {css_class}">
<strong>{title}</strong><br>{body}
</div>
""",
            unsafe_allow_html=True,
        )

    if st.button("💾 Simpan ke Riwayat Evaluasi", use_container_width=True):
        record = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Kode": animal_id,
            "Lokasi": location,
            "Jenis": species,
            "Bangsa/Rumpun": breed,
            "Mode": mode,
            "Tujuan": purpose,
            "Kelamin": sex,
            "Umur bulan": age_months,
            "Fase": age_stage,
            "Bobot kg": round(weight, 3),
            "Lingkar dada cm": girth,
            "Panjang badan cm": length,
            "Tinggi cm": height,
            "BCS": bcs,
            "Skor total": total_score,
            "Kategori": category,
            "Status SNI/acuan": sni_status_calc,
            "Kesesuaian SNI %": sni_percent_calc,
            "Laba/rugi kasar": profit,
            "Rekomendasi akhir": decision,
        }
        st.session_state.records.append(record)
        st.success("Data tersimpan ke riwayat.")


# =========================================================
# HISTORY
# =========================================================

with tab_history:
    st.subheader("Riwayat Evaluasi dan Grafik")

    upload = st.file_uploader("Upload CSV riwayat lama bila ada", type=["csv"])

    if upload is not None:
        try:
            uploaded_df = pd.read_csv(upload)
            st.session_state.records.extend(uploaded_df.to_dict("records"))
            st.success("CSV berhasil dimuat ke riwayat sementara.")
        except Exception as exc:
            st.error(f"Gagal membaca CSV: {exc}")

    if st.button("🧹 Reset Riwayat", use_container_width=True):
        st.session_state.records = []
        st.success("Riwayat sementara direset.")
        st.rerun()

    if not st.session_state.records:
        st.info("Belum ada riwayat. Simpan hasil dari tab Hasil.")
    else:
        hist_df = pd.DataFrame(st.session_state.records)
        st.dataframe(hist_df, use_container_width=True, hide_index=True)

        csv = hist_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Download CSV Riwayat", data=csv, file_name="riwayat_evaluasi_ternak.csv", mime="text/csv", use_container_width=True)

        st.markdown("---")
        st.subheader("Grafik Perkembangan")

        if "Waktu" in hist_df.columns:
            chart_df = hist_df.copy()
            chart_df["Urutan"] = range(1, len(chart_df) + 1)
            if "Bobot kg" in chart_df.columns:
                st.line_chart(chart_df.set_index("Urutan")[["Bobot kg"]])
            if "Skor total" in chart_df.columns:
                st.line_chart(chart_df.set_index("Urutan")[["Skor total"]])

        st.markdown("---")
        st.subheader("Ringkasan")
        st.metric("Jumlah data", len(hist_df))
        if "Skor total" in hist_df.columns:
            st.metric("Rata-rata skor", f"{pd.to_numeric(hist_df['Skor total'], errors='coerce').mean():.1f}")


# =========================================================
# REPORT
# =========================================================

with tab_report:
    st.subheader("Laporan Ringkas")

    report_record = {
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Kode": animal_id,
        "Lokasi": location,
        "Jenis": species,
        "Bangsa/Rumpun": breed,
        "Mode": mode,
        "Tujuan": purpose,
        "Kelamin": sex,
        "Umur/Fase": f"{age_months} bulan / {age_stage}",
        "Bobot": f"{weight:.3f} kg",
        "BCS": bcs,
        "Skor total": total_score,
        "Kategori": category,
        "Status SNI/acuan": sni_status_calc,
        "Kesesuaian SNI/acuan": f"{sni_percent_calc:.1f}%",
        "Rekomendasi akhir": decision,
        "Estimasi laba/rugi kasar": rupiah(profit),
        "Harga maksimal beli": rupiah(max_buy_price),
    }

    st.dataframe(
        pd.DataFrame(list(report_record.items()), columns=["Item", "Nilai"]),
        use_container_width=True,
        hide_index=True,
    )

    html_report = make_report_html(report_record, insights)

    st.download_button(
        "⬇️ Download Laporan HTML",
        data=html_report.encode("utf-8"),
        file_name=f"laporan_evaluasi_{animal_id}.html",
        mime="text/html",
        use_container_width=True,
    )


# =========================================================
# GUIDE
# =========================================================

with tab_guide:
    st.subheader("Panduan Fitur Baru")

    st.markdown(
        """
### Fitur yang sudah ditambahkan

| Fitur | Fungsi |
|---|---|
| Form adaptif | Ruminansia dan ayam memakai input yang berbeda |
| Mode pengguna | Insight berubah sesuai peternak, jagal, blantik, pembibit, atau ayam lokal |
| Rekomendasi akhir | Memberi keputusan praktis layak/tunda/perbaikan |
| SNI/acuan editable | Ambang bisa disesuaikan dengan dokumen resmi atau SOP |
| Ekonomi lanjutan | Hitung BEP, laba/rugi, hari target, biaya pakan, dan harga maksimal beli |
| Riwayat evaluasi | Simpan, upload CSV, download CSV, dan lihat grafik |
| Laporan HTML | Download laporan ringkas per ternak |
| Ayam lokal Indonesia | Termasuk Kampung, KUB-1, KUB Janaka, Sentul, Pelung, Kedu, Cemani, Nunukan, Merawang, Gaok, dan Kokok Balenggek |

### Catatan ayam

Untuk ayam, bobot dimasukkan langsung dari hasil timbang. Jangan memakai rumus estimasi bobot sapi/kambing.
Untuk ayam penyanyi seperti Pelung, Gaok, dan Kokok Balenggek, nilai suara tetap perlu dinilai manual di luar skor bobot.

### Catatan SNI

Pembanding SNI/acuan pada aplikasi bukan sertifikasi resmi. Untuk keputusan bibit resmi, gunakan dokumen SNI lengkap dan pemeriksaan pihak berwenang.
"""
    )
