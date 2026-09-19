"""
Synthetic Trade Finance Document Generator
Produces realistic PDF test sets for the LC Document Checker.
Each set contains: Commercial Invoice + Letter of Credit + Bill of Lading.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

# Compute paths relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DOCS_DIR = os.path.join(BASE_DIR, "tests", "sample_docs")

SET01_DIR = os.path.join(SAMPLE_DOCS_DIR, "set_01_clean")
SET02_DIR = os.path.join(SAMPLE_DOCS_DIR, "set_02_amount_error")
SET03_DIR = os.path.join(SAMPLE_DOCS_DIR, "set_03_date_error")

# Ensure directories exist
os.makedirs(SET01_DIR, exist_ok=True)
os.makedirs(SET02_DIR, exist_ok=True)
os.makedirs(SET03_DIR, exist_ok=True)

styles = getSampleStyleSheet()

def H1(text):
    return Paragraph(f"<b>{text}</b>", ParagraphStyle('h1', fontSize=14, spaceAfter=4, alignment=TA_CENTER))

def H2(text):
    return Paragraph(f"<b>{text}</b>", ParagraphStyle('h2', fontSize=11, spaceAfter=3))

def Body(text):
    return Paragraph(text, ParagraphStyle('body', fontSize=9, spaceAfter=2))

def Bold(text):
    return Paragraph(f"<b>{text}</b>", ParagraphStyle('bold', fontSize=9, spaceAfter=2))

def kv_table(rows, col_widths=None):
    """Two-column key-value table."""
    cw = col_widths or [6*cm, 11*cm]
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.whitesmoke, colors.white]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return t

def goods_table(headers, rows):
    data = [headers] + rows
    t = Table(data, colWidths=[7*cm, 2.5*cm, 1.8*cm, 2.5*cm, 3*cm])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2C5F8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F8FB')]),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return t

def divider():
    return HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=6, spaceBefore=6)

# ─────────────────────────────────────────────
# DOCUMENT SET 01 — FULLY COMPLIANT
# ─────────────────────────────────────────────

def set01_invoice():
    doc = SimpleDocTemplate(os.path.join(SET01_DIR, "invoice.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("COMMERCIAL INVOICE"))
    story.append(Spacer(1, 4))
    story.append(kv_table([
        ["Seller / Exporter:", "GLOBAL TEXTILE EXPORTS PTE. LTD.\n18 Raffles Quay, Singapore 048583\nTel: +65 6221 4400"],
        ["Buyer / Consignee:", "NEXUS FASHION GROUP GMBH\nKaiserstrasse 88, 60329 Frankfurt am Main, Germany"],
        ["Invoice Number:", "GTE-2024-11042"],
        ["Invoice Date:", "20 November 2024"],
        ["LC Reference:", "LC-FRK-2024-008817"],
        ["Incoterms:", "CIF Hamburg"],
        ["Payment Terms:", "Irrevocable Letter of Credit at Sight"],
        ["Country of Origin:", "Singapore"],
        ["Currency:", "USD – United States Dollar"],
    ]))
    story.append(Spacer(1, 8))
    story.append(H2("GOODS DESCRIPTION"))
    story.append(goods_table(
        ["Description", "HS Code", "Qty", "Unit Price (USD)", "Line Total (USD)"],
        [
            ["Premium Cotton Fabric Roll, 180gsm, Ivory", "5208.31", "2,000 m", "12.50", "25,000.00"],
            ["Stretch Denim Fabric Roll, 320gsm, Indigo", "5209.42", "1,500 m", "18.00", "27,000.00"],
            ["Silk Blend Fabric Roll, 95gsm, Ecru", "5007.20", "500 m", "48.00", "24,000.00"],
        ]
    ))
    story.append(Spacer(1, 6))
    story.append(kv_table([
        ["Subtotal:", "USD 76,000.00"],
        ["Freight (CIF):", "USD 3,200.00"],
        ["Insurance:", "USD 800.00"],
        ["TOTAL AMOUNT:", "USD 80,000.00"],
    ]))
    story.append(divider())
    story.append(Body("This invoice is true and correct. Goods are of Singapore origin and comply with all applicable regulations."))
    story.append(Spacer(1, 8))
    story.append(Body("Authorised Signatory: _________________________    Stamp: [COMPANY SEAL]"))
    doc.build(story)
    print("  [OK] set01: invoice.pdf")

def set01_lc():
    doc = SimpleDocTemplate(os.path.join(SET01_DIR, "lc.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("IRREVOCABLE DOCUMENTARY LETTER OF CREDIT"))
    story.append(Body("SWIFT MT700 — Documentary Credit"))
    story.append(divider())
    story.append(kv_table([
        ["Issuing Bank:", "DEUTSCHE HANDELSBANK AG\nFrankfurter Allee 100, 60314 Frankfurt, Germany\nSWIFT: DTHBDEFF"],
        ["LC Number:", "LC-FRK-2024-008817"],
        ["Date of Issue:", "01 November 2024"],
        ["Date of Expiry:", "31 December 2024"],
        ["Place of Expiry:", "Singapore"],
        ["Applicant:", "NEXUS FASHION GROUP GMBH\nKaiserstrasse 88, 60329 Frankfurt am Main, Germany"],
        ["Beneficiary:", "GLOBAL TEXTILE EXPORTS PTE. LTD.\n18 Raffles Quay, Singapore 048583"],
        ["Amount:", "USD 80,000.00 (EIGHTY THOUSAND US DOLLARS)"],
        ["Tolerance:", "+/- 10 percent"],
        ["Available With:", "Any bank by negotiation"],
        ["Tenor:", "At Sight"],
        ["Latest Shipment Date:", "25 November 2024"],
        ["Presentation Period:", "21 days after date of shipment"],
        ["Port of Loading:", "Port of Singapore"],
        ["Port of Discharge:", "Port of Hamburg, Germany"],
        ["Incoterms:", "CIF Hamburg (Incoterms 2020)"],
        ["Partial Shipment:", "NOT ALLOWED"],
        ["Transhipment:", "ALLOWED"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("GOODS DESCRIPTION"))
    story.append(Body("Textile Fabrics — Cotton, Denim, and Silk Blend Rolls of Singapore origin as per Proforma Invoice No. GTE-2024-PI-1104 dated October 2024."))
    story.append(Spacer(1, 6))
    story.append(H2("REQUIRED DOCUMENTS"))
    story.append(Body("1. Signed Commercial Invoice in triplicate\n2. Full set (3/3) Original Clean On-Board Bills of Lading made out to Order of Deutsche Handelsbank AG, notify Nexus Fashion Group GmbH\n3. Packing List in duplicate\n4. Insurance Certificate for 110% of invoice value covering all risks\n5. Certificate of Origin issued by Singapore Customs"))
    story.append(divider())
    story.append(Body("This credit is subject to UCP 600 (ICC Publication No. 600). All documents must be presented within the presentation period."))
    doc.build(story)
    print("  [OK] set01: lc.pdf")

def set01_bl():
    doc = SimpleDocTemplate(os.path.join(SET01_DIR, "bl.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("BILL OF LADING"))
    story.append(Body("ORIGINAL — NEGOTIABLE"))
    story.append(divider())
    story.append(kv_table([
        ["BL Number:", "SINHAM-2024-BL-77341"],
        ["Carrier:", "OCEAN FREIGHT CARRIERS (OFC) PTE. LTD."],
        ["Shipper:", "GLOBAL TEXTILE EXPORTS PTE. LTD.\n18 Raffles Quay, Singapore 048583"],
        ["Consignee:", "TO THE ORDER OF DEUTSCHE HANDELSBANK AG"],
        ["Notify Party:", "NEXUS FASHION GROUP GMBH\nKaiserstrasse 88, 60329 Frankfurt am Main, Germany"],
        ["Vessel Name / Voyage:", "MV PACIFIC TRADER / VOY 224W"],
        ["Port of Loading:", "PORT OF SINGAPORE"],
        ["Port of Discharge:", "PORT OF HAMBURG, GERMANY"],
        ["Place of Receipt:", "Singapore"],
        ["Place of Delivery:", "Hamburg CFS"],
        ["On Board Date:", "22 November 2024"],
        ["Freight Terms:", "FREIGHT PREPAID"],
        ["Number of Originals:", "THREE (3/3)"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("DESCRIPTION OF GOODS"))
    story.append(kv_table([
        ["Container No.:", "TCKU3456781 / Seal: OFC-882341"],
        ["Goods Description:", "Textile Fabric Rolls — Cotton, Denim and Silk Blend\nCountry of Origin: Singapore"],
        ["Gross Weight:", "4,200 KGS"],
        ["Measurement:", "18.5 CBM"],
        ["Packages:", "45 Rolls on 9 Pallets"],
    ]))
    story.append(divider())
    story.append(Body("SHIPPED ON BOARD in apparent good order and condition. This Bill of Lading is issued in THREE (3) originals, one of which being accomplished, the others to stand void."))
    story.append(Spacer(1, 8))
    story.append(Body("For: OCEAN FREIGHT CARRIERS (OFC) PTE. LTD.\nSignature: _________________________    Date: 22 November 2024"))
    doc.build(story)
    print("  [OK] set01: bl.pdf")


# ─────────────────────────────────────────────
# DOCUMENT SET 02 — AMOUNT EXCEEDED + CURRENCY MISMATCH
# ─────────────────────────────────────────────

def set02_invoice():
    doc = SimpleDocTemplate(os.path.join(SET02_DIR, "invoice.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("COMMERCIAL INVOICE"))
    story.append(kv_table([
        ["Seller:", "AGRO COMMODITIES EXPORT LTD.\nMumbai Port Industrial Zone, Maharashtra 400001, India"],
        ["Buyer:", "AL-BARAKA TRADING COMPANY LLC\nJebel Ali Free Zone, Dubai, UAE"],
        ["Invoice Number:", "ACE-INV-2024-0392"],
        ["Invoice Date:", "10 November 2024"],
        ["LC Reference:", "LC-DXB-2024-44219"],
        ["Incoterms:", "FOB Mumbai"],
        ["Payment Terms:", "Letter of Credit at Sight"],
        ["Currency:", "EUR – Euro"],  # DISCREPANCY: LC is in USD
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("GOODS DESCRIPTION"))
    story.append(goods_table(
        ["Description", "HS Code", "Qty (MT)", "Price/MT (EUR)", "Total (EUR)"],
        [
            ["Basmati Rice, Grade A, 5% Broken", "1006.30", "200", "1,100.00", "220,000.00"],
            ["Parboiled Rice, Long Grain", "1006.30", "100", "850.00", "85,000.00"],
        ]
    ))
    story.append(Spacer(1, 6))
    story.append(kv_table([
        ["TOTAL AMOUNT:", "EUR 305,000.00"],  # DISCREPANCY: LC amount is USD 250,000
    ]))
    story.append(divider())
    story.append(Body("Goods packed in 50KG polypropylene bags, 6,000 bags total. Fumigated and phytosanitary certified."))
    doc.build(story)
    print("  [OK] set02: invoice.pdf")

def set02_lc():
    doc = SimpleDocTemplate(os.path.join(SET02_DIR, "lc.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("IRREVOCABLE DOCUMENTARY LETTER OF CREDIT"))
    story.append(divider())
    story.append(kv_table([
        ["Issuing Bank:", "EMIRATES NBD BANK PJSC\nBur Dubai Branch, Dubai, UAE\nSWIFT: EBILAEAD"],
        ["LC Number:", "LC-DXB-2024-44219"],
        ["Date of Issue:", "20 October 2024"],
        ["Date of Expiry:", "30 November 2024"],
        ["Applicant:", "AL-BARAKA TRADING COMPANY LLC\nJebel Ali Free Zone, Dubai, UAE"],
        ["Beneficiary:", "AGRO COMMODITIES EXPORT LTD.\nMumbai Port Industrial Zone, Maharashtra 400001, India"],
        ["Amount:", "USD 250,000.00 (TWO HUNDRED AND FIFTY THOUSAND US DOLLARS)"],  # USD not EUR
        ["Tolerance:", "+/- 5 percent"],
        ["Latest Shipment Date:", "20 November 2024"],
        ["Presentation Period:", "21 days"],
        ["Port of Loading:", "PORT OF MUMBAI, INDIA"],
        ["Port of Discharge:", "PORT OF JEBEL ALI, UAE"],
        ["Incoterms:", "FOB Mumbai Port (Incoterms 2020)"],
        ["Partial Shipment:", "NOT ALLOWED"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("GOODS DESCRIPTION"))
    story.append(Body("Rice — Basmati and Parboiled Long Grain varieties, Indian origin, as per sales contract SC-2024-887."))
    doc.build(story)
    print("  [OK] set02: lc.pdf")

def set02_bl():
    doc = SimpleDocTemplate(os.path.join(SET02_DIR, "bl.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("BILL OF LADING"))
    story.append(Body("ORIGINAL — NEGOTIABLE"))
    story.append(divider())
    story.append(kv_table([
        ["BL Number:", "BOMJAL-2024-BL-29918"],
        ["Carrier:", "INDIA SHIPPING CORPORATION LTD."],
        ["Shipper:", "AGRO COMMODITIES EXPORT LTD., MUMBAI"],
        ["Consignee:", "TO THE ORDER OF EMIRATES NBD BANK PJSC"],
        ["Notify Party:", "AL-BARAKA TRADING COMPANY LLC, DUBAI"],
        ["Vessel / Voyage:", "MV ARABIAN STAR / VOY 089E"],
        ["Port of Loading:", "PORT OF MUMBAI, INDIA"],
        ["Port of Discharge:", "PORT OF JEBEL ALI, UAE"],
        ["On Board Date:", "15 November 2024"],
        ["Freight Terms:", "FREIGHT COLLECT"],
        ["Number of Originals:", "THREE (3/3)"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("DESCRIPTION OF GOODS"))
    story.append(kv_table([
        ["Goods:", "Rice in 50KG Polypropylene Bags — 6,000 Bags"],
        ["Gross Weight:", "300,000 KGS"],
        ["Container:", "MSCU8812340 / Seal: ISC-441290"],
    ]))
    story.append(divider())
    story.append(Body("SHIPPED ON BOARD in apparent good order and condition."))
    doc.build(story)
    print("  [OK] set02: bl.pdf")


# ─────────────────────────────────────────────
# DOCUMENT SET 03 — LATE SHIPMENT + PARTY MISMATCH
# ─────────────────────────────────────────────

def set03_invoice():
    doc = SimpleDocTemplate(os.path.join(SET03_DIR, "invoice.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("COMMERCIAL INVOICE"))
    story.append(kv_table([
        ["Seller:", "SHENZHEN ELECTRONICS MANUFACTURING CO., LTD.\nShenzhen Export Processing Zone, Guangdong, China"],
        ["Buyer:", "EURO TECH DISTRIBUTORS B.V.\nAmsterdamseweg 99, 1182 HG Amstelveen, Netherlands"],
        ["Invoice Number:", "SEM-2024-EUR-7721"],
        ["Invoice Date:", "02 December 2024"],
        ["LC Reference:", "LC-AMS-2024-00531"],
        ["Incoterms:", "CIF Rotterdam"],
        ["Currency:", "USD"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("GOODS DESCRIPTION"))
    story.append(goods_table(
        ["Description", "HS Code", "Qty", "Unit (USD)", "Total (USD)"],
        [
            ["LED Smart TV 55 inch 4K UHD", "8528.72", "500 units", "320.00", "160,000.00"],
            ["Wireless Bluetooth Headphones", "8518.30", "2,000 units", "45.00", "90,000.00"],
            ["USB-C Charging Hub 7-Port", "8504.40", "3,000 units", "18.50", "55,500.00"],
        ]
    ))
    story.append(Spacer(1, 6))
    story.append(kv_table([
        ["TOTAL AMOUNT:", "USD 305,500.00"],
    ]))
    doc.build(story)
    print("  [OK] set03: invoice.pdf")

def set03_lc():
    doc = SimpleDocTemplate(os.path.join(SET03_DIR, "lc.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("IRREVOCABLE DOCUMENTARY LETTER OF CREDIT"))
    story.append(divider())
    story.append(kv_table([
        ["Issuing Bank:", "ING BANK N.V.\nAmsterdam, Netherlands\nSWIFT: INGBNL2A"],
        ["LC Number:", "LC-AMS-2024-00531"],
        ["Date of Issue:", "01 November 2024"],
        ["Date of Expiry:", "20 December 2024"],
        ["Applicant:", "EURO TECH DISTRIBUTORS B.V.\nAmsterdamseweg 99, 1182 HG Amstelveen, Netherlands"],
        ["Beneficiary:", "SHENZHEN ELECTRONICS MANUFACTURING COMPANY LIMITED\nShenzhen Export Processing Zone, Guangdong, PRC"],  # slightly different name
        ["Amount:", "USD 300,000.00"],
        ["Tolerance:", "+/- 5 percent"],
        ["Latest Shipment Date:", "25 November 2024"],  # DISCREPANCY: BL date is Dec 5
        ["Presentation Period:", "21 days"],
        ["Port of Loading:", "PORT OF YANTIAN / PORT OF SHEKOU, SHENZHEN"],
        ["Port of Discharge:", "PORT OF ROTTERDAM, NETHERLANDS"],
        ["Incoterms:", "CIF Rotterdam (Incoterms 2020)"],
        ["Partial Shipment:", "NOT ALLOWED"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("GOODS DESCRIPTION"))
    story.append(Body("Consumer Electronic Goods including LED Smart TVs, Wireless Headphones, and USB accessories of Chinese manufacture."))
    doc.build(story)
    print("  [OK] set03: lc.pdf")

def set03_bl():
    doc = SimpleDocTemplate(os.path.join(SET03_DIR, "bl.pdf"), pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    story.append(H1("BILL OF LADING"))
    story.append(Body("ORIGINAL — NEGOTIABLE"))
    story.append(divider())
    story.append(kv_table([
        ["BL Number:", "YRTRTM-2024-BL-55102"],
        ["Carrier:", "COSCO SHIPPING LINES CO., LTD."],
        ["Shipper:", "SHENZHEN ELECTRONICS MANUFACTURING CO., LTD."],  # slightly different from LC beneficiary
        ["Consignee:", "TO THE ORDER OF ING BANK N.V."],
        ["Notify Party:", "EURO TECH DISTRIBUTORS B.V., AMSTELVEEN, NETHERLANDS"],
        ["Vessel / Voyage:", "MV COSCO EUROPE / VOY 2024-47W"],
        ["Port of Loading:", "PORT OF YANTIAN, SHENZHEN, CHINA"],
        ["Port of Discharge:", "PORT OF ROTTERDAM, NETHERLANDS"],
        ["On Board Date:", "05 December 2024"],  # DISCREPANCY: after LC latest shipment date of Nov 25
        ["Freight Terms:", "FREIGHT PREPAID"],
        ["Number of Originals:", "THREE (3/3)"],
    ]))
    story.append(Spacer(1, 6))
    story.append(H2("DESCRIPTION OF GOODS"))
    story.append(kv_table([
        ["Goods:", "Consumer Electronics — LED TVs, Headphones, USB Hubs\n5,500 cartons on 22 pallets"],
        ["Gross Weight:", "18,700 KGS"],
        ["Container No.:", "COSU6712890 / Seal: CSL-990341"],
    ]))
    story.append(divider())
    story.append(Body("SHIPPED ON BOARD in apparent good order and condition."))
    doc.build(story)
    print("  [OK] set03: bl.pdf")

def generate_all():
    print("\n--- SET 01: FULLY COMPLIANT ---")
    set01_invoice(); set01_lc(); set01_bl()

    print("\n--- SET 02: CURRENCY MISMATCH + AMOUNT EXCEEDED ---")
    set02_invoice(); set02_lc(); set02_bl()

    print("\n--- SET 03: LATE SHIPMENT + PARTY NAME VARIANT ---")
    set03_invoice(); set03_lc(); set03_bl()

    print(f"\n[SUCCESS] All 9 PDFs generated in {SAMPLE_DOCS_DIR}/")

if __name__ == "__main__":
    generate_all()
