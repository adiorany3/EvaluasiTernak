import math
from datetime import datetime

import pandas as pd
import streamlit as st


# =========================================================
# SISTEM PENILAIAN TERNAK BERBASIS JENIS DAN BANGSA TERNAK
# Streamlit Online App
# =========================================================
# Catatan:
# - Aplikasi ini adalah alat bantu estimasi awal.
# - Hasil bukan pengganti pemeriksaan dokter hewan, ahli nutrisi,
#   petugas teknis, atau penilaian langsung di lapangan.
# - Parameter target dapat disesuaikan dengan kondisi daerah,
#   sistem pemeliharaan, pasar, dan standar internal pengguna.
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


# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def clamp(value, low, high):
    return max(low, min(high, value))


def estimate_weight(species, heart_girth_cm, body_length_cm):
    """
    Estimasi bobot hidup berbasis lingkar dada dan panjang badan.
    Rumus disederhanakan agar mudah digunakan di lapangan.
    """
    formula_type = SPECIES_CONFIG[species]["formula"]

    if formula_type == "large":
        # Umum dipakai untuk sapi/kerbau: LD^2 x PB / 10840
        weight = (heart_girth_cm ** 2 * body_length_cm) / 10840
    else:
        # Pendekatan praktis untuk kambing/domba: LD^2 x PB / 10000
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
    else:
        if age_months < 4:
            return "Cempe/anak"
        if age_months < 10:
            return "Muda/tumbuh"
        if age_months < 24:
            return "Dewasa muda/siap produksi"
        return "Dewasa"


def score_weight(weight, target_min, target_ideal):
    if weight <= 0:
        return 0

    if weight < target_min:
        ratio = weight / target_min
        return round(clamp(ratio * 22, 0, 22), 1)

    if target_min <= weight <= target_ideal:
        ratio = (weight - target_min) / max(target_ideal - target_min, 1)
        return round(22 + ratio * 8, 1)

    # Di atas ideal belum tentu buruk, tetapi bisa terlalu berat/boros pakan.
    excess_ratio = (weight - target_ideal) / target_ideal
    penalty = min(excess_ratio * 10, 5)
    return round(30 - penalty, 1)


def score_bcs(bcs, ideal_low, ideal_high, purpose):
    if ideal_low <= bcs <= ideal_high:
        base = 25
    else:
        distance = min(abs(bcs - ideal_low), abs(bcs - ideal_high))
        base = 25 - distance * 8

    if purpose == "Perah" and bcs > 3.75:
        base -= 2
    if purpose == "Jagal" and bcs < 3.0:
        base -= 3
    if purpose == "Bibit / Breeding" and (bcs < 2.75 or bcs > 4.0):
        base -= 3

    return round(clamp(base, 0, 25), 1)


def score_frame(height_cm, height_min, height_max):
    if height_min <= height_cm <= height_max:
        return 15

    if height_cm < height_min:
        ratio = height_cm / height_min
        return round(clamp(ratio * 13, 0, 13), 1)

    # Tinggi di atas rentang masih bisa baik, tetapi perlu dicek proporsi.
    excess_ratio = (height_cm - height_max) / height_max
    penalty = min(excess_ratio * 8, 3)
    return round(15 - penalty, 1)


def score_proportion(heart_girth_cm, body_length_cm, species):
    if heart_girth_cm <= 0:
        return 0

    proportion = body_length_cm / heart_girth_cm

    if species in ["Sapi Potong", "Sapi Perah", "Kerbau"]:
        low, high = 0.85, 1.18
    else:
        low, high = 0.80, 1.20

    if low <= proportion <= high:
        return 10, proportion

    distance = min(abs(proportion - low), abs(proportion - high))
    score = 10 - distance * 20
    return round(clamp(score, 0, 10), 1), proportion


def score_health(health_checks):
    total = len(health_checks)
    if total == 0:
        return 0
    positive = sum(1 for value in health_checks.values() if value)
    return round((positive / total) * 20, 1)


def score_market_readiness(weight, target_min, bcs, health_score, purpose):
    score = 0

    if weight >= target_min:
        score += 4
    elif weight >= target_min * 0.9:
        score += 3
    elif weight >= target_min * 0.8:
        score += 2
    else:
        score += 1

    if purpose in ["Jagal", "Penggemukan / Potong", "Blantik / Jual Beli"]:
        if 3.0 <= bcs <= 4.0:
            score += 3
        elif 2.5 <= bcs < 3.0 or 4.0 < bcs <= 4.5:
            score += 2
        else:
            score += 1
    else:
        if 2.75 <= bcs <= 3.75:
            score += 3
        else:
            score += 1

    if health_score >= 18:
        score += 3
    elif health_score >= 14:
        score += 2
    else:
        score += 1

    return round(clamp(score, 0, 10), 1)


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


