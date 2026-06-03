# IncidentGPT

## Hybrid and Multimodal AI-Powered Cyber Incident Response System

IncidentGPT is a hybrid and multimodal cybersecurity incident response platform developed as an undergraduate thesis project at Düzce University.

The system combines Large Language Models (LLMs), OCR-based visual analysis, structured log parsing, correlation-based attack detection, and rule-based fallback mechanisms to assist security analysts in incident investigation and response processes.

---

## Key Features

### AI-Powered Incident Analysis

* Security log analysis using Large Language Models
* Context-aware incident classification
* Incident severity assessment
* Automated incident summaries

### Multimodal Security Analysis

* Analysis of both textual and visual security data
* OCR-supported image processing pipeline
* Security dashboard and screenshot interpretation
* Context extraction from visual evidence

### Hybrid AI Architecture

* OpenAI integration for text-based analysis
* Google Gemini integration for multimodal analysis
* Rule-based fallback engine for service failures
* Fault-tolerant architecture

### Security Analytics

* Structured log parsing
* Correlation-based brute force detection
* Authentication attack identification
* Phishing detection
* Malware activity classification
* DDoS activity analysis

### Threat Intelligence Mapping

* MITRE ATT&CK technique mapping
* Confidence score generation
* NIST SP 800-61 compliant response recommendations

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
MITRE Mapping & Response Generation
        │
        ▼
SQLite Database & Dashboard
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
* HTML/CSS/JavaScript
* Chart.js

---

## Installation

```bash
git clone https://github.com/betboyda/IncidentGPT.git
cd IncidentGPT

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Run the application:

```bash
python app.py
```

---

## Research Contributions

* Hybrid LLM architecture with fallback support
* OCR-enhanced multimodal incident analysis
* Correlation-based brute force detection
* Confidence score generation for explainable analysis
* MITRE ATT&CK mapping integration
* NIST-aligned response generation

---

## Author

**Ayşe Betül Boydaş**

Department of Computer Engineering
Düzce University

Supervisor: **Dr. Ahmet Albayrak**

---

## Academic Information

This project was developed as a Graduation Thesis (BM498) in the Department of Computer Engineering at Düzce University during the 2025–2026 academic year.
# IncidentGPT

## Hybrid and Multimodal AI-Powered Cyber Incident Response System

IncidentGPT is a hybrid and multimodal cybersecurity incident response platform developed as an undergraduate thesis project at Düzce University.

The system combines Large Language Models (LLMs), OCR-based visual analysis, structured log parsing, correlation-based attack detection, and rule-based fallback mechanisms to assist security analysts in incident investigation and response processes.

---

## Key Features

### AI-Powered Incident Analysis

* Security log analysis using Large Language Models
* Context-aware incident classification
* Incident severity assessment
* Automated incident summaries

### Multimodal Security Analysis

* Analysis of both textual and visual security data
* OCR-supported image processing pipeline
* Security dashboard and screenshot interpretation
* Context extraction from visual evidence

### Hybrid AI Architecture

* OpenAI integration for text-based analysis
* Google Gemini integration for multimodal analysis
* Rule-based fallback engine for service failures
* Fault-tolerant architecture

### Security Analytics

* Structured log parsing
* Correlation-based brute force detection
* Authentication attack identification
* Phishing detection
* Malware activity classification
* DDoS activity analysis

### Threat Intelligence Mapping

* MITRE ATT&CK technique mapping
* Confidence score generation
* NIST SP 800-61 compliant response recommendations

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
MITRE Mapping & Response Generation
        │
        ▼
SQLite Database & Dashboard
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
* HTML/CSS/JavaScript
* Chart.js

---

## Installation

```bash
git clone https://github.com/betboyda/IncidentGPT.git
cd IncidentGPT

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Run the application:

```bash
python app.py
```

---

## Research Contributions

* Hybrid LLM architecture with fallback support
* OCR-enhanced multimodal incident analysis
* Correlation-based brute force detection
* Confidence score generation for explainable analysis
* MITRE ATT&CK mapping integration
* NIST-aligned response generation

---


---

## Academic Information

This project was developed as a Graduation Thesis (BM498) in the Department of Computer Engineering at Düzce University during the 2025–2026 academic year.
