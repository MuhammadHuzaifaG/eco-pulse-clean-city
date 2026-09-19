# EcoPulse : Urban Intelligence and Public Preparedness API

EcoPulse is an automated urban intelligence API and public safety pipeline designed to ingest unstructured citizen incident reports, classify environmental hazards using zero-shot natural language processing, and generate location-specific emergency advisories in real time.

---

## 1. Main Challenge and Track Alignment

### Main Challenge

Metropolitan areas face severe environmental and infrastructural challenges, including toxic seasonal smog, municipal waste accumulation, water contamination, and traffic noise. Citizen reports regarding these hazards are typically received as unstructured text via various public channels. Municipal bodies often lack automated pipelines to rapidly categorize these reports, evaluate threat severity, and broadcast actionable public safety guidance to affected communities.

### Track Alignment

This project aligns directly with the **AI-Supported Assessment and Resilience Informatics** track. By leveraging machine learning models for real-time text classification and natural language generation, the system automates the processing of public reports and accelerates municipal hazard response.

---

## 2. Project Description

### Problem Statement

Unstructured complaints submitted by citizens require manual review, causing delays in identifying localized environmental risks. Without immediate severity scoring and rapid public communication, citizens remain exposed to environmental hazards such as severe air quality drops or contaminated water lines before official municipal interventions occur.

### Solution Overview

EcoPulse implements an asynchronous RESTful API built with FastAPI that processes raw text input from citizen submissions. The backend routes incoming text through a two-stage artificial intelligence model pipeline:

1. **Zero-Shot Classification:** Categorizes the text into one of five predefined urban hazard classes and calculates a severity score based on label confidence.
2. **Generative Advisory Pipeline:** Consumes the classification data and severity score to construct a 3-sentence public safety advisory for local residents.

### Target Users

* **Municipal Operations Centers:** Environmental protection departments and emergency management personnel who require structured data to prioritize field responses.
* **Urban Planners and Analysts:** Municipal teams tracking localized incident frequency across urban sectors.
* **Local Residents:** Citizens receiving automated, immediate public preparedness guidance based on confirmed neighborhood reports.

### Impact and Scalability

By automating the report triage process, the system reduces the time required to generate public advisories from hours to seconds. The modular architecture permits straightforward deployment across other metropolitan regions by updating localized geographical parameters and target category definitions without requiring model retraining.

---

## 3. Technology and Innovation Component

### Architecture and AI Integration

The solution uses two distinct cloud-hosted language models to separate risk assessment from public communication generation:

1. **Classification Engine (Hugging Face Inference API):**
* **Model:** `facebook/bart-large-mnli`
* **Method:** Zero-shot sequence classification.
* **Candidate Labels:** `Air Pollution / Smog`, `Waste Management`, `Water Quality`, `Infrastructure Damage`, `Traffic / Noise`.
* **Rationale:** Zero-shot classification eliminates the need for expensive domain-specific training data while maintaining high precision across diverse phrasing styles in citizen complaints.


2. **Public Preparedness Engine (OpenAI API):**
* **Model:** `gpt-3.5-turbo`
* **Method:** Parameterized system prompting based on classification output and severity metrics.
* **Rationale:** Formulates clear, professional, context-aware 3-sentence public broadcast advisories formatted for immediate distribution.


3. **Asynchronous Execution:**
* Built on `FastAPI` and `httpx.AsyncClient` with automated transport retries to handle external API rate limits and network latency gracefully.



---

## 4. Key Results and Proof of Concept

The functional prototype delivers an end-to-end processing pipeline verified through integration testing:

* **Endpoint `/api/v1/analyze-report`:** Accepts raw text complaints and returns structured JSON responses containing top-label predictions, confidence scores, computed severity percentages, and generated advisory text.
* **Static Dashboard Interface:** A responsive browser dashboard served directly from the FastAPI application allows users to submit reports, inspect raw API JSON outputs, and view live system status.
* **Health Check Endpoint `/health`:** Reports active service status and verifies the presence of configured API authentication tokens.

---

## 5. Tech Stack

* **Backend Framework:** Python 3.12, FastAPI, Uvicorn
* **HTTP Client:** HTTPX (Async HTTP transport)
* **Configuration & Validation:** Pydantic, Pydantic-Settings, Python-Dotenv
* **External APIs:** Hugging Face Inference API, OpenAI Chat Completions API
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (served via FastAPI StaticFiles)

---

## 6. Prerequisites

* Python 3.10 or higher
* Active OpenAI API Key (`OPENAI_API_KEY`)
* Active Hugging Face User Access Token (`HUGGINGFACE_API_KEY`)

---

## 7. Local Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/eco-pulse.git
cd eco-pulse

```

### Step 2: Create and Activate Virtual Environment

**On Windows:**

```cmd
python -m venv backend/venv
backend\venv\Scripts\activate

```

**On Linux / macOS:**

```bash
python3 -m venv backend/venv
source backend/venv/bin/activate

```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt

```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory (`eco-pulse/.env`):

```env
PROJECT_NAME="Smart City : Urban Intelligence API"
VERSION="1.0.0"
API_PREFIX="/api/v1"

OPENAI_API_KEY="your_openai_api_key_here"
HUGGINGFACE_API_KEY="your_huggingface_api_key_here"

```

### Step 5: Start the Application

From the `backend` directory, run:

```bash
python main.py

```

Alternatively, launch via Uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```

### Step 6: Access the Application

* **Dashboard Interface:** `[http://127.0.0.1:8000/](http://127.0.0.1:8000/)`
* **Interactive API Documentation (Swagger UI):** `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`
* **Health Status:** `[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)`

---

## 8. Project Structure

```text
eco-pulse/
├── .env                    # System environment configuration
├── README.md               # Technical project documentation
├── backend/
│   ├── main.py             # FastAPI app initialization and static mounts
│   ├── config.py           # Pydantic configuration settings
│   ├── requirements.txt    # Python package dependencies
│   ├── api/
│   │   └── routes.py       # API route definitions and request handlers
│   └── services/
│       ├── huggingface_service.py # Zero-shot NLP classification logic
│       └── openai_service.py      # LLM advisory generation logic
└── frontend/
    ├── index.html          # Web dashboard layout
    ├── css/
    │   └── styles.css      # Dashboard styling
    └── js/
        └── app.js          # Dashboard API interaction logic

```
