import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json
import os

from app.main import app
from app.gemini_extractor import ExtractionResult

client = TestClient(app)

@pytest.fixture
def mock_extraction_data():
    mock_path = os.path.join(os.path.dirname(__file__), "mocks", "extraction_mock.json")
    with open(mock_path, "r") as f:
        data = json.load(f)
    return ExtractionResult(**data)

@pytest.fixture
def dummy_pdfs():
    # Small valid-ish mock files
    dummy_bytes = b"%PDF-1.4 mock pdf data"
    return {
        "invoice": ("invoice.pdf", dummy_bytes, "application/pdf"),
        "lc": ("lc.pdf", dummy_bytes, "application/pdf"),
        "bl": ("bl.pdf", dummy_bytes, "application/pdf")
    }

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    res_json = response.json()
    assert "status" in res_json
    assert res_json["status"] == "ok"
    assert "configuration" in res_json

@patch("app.main.extract_all_documents")
@patch("app.main.analyze_discrepancies")
@patch.dict(os.environ, {"GEMINI_API_KEY": "fake_gemini_key", "GROQ_API_KEY": "fake_groq_key"})
def test_check_endpoint_json(mock_analyze, mock_extract, mock_extraction_data, dummy_pdfs):
    # Setup mocks
    mock_extract.return_value = mock_extraction_data
    mock_analyze.return_value = {
        "overall_verdict": "COMPLIANT",
        "summary": "Mock audit summary showing compliance.",
        "confirmed_discrepancies": [],
        "dismissed_candidates": [
            {"id": "C006", "reason": "Names match via abbreviation"}
        ],
        "warnings": []
    }
    
    # POST documents
    response = client.post("/check?output_format=json", files=dummy_pdfs)
    
    assert response.status_code == 200
    res_json = response.json()
    
    assert res_json["status"] == "COMPLIANT"
    assert "summary" in res_json
    assert "discrepancies" in res_json
    assert len(res_json["discrepancies"]) == 0
    assert len(res_json["dismissed"]) == 1
    assert res_json["metadata"]["invoice_number"] == "INV-2024-001"

@patch("app.main.extract_all_documents")
@patch("app.main.analyze_discrepancies")
@patch.dict(os.environ, {"GEMINI_API_KEY": "fake_gemini_key", "GROQ_API_KEY": "fake_groq_key"})
def test_check_endpoint_html(mock_analyze, mock_extract, mock_extraction_data, dummy_pdfs):
    # Setup mocks
    mock_extract.return_value = mock_extraction_data
    mock_analyze.return_value = {
        "overall_verdict": "DISCREPANT",
        "summary": "Mock audit summary showing discrepancy.",
        "confirmed_discrepancies": [
            {
                "id": "C001",
                "type": "AMOUNT_OUT_OF_TOLERANCE",
                "severity": "CRITICAL",
                "field_reference": "total_amount",
                "document_a": "120000.0",
                "document_b": "100000.0",
                "ucp_rule": "UCP 600 Art 18",
                "explanation": "Amount exceeds tolerance.",
                "recommended_action": "Request invoice amendment."
            }
        ],
        "dismissed_candidates": [],
        "warnings": []
    }
    
    # POST documents requesting HTML
    response = client.post("/check?output_format=html", files=dummy_pdfs)
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html_content = response.text
    
    # Ensure important HTML sections exist
    assert "Trade Finance Compliance Report" in html_content
    assert "DISCREPANT" in html_content
    assert "C001" in html_content
    assert "AMOUNT_OUT_OF_TOLERANCE" in html_content
    assert "UCP 600 Art 18" in html_content

def test_missing_api_keys(dummy_pdfs):
    # Temporarily remove keys from env
    with patch.dict(os.environ, {"GEMINI_API_KEY": "", "GROQ_API_KEY": ""}):
        response = client.post("/check", files=dummy_pdfs)
        assert response.status_code == 400
        assert "GEMINI_API_KEY" in response.json()["detail"]