def rupiah(value):
    try:
        return f"Rp{value:,.0f}".replace(",", ".")
    except Exception:
        return "-"


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

    # Insight utama
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
                    f"Ternak masih **perlu perbaikan** sebelum dijadikan pilihan utama. "
                    f"Fokus evaluasi ada pada bobot, BCS, proporsi tubuh, dan kesehatan lapangan."
                ),
            }
        )
    else:
        insights.append(
            {
                "type": "danger",
                "title": "Kesimpulan utama",
                "body": (
                    f"Ternak masuk kategori **risiko tinggi**. Sebaiknya tidak langsung dibeli, "
                    f"dijual sebagai premium, atau dijadikan bibit sebelum dilakukan pemeriksaan lanjutan."
                ),
            }
        )

    # Insight berdasarkan bobot
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

    # Insight BCS
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

    # Insight proporsi
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
                f"Skor rangka/tinggi: **{frame_score}/15**."
            ),
        }
    )

    # Insight kesehatan
    if health_score < 14:
        insights.append(
            {
                "type": "danger",
                "title": "Kesehatan lapangan perlu diperiksa",
                "body": (
                    f"Skor kesehatan hanya **{health_score}/20**. Jangan hanya mengejar bobot. "
                    "Periksa nafsu makan, pernapasan, mata-hidung, feses, pincang, luka, dan tanda parasit."
                ),
            }
        )
    elif health_score < 18:
        insights.append(
            {
                "type": "warning",
                "title": "Kesehatan cukup, tetapi belum optimal",
                "body": (
                    f"Skor kesehatan **{health_score}/20**. Ternak masih bisa dipertimbangkan, "
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
                    f"Skor kesehatan **{health_score}/20**. Kondisi ini mendukung keputusan beli/pelihara, "
                    "selama tidak ada penyakit tersembunyi."
                ),
            }
        )

    # Insight berdasarkan tujuan
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
                    "Ternak yang bobotnya belum mencapai target tetapi rangkanya bagus bisa menarik sebagai bakalan."
                ),
            }
        )
    elif purpose == "Penggemukan / Potong":
        insights.append(
            {
                "type": "info",
                "title": "Insight penggemukan",
                "body": (
                    f"Potensi penggemukan dipengaruhi bangsa {breed}, pakan, kesehatan, dan umur. "
                    f"Asumsi ADG sistem ini: **{adg:.2f} kg/hari**. "
                    "Pilih ternak dengan rangka cukup besar, sehat, dan belum terlalu gemuk."
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
                    "Untuk bibit, prioritaskan kesehatan, struktur kaki, alat reproduksi, riwayat keturunan, "
                    "umur produktif, dan BCS yang tidak terlalu kurus atau terlalu gemuk."
                ),
            }
        )

    # Insight ekonomi sederhana
    if price_per_kg > 0:
        estimated_value = weight * price_per_kg
        carcass_value_basis = (weight * dressing / 100) * price_per_kg

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

    # Catatan bangsa
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
    total_score,
    category,
    health_score,
    market_score,
    price_per_kg,
    feed_cost_per_day,
    notes,
):
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
- Lingkar dada: {heart_girth_cm} cm
- Panjang badan: {body_length_cm} cm
- Tinggi badan: {height_cm} cm
- Estimasi bobot hidup: {weight:.2f} kg
- Target bobot minimum bangsa ini: {target_min} kg
- Target bobot ideal bangsa ini: {target_ideal} kg
- BCS: {bcs}
- Skor kesehatan lapangan: {health_score}/20
- Skor kesiapan pasar: {market_score}/10
- Skor total: {total_score}/100
- Kategori hasil: {category}
- Harga per kg bobot hidup: Rp{price_per_kg:,.0f}
- Biaya pakan per hari: Rp{feed_cost_per_day:,.0f}
- Catatan bangsa: {notes}

TUGAS ANALISIS:
1. Berikan kesimpulan kelayakan ternak.
2. Jelaskan kekuatan dan kelemahannya.
3. Berikan rekomendasi untuk peternak.
4. Berikan insight untuk jagal.
5. Berikan insight untuk blantik ternak.
6. Berikan strategi negosiasi harga yang wajar.
7. Berikan tindakan perbaikan 7-30 hari.
8. Jelaskan risiko yang harus diperiksa langsung di lapangan.

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
st.sidebar.caption("Berbasis jenis, bangsa, bobot estimasi, BCS, kesehatan, dan tujuan pasar.")

