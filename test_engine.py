import pytest
import json
import os
from app.engine.comparison_engine import ComparisonEngine

@pytest.fixture
def base_data():
    mock_path = os.path.join(os.path.dirname(__file__), "mocks", "extraction_mock.json")
    with open(mock_path, "r") as f:
        return json.load(f)

def test_compliant_package(base_data):
    engine = ComparisonEngine()
    # If we adjust names to match exactly to avoid any engine candidates:
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    invoice["seller_name"] = "ACME TRADING CO. LTD"
    lc["beneficiary_name"] = "ACME TRADING CO. LTD"
    bl["shipper_name"] = "ACME TRADING CO. LTD"
    
    candidates = engine.run(invoice, lc, bl)
    
    # Assert no major discrepancies generated
    discrepancy_types = [c.type for c in candidates]
    assert "AMOUNT_OUT_OF_TOLERANCE" not in discrepancy_types
    assert "CURRENCY_MISMATCH" not in discrepancy_types
    assert "LATE_SHIPMENT" not in discrepancy_types
    assert "INVOICE_AFTER_EXPIRY" not in discrepancy_types
    assert "PORT_MISMATCH" not in discrepancy_types
    assert "INCOTERMS_MISMATCH" not in discrepancy_types

def test_amount_out_of_tolerance(base_data):
    engine = ComparisonEngine()
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    # LC amount is 100k, 10% tolerance = range [90k - 110k]
    # Set invoice amount to 115k (exceeds upper limit)
    invoice["total_amount"] = 115000.0
    
    candidates = engine.run(invoice, lc, bl)
    discrepancy_types = [c.type for c in candidates]
    assert "AMOUNT_OUT_OF_TOLERANCE" in discrepancy_types

def test_currency_mismatch(base_data):
    engine = ComparisonEngine()
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    invoice["currency"] = "EUR"
    
    candidates = engine.run(invoice, lc, bl)
    discrepancy_types = [c.type for c in candidates]
    assert "CURRENCY_MISMATCH" in discrepancy_types

def test_late_shipment(base_data):
    engine = ComparisonEngine()
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    # LC latest shipment: 2024-11-15. Set BL onboard date: 2024-11-20 (late!)
    bl["onboard_date"] = "2024-11-20"
    
    candidates = engine.run(invoice, lc, bl)
    discrepancy_types = [c.type for c in candidates]
    assert "LATE_SHIPMENT" in discrepancy_types

def test_invoice_after_expiry(base_data):
    engine = ComparisonEngine()
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    # LC expiry date: 2024-11-30. Set invoice date: 2024-12-05 (expired!)
    invoice["invoice_date"] = "2024-12-05"
    
    candidates = engine.run(invoice, lc, bl)
    discrepancy_types = [c.type for c in candidates]
    assert "INVOICE_AFTER_EXPIRY" in discrepancy_types

def test_port_mismatch(base_data):
    engine = ComparisonEngine()
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    # LC port of discharge: "PORT OF HAMBURG". BL: "PORT OF ROTTERDAM"
    bl["port_of_discharge"] = "PORT OF ROTTERDAM"
    
    candidates = engine.run(invoice, lc, bl)
    discrepancy_types = [c.type for c in candidates]
    assert "PORT_MISMATCH" in discrepancy_types

def test_incoterms_mismatch(base_data):
    engine = ComparisonEngine()
    invoice = base_data["invoice"].copy()
    lc = base_data["lc"].copy()
    bl = base_data["bl"].copy()
    
    # Invoice incoterms: "FOB". LC: "CIF"
    invoice["incoterms"] = "CIF"
    lc["incoterms"] = "FOB"
    
    candidates = engine.run(invoice, lc, bl)
    discrepancy_types = [c.type for c in candidates]
    assert "INCOTERMS_MISMATCH" in discrepancy_types
