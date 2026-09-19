# Trade Finance Document Checker (PS072)

An intelligent, multi-stage compliance auditor designed to scan and compare Commercial Invoices, Letters of Credit (LC), and Bills of Lading (BL) under ICC **UCP 600** and **ISBP 821** guidelines.

The pipeline combines deterministic programmatic matching with LLM reasoning:
1. **Extraction (Gemini 2.5 Flash)**: Reads all three PDF documents inside a single API call to extract structured JSON matching a rigorous Pydantic schema.
2. **Deterministic Engine (Python Rules)**: Runs math tolerances, currency matching, date ordering, fuzzy string matching (buyer/seller names, ports) and Incoterms check.
3. **Reasoning Analyst (Groq Llama 4 Maverick)**: Reviews all engine-flagged discrepancy candidates under UCP 600 articles, confirms or dismisses them with clear banking rationale, and issues a final verdict (`COMPLIANT`, `DISCREPANT`, or `CONDITIONAL`).
4. **Visual Dashboard (HTML/CSS/JS)**: An interactive glassmorphic web UI to run verifications, view side-by-side extractions, inspect confirmed/dismissed items, and download PDF or JSON reports.

---

## Project Structure

```
trade-finance-checker/
├── app/
│   ├── main.py                       # FastAPI app server + endpoints
│   ├── gemini_extractor.py           # Gemini 2.5 Flash visual PDF extraction
│   ├── groq_analyst.py               # Groq Llama 4 UCP 600 reasoner
│   ├── engine/
│   │   ├── comparison_engine.py      # Main comparison orchestrator
│   │   ├── models.py                 # DiscrepancyCandidate dataclass
│   │   └── rules/
│   │       ├── amount_rules.py       # Currency checks & amount tolerances
│   │       ├── date_rules.py         # Expiry, shipment limits, presentation risk
│   │       ├── party_rules.py        # RapidFuzz fuzzy party checks
│   │       ├── port_rules.py         # Loading/discharge port validation
│   │       └── incoterm_rules.py     # Incoterms compatibility checks
│   ├── report/
│   │   ├── html_report.py            # Jinja2 HTML report generator
│   │   ├── pdf_report.py             # WeasyPrint PDF compiler with fallback
│   │   └── templates/
│   │       └── report.html           # Print-optimized Jinja2 template
│   └── static/
│       └── index.html                # Gorgeous glassmorphic user dashboard
├── tests/
│   ├── mocks/
│   │   └── extraction_mock.json      # Offline compliant document payload
│   ├── test_engine.py                # Unit tests for comparing rules
│   └── test_end_to_end.py            # FastAPI route tests using mocks
├── .env                              # API keys configuration
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Multi-stage image with WeasyPrint libraries
├── docker-compose.yml                # Docker orchestrator
└── README.md                         # Documentation
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- [Gemini API Key](https://aistudio.google.com/)
- [Groq API Key](https://console.groq.com/)

### Local Setup

1. **Clone and Navigate**:
   ```bash
   cd "c:\Users\ridhi malawade\OneDrive\Desktop\sample 2"
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   > [!NOTE]
   > WeasyPrint requires GTK+ libraries on Windows to compile PDFs. If GTK+ is not present locally, PDF generation will report warnings and direct you to use the HTML print function or run in Docker.

4. **Environment Variables**:
   Configure `.env` with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Start Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Visit `http://localhost:8000` to interact with the dashboard.

---

## Running in Docker (Recommended)

Docker contains all native system dependencies for WeasyPrint pre-installed:

1. Start container:
   ```bash
   docker-compose up --build
   ```

2. Open browser:
   Visit `http://localhost:8000` to run audits.

---

## Running Tests

Tests run automatically using `pytest` and mock extraction schemas:

```bash
pytest tests/
```

---

## API Endpoints

### 1. `POST /check`
Upload the three PDFs to analyze them:
- **Parameters**:
  - `invoice`: File (Commercial Invoice PDF)
  - `lc`: File (Letter of Credit PDF)
  - `bl`: File (Bill of Lading PDF)
  - `output_format`: `json` (default) | `html` | `pdf`
- **Response**: Returns either JSON compliance details, HTML string, or download PDF binary.

### 2. `GET /health`
Returns configuration health check (checks if Gemini and Groq API keys are loaded and if PDF export is active).