with st.sidebar.expander("Cara pakai singkat", expanded=True):
    st.write(
        """
1. Pilih jenis dan bangsa ternak.  
2. Masukkan umur, ukuran tubuh, BCS, dan kesehatan.  
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

st.title("🐄 Sistem Penilaian Ternak dan Evaluasi Berbasis Jenis & Bangsa")
st.caption(
    "Aplikasi Streamlit untuk membantu peternak, jagal, dan blantik menilai kelayakan ternak secara lebih sistematis."
)


# =========================================================
# INPUT AREA
# =========================================================

tab_input, tab_result, tab_compare, tab_prompt, tab_guide = st.tabs(
    [
        "📝 Input Penilaian",
        "📊 Hasil & Insight",
        "📋 Tabel Evaluasi",
        "🤖 Prompt AI",
        "📘 Panduan",
    ]
)


with tab_input:
    st.subheader("Input Data Ternak")

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
    st.subheader("Ukuran Tubuh")

    breed_info = BREED_DATA[species][breed]

    default_weight = breed_info["target_market_min"]
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

total_score = round(
    weight_score
    + bcs_score
    + frame_score
    + prop_score
    + health_score
    + market_score,
    1,
)

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
            ["Bobot vs target bangsa", weight_score, 30],
            ["BCS / kondisi tubuh", bcs_score, 25],
            ["Rangka dan tinggi", frame_score, 15],
            ["Proporsi tubuh", prop_score, 10],
            ["Kesehatan lapangan", health_score, 20],
            ["Kesiapan pasar", market_score, 10],
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
Indeks proporsi: {proportion:.2f}
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
                "Estimasi Bobot kg": estimated_weight,
                "BCS": bcs,
                "Skor Bobot": weight_score,
                "Skor BCS": bcs_score,
                "Skor Rangka": frame_score,
                "Skor Proporsi": prop_score,
                "Skor Kesehatan": health_score,
                "Skor Pasar": market_score,
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
        total_score=total_score,
        category=category,
        health_score=health_score,
        market_score=market_score,
        price_per_kg=price_per_kg,
        feed_cost_per_day=feed_cost_per_day,
        notes=notes,
    )

    st.write(
        "Prompt ini bisa disalin ke AI lain agar pengguna mendapat penjelasan lanjutan "
        "berdasarkan hasil penilaian."
    )

    st.text_area(
        "Prompt siap pakai",
        value=ai_prompt,
        height=420,
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
| Bobot vs target bangsa | 30 | Menilai apakah bobot ternak sesuai target jenis/bangsa |
| BCS | 25 | Menilai kondisi tubuh: kurus, ideal, atau terlalu gemuk |
| Rangka dan tinggi | 15 | Menilai kesesuaian tinggi dengan karakter bangsa |
| Proporsi tubuh | 10 | Membandingkan panjang badan dan lingkar dada |
| Kesehatan lapangan | 20 | Menilai tanda kesehatan dasar dari pengamatan |
| Kesiapan pasar | 10 | Menilai kesiapan sesuai tujuan jual, potong, bibit, atau perah |

### 2. Kategori hasil

| Skor | Kategori | Arti praktis |
|---:|---|---|
| 85-100 | Sangat Layak | Ternak kuat untuk dipilih/dibeli/dipelihara |
| 70-84 | Layak | Cukup baik, tetap perlu cek harga dan kesehatan |
| 55-69 | Perlu Perbaikan | Perlu pakan, perawatan, atau pemeriksaan tambahan |
| <55 | Risiko Tinggi | Tidak disarankan untuk keputusan besar tanpa pemeriksaan lanjut |

### 3. Cara membaca insight

- **Peternak**: fokus pada pakan, kesehatan, BCS, dan target bobot.
- **Jagal**: fokus pada karkas, kondisi daging, paha, dada, punggung, dan kesehatan.
- **Blantik**: fokus pada selisih harga, potensi naik bobot, tampilan, bangsa, dan risiko transaksi.
- **Bibit/perah**: jangan hanya melihat bobot; perhatikan reproduksi, ambing, kaki, dan riwayat produksi.

### 4. Keterbatasan sistem

Aplikasi ini menggunakan estimasi berbasis ukuran tubuh dan parameter umum. 
Hasil dapat berbeda dengan timbangan aktual, kondisi pasar, kualitas pakan, kesehatan tersembunyi, 
dan standar lokal masing-masing daerah.
"""
    )

    st.markdown("---")
    st.subheader("Saran Pengembangan Lanjutan")

    st.markdown(
        """
- Tambahkan login admin dan database online.
- Tambahkan upload foto ternak untuk dokumentasi.
- Tambahkan grafik perkembangan bobot per minggu.
- Tambahkan mode kandang kolektif untuk membandingkan banyak ternak.
- Tambahkan standar harga lokal berdasarkan wilayah.
- Tambahkan rekomendasi ransum berdasarkan hijauan, konsentrat, dan target ADG.
"""
    )
