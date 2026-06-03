# IncidentGPT

## Hybrid and Multimodal AI-Powered Cyber Incident Response System

IncidentGPT is an experimental cybersecurity incident response platform developed as an undergraduate thesis project at Düzce University.

The system combines Large Language Models (LLMs), OCR-supported visual analysis, structured log parsing, correlation-based attack detection, and rule-based fallback mechanisms to support incident investigation and response activities. The platform is designed to analyze both textual and visual security artifacts within a unified workflow and generate standards-aligned response recommendations.

---

## Key Features

* Hybrid AI architecture (OpenAI, Gemini, and Rule-Based Fallback)
* Multimodal incident analysis (logs and images)
* OCR-supported security data extraction
* Structured log parsing
* Correlation-based brute force detection
* MITRE ATT&CK technique mapping
* Confidence score generation
* NIST SP 800-61 aligned response recommendations
* Incident severity assessment
* Security event classification and reporting

---

## System Architecture

```text
User Interface (Flask)
        │
        ▼
Preprocessing Layer
        │
 ┌──────┴──────┐
 ▼             ▼
Log Parser   OCR Pipeline
 │             │
 └──────┬──────┘
        ▼
 Hybrid Analysis Layer
(OpenAI + Gemini + Fallback)
        │
        ▼
Correlation Engine
        │
        ▼
MITRE ATT&CK Mapping
        │
        ▼
Response Generation
        │
        ▼
Database & Dashboard
```

---

## Technologies

* Python
* Flask
* SQLite
* OpenAI API
* Google Gemini API
* Tesseract OCR
* OpenCV
* Pillow (PIL)
* HTML / CSS / JavaScript
* Chart.js

---

## Research Contributions

This study introduces a hybrid and multimodal incident response framework capable of:

* Processing both textual and visual cybersecurity data
* Performing OCR-assisted security analysis
* Detecting correlation-based attack patterns
* Generating confidence-aware incident assessments
* Mapping incidents to MITRE ATT&CK techniques
* Producing NIST-compliant response recommendations
* Maintaining operational continuity through fallback mechanisms

---

## Academic Information

**Title:** IncidentGPT: Hybrid and Multimodal Artificial Intelligence-Based Cyber Incident Response System


---

## License

This repository is published for academic and educational purposes.
