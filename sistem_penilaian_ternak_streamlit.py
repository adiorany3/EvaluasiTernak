import math
from datetime import datetime

import pandas as pd
import streamlit as st


# =========================================================
# SISTEM PENILAIAN TERNAK
# Faktor kuantitatif + kualitatif berbasis jenis dan bangsa
# =========================================================
# Catatan:
# - Aplikasi ini adalah alat bantu estimasi awal.
# - Parameter dapat disesuaikan dengan standar lokal, pasar,
#   pengalaman peternak, dan hasil validasi lapangan.
# - Hasil bukan pengganti pemeriksaan dokter hewan, ahli nutrisi,
#   inseminator, petugas teknis, jagal profesional, atau penilai ternak.
# =========================================================


st.set_page_config(
    page_title="Sistem Penilaian Ternak",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# STYLE
# =========================================================

CUSTOM_CSS = """
<style>
:root {
    --card-radius: 18px;
}

.main .block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.metric-card {
    border-radius: var(--card-radius);
    padding: 18px 20px;
    border: 1px solid rgba(128, 128, 128, 0.22);
    background: rgba(255, 255, 255, 0.06);
    box-shadow: 0 8px 26px rgba(0,0,0,0.06);
    height: 100%;
}

.insight-card {
    border-radius: var(--card-radius);
    padding: 18px 20px;
    border-left: 6px solid #888;
    background: rgba(128, 128, 128, 0.08);
    margin-bottom: 14px;
}

.good {
    border-left-color: #16a34a;
}

.warning {
    border-left-color: #f59e0b;
}

.danger {
    border-left-color: #dc2626;
}

.info {
    border-left-color: #2563eb;
}

.small-text {
    font-size: 0.88rem;
    opacity: 0.85;
}

.big-score {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid rgba(128,128,128,0.35);
    background: rgba(128,128,128,0.10);
    font-size: 0.88rem;
    margin-right: 6px;
    margin-bottom: 6px;
}

.section-note {
    padding: 12px 14px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.07);
}

hr {
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# MASTER DATA
# =========================================================

BREED_DATA = {
    "Sapi Potong": {
        "Bali": {
            "target_market_min": 280,
            "target_market_ideal": 350,
            "adult_weight_min": 300,
            "adult_weight_max": 450,
            "height_min": 115,
            "height_max": 130,
            "adg": 0.55,
            "dressing": 50,
            "quant": {
                "chest_depth_ratio": (0.42, 0.53),
                "rump_width_ratio": (0.20, 0.30),
                "cannon_ratio": (0.10, 0.16),
            },
            "phenotype": {
                "colors": ["Merah bata", "Cokelat kemerahan", "Hitam pada jantan dewasa"],
                "faces": ["Lurus", "Pendek agak lebar"],
                "horns": ["Bertanduk", "Tanduk kecil", "Tanduk melengkung"],
                "ears": ["Sedang", "Tegak sedang"],
                "body_builds": ["Kompak", "Padat", "Rangka sedang"],
                "features": [
                    "Garis punggung relatif lurus",
                    "Kaki kuat",
                    "Paha cukup berisi",
                    "Kulit dan bulu tampak bersih",
                ],
            },
            "notes": "Tahan lingkungan tropis, efisien pakan, cocok untuk pasar lokal dan penggemukan sedang.",
        },
        "Peranakan Ongole / PO": {
            "target_market_min": 320,
            "target_market_ideal": 450,
            "adult_weight_min": 350,
            "adult_weight_max": 550,
            "height_min": 125,
            "height_max": 145,
            "adg": 0.65,
            "dressing": 49,
            "quant": {
                "chest_depth_ratio": (0.42, 0.55),
                "rump_width_ratio": (0.20, 0.31),
                "cannon_ratio": (0.10, 0.17),
            },
            "phenotype": {
                "colors": ["Putih", "Abu-abu muda", "Abu-abu tua"],
                "faces": ["Panjang", "Cembung ringan", "Lurus"],
                "horns": ["Bertanduk", "Tanduk kecil", "Tanduk melengkung"],
                "ears": ["Sedang", "Agak menggantung"],
                "body_builds": ["Rangka besar", "Tinggi", "Panjang"],
                "features": [
                    "Punuk terlihat",
                    "Gelambir berkembang",
                    "Kaki kuat",
                    "Dada cukup dalam",
                ],
            },
            "notes": "Adaptif, rangka cukup besar, umum dipakai untuk kerja, bibit, dan penggemukan.",
        },
        "Madura": {
            "target_market_min": 250,
            "target_market_ideal": 350,
            "adult_weight_min": 250,
            "adult_weight_max": 400,
            "height_min": 110,
            "height_max": 125,
            "adg": 0.50,
            "dressing": 49,
            "quant": {
                "chest_depth_ratio": (0.40, 0.52),
                "rump_width_ratio": (0.19, 0.29),
                "cannon_ratio": (0.10, 0.15),
            },
            "phenotype": {
                "colors": ["Cokelat kemerahan", "Merah bata", "Cokelat"],
                "faces": ["Pendek agak lebar", "Lurus"],
                "horns": ["Bertanduk", "Tanduk kecil"],
                "ears": ["Kecil", "Sedang"],
                "body_builds": ["Kompak", "Rangka sedang", "Padat"],
                "features": [
                    "Kaki kuat",
                    "Tubuh kompak",
                    "Paha cukup berisi",
                    "Bulu mengilap",
                ],
            },
            "notes": "Ukuran relatif kompak, tahan lingkungan, cocok untuk sistem rakyat.",
        },
        "Brahman Cross": {
            "target_market_min": 400,
            "target_market_ideal": 550,
            "adult_weight_min": 450,
            "adult_weight_max": 700,
            "height_min": 130,
            "height_max": 150,
            "adg": 0.85,
            "dressing": 51,
            "quant": {
                "chest_depth_ratio": (0.43, 0.56),
                "rump_width_ratio": (0.21, 0.32),
                "cannon_ratio": (0.11, 0.18),
            },
            "phenotype": {
                "colors": ["Abu-abu", "Putih keabu-abuan", "Merah kecokelatan", "Cokelat"],
                "faces": ["Panjang", "Cembung ringan"],
                "horns": ["Bertanduk", "Tanduk kecil", "Tidak bertanduk/polled"],
                "ears": ["Menggantung/lebar", "Panjang menggantung"],
                "body_builds": ["Rangka besar", "Panjang", "Berotot sedang"],
                "features": [
                    "Punuk jelas",
                    "Gelambir berkembang",
                    "Kulit longgar",
                    "Telinga menggantung",
                    "Dada dalam",
                ],
            },
            "notes": "Rangka besar, tahan panas, potensi penggemukan tinggi jika pakan dan manajemen baik.",
        },
        "Simmental Cross": {
            "target_market_min": 450,
            "target_market_ideal": 650,
            "adult_weight_min": 500,
            "adult_weight_max": 850,
            "height_min": 135,
            "height_max": 155,
            "adg": 0.95,
            "dressing": 53,
            "quant": {
                "chest_depth_ratio": (0.44, 0.57),
                "rump_width_ratio": (0.22, 0.34),
                "cannon_ratio": (0.11, 0.18),
            },
            "phenotype": {
                "colors": ["Cokelat putih", "Merah putih", "Krem putih", "Cokelat muda"],
                "faces": ["Lebar", "Lurus", "Pendek agak lebar"],
                "horns": ["Bertanduk", "Tidak bertanduk/polled", "Tanduk kecil"],
                "ears": ["Sedang", "Tegak sedang"],
                "body_builds": ["Rangka besar", "Berotot", "Panjang dan dalam"],
                "features": [
                    "Dada dalam",
                    "Punggung lebar",
                    "Paha penuh",
                    "Kaki kokoh",
                    "Warna belang khas",
                ],
            },
            "notes": "Pertumbuhan cepat, rangka besar, cocok untuk penggemukan intensif.",
        },
        "Limousin Cross": {
            "target_market_min": 450,
            "target_market_ideal": 650,
            "adult_weight_min": 500,
            "adult_weight_max": 850,
            "height_min": 135,
            "height_max": 155,
            "adg": 0.95,
            "dressing": 54,
            "quant": {
                "chest_depth_ratio": (0.43, 0.56),
                "rump_width_ratio": (0.22, 0.35),
                "cannon_ratio": (0.11, 0.18),
            },
            "phenotype": {
                "colors": ["Cokelat keemasan", "Merah kecokelatan", "Cokelat muda"],
                "faces": ["Panjang", "Lurus"],
                "horns": ["Bertanduk", "Tidak bertanduk/polled", "Tanduk kecil"],
                "ears": ["Sedang", "Tegak sedang"],
                "body_builds": ["Berotot", "Rangka besar", "Punggung panjang"],
                "features": [
                    "Paha sangat berisi",
                    "Punggung lebar",
                    "Dada dalam",
                    "Otot tampak jelas",
                    "Kaki kokoh",
                ],
            },
            "notes": "Potensi daging tinggi, cocok untuk pasar premium dan sistem pakan intensif.",
        },
    },
    "Sapi Perah": {
        "Friesian Holstein / FH": {
            "target_market_min": 400,
            "target_market_ideal": 550,
            "adult_weight_min": 450,
            "adult_weight_max": 700,
            "height_min": 130,
            "height_max": 150,
            "adg": 0.70,
            "dressing": 47,
            "quant": {
                "chest_depth_ratio": (0.42, 0.55),
                "rump_width_ratio": (0.21, 0.33),
                "cannon_ratio": (0.09, 0.16),
            },
            "phenotype": {
                "colors": ["Hitam putih", "Putih hitam", "Belang hitam putih"],
                "faces": ["Panjang", "Lurus"],
                "horns": ["Tidak bertanduk/polled", "Bertanduk", "Tanduk kecil"],
                "ears": ["Sedang", "Tegak sedang"],
                "body_builds": ["Tinggi", "Panjang", "Bentuk tubuh perah"],
                "features": [
                    "Ambing proporsional",
                    "Vena susu tampak baik",
                    "Punggung relatif lurus",
                    "Kaki dan kuku kuat",
                    "Rangka panjang",
                ],
            },
            "notes": "Fokus utama produksi susu. Penilaian perlu memperhatikan BCS, ambing, dan kondisi laktasi.",
        },
        "Jersey": {
            "target_market_min": 300,
            "target_market_ideal": 420,
            "adult_weight_min": 350,
            "adult_weight_max": 500,
            "height_min": 120,
            "height_max": 140,
            "adg": 0.55,
            "dressing": 46,
            "quant": {
                "chest_depth_ratio": (0.40, 0.53),
                "rump_width_ratio": (0.20, 0.31),
                "cannon_ratio": (0.09, 0.15),
            },
            "phenotype": {
                "colors": ["Cokelat muda", "Cokelat kekuningan", "Abu-cokelat"],
                "faces": ["Panjang", "Halus", "Lurus"],
                "horns": ["Tidak bertanduk/polled", "Bertanduk", "Tanduk kecil"],
                "ears": ["Sedang", "Tegak sedang"],
                "body_builds": ["Kompak", "Bentuk tubuh perah", "Rangka sedang"],
                "features": [
                    "Ambing proporsional",
                    "Tubuh ramping perah",
                    "Kaki kuat",
                    "Bulu halus",
                ],
            },
            "notes": "Ukuran lebih kecil dari FH, dikenal efisien dan susu berlemak relatif tinggi.",
        },
        "Peranakan FH": {
            "target_market_min": 350,
            "target_market_ideal": 500,
            "adult_weight_min": 400,
            "adult_weight_max": 650,
            "height_min": 125,
            "height_max": 145,
            "adg": 0.65,
            "dressing": 46,
            "quant": {
                "chest_depth_ratio": (0.41, 0.54),
                "rump_width_ratio": (0.20, 0.32),
                "cannon_ratio": (0.09, 0.16),
            },
            "phenotype": {
                "colors": ["Hitam putih", "Putih hitam", "Belang tidak seragam"],
                "faces": ["Panjang", "Lurus"],
                "horns": ["Tidak bertanduk/polled", "Bertanduk", "Tanduk kecil"],
                "ears": ["Sedang", "Tegak sedang"],
                "body_builds": ["Panjang", "Rangka sedang", "Bentuk tubuh perah"],
                "features": [
                    "Ambing proporsional",
                    "Rangka cukup panjang",
                    "Kaki kuat",
                    "Punggung relatif lurus",
                ],
            },
            "notes": "Adaptasi lebih beragam, penilaian perlu melihat garis keturunan dan performa produksi.",
        },
    },
    "Kerbau": {
        "Kerbau Lumpur / Rawa": {
            "target_market_min": 350,
            "target_market_ideal": 500,
            "adult_weight_min": 400,
            "adult_weight_max": 650,
            "height_min": 125,
            "height_max": 145,
            "adg": 0.55,
            "dressing": 45,
            "quant": {
                "chest_depth_ratio": (0.42, 0.56),
                "rump_width_ratio": (0.22, 0.34),
                "cannon_ratio": (0.11, 0.18),
            },
            "phenotype": {
                "colors": ["Abu-abu gelap", "Hitam keabu-abuan", "Cokelat kehitaman"],
                "faces": ["Panjang", "Lebar"],
                "horns": ["Tanduk besar", "Tanduk melengkung", "Bertanduk"],
                "ears": ["Sedang", "Agak menggantung"],
                "body_builds": ["Rangka besar", "Dada dalam", "Kuat"],
                "features": [
                    "Tanduk melengkung ke belakang/samping",
                    "Kulit tebal",
                    "Kaki kuat",
                    "Tubuh lebar",
                ],
            },
            "notes": "Kuat, adaptif, cocok untuk daerah basah dan sistem tradisional.",
        },
        "Murrah": {
            "target_market_min": 450,
            "target_market_ideal": 650,
            "adult_weight_min": 500,
            "adult_weight_max": 800,
            "height_min": 130,
            "height_max": 150,
            "adg": 0.70,
            "dressing": 46,
            "quant": {
                "chest_depth_ratio": (0.43, 0.57),
                "rump_width_ratio": (0.22, 0.35),
                "cannon_ratio": (0.11, 0.18),
            },
            "phenotype": {
                "colors": ["Hitam", "Hitam mengilap", "Hitam keabu-abuan"],
                "faces": ["Panjang", "Halus"],
                "horns": ["Tanduk melingkar", "Tanduk kecil melengkung", "Bertanduk"],
                "ears": ["Sedang", "Agak menggantung"],
                "body_builds": ["Rangka besar", "Dada dalam", "Bentuk tubuh perah"],
                "features": [
                    "Tanduk melingkar rapat",
                    "Ambing proporsional",
                    "Kulit hitam mengilap",
                    "Dada dalam",
                    "Kaki kuat",
                ],
            },
            "notes": "Potensi susu baik, ukuran tubuh besar, perlu manajemen pakan dan kesehatan lebih intensif.",
        },
    },
    "Kambing": {
        "Kacang": {
            "target_market_min": 18,
            "target_market_ideal": 28,
            "adult_weight_min": 20,
            "adult_weight_max": 35,
            "height_min": 45,
            "height_max": 60,
            "adg": 0.06,
            "dressing": 43,
            "quant": {
                "chest_depth_ratio": (0.35, 0.49),
                "rump_width_ratio": (0.16, 0.27),
                "cannon_ratio": (0.07, 0.13),
            },
            "phenotype": {
                "colors": ["Cokelat", "Hitam", "Putih", "Belang"],
                "faces": ["Pendek", "Lurus"],
                "horns": ["Bertanduk", "Tanduk kecil"],
                "ears": ["Kecil", "Tegak"],
                "body_builds": ["Kompak", "Kecil", "Lincah"],
                "features": [
                    "Tubuh kompak",
                    "Kaki kuat",
                    "Bulu bersih",
                    "Gerak lincah",
                ],
            },
            "notes": "Adaptif, ukuran kecil, cocok untuk pasar lokal dan sistem pemeliharaan sederhana.",
        },
        "Peranakan Etawa / PE": {
            "target_market_min": 35,
            "target_market_ideal": 60,
            "adult_weight_min": 40,
            "adult_weight_max": 80,
            "height_min": 65,
            "height_max": 90,
            "adg": 0.10,
            "dressing": 44,
            "quant": {
                "chest_depth_ratio": (0.36, 0.50),
                "rump_width_ratio": (0.17, 0.29),
                "cannon_ratio": (0.07, 0.13),
            },
            "phenotype": {
                "colors": ["Putih hitam", "Putih cokelat", "Belang", "Cokelat putih"],
                "faces": ["Cembung", "Roman nose", "Panjang"],
                "horns": ["Bertanduk", "Tanduk kecil"],
                "ears": ["Panjang menggantung", "Menggantung/lebar"],
                "body_builds": ["Tinggi", "Panjang", "Dwiguna"],
                "features": [
                    "Telinga panjang menggantung",
                    "Profil wajah cembung",
                    "Ambing proporsional",
                    "Kaki tinggi",
                    "Rangka panjang",
                ],
            },
            "notes": "Dwiguna, potensi susu dan daging. Perhatikan ambing, bentuk tubuh, dan reproduksi.",
        },
        "Boer": {
            "target_market_min": 35,
            "target_market_ideal": 70,
            "adult_weight_min": 50,
            "adult_weight_max": 100,
            "height_min": 60,
            "height_max": 80,
            "adg": 0.15,
            "dressing": 48,
            "quant": {
                "chest_depth_ratio": (0.38, 0.53),
                "rump_width_ratio": (0.19, 0.32),
                "cannon_ratio": (0.08, 0.14),
            },
            "phenotype": {
                "colors": ["Putih kepala cokelat", "Putih cokelat", "Cokelat putih"],
                "faces": ["Cembung ringan", "Lebar", "Roman nose"],
                "horns": ["Bertanduk", "Tanduk kecil", "Melengkung ke belakang"],
                "ears": ["Menggantung/lebar", "Sedang menggantung"],
                "body_builds": ["Berotot", "Dada lebar", "Paha penuh"],
                "features": [
                    "Kepala cokelat",
                    "Badan putih dominan",
                    "Paha penuh",
                    "Dada lebar",
                    "Tubuh padat",
                ],
            },
            "notes": "Tipe pedaging, pertumbuhan cepat, cocok untuk penggemukan dan bakalan premium.",
        },
        "Saanen": {
            "target_market_min": 35,
            "target_market_ideal": 65,
            "adult_weight_min": 45,
            "adult_weight_max": 90,
            "height_min": 70,
            "height_max": 90,
            "adg": 0.10,
            "dressing": 42,
            "quant": {
                "chest_depth_ratio": (0.36, 0.50),
                "rump_width_ratio": (0.17, 0.29),
                "cannon_ratio": (0.07, 0.13),
            },
            "phenotype": {
                "colors": ["Putih", "Krem muda", "Putih bersih"],
                "faces": ["Panjang", "Lurus", "Halus"],
                "horns": ["Tidak bertanduk/polled", "Bertanduk", "Tanduk kecil"],
                "ears": ["Tegak", "Sedang"],
                "body_builds": ["Tinggi", "Ramping perah", "Panjang"],
                "features": [
                    "Warna putih/krem dominan",
                    "Ambing proporsional",
                    "Tubuh perah",
                    "Kaki kuat",
                    "Bulu halus",
                ],
            },
            "notes": "Tipe perah, penilaian lebih kuat pada kesehatan, ambing, dan performa susu.",
        },
    },
    "Domba": {
        "Domba Garut": {
            "target_market_min": 30,
            "target_market_ideal": 55,
            "adult_weight_min": 35,
            "adult_weight_max": 80,
            "height_min": 55,
            "height_max": 75,
            "adg": 0.12,
            "dressing": 47,
            "quant": {
                "chest_depth_ratio": (0.36, 0.51),
                "rump_width_ratio": (0.18, 0.30),
                "cannon_ratio": (0.08, 0.14),
            },
            "phenotype": {
                "colors": ["Putih", "Hitam", "Cokelat", "Belang"],
                "faces": ["Sedang", "Lurus"],
                "horns": ["Tanduk besar", "Tanduk melingkar", "Bertanduk"],
                "ears": ["Kecil", "Sedang"],
                "body_builds": ["Berotot", "Kompak", "Dada lebar"],
                "features": [
                    "Tanduk kuat/melingkar pada jantan",
                    "Dada lebar",
                    "Punggung kuat",
                    "Paha berisi",
                    "Kaki kokoh",
                ],
            },
            "notes": "Potensi pedaging dan kontes, rangka baik menjadi nilai tambah.",
        },
        "Domba Ekor Tipis": {
            "target_market_min": 20,
            "target_market_ideal": 35,
            "adult_weight_min": 25,
            "adult_weight_max": 45,
            "height_min": 45,
            "height_max": 65,
            "adg": 0.08,
            "dressing": 44,
            "quant": {
                "chest_depth_ratio": (0.34, 0.49),
                "rump_width_ratio": (0.16, 0.28),
                "cannon_ratio": (0.07, 0.13),
            },
            "phenotype": {
                "colors": ["Putih", "Cokelat", "Hitam", "Belang"],
                "faces": ["Sedang", "Lurus"],
                "horns": ["Bertanduk", "Tidak bertanduk/polled", "Tanduk kecil"],
                "ears": ["Kecil", "Sedang"],
                "body_builds": ["Kecil sedang", "Kompak", "Adaptif"],
                "features": [
                    "Ekor tipis",
                    "Tubuh kompak",
                    "Kaki kuat",
                    "Bulu bersih",
                ],
            },
            "notes": "Adaptif, banyak dipelihara rakyat, cocok untuk pasar lokal.",
        },
        "Domba Ekor Gemuk": {
            "target_market_min": 25,
            "target_market_ideal": 45,
            "adult_weight_min": 30,
            "adult_weight_max": 60,
            "height_min": 50,
            "height_max": 70,
            "adg": 0.09,
            "dressing": 45,
            "quant": {
                "chest_depth_ratio": (0.35, 0.50),
                "rump_width_ratio": (0.17, 0.29),
                "cannon_ratio": (0.07, 0.13),
            },
            "phenotype": {
                "colors": ["Putih", "Cokelat", "Hitam", "Belang"],
                "faces": ["Sedang", "Lurus"],
                "horns": ["Bertanduk", "Tidak bertanduk/polled", "Tanduk kecil"],
                "ears": ["Sedang", "Kecil"],
                "body_builds": ["Kompak", "Dada cukup lebar", "Padat"],
                "features": [
                    "Ekor gemuk",
                    "Cadangan lemak ekor jelas",
                    "Kaki kuat",
                    "Punggung relatif lurus",
                ],
            },
            "notes": "Cadangan lemak di ekor perlu diperhatikan saat menilai komposisi tubuh.",
        },
        "Merino Cross": {
            "target_market_min": 35,
            "target_market_ideal": 60,
            "adult_weight_min": 45,
            "adult_weight_max": 85,
            "height_min": 60,
            "height_max": 80,
            "adg": 0.12,
            "dressing": 46,
            "quant": {
                "chest_depth_ratio": (0.36, 0.51),
                "rump_width_ratio": (0.18, 0.31),
                "cannon_ratio": (0.08, 0.14),
            },
            "phenotype": {
                "colors": ["Putih", "Krem", "Putih krem"],
                "faces": ["Sedang", "Lurus"],
                "horns": ["Bertanduk", "Tidak bertanduk/polled", "Tanduk kecil"],
                "ears": ["Sedang", "Kecil"],
                "body_builds": ["Rangka sedang besar", "Panjang", "Berbulu tebal"],
                "features": [
                    "Bulu/wol lebih tebal",
                    "Rangka panjang",
                    "Dada dalam",
                    "Kaki kuat",
                ],
            },
            "notes": "Rangka lebih besar, perlu manajemen pakan baik untuk mencapai performa optimal.",
        },
    },
}


SPECIES_CONFIG = {
    "Sapi Potong": {
        "formula": "large",
        "ideal_bcs": (3.0, 4.0),
        "market_name": "potong/penggemukan",
        "price_unit": "kg bobot hidup",
    },
    "Sapi Perah": {
        "formula": "large",
        "ideal_bcs": (2.75, 3.5),
        "market_name": "perah/bibit",
        "price_unit": "kg bobot hidup",
    },
    "Kerbau": {
        "formula": "large",
        "ideal_bcs": (3.0, 4.0),
        "market_name": "kerja/potong/bibit",
        "price_unit": "kg bobot hidup",
    },
    "Kambing": {
        "formula": "small",
        "ideal_bcs": (2.5, 3.5),
        "market_name": "pedaging/perah/bibit",
        "price_unit": "kg bobot hidup",
    },
    "Domba": {
        "formula": "small",
        "ideal_bcs": (2.5, 3.5),
        "market_name": "pedaging/bibit",
        "price_unit": "kg bobot hidup",
    },
}


PURPOSE_OPTIONS = [
    "Penggemukan / Potong",
    "Bibit / Breeding",
    "Perah",
    "Jagal",
    "Blantik / Jual Beli",
]


COLOR_OPTIONS = [
    "Merah bata",
    "Cokelat kemerahan",
    "Hitam pada jantan dewasa",
    "Putih",
    "Abu-abu muda",
    "Abu-abu tua",
    "Cokelat",
    "Abu-abu",
    "Putih keabu-abuan",
    "Merah kecokelatan",
    "Cokelat putih",
    "Merah putih",
    "Krem putih",
    "Cokelat muda",
    "Cokelat keemasan",
    "Hitam putih",
    "Putih hitam",
    "Belang hitam putih",
    "Cokelat kekuningan",
    "Abu-cokelat",
    "Belang tidak seragam",
    "Abu-abu gelap",
    "Hitam keabu-abuan",
    "Cokelat kehitaman",
    "Hitam",
    "Hitam mengilap",
    "Putih cokelat",
    "Belang",
    "Putih kepala cokelat",
    "Krem muda",
    "Putih bersih",
    "Krem",
    "Putih krem",
    "Lainnya / tidak sesuai",
    "Tidak yakin",
]


FACE_OPTIONS = [
    "Lurus",
    "Panjang",
    "Pendek",
    "Pendek agak lebar",
    "Lebar",
    "Halus",
    "Cembung",
    "Cembung ringan",
    "Roman nose",
    "Sedang",
    "Tidak yakin",
]


HORN_OPTIONS = [
    "Bertanduk",
    "Tidak bertanduk/polled",
    "Tanduk kecil",
    "Tanduk melengkung",
    "Tanduk besar",
    "Tanduk melingkar",
    "Tanduk kecil melengkung",
    "Melengkung ke belakang",
    "Tidak yakin",
]


EAR_OPTIONS = [
    "Kecil",
    "Sedang",
    "Tegak",
    "Tegak sedang",
    "Agak menggantung",
    "Menggantung/lebar",
    "Panjang menggantung",
    "Sedang menggantung",
    "Tidak yakin",
]


BODY_BUILD_OPTIONS = [
    "Kompak",
    "Padat",
    "Rangka sedang",
    "Rangka besar",
    "Tinggi",
    "Panjang",
    "Berotot",
    "Berotot sedang",
    "Panjang dan dalam",
    "Punggung panjang",
    "Bentuk tubuh perah",
    "Dwiguna",
    "Dada lebar",
    "Paha penuh",
    "Ramping perah",
    "Dada dalam",
    "Kuat",
    "Kecil",
    "Lincah",
    "Kecil sedang",
    "Adaptif",
    "Rangka sedang besar",
    "Berbulu tebal",
    "Lainnya / tidak sesuai",
    "Tidak yakin",
]


# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def clamp(value, low, high):
    return max(low, min(high, value))


def rupiah(value):
    try:
        return f"Rp{value:,.0f}".replace(",", ".")
    except Exception:
        return "-"


def estimate_weight(species, heart_girth_cm, body_length_cm):
    formula_type = SPECIES_CONFIG[species]["formula"]

    if formula_type == "large":
        weight = (heart_girth_cm ** 2 * body_length_cm) / 10840
    else:
        weight = (heart_girth_cm ** 2 * body_length_cm) / 10000

    return round(weight, 2)


def get_age_stage(species, age_months):
    if species in ["Sapi Potong", "Sapi Perah", "Kerbau"]:
        if age_months < 8:
            return "Pedet/anak"
        if age_months < 18:
            return "Muda/tumbuh"
        if age_months < 36:
            return "Dewasa muda/siap produksi"
        return "Dewasa"

    if age_months < 4:
        return "Cempe/anak"
    if age_months < 10:
        return "Muda/tumbuh"
    if age_months < 24:
        return "Dewasa muda/siap produksi"
    return "Dewasa"


def score_weight(weight, target_min, target_ideal):
    max_score = 20

    if weight <= 0:
        return 0

    if weight < target_min:
        ratio = weight / target_min
        return round(clamp(ratio * 15, 0, 15), 1)

    if target_min <= weight <= target_ideal:
        ratio = (weight - target_min) / max(target_ideal - target_min, 1)
        return round(15 + ratio * 5, 1)

    excess_ratio = (weight - target_ideal) / target_ideal
    penalty = min(excess_ratio * 8, 4)
    return round(max_score - penalty, 1)


def score_bcs(bcs, ideal_low, ideal_high, purpose):
    max_score = 15

    if ideal_low <= bcs <= ideal_high:
        base = max_score
    else:
        distance = min(abs(bcs - ideal_low), abs(bcs - ideal_high))
        base = max_score - distance * 5

    if purpose == "Perah" and bcs > 3.75:
        base -= 1.5
    if purpose == "Jagal" and bcs < 3.0:
        base -= 2
    if purpose == "Bibit / Breeding" and (bcs < 2.75 or bcs > 4.0):
        base -= 2

    return round(clamp(base, 0, max_score), 1)


def score_frame(height_cm, height_min, height_max):
    max_score = 10

    if height_min <= height_cm <= height_max:
        return max_score

    if height_cm < height_min:
        ratio = height_cm / height_min
        return round(clamp(ratio * 8, 0, 8), 1)

    excess_ratio = (height_cm - height_max) / height_max
    penalty = min(excess_ratio * 6, 2.5)
    return round(max_score - penalty, 1)


def score_proportion(heart_girth_cm, body_length_cm, species):
    max_score = 8

    if heart_girth_cm <= 0:
        return 0, 0

    proportion = body_length_cm / heart_girth_cm

    if species in ["Sapi Potong", "Sapi Perah", "Kerbau"]:
        low, high = 0.85, 1.18
    else:
        low, high = 0.80, 1.20

    if low <= proportion <= high:
        return max_score, proportion

    distance = min(abs(proportion - low), abs(proportion - high))
    score = max_score - distance * 15
    return round(clamp(score, 0, max_score), 1), proportion


def score_health(health_checks):
    max_score = 15
    total = len(health_checks)

    if total == 0:
        return 0

    positive = sum(1 for value in health_checks.values() if value)
    return round((positive / total) * max_score, 1)


def score_market_readiness(weight, target_min, bcs, health_score, purpose):
    max_score = 7
    score = 0

    if weight >= target_min:
        score += 3
    elif weight >= target_min * 0.9:
        score += 2.3
    elif weight >= target_min * 0.8:
        score += 1.6
    else:
        score += 0.8

    if purpose in ["Jagal", "Penggemukan / Potong", "Blantik / Jual Beli"]:
        if 3.0 <= bcs <= 4.0:
            score += 2
        elif 2.5 <= bcs < 3.0 or 4.0 < bcs <= 4.5:
            score += 1.2
        else:
            score += 0.5
    else:
        if 2.75 <= bcs <= 3.75:
            score += 2
        else:
            score += 0.8

    if health_score >= 13:
        score += 2
    elif health_score >= 10:
        score += 1.2
    else:
        score += 0.5

    return round(clamp(score, 0, max_score), 1)


def score_ratio(value, target_range, max_score):
    low, high = target_range

    if value <= 0:
        return 0

    if low <= value <= high:
        return max_score

    if value < low:
        gap = low - value
    else:
        gap = value - high

    tolerance = max((high - low), 0.01)
    penalty = min((gap / tolerance) * max_score, max_score)
    return round(max_score - penalty, 1)


def score_quantitative_traits(
    chest_depth_cm,
    rump_width_cm,
    cannon_circumference_cm,
    height_cm,
    breed_info,
):
    max_score = 10

    if height_cm <= 0:
        return 0, {
            "Rasio kedalaman dada": 0,
            "Rasio lebar pinggul": 0,
            "Rasio lingkar tulang kering": 0,
        }

    chest_ratio = chest_depth_cm / height_cm
    rump_ratio = rump_width_cm / height_cm
    cannon_ratio = cannon_circumference_cm / height_cm

    quant = breed_info["quant"]

    chest_score = score_ratio(
        chest_ratio,
        quant["chest_depth_ratio"],
        4,
    )

    rump_score = score_ratio(
        rump_ratio,
        quant["rump_width_ratio"],
        3,
    )

    cannon_score = score_ratio(
        cannon_ratio,
        quant["cannon_ratio"],
        3,
    )

    total = round(chest_score + rump_score + cannon_score, 1)

    details = {
        "Rasio kedalaman dada": round(chest_ratio, 3),
        "Rasio lebar pinggul": round(rump_ratio, 3),
        "Rasio lingkar tulang kering": round(cannon_ratio, 3),
        "Skor kedalaman dada": chest_score,
        "Skor lebar pinggul": rump_score,
        "Skor tulang kering": cannon_score,
    }

    return clamp(total, 0, max_score), details


def match_score(selected_value, expected_values, max_score):
    if selected_value == "Tidak yakin":
        return round(max_score * 0.45, 1), "Tidak yakin"

    if selected_value == "Lainnya / tidak sesuai":
        return 0, "Tidak sesuai"

    if selected_value in expected_values:
        return max_score, "Sesuai"

    return round(max_score * 0.35, 1), "Kurang sesuai"


def score_qualitative_traits(
    selected_color,
    selected_face,
    selected_horn,
    selected_ear,
    selected_body_build,
    selected_features,
    breed_info,
):
    pheno = breed_info["phenotype"]

    color_score, color_status = match_score(selected_color, pheno["colors"], 3)
    face_score, face_status = match_score(selected_face, pheno["faces"], 2)
    horn_score, horn_status = match_score(selected_horn, pheno["horns"], 2)
    ear_score, ear_status = match_score(selected_ear, pheno["ears"], 2)
    body_score, body_status = match_score(selected_body_build, pheno["body_builds"], 2.5)

    expected_features = pheno["features"]

    if len(expected_features) == 0:
        feature_score = 3.5
    else:
        matched_features = [
            feature
            for feature in selected_features
            if feature in expected_features
        ]
        feature_score = 3.5 * (len(matched_features) / len(expected_features))
        feature_score = clamp(feature_score, 0, 3.5)

    total = round(
        color_score
        + face_score
        + horn_score
        + ear_score
        + body_score
        + feature_score,
        1,
    )

    details = {
        "Warna bulu": {
            "Input": selected_color,
            "Status": color_status,
            "Skor": color_score,
            "Acuan": ", ".join(pheno["colors"]),
        },
        "Bentuk wajah": {
            "Input": selected_face,
            "Status": face_status,
            "Skor": face_score,
            "Acuan": ", ".join(pheno["faces"]),
        },
        "Tanduk": {
            "Input": selected_horn,
            "Status": horn_status,
            "Skor": horn_score,
            "Acuan": ", ".join(pheno["horns"]),
        },
        "Telinga": {
            "Input": selected_ear,
            "Status": ear_status,
            "Skor": ear_score,
            "Acuan": ", ".join(pheno["ears"]),
        },
        "Bentuk tubuh": {
            "Input": selected_body_build,
            "Status": body_status,
            "Skor": body_score,
            "Acuan": ", ".join(pheno["body_builds"]),
        },
        "Ciri khas bangsa": {
            "Input": ", ".join(selected_features) if selected_features else "-",
            "Status": f"{len(selected_features)} dipilih",
            "Skor": round(feature_score, 1),
            "Acuan": ", ".join(expected_features),
        },
    }

    return clamp(total, 0, 15), details


def classify_total_score(total_score):
    if total_score >= 85:
        return "Sangat Layak", "good"
    if total_score >= 70:
        return "Layak", "good"
    if total_score >= 55:
        return "Perlu Perbaikan", "warning"
    return "Risiko Tinggi", "danger"


def classify_weight_position(weight, target_min, target_ideal):
    if weight < target_min * 0.85:
        return "Jauh di bawah target"
    if weight < target_min:
        return "Mendekati target minimum"
    if target_min <= weight <= target_ideal:
        return "Dalam rentang target"
    if weight <= target_ideal * 1.15:
        return "Di atas target ideal"
    return "Terlalu berat untuk target umum"


def generate_insights(
    species,
    breed,
    purpose,
    sex,
    age_months,
    age_stage,
    weight,
    target_min,
    target_ideal,
    bcs,
    ideal_bcs,
    height_cm,
    heart_girth_cm,
    body_length_cm,
    total_score,
    category,
    weight_position,
    frame_score,
    proportion,
    health_score,
    market_score,
    quant_score,
    quant_details,
    qualitative_score,
    qualitative_details,
    price_per_kg,
    feed_cost_per_day,
    desired_target_weight,
    adg,
    dressing,
    notes,
):
    insights = []

    deficit_to_min = max(target_min - weight, 0)
    deficit_to_desired = max(desired_target_weight - weight, 0)
    days_to_target = math.ceil(deficit_to_desired / adg) if adg > 0 and deficit_to_desired > 0 else 0

    if category in ["Sangat Layak", "Layak"]:
        insights.append(
            {
                "type": "good",
                "title": "Kesimpulan utama",
                "body": (
                    f"Ternak {species} bangsa {breed} masuk kategori **{category}**. "
                    f"Bobot estimasi {weight:.1f} kg berada pada posisi **{weight_position.lower()}** "
                    f"untuk target {target_min}-{target_ideal} kg."
                ),
            }
        )
    elif category == "Perlu Perbaikan":
        insights.append(
            {
                "type": "warning",
                "title": "Kesimpulan utama",
                "body": (
                    "Ternak masih **perlu perbaikan** sebelum dijadikan pilihan utama. "
                    "Fokus evaluasi ada pada bobot, BCS, proporsi tubuh, kesehatan, dan kesesuaian fenotipe bangsa."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "danger",
                "title": "Kesimpulan utama",
                "body": (
                    "Ternak masuk kategori **risiko tinggi**. Sebaiknya tidak langsung dibeli, "
                    "dijual sebagai premium, atau dijadikan bibit sebelum dilakukan pemeriksaan lanjutan."
                ),
            }
        )

    if weight < target_min:
        insights.append(
            {
                "type": "warning",
                "title": "Bobot belum mencapai target minimum",
                "body": (
                    f"Selisih terhadap target minimum sekitar **{deficit_to_min:.1f} kg**. "
                    f"Dengan asumsi pertambahan bobot harian {adg:.2f} kg/hari, ternak membutuhkan "
                    f"sekitar **{math.ceil(deficit_to_min / adg) if adg > 0 else 0} hari** untuk mencapai target minimum."
                ),
            }
        )
    elif weight > target_ideal * 1.15:
        insights.append(
            {
                "type": "warning",
                "title": "Bobot terlalu tinggi untuk target umum",
                "body": (
                    "Bobot yang terlalu tinggi dapat menurunkan efisiensi pembelian bila harga tidak sebanding "
                    "dengan tambahan karkas. Untuk jagal atau blantik, cek lagi umur, lemak, dan harga per kg."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "good",
                "title": "Bobot berada pada rentang ekonomis",
                "body": (
                    "Bobot sudah berada pada rentang yang relatif aman untuk dipertimbangkan. "
                    "Keputusan akhir tetap perlu melihat harga beli, kondisi kesehatan, dan tujuan pemeliharaan."
                ),
            }
        )

    if bcs < ideal_bcs[0]:
        insights.append(
            {
                "type": "warning",
                "title": "BCS cenderung kurus",
                "body": (
                    f"BCS {bcs:.1f} berada di bawah rentang ideal {ideal_bcs[0]}-{ideal_bcs[1]}. "
                    "Perlu evaluasi pakan, parasit, penyakit kronis, stres transportasi, dan kompetisi pakan."
                ),
            }
        )
    elif bcs > ideal_bcs[1]:
        insights.append(
            {
                "type": "warning",
                "title": "BCS cenderung gemuk",
                "body": (
                    f"BCS {bcs:.1f} berada di atas rentang ideal {ideal_bcs[0]}-{ideal_bcs[1]}. "
                    "Untuk indukan/perah, kondisi terlalu gemuk dapat mengganggu efisiensi reproduksi atau metabolisme. "
                    "Untuk potong, pastikan tambahan lemak masih dihargai pasar."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "good",
                "title": "BCS sesuai tujuan umum",
                "body": (
                    f"BCS {bcs:.1f} berada dalam rentang ideal. Ini mendukung performa pasar, "
                    "kesehatan, dan efisiensi pemeliharaan."
                ),
            }
        )

    if quant_score >= 8:
        insights.append(
            {
                "type": "good",
                "title": "Faktor kuantitatif tambahan baik",
                "body": (
                    f"Skor kuantitatif tambahan **{quant_score}/10**. "
                    "Rasio kedalaman dada, lebar pinggul, dan lingkar tulang kering relatif sesuai acuan bangsa."
                ),
            }
        )
    elif quant_score >= 5.5:
        insights.append(
            {
                "type": "warning",
                "title": "Faktor kuantitatif tambahan cukup",
                "body": (
                    f"Skor kuantitatif tambahan **{quant_score}/10**. "
                    "Masih perlu dicek apakah dada cukup dalam, pinggul cukup lebar, dan kaki cukup kuat untuk tujuan ternak."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "danger",
                "title": "Faktor kuantitatif tambahan lemah",
                "body": (
                    f"Skor kuantitatif tambahan **{quant_score}/10**. "
                    "Indikasi rangka, kapasitas tubuh, atau kekuatan kaki belum mendukung performa optimal."
                ),
            }
        )

    if qualitative_score >= 12:
        insights.append(
            {
                "type": "good",
                "title": "Kesesuaian ciri bangsa tinggi",
                "body": (
                    f"Skor kualitatif/fenotipe **{qualitative_score}/15**. "
                    f"Ciri luar ternak cukup sesuai dengan karakter bangsa {breed}."
                ),
            }
        )
    elif qualitative_score >= 8:
        insights.append(
            {
                "type": "warning",
                "title": "Kesesuaian ciri bangsa sedang",
                "body": (
                    f"Skor kualitatif/fenotipe **{qualitative_score}/15**. "
                    "Masih ada ciri yang kurang kuat. Untuk transaksi bibit atau premium, minta riwayat keturunan atau bukti asal ternak."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "danger",
                "title": "Kesesuaian ciri bangsa rendah",
                "body": (
                    f"Skor kualitatif/fenotipe **{qualitative_score}/15**. "
                    "Jangan langsung menganggap ternak murni atau premium hanya dari klaim penjual. Gunakan sebagai bahan negosiasi harga."
                ),
            }
        )

    mismatches = []
    for trait_name, trait_data in qualitative_details.items():
        if trait_data["Status"] in ["Kurang sesuai", "Tidak sesuai"]:
            mismatches.append(f"{trait_name}: {trait_data['Input']}")

    if mismatches:
        insights.append(
            {
                "type": "warning",
                "title": "Ciri kualitatif yang perlu dicermati",
                "body": (
                    "Beberapa ciri kurang sesuai dengan acuan bangsa: "
                    + "; ".join(mismatches)
                    + ". Ini bisa disebabkan persilangan, umur, jenis kelamin, kondisi perawatan, atau salah identifikasi bangsa."
                ),
            }
        )

    if proportion < 0.8:
        prop_msg = "Panjang badan relatif pendek dibanding lingkar dada. Cek kembali pengukuran, umur, dan tipe genetik."
        prop_type = "warning"
    elif proportion > 1.2:
        prop_msg = "Panjang badan relatif panjang dibanding lingkar dada. Ternak bisa terlihat rangka panjang tetapi belum cukup berisi."
        prop_type = "warning"
    else:
        prop_msg = "Proporsi panjang badan dan lingkar dada relatif seimbang."
        prop_type = "good"

    insights.append(
        {
            "type": prop_type,
            "title": "Proporsi tubuh",
            "body": (
                f"Indeks panjang/lingkar dada = **{proportion:.2f}**. {prop_msg} "
                f"Skor rangka/tinggi: **{frame_score}/10**."
            ),
        }
    )

    if health_score < 10:
        insights.append(
            {
                "type": "danger",
                "title": "Kesehatan lapangan perlu diperiksa",
                "body": (
                    f"Skor kesehatan hanya **{health_score}/15**. Jangan hanya mengejar bobot. "
                    "Periksa nafsu makan, pernapasan, mata-hidung, feses, pincang, luka, dan tanda parasit."
                ),
            }
        )
    elif health_score < 13:
        insights.append(
            {
                "type": "warning",
                "title": "Kesehatan cukup, tetapi belum optimal",
                "body": (
                    f"Skor kesehatan **{health_score}/15**. Ternak masih bisa dipertimbangkan, "
                    "namun perlu pemeriksaan lapangan sebelum transaksi."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "good",
                "title": "Kesehatan lapangan baik",
                "body": (
                    f"Skor kesehatan **{health_score}/15**. Kondisi ini mendukung keputusan beli/pelihara, "
                    "selama tidak ada penyakit tersembunyi."
                ),
            }
        )

    if purpose == "Jagal":
        carcass = weight * dressing / 100
        meat = carcass * 0.70
        insights.append(
            {
                "type": "info",
                "title": "Insight untuk jagal",
                "body": (
                    f"Estimasi karkas sekitar **{carcass:.1f} kg** dengan asumsi dressing {dressing}%. "
                    f"Estimasi daging bersih kasar sekitar **{meat:.1f} kg**. "
                    "Prioritaskan ternak dengan dada dalam, paha berisi, punggung lebar, tidak pincang, dan BCS cukup."
                ),
            }
        )
    elif purpose == "Blantik / Jual Beli":
        insights.append(
            {
                "type": "info",
                "title": "Insight untuk blantik",
                "body": (
                    "Nilai tawar utama ada pada kombinasi bobot, tampilan tubuh, bangsa, umur, kesehatan, dan momentum pasar. "
                    "Ciri bangsa yang kuat dapat menaikkan nilai jual, sedangkan ciri yang meragukan bisa menjadi bahan negosiasi."
                ),
            }
        )
    elif purpose == "Penggemukan / Potong":
        insights.append(
            {
                "type": "info",
                "title": "Insight penggemukan",
                "body": (
                    f"Potensi penggemukan dipengaruhi bangsa {breed}, pakan, kesehatan, umur, dan kapasitas rangka. "
                    f"Asumsi ADG sistem ini: **{adg:.2f} kg/hari**. "
                    "Pilih ternak dengan rangka cukup besar, sehat, belum terlalu gemuk, dan dada/pinggul berkembang."
                ),
            }
        )
    elif purpose == "Perah":
        insights.append(
            {
                "type": "info",
                "title": "Insight ternak perah",
                "body": (
                    "Untuk ternak perah, bobot bukan satu-satunya indikator. Perlu penilaian ambing, riwayat laktasi, "
                    "kesehatan reproduksi, kaki, kuku, dan riwayat pakan."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "info",
                "title": "Insight bibit/breeding",
                "body": (
                    "Untuk bibit, ciri bangsa dan struktur tubuh penting. Prioritaskan kesehatan, kaki, alat reproduksi, "
                    "riwayat keturunan, umur produktif, BCS sedang, serta bentuk tubuh yang sesuai tujuan produksi."
                ),
            }
        )

    if price_per_kg > 0:
        estimated_value = weight * price_per_kg
        insights.append(
            {
                "type": "info",
                "title": "Estimasi ekonomi sederhana",
                "body": (
                    f"Estimasi nilai bobot hidup: **{rupiah(estimated_value)}**. "
                    f"Bila memakai basis karkas kasar, bobot karkas estimasi sekitar "
                    f"**{weight * dressing / 100:.1f} kg**. "
                    "Gunakan ini sebagai pembanding awal, bukan harga final transaksi."
                ),
            }
        )

    if feed_cost_per_day > 0 and days_to_target > 0:
        total_feed_cost = feed_cost_per_day * days_to_target
        added_weight_value = deficit_to_desired * price_per_kg if price_per_kg > 0 else 0

        body = (
            f"Untuk mengejar target {desired_target_weight:.1f} kg, estimasi waktu sekitar "
            f"**{days_to_target} hari**. Estimasi biaya pakan tambahan: **{rupiah(total_feed_cost)}**."
        )

        if price_per_kg > 0:
            body += (
                f" Nilai tambahan bobot kasar: **{rupiah(added_weight_value)}**. "
                f"Selisih kasar nilai tambahan dan biaya pakan: **{rupiah(added_weight_value - total_feed_cost)}**."
            )

        insights.append(
            {
                "type": "info",
                "title": "Simulasi menuju target bobot",
                "body": body,
            }
        )

    insights.append(
        {
            "type": "info",
            "title": f"Catatan bangsa {breed}",
            "body": notes,
        }
    )

    return insights


def build_ai_prompt(
    species,
    breed,
    purpose,
    sex,
    age_months,
    age_stage,
    weight,
    target_min,
    target_ideal,
    bcs,
    height_cm,
    heart_girth_cm,
    body_length_cm,
    chest_depth_cm,
    rump_width_cm,
    cannon_circumference_cm,
    selected_color,
    selected_face,
    selected_horn,
    selected_ear,
    selected_body_build,
    selected_features,
    total_score,
    category,
    health_score,
    market_score,
    quant_score,
    qualitative_score,
    qualitative_details,
    price_per_kg,
    feed_cost_per_day,
    notes,
):
    mismatch_lines = []

    for trait_name, trait_data in qualitative_details.items():
        mismatch_lines.append(
            f"- {trait_name}: input {trait_data['Input']} | status {trait_data['Status']} | acuan {trait_data['Acuan']}"
        )

    feature_text = ", ".join(selected_features) if selected_features else "-"

    prompt = f"""
Anda adalah konsultan peternakan, jagal, dan perdagangan ternak.
Analisis data ternak berikut secara detail, praktis, dan berbasis keputusan lapangan.

DATA TERNAK:
- Jenis ternak: {species}
- Bangsa/ras: {breed}
- Tujuan penilaian: {purpose}
- Jenis kelamin: {sex}
- Umur: {age_months} bulan
- Fase umur: {age_stage}

DATA KUANTITATIF:
- Lingkar dada: {heart_girth_cm} cm
- Panjang badan: {body_length_cm} cm
- Tinggi badan: {height_cm} cm
- Kedalaman dada: {chest_depth_cm} cm
- Lebar pinggul/panggul: {rump_width_cm} cm
- Lingkar tulang kering/metacarpus: {cannon_circumference_cm} cm
- Estimasi bobot hidup: {weight:.2f} kg
- Target bobot minimum bangsa ini: {target_min} kg
- Target bobot ideal bangsa ini: {target_ideal} kg
- BCS: {bcs}

DATA KUALITATIF / FENOTIPE:
- Warna bulu: {selected_color}
- Bentuk wajah/profil kepala: {selected_face}
- Tanduk: {selected_horn}
- Bentuk telinga: {selected_ear}
- Bentuk tubuh umum: {selected_body_build}
- Ciri khas yang tampak: {feature_text}

KESESUAIAN CIRI BANGSA:
{chr(10).join(mismatch_lines)}

HASIL SKOR:
- Skor kesehatan lapangan: {health_score}/15
- Skor kesiapan pasar: {market_score}/7
- Skor kuantitatif tambahan: {quant_score}/10
- Skor kualitatif/fenotipe: {qualitative_score}/15
- Skor total: {total_score}/100
- Kategori hasil: {category}

EKONOMI:
- Harga per kg bobot hidup: Rp{price_per_kg:,.0f}
- Biaya pakan per hari: Rp{feed_cost_per_day:,.0f}

CATATAN BANGSA:
{notes}

TUGAS ANALISIS:
1. Berikan kesimpulan kelayakan ternak.
2. Jelaskan kekuatan dan kelemahannya dari sisi kuantitatif.
3. Jelaskan kesesuaian kualitatif/fenotipe terhadap bangsa ternak.
4. Berikan rekomendasi untuk peternak.
5. Berikan insight untuk jagal.
6. Berikan insight untuk blantik ternak.
7. Berikan strategi negosiasi harga yang wajar.
8. Berikan tindakan perbaikan 7-30 hari.
9. Jelaskan risiko yang harus diperiksa langsung di lapangan.

Gunakan bahasa Indonesia yang praktis, mudah dipahami, dan tidak terlalu teoritis.
""".strip()

    return prompt


# =========================================================
# SESSION STATE
# =========================================================

if "records" not in st.session_state:
    st.session_state.records = []


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🐄 Sistem Penilaian Ternak")
st.sidebar.caption("Kuantitatif + kualitatif berbasis jenis dan bangsa.")

with st.sidebar.expander("Cara pakai singkat", expanded=True):
    st.write(
        """
1. Pilih jenis dan bangsa ternak.  
2. Masukkan ukuran tubuh, BCS, kesehatan, dan ciri luar/fenotipe.  
3. Buka tab hasil untuk melihat skor, evaluasi, insight, dan prompt AI.  
4. Simpan data ke tabel evaluasi bila ingin membandingkan beberapa ternak.
"""
    )

st.sidebar.warning(
    "Hasil bersifat estimasi awal. Untuk keputusan besar, tetap lakukan pemeriksaan langsung dan konsultasi teknis."
)


# =========================================================
# HEADER
# =========================================================

st.title("🐄 Sistem Penilaian Ternak Berbasis Kuantitatif & Kualitatif")
st.caption(
    "Menilai ternak berdasarkan jenis, bangsa, ukuran tubuh, BCS, kesehatan, ciri fenotipe, dan tujuan pasar."
)


# =========================================================
# INPUT AREA
# =========================================================

tab_input, tab_result, tab_pheno, tab_compare, tab_prompt, tab_guide = st.tabs(
    [
        "📝 Input Penilaian",
        "📊 Hasil & Insight",
        "🧬 Ciri Bangsa",
        "📋 Tabel Evaluasi",
        "🤖 Prompt AI",
        "📘 Panduan",
    ]
)


with tab_input:
    st.subheader("Input Identitas Ternak")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        species = st.selectbox(
            "Jenis ternak",
            list(BREED_DATA.keys()),
            index=0,
        )

        breed = st.selectbox(
            "Bangsa / ras ternak",
            list(BREED_DATA[species].keys()),
        )

        purpose = st.selectbox(
            "Tujuan penilaian",
            PURPOSE_OPTIONS,
            index=0,
        )

    breed_info = BREED_DATA[species][breed]
    pheno = breed_info["phenotype"]

    with col_b:
        sex = st.selectbox(
            "Jenis kelamin",
            ["Jantan", "Betina", "Kebiri / tidak diketahui"],
        )

        age_months = st.number_input(
            "Umur ternak (bulan)",
            min_value=0,
            max_value=240,
            value=24 if species in ["Sapi Potong", "Sapi Perah", "Kerbau"] else 12,
            step=1,
        )

        bcs = st.slider(
            "BCS / Body Condition Score",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.1,
            help="Skor 1 sangat kurus, 3 sedang/ideal, 5 sangat gemuk.",
        )

    with col_c:
        animal_id = st.text_input(
            "Kode / nama ternak",
            value=f"{species}-{breed}-{datetime.now().strftime('%H%M%S')}",
        )

        location = st.text_input(
            "Lokasi / kandang",
            value="",
            placeholder="Contoh: Kandang A / Pasar Hewan",
        )

        evaluator = st.text_input(
            "Penilai",
            value="",
            placeholder="Nama peternak / petugas / blantik",
        )

    st.markdown("---")
    st.subheader("Faktor Kuantitatif: Ukuran Tubuh")

    default_height = int((breed_info["height_min"] + breed_info["height_max"]) / 2)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        heart_girth_cm = st.number_input(
            "Lingkar dada (cm)",
            min_value=10.0,
            max_value=300.0,
            value=150.0 if species in ["Sapi Potong", "Sapi Perah", "Kerbau"] else 70.0,
            step=0.5,
        )

    with col_m2:
        body_length_cm = st.number_input(
            "Panjang badan (cm)",
            min_value=10.0,
            max_value=300.0,
            value=130.0 if species in ["Sapi Potong", "Sapi Perah", "Kerbau"] else 65.0,
            step=0.5,
        )

    with col_m3:
        height_cm = st.number_input(
            "Tinggi badan / gumba (cm)",
            min_value=10.0,
            max_value=250.0,
            value=float(default_height),
            step=0.5,
        )

    q1, q2, q3 = st.columns(3)

    with q1:
        chest_depth_cm = st.number_input(
            "Kedalaman dada (cm)",
            min_value=1.0,
            max_value=150.0,
            value=60.0 if species in ["Sapi Potong", "Sapi Perah", "Kerbau"] else 28.0,
            step=0.5,
            help="Diukur dari bagian atas punggung/gumba ke bagian bawah dada secara vertikal.",
        )

    with q2:
        rump_width_cm = st.number_input(
            "Lebar pinggul / panggul (cm)",
            min_value=1.0,
            max_value=150.0,
            value=35.0 if species in ["Sapi Potong", "Sapi Perah", "Kerbau"] else 16.0,
            step=0.5,
            help="Menggambarkan kapasitas rangka belakang, penting untuk daging, reproduksi, dan keseimbangan tubuh.",
        )

    with q3:
        cannon_circumference_cm = st.number_input(
            "Lingkar tulang kering / kaki depan (cm)",
            min_value=1.0,
            max_value=80.0,
            value=18.0 if species in ["Sapi Potong", "Sapi Perah", "Kerbau"] else 7.0,
            step=0.5,
            help="Indikator kasar kekuatan kaki/rangka. Jangan dinilai sendiri tanpa melihat postur dan kesehatan kuku.",
        )

    st.markdown(
        """
<div class="section-note">
<strong>Faktor kuantitatif tambahan</strong> membantu membaca kapasitas tubuh: dada dalam untuk volume tubuh,
pinggul lebar untuk rangka belakang/reproduksi, dan tulang kering untuk indikasi kekuatan kaki.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("Faktor Kualitatif: Ciri Luar / Fenotipe Bangsa")

    k1, k2, k3 = st.columns(3)

    with k1:
        selected_color = st.selectbox(
            "Warna bulu dominan",
            COLOR_OPTIONS,
            index=COLOR_OPTIONS.index(pheno["colors"][0]) if pheno["colors"][0] in COLOR_OPTIONS else 0,
        )

        selected_face = st.selectbox(
            "Bentuk wajah / profil kepala",
            FACE_OPTIONS,
            index=FACE_OPTIONS.index(pheno["faces"][0]) if pheno["faces"][0] in FACE_OPTIONS else 0,
        )

    with k2:
        selected_horn = st.selectbox(
            "Kondisi tanduk",
            HORN_OPTIONS,
            index=HORN_OPTIONS.index(pheno["horns"][0]) if pheno["horns"][0] in HORN_OPTIONS else 0,
        )

        selected_ear = st.selectbox(
            "Bentuk telinga",
            EAR_OPTIONS,
            index=EAR_OPTIONS.index(pheno["ears"][0]) if pheno["ears"][0] in EAR_OPTIONS else 0,
        )

    with k3:
        selected_body_build = st.selectbox(
            "Bentuk tubuh umum",
            BODY_BUILD_OPTIONS,
            index=BODY_BUILD_OPTIONS.index(pheno["body_builds"][0]) if pheno["body_builds"][0] in BODY_BUILD_OPTIONS else 0,
        )

        selected_features = st.multiselect(
            "Ciri khas yang tampak",
            options=pheno["features"],
            default=pheno["features"][:2],
        )

    with st.expander("Acuan ciri bangsa yang sedang dipilih", expanded=False):
        st.write(f"**Bangsa:** {breed}")
        st.write(f"**Warna acuan:** {', '.join(pheno['colors'])}")
        st.write(f"**Wajah acuan:** {', '.join(pheno['faces'])}")
        st.write(f"**Tanduk acuan:** {', '.join(pheno['horns'])}")
        st.write(f"**Telinga acuan:** {', '.join(pheno['ears'])}")
        st.write(f"**Bentuk tubuh acuan:** {', '.join(pheno['body_builds'])}")
        st.write(f"**Ciri khas:** {', '.join(pheno['features'])}")

    st.markdown("---")
    st.subheader("Kesehatan Lapangan")

    h1, h2, h3 = st.columns(3)

    with h1:
        check_appetite = st.checkbox("Nafsu makan baik", value=True)
        check_active = st.checkbox("Aktif dan responsif", value=True)
        check_eye_nose = st.checkbox("Mata dan hidung normal", value=True)

    with h2:
        check_feces = st.checkbox("Feses normal", value=True)
        check_limping = st.checkbox("Tidak pincang", value=True)
        check_skin = st.checkbox("Bulu/kulit tampak baik", value=True)

    with h3:
        check_breathing = st.checkbox("Napas normal", value=True)
        check_wound = st.checkbox("Tidak ada luka serius", value=True)
        check_parasite = st.checkbox("Tidak tampak gejala parasit berat", value=True)

    health_checks = {
        "Nafsu makan baik": check_appetite,
        "Aktif dan responsif": check_active,
        "Mata dan hidung normal": check_eye_nose,
        "Feses normal": check_feces,
        "Tidak pincang": check_limping,
        "Bulu/kulit baik": check_skin,
        "Napas normal": check_breathing,
        "Tidak ada luka serius": check_wound,
        "Tidak tampak parasit berat": check_parasite,
    }

    st.markdown("---")
    st.subheader("Ekonomi dan Target")

    e1, e2, e3 = st.columns(3)

    with e1:
        price_per_kg = st.number_input(
            "Harga per kg bobot hidup (Rp)",
            min_value=0,
            value=0,
            step=1000,
        )

    with e2:
        feed_cost_per_day = st.number_input(
            "Biaya pakan per hari (Rp)",
            min_value=0,
            value=0,
            step=1000,
        )

    with e3:
        desired_target_weight = st.number_input(
            "Target bobot yang ingin dicapai (kg)",
            min_value=0.0,
            value=float(breed_info["target_market_ideal"]),
            step=1.0,
        )

    st.success("Input selesai. Buka tab **Hasil & Insight** untuk melihat evaluasi.")


# =========================================================
# CALCULATION
# =========================================================

target_min = breed_info["target_market_min"]
target_ideal = breed_info["target_market_ideal"]
adult_min = breed_info["adult_weight_min"]
adult_max = breed_info["adult_weight_max"]
height_min = breed_info["height_min"]
height_max = breed_info["height_max"]
adg = breed_info["adg"]
dressing = breed_info["dressing"]
notes = breed_info["notes"]
ideal_bcs = SPECIES_CONFIG[species]["ideal_bcs"]

estimated_weight = estimate_weight(species, heart_girth_cm, body_length_cm)
age_stage = get_age_stage(species, age_months)

weight_score = score_weight(estimated_weight, target_min, target_ideal)
bcs_score = score_bcs(bcs, ideal_bcs[0], ideal_bcs[1], purpose)
frame_score = score_frame(height_cm, height_min, height_max)
prop_score, proportion = score_proportion(heart_girth_cm, body_length_cm, species)
health_score = score_health(health_checks)
market_score = score_market_readiness(
    estimated_weight,
    target_min,
    bcs,
    health_score,
    purpose,
)

quant_score, quant_details = score_quantitative_traits(
    chest_depth_cm=chest_depth_cm,
    rump_width_cm=rump_width_cm,
    cannon_circumference_cm=cannon_circumference_cm,
    height_cm=height_cm,
    breed_info=breed_info,
)

qualitative_score, qualitative_details = score_qualitative_traits(
    selected_color=selected_color,
    selected_face=selected_face,
    selected_horn=selected_horn,
    selected_ear=selected_ear,
    selected_body_build=selected_body_build,
    selected_features=selected_features,
    breed_info=breed_info,
)

total_score = round(
    weight_score
    + bcs_score
    + frame_score
    + prop_score
    + health_score
    + market_score
    + quant_score
    + qualitative_score,
    1,
)

total_score = round(clamp(total_score, 0, 100), 1)

category, category_style = classify_total_score(total_score)
weight_position = classify_weight_position(estimated_weight, target_min, target_ideal)

carcass_estimate = round(estimated_weight * dressing / 100, 2)
meat_estimate = round(carcass_estimate * 0.70, 2)
estimated_value = estimated_weight * price_per_kg if price_per_kg > 0 else 0

deficit_to_desired = max(desired_target_weight - estimated_weight, 0)
days_to_desired = math.ceil(deficit_to_desired / adg) if adg > 0 and deficit_to_desired > 0 else 0
additional_feed_cost = days_to_desired * feed_cost_per_day


# =========================================================
# RESULTS
# =========================================================

with tab_result:
    st.subheader("Hasil Penilaian")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
<div class="metric-card">
    <div class="small-text">Skor Total</div>
    <div class="big-score">{total_score:.1f}</div>
    <div class="small-text">dari 100</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:
        st.metric("Kategori", category)
        st.caption(f"Tujuan: {purpose}")

    with col3:
        st.metric("Estimasi bobot hidup", f"{estimated_weight:.1f} kg")
        st.caption(weight_position)

    with col4:
        st.metric("Estimasi karkas", f"{carcass_estimate:.1f} kg")
        st.caption(f"Asumsi dressing {dressing}%")

    st.markdown("---")

    st.subheader("Rincian Skor")

    score_df = pd.DataFrame(
        [
            ["Bobot vs target bangsa", weight_score, 20],
            ["BCS / kondisi tubuh", bcs_score, 15],
            ["Rangka dan tinggi", frame_score, 10],
            ["Proporsi tubuh", prop_score, 8],
            ["Kesehatan lapangan", health_score, 15],
            ["Kesiapan pasar", market_score, 7],
            ["Kuantitatif tambahan", quant_score, 10],
            ["Kualitatif / fenotipe bangsa", qualitative_score, 15],
        ],
        columns=["Komponen", "Skor", "Maksimum"],
    )

    st.dataframe(
        score_df,
        use_container_width=True,
        hide_index=True,
    )

    st.progress(int(clamp(total_score, 0, 100)))

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            f"""
**Data bangsa/ras**  
Jenis: {species}  
Bangsa: {breed}  
Target pasar: {target_min}-{target_ideal} kg  
Bobot dewasa acuan: {adult_min}-{adult_max} kg
"""
        )

    with c2:
        st.info(
            f"""
**Kondisi tubuh**  
BCS: {bcs:.1f}  
BCS ideal: {ideal_bcs[0]}-{ideal_bcs[1]}  
Fase umur: {age_stage}  
Indeks panjang/lingkar dada: {proportion:.2f}
"""
        )

    with c3:
        st.info(
            f"""
**Ekonomi**  
Nilai bobot hidup: {rupiah(estimated_value) if price_per_kg > 0 else "-"}  
Target bobot: {desired_target_weight:.1f} kg  
Estimasi waktu ke target: {days_to_desired} hari  
Biaya pakan tambahan: {rupiah(additional_feed_cost) if feed_cost_per_day > 0 else "-"}
"""
        )

    st.markdown("---")

    st.subheader("Ringkasan Kuantitatif Tambahan")

    quant_df = pd.DataFrame(
        [
            [
                "Kedalaman dada / tinggi",
                quant_details["Rasio kedalaman dada"],
                f"{breed_info['quant']['chest_depth_ratio'][0]} - {breed_info['quant']['chest_depth_ratio'][1]}",
                quant_details["Skor kedalaman dada"],
                4,
            ],
            [
                "Lebar pinggul / tinggi",
                quant_details["Rasio lebar pinggul"],
                f"{breed_info['quant']['rump_width_ratio'][0]} - {breed_info['quant']['rump_width_ratio'][1]}",
                quant_details["Skor lebar pinggul"],
                3,
            ],
            [
                "Lingkar tulang kering / tinggi",
                quant_details["Rasio lingkar tulang kering"],
                f"{breed_info['quant']['cannon_ratio'][0]} - {breed_info['quant']['cannon_ratio'][1]}",
                quant_details["Skor tulang kering"],
                3,
            ],
        ],
        columns=["Indikator", "Nilai", "Acuan Rasio", "Skor", "Maksimum"],
    )

    st.dataframe(
        quant_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.subheader("Insight Otomatis")

    insight_list = generate_insights(
        species=species,
        breed=breed,
        purpose=purpose,
        sex=sex,
        age_months=age_months,
        age_stage=age_stage,
        weight=estimated_weight,
        target_min=target_min,
        target_ideal=target_ideal,
        bcs=bcs,
        ideal_bcs=ideal_bcs,
        height_cm=height_cm,
        heart_girth_cm=heart_girth_cm,
        body_length_cm=body_length_cm,
        total_score=total_score,
        category=category,
        weight_position=weight_position,
        frame_score=frame_score,
        proportion=proportion,
        health_score=health_score,
        market_score=market_score,
        quant_score=quant_score,
        quant_details=quant_details,
        qualitative_score=qualitative_score,
        qualitative_details=qualitative_details,
        price_per_kg=price_per_kg,
        feed_cost_per_day=feed_cost_per_day,
        desired_target_weight=desired_target_weight,
        adg=adg,
        dressing=dressing,
        notes=notes,
    )

    for insight in insight_list:
        st.markdown(
            f"""
<div class="insight-card {insight['type']}">
    <strong>{insight['title']}</strong><br>
    {insight['body']}
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    save_col1, save_col2 = st.columns([1, 2])

    with save_col1:
        save_button = st.button("💾 Simpan ke Tabel Evaluasi", use_container_width=True)

    if save_button:
        st.session_state.records.append(
            {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Kode Ternak": animal_id,
                "Lokasi": location,
                "Penilai": evaluator,
                "Jenis": species,
                "Bangsa": breed,
                "Tujuan": purpose,
                "Jenis Kelamin": sex,
                "Umur Bulan": age_months,
                "Fase Umur": age_stage,
                "Lingkar Dada cm": heart_girth_cm,
                "Panjang Badan cm": body_length_cm,
                "Tinggi cm": height_cm,
                "Kedalaman Dada cm": chest_depth_cm,
                "Lebar Pinggul cm": rump_width_cm,
                "Lingkar Tulang Kering cm": cannon_circumference_cm,
                "Estimasi Bobot kg": estimated_weight,
                "BCS": bcs,
                "Warna Bulu": selected_color,
                "Bentuk Wajah": selected_face,
                "Tanduk": selected_horn,
                "Telinga": selected_ear,
                "Bentuk Tubuh": selected_body_build,
                "Ciri Khas": ", ".join(selected_features),
                "Skor Bobot": weight_score,
                "Skor BCS": bcs_score,
                "Skor Rangka": frame_score,
                "Skor Proporsi": prop_score,
                "Skor Kesehatan": health_score,
                "Skor Pasar": market_score,
                "Skor Kuantitatif": quant_score,
                "Skor Kualitatif": qualitative_score,
                "Skor Total": total_score,
                "Kategori": category,
                "Posisi Bobot": weight_position,
                "Estimasi Karkas kg": carcass_estimate,
                "Estimasi Daging kg": meat_estimate,
                "Harga per kg": price_per_kg,
                "Estimasi Nilai": estimated_value,
            }
        )
        st.success("Data berhasil disimpan ke Tabel Evaluasi.")


# =========================================================
# PHENOTYPE TAB
# =========================================================

with tab_pheno:
    st.subheader("Evaluasi Ciri Bangsa / Fenotipe")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric("Skor Kualitatif", f"{qualitative_score:.1f}/15")
        st.caption("Berdasarkan warna, wajah, tanduk, telinga, tubuh, dan ciri khas.")

    with p2:
        st.metric("Skor Kuantitatif Tambahan", f"{quant_score:.1f}/10")
        st.caption("Berdasarkan rasio dada, pinggul, dan tulang kering.")

    with p3:
        conformity_pct = round((qualitative_score / 15) * 100, 1)
        st.metric("Kesesuaian Fenotipe", f"{conformity_pct}%")
        st.caption(f"Acuan: {breed}")

    st.markdown("---")

    qualitative_rows = []

    for trait_name, trait_data in qualitative_details.items():
        qualitative_rows.append(
            [
                trait_name,
                trait_data["Input"],
                trait_data["Status"],
                trait_data["Skor"],
                trait_data["Acuan"],
            ]
        )

    qualitative_df = pd.DataFrame(
        qualitative_rows,
        columns=["Ciri", "Input", "Status", "Skor", "Acuan Bangsa"],
    )

    st.dataframe(
        qualitative_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.subheader("Interpretasi Praktis")

    if qualitative_score >= 12:
        st.success(
            f"Ciri luar ternak relatif kuat mengarah ke bangsa {breed}. Ini bisa meningkatkan kepercayaan untuk tujuan bibit, jual beli, atau premium."
        )
    elif qualitative_score >= 8:
        st.warning(
            "Ciri luar masih sedang. Ternak bisa saja persilangan, kurang terawat, atau belum menunjukkan karakter penuh karena umur/jenis kelamin."
        )
    else:
        st.error(
            "Ciri luar kurang sesuai. Hindari membeli dengan harga premium hanya berdasarkan klaim bangsa tanpa bukti tambahan."
        )

    st.info(
        """
Untuk penilaian bibit atau harga premium, ciri fenotipe sebaiknya dilengkapi dengan:
riwayat induk-pejantan, catatan kelahiran, performa pertumbuhan, riwayat kesehatan,
dan pengamatan langsung oleh orang yang berpengalaman.
"""
    )


# =========================================================
# COMPARE TABLE
# =========================================================

with tab_compare:
    st.subheader("Tabel Evaluasi Ternak")

    if len(st.session_state.records) == 0:
        st.info("Belum ada data tersimpan. Simpan hasil dari tab **Hasil & Insight**.")
    else:
        records_df = pd.DataFrame(st.session_state.records)

        st.dataframe(
            records_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = records_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="⬇️ Download CSV Evaluasi",
            data=csv_data,
            file_name="evaluasi_ternak.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("---")
        st.subheader("Ringkasan Perbandingan")

        avg_score = records_df["Skor Total"].mean()
        best_idx = records_df["Skor Total"].idxmax()
        best_row = records_df.loc[best_idx]

        a, b, c = st.columns(3)

        with a:
            st.metric("Jumlah ternak dinilai", len(records_df))

        with b:
            st.metric("Rata-rata skor", f"{avg_score:.1f}")

        with c:
            st.metric(
                "Ternak terbaik",
                f"{best_row['Kode Ternak']}",
                f"{best_row['Skor Total']:.1f}",
            )

        st.markdown("**Jumlah berdasarkan kategori:**")
        category_count = (
            records_df["Kategori"]
            .value_counts()
            .reset_index()
        )
        category_count.columns = ["Kategori", "Jumlah"]
        st.dataframe(category_count, use_container_width=True, hide_index=True)

        st.markdown("**Rata-rata skor per jenis dan bangsa:**")
        group_df = (
            records_df
            .groupby(["Jenis", "Bangsa"], as_index=False)[
                ["Skor Total", "Skor Kuantitatif", "Skor Kualitatif"]
            ]
            .mean()
            .round(1)
        )
        st.dataframe(group_df, use_container_width=True, hide_index=True)


# =========================================================
# AI PROMPT
# =========================================================

with tab_prompt:
    st.subheader("Generator Prompt untuk AI Lain")

    ai_prompt = build_ai_prompt(
        species=species,
        breed=breed,
        purpose=purpose,
        sex=sex,
        age_months=age_months,
        age_stage=age_stage,
        weight=estimated_weight,
        target_min=target_min,
        target_ideal=target_ideal,
        bcs=bcs,
        height_cm=height_cm,
        heart_girth_cm=heart_girth_cm,
        body_length_cm=body_length_cm,
        chest_depth_cm=chest_depth_cm,
        rump_width_cm=rump_width_cm,
        cannon_circumference_cm=cannon_circumference_cm,
        selected_color=selected_color,
        selected_face=selected_face,
        selected_horn=selected_horn,
        selected_ear=selected_ear,
        selected_body_build=selected_body_build,
        selected_features=selected_features,
        total_score=total_score,
        category=category,
        health_score=health_score,
        market_score=market_score,
        quant_score=quant_score,
        qualitative_score=qualitative_score,
        qualitative_details=qualitative_details,
        price_per_kg=price_per_kg,
        feed_cost_per_day=feed_cost_per_day,
        notes=notes,
    )

    st.write(
        "Prompt ini bisa disalin ke AI lain agar pengguna mendapat penjelasan lanjutan "
        "berdasarkan hasil penilaian kuantitatif dan kualitatif."
    )

    st.text_area(
        "Prompt siap pakai",
        value=ai_prompt,
        height=520,
    )

    st.download_button(
        label="⬇️ Download Prompt TXT",
        data=ai_prompt.encode("utf-8"),
        file_name="prompt_analisis_ternak.txt",
        mime="text/plain",
        use_container_width=True,
    )


# =========================================================
# GUIDE
# =========================================================

with tab_guide:
    st.subheader("Panduan Penilaian")

    st.markdown(
        """
### 1. Komponen yang dinilai

| Komponen | Maksimum | Makna |
|---|---:|---|
| Bobot vs target bangsa | 20 | Menilai apakah bobot ternak sesuai target jenis/bangsa |
| BCS | 15 | Menilai kondisi tubuh: kurus, ideal, atau terlalu gemuk |
| Rangka dan tinggi | 10 | Menilai kesesuaian tinggi dengan karakter bangsa |
| Proporsi tubuh | 8 | Membandingkan panjang badan dan lingkar dada |
| Kesehatan lapangan | 15 | Menilai tanda kesehatan dasar dari pengamatan |
| Kesiapan pasar | 7 | Menilai kesiapan sesuai tujuan jual, potong, bibit, atau perah |
| Kuantitatif tambahan | 10 | Kedalaman dada, lebar pinggul, dan lingkar tulang kering |
| Kualitatif/fenotipe bangsa | 15 | Warna bulu, wajah, tanduk, telinga, bentuk tubuh, dan ciri khas bangsa |

### 2. Faktor kuantitatif tambahan

| Faktor | Kegunaan praktis |
|---|---|
| Kedalaman dada | Indikasi kapasitas tubuh, volume organ, dan potensi penggemukan/perah |
| Lebar pinggul/panggul | Indikasi rangka belakang, keseimbangan tubuh, dan reproduksi |
| Lingkar tulang kering | Indikasi kasar kekuatan kaki/rangka |
| Rasio terhadap tinggi | Membantu membandingkan ternak kecil dan besar secara lebih adil |

### 3. Faktor kualitatif/fenotipe

| Faktor | Kegunaan praktis |
|---|---|
| Warna bulu | Membantu identifikasi bangsa/persilangan |
| Bentuk wajah | Beberapa bangsa memiliki profil kepala khas |
| Tanduk | Bentuk dan keberadaan tanduk dapat menjadi ciri pembeda |
| Telinga | Penting pada Brahman Cross, PE, Boer, dan beberapa bangsa lain |
| Bentuk tubuh | Membaca tipe pedaging, perah, dwiguna, atau kerja |
| Ciri khas | Punuk, gelambir, ambing, ekor gemuk, paha penuh, punggung lebar, dan lain-lain |

### 4. Kategori hasil

| Skor | Kategori | Arti praktis |
|---:|---|---|
| 85-100 | Sangat Layak | Ternak kuat untuk dipilih/dibeli/dipelihara |
| 70-84 | Layak | Cukup baik, tetap perlu cek harga dan kesehatan |
| 55-69 | Perlu Perbaikan | Perlu pakan, perawatan, atau pemeriksaan tambahan |
| <55 | Risiko Tinggi | Tidak disarankan untuk keputusan besar tanpa pemeriksaan lanjut |

### 5. Cara membaca hasil

- **Peternak**: fokus pada bobot, BCS, kesehatan, target penggemukan, dan biaya pakan.
- **Jagal**: fokus pada karkas, dada, paha, punggung, BCS, dan kesehatan.
- **Blantik**: fokus pada selisih harga, tampilan, bangsa, umur, bobot, dan risiko klaim kualitas.
- **Bibit/perah**: jangan hanya melihat bobot; perhatikan reproduksi, ambing, kaki, dan riwayat produksi.

### 6. Keterbatasan sistem

Aplikasi ini menggunakan estimasi berbasis ukuran tubuh, ciri visual, dan parameter umum. 
Hasil dapat berbeda dengan timbangan aktual, kondisi pasar, kualitas pakan, kesehatan tersembunyi, 
umur sebenarnya, kemurnian bangsa, dan standar lokal masing-masing daerah.
"""
    )

    st.markdown("---")
    st.subheader("Saran Pengembangan Lanjutan")

    st.markdown(
        """
- Tambahkan upload foto ternak untuk dokumentasi visual.
- Tambahkan database online untuk riwayat kandang.
- Tambahkan grafik perkembangan bobot mingguan.
- Tambahkan standar harga lokal berdasarkan wilayah.
- Tambahkan rekomendasi ransum berdasarkan hijauan, konsentrat, dan target ADG.
- Tambahkan mode verifikasi foto dengan catatan manual dari petugas.
- Tambahkan template laporan PDF per ternak.
"""
    )
