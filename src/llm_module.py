import os
import json

from typing import Dict, Any

from dotenv import load_dotenv

from log_parser import (
    parse_log,
    detect_brute_force
)

# ---------------------------------------------------
# OPENAI
# ---------------------------------------------------

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# ---------------------------------------------------
# GEMINI
# ---------------------------------------------------

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# ---------------------------------------------------
# ENV
# ---------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

if OPENAI_API_KEY and OpenAI:

    openai_client = OpenAI(
        api_key=OPENAI_API_KEY
    )

else:

    openai_client = None

# ---------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------

if GEMINI_API_KEY and genai:

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    gemini_model = genai.GenerativeModel(
        "gemini-pro"
    )

else:

    gemini_model = None

# ---------------------------------------------------
# RULE BASED + GENERIC DETECTION
# ---------------------------------------------------

def _rule_based_analysis(
    log_text: str
):

    text = log_text.lower()

    parsed_logs = parse_log(
        log_text
    )

    brute_force = detect_brute_force(
        parsed_logs
    )

    incident_type = "info_only"

    severity = "low"

    confidence_score = 50

    summary = (
        "Belirgin bir tehdit tespit edilmedi."
    )

    actions = [

        "[Identify] Olayı doğrula.",

        "[Contain] Şüpheli sistemi izole et.",

        "[Eradicate] Zararlı aktiviteyi temizle.",

        "[Recover] Sistemi güvenli şekilde geri yükle.",

        "[Lessons Learned] Güvenlik politikalarını güncelle."
    ]

    # ---------------------------------------------------
    # GENERIC KEYWORDS
    # ---------------------------------------------------

    auth_keywords = [

        "failed",
        "login",
        "authentication",
        "4625",
        "invalid password",
        "unauthorized"
    ]

    malware_keywords = [

        "powershell",
        "encodedcommand",
        ".exe",
        "ransomware",
        "malware",
        "payload"
    ]

    network_keywords = [

        "ddos",
        "flood",
        "traffic spike",
        "syn flood",
        "port scan"
    ]

    phishing_keywords = [

        "phishing",
        "suspicious email",
        "credential",
        "fake login"
    ]

    # ---------------------------------------------------
    # BRUTE FORCE
    # ---------------------------------------------------

    if brute_force:

        top_attack = brute_force[0]

        incident_type = (
            "brute_force_attack"
        )

        severity = "high"

        confidence_score = 92

        summary = (
            f"{top_attack['ip']} adresinden "
            f"{top_attack['attempts']} adet "
            f"başarısız giriş denemesi "
            f"tespit edildi."
        )

    # ---------------------------------------------------
    # AUTH ATTACK
    # ---------------------------------------------------

    elif any(
        keyword in text
        for keyword in auth_keywords
    ):

        incident_type = (
            "authentication_attack"
        )

        severity = "medium"

        confidence_score = 84

        summary = (
            "Kimlik doğrulama ilişkili "
            "şüpheli aktiviteler tespit edildi."
        )

    # ---------------------------------------------------
    # MALWARE
    # ---------------------------------------------------

    elif any(
        keyword in text
        for keyword in malware_keywords
    ):

        incident_type = (
            "malware_activity"
        )

        severity = "high"

        confidence_score = 89

        summary = (
            "Kötü amaçlı yazılım ilişkili "
            "aktiviteler tespit edildi."
        )

    # ---------------------------------------------------
    # NETWORK
    # ---------------------------------------------------

    elif any(
        keyword in text
        for keyword in network_keywords
    ):

        incident_type = (
            "network_attack"
        )

        severity = "high"

        confidence_score = 86

        summary = (
            "Ağ tabanlı saldırı "
            "göstergeleri tespit edildi."
        )

    # ---------------------------------------------------
    # PHISHING
    # ---------------------------------------------------

    elif any(
        keyword in text
        for keyword in phishing_keywords
    ):

        incident_type = (
            "phishing"
        )

        severity = "medium"

        confidence_score = 81

        summary = (
            "Phishing ilişkili "
            "aktiviteler tespit edildi."
        )

    # ---------------------------------------------------
    # GENERIC
    # ---------------------------------------------------

    else:

        incident_type = (
            "suspicious_activity"
        )

        severity = "low"

        confidence_score = 60

        summary = (
            "Yarı-yapısal log içerisinde "
            "şüpheli güvenlik aktiviteleri "
            "tespit edildi."
        )

    return {

        "incident_type": incident_type,

        "severity": severity,

        "confidence_score": confidence_score,

        "summary": summary,

        "actions": actions
    }

# ---------------------------------------------------
# DEFAULTS
# ---------------------------------------------------

def _fill_defaults(
    data: Dict[str, Any],
    multimodal=False
):

    if "incident_type" not in data:

        data["incident_type"] = "unknown"

    if "severity" not in data:

        data["severity"] = "medium"

    if "summary" not in data:

        data["summary"] = ""

    if "actions" not in data:

        data["actions"] = []

    if "confidence_score" not in data:

        data["confidence_score"] = 75

    if multimodal:

        if "diagram_observations" not in data:

            data["diagram_observations"] = []

    return data

# ---------------------------------------------------
# MULTIMODAL
# ---------------------------------------------------

def analyze_multimodal(
    log_text: str,
    ocr_text: str
):

    base = _rule_based_analysis(
        log_text
    )

    findings = []

    if ocr_text.strip():

        findings.append(
            f"OCR ile tespit edilen metin: "
            f"{ocr_text[:250]}"
        )

        lower_ocr = ocr_text.lower()

        if (

            "admin" in lower_ocr
            or "login" in lower_ocr
            or "authentication" in lower_ocr
        ):

            findings.append(
                "Görsel üzerinde authentication ilişkili ifadeler tespit edildi."
            )

        if (

            "firewall" in lower_ocr
            or "alert" in lower_ocr
            or "attack" in lower_ocr
        ):

            findings.append(
                "Görsel üzerinde güvenlik altyapısı ilişkili ifadeler tespit edildi."
            )

    else:

        findings.append(
            "Görsel analiz edildi ancak anlamlı OCR çıktısı elde edilemedi."
        )

    base["diagram_observations"] = findings

    base["model_used"] = (
        "Rule-Based + OCR"
    )

    return base

# ---------------------------------------------------
# TEXT ONLY
# ---------------------------------------------------

def analyze_text_only(
    log_text: str
):

    data = _rule_based_analysis(
        log_text
    )

    data["model_used"] = (
        "Rule-Based"
    )

    return data