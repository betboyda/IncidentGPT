# src/preprocessing.py

from pathlib import Path
from typing import List, Dict


def read_log_file(path: str) -> str:
    """
    Dosya yolundan log dosyasını okur ve tek bir string döndürür.
    """
    return Path(path).read_text(encoding="utf-8")


def parse_log_lines(log_text: str) -> List[Dict]:
    """
    Basit parse:
    - Her dolu satırı bir event sayıyoruz.
    - Şimdilik sadece 'raw' alanı var.
    """
    events: List[Dict] = []

    for line in log_text.splitlines():
        line = line.strip()
        if line == "":
            continue

        events.append({"raw": line})

    return events


def build_log_context_for_llm(log_text: str, max_lines: int = 50) -> str:
    """
    LLM'e gönderilecek metni hazırlar.
    Çok uzunsa ilk max_lines satırı alır.
    """
    cleaned_lines = []
    for line in log_text.splitlines():
        line = line.strip()
        if line != "":
            cleaned_lines.append(line)

    if len(cleaned_lines) > max_lines:
        cleaned_lines = cleaned_lines[:max_lines]

    return "\n".join(cleaned_lines)
