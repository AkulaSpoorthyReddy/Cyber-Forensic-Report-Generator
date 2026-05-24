import datetime
import io
import sys
from fpdf import FPDF

class ForensicReport(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.primary_color = (10, 17, 40)
        self.secondary_color = (65, 90, 119)
        self.accent_teal = (78, 204, 163)
        self.accent_red = (255, 75, 75)
        self.text_dark = (33, 37, 41)
        
    def header(self):
        if hasattr(self, 'set_font'):
            self.set_fill_color(*self.primary_color)
            self.rect(0, 0, 210, 12, 'F')
            self.set_y(15)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*self.secondary_color)
            self.cell(0, 5, 'CYBER FORENSIC AUDIT CENTRE | AUTOMATED DIAGNOSTIC SYSTEM', 0, 0, 'L')
            self.cell(0, 5, 'CLASSIFICATION: SECURE LEVEL 4', 0, 1, 'R')
            self.set_draw_color(*self.secondary_color)
            self.set_line_width(0.4)
            self.line(10, 22, 200, 22)
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*self.secondary_color)
        self.line(10, 282, 200, 282)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 10, f'REPORT SEGMENT PROOF {self.page_no()} | DATA SECURE TRANSMISSION NODES', 0, 0, 'L')
        self.cell(0, 10, 'CRITICAL INFRASTRUCTURE DEFENSE DOCUMENT', 0, 0, 'R')

    def generate_full_report(self, operator, res, f_hash):
        self.add_page()
        
        # --- TITLE BANNER BLOCK ---
        self.set_fill_color(240, 243, 246)
        self.rect(10, 26, 190, 24, 'F')
        self.set_y(29)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*self.primary_color)
        self.cell(0, 7, 'OFFICIAL FORENSIC ENGINE DIAGNOSTIC DOSSIER', 0, 1, 'C')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 5, f"REFERENCE CASE ASSIGNMENT NUMBER: {res['case_no']}", 0, 1, 'C')
        self.ln(10)

        # --- SECTION 1: SYSTEM IDENTIFICATION MATRIX (TABLE) ---
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 6, 'SECTION 01: SYSTEM AND FILE AUDIT REFERENCE METADATA', 0, 1, 'L')
        self.ln(3)
        
        table_rows = [
            ["CASE FILE NUMBER", str(res['case_no'])],
            ["GENERATION TIMESTAMP", str(res['generated_date'])],
            ["AUTHENTICATED OPERATOR", str(operator).upper()],
            ["INTEGRITY SOURCE FILE HASH", str(f_hash)],
            ["THREAT VECTOR CLASSIFICATION", str(res['category']).upper()],
            ["COMPUTED SIMILARITY COEFFICIENT", f"{res['certainty']}%"],
            ["SYSTEM EVALUATED THREAT RISK", str(res['risk']).upper()]
        ]
        
        for index, row in enumerate(table_rows):
            self.set_fill_color(245, 247, 250) if index % 2 == 0 else self.set_fill_color(255, 255, 255)
            self.set_font('Helvetica', 'B', 9)
            self.cell(65, 8, f" {row[0]}", 1, 0, 'L', fill=True)
            self.set_font('Helvetica', '', 9)
            self.cell(125, 8, f" {row[1]}", 1, 1, 'L', fill=True)
            
        self.ln(12)

        # --- SECTION 2: ADVANCED PATTERN ANALYSIS & RISK METRICS ---
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 6, 'SECTION 02: ADVANCED PATTERN ANALYSIS AND RISK METRICS', 0, 1, 'L')
        self.ln(3)
        
        if res['certainty'] > 80:
            self.set_fill_color(254, 242, 242)
            self.set_text_color(185, 28, 28)
        else:
            self.set_fill_color(255, 251, 235)
            self.set_text_color(180, 83, 9)

        self.rect(10, self.get_y(), 190, 24, 'F')
        self.set_y(self.get_y() + 2)
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 5, " EXECUTIVE SUMMARY SYNOPSIS INDICATOR:", 0, 1, 'L')
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(*self.text_dark)
        self.multi_cell(185, 5, f" {res['summary']}")
        
        self.set_y(self.get_y() + 6)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*self.primary_color)
        self.cell(0, 6, 'DETECTION AND HEURISTIC BEHAVIOR BREAKDOWN:', 0, 1, 'L')
        self.set_font('Helvetica', '', 10)
        detailed_narrative = (
            f"The analyzed dataset patterns were evaluated against structural baselines using multi-dimensional "
            f"vector modeling tracking. The matching architecture identified threat parameters that match the "
            f"'{res['family']}' threat taxonomy group. The signature records map to the following functional "
            f"threat profile and execution traits: {res['modus']}"
        )
        self.multi_cell(0, 6, detailed_narrative)
        self.ln(8)

        # --- SECTION 3: SYSTEM RISK MITIGATION SUGGESTIONS ---
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 6, 'SECTION 03: PRESCRIBED STRATEGIC MITIGATION PROTOCOLS', 0, 1, 'L')
        self.ln(3)
        
        for idx, suggestion in enumerate(res['suggestions'], 1):
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(*self.secondary_color)
            self.cell(12, 7, f" [{idx}] ", 0, 0, 'L')
            self.set_font('Helvetica', '', 10)
            self.set_text_color(*self.text_dark)
            self.multi_cell(178, 7, suggestion)

        # --- SECTION 4: USER READABLE RISK MANAGEMENT ROADMAP ---
        self.add_page()
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 6, 'SECTION 04: SYSTEM SECURITY RISK ASSESSMENT ROADMAP', 0, 1, 'L')
        self.ln(4)

        # Dynamic mapping inside the roadmap tracking layout arrays
        roadmap_items = [
            ("VULNERABILITY ID", f"Classification target set to focus on signature: {res['category']}."),
            ("IMPACT SCALING", f"Calculated absolute profile compromise factor verified at {res['certainty']}% confidence."),
            ("ISOLATION PHASE", f"Deploy containment tunnels targeting isolation group family: {res['family']}.")
        ]

        for title, desc in roadmap_items:
            self.set_fill_color(240, 249, 255)
            self.rect(10, self.get_y(), 190, 15, 'F')
            self.set_fill_color(*self.secondary_color)
            self.rect(10, self.get_y(), 2.5, 15, 'F')
            
            self.set_x(15)
            self.set_y(self.get_y() + 2)
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(*self.primary_color)
            self.cell(45, 5, title, 0, 0, 'L')
            
            self.set_font('Helvetica', '', 9.5)
            self.set_text_color(*self.text_dark)
            self.cell(0, 5, desc, 0, 1, 'L')
            self.ln(6)

        # --- SECTION 5: SECURITY ACTION FRAMEWORK (CHECKBOXES) ---
        self.add_page()
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 6, 'SECTION 05: ACTIONABLE SECURITY MANAGEMENT FRAMEWORK', 0, 1, 'L')
        self.ln(4)

        self.set_font('Helvetica', '', 10)
        self.set_text_color(*self.text_dark)
        self.multi_cell(0, 6, "To maintain production validation and enforce structural compliance boundaries, execution teams must audit these checklist items:")
        self.ln(6)

        framework_checks = [
            ("PHASED CONTROL AUDITS", f"Perform manual validation runs over the matching {res['category']} vector stream files."),
            ("NETWORK LOG INSULATION", f"Isolate out-of-bounds process calls linked to the {res['family']} anomaly footprint."),
            ("RECURSIVE RE-HASHING", f"Re-verify integrity signatures to confirm zero dynamic mutation remains across historical arrays.")
        ]

        for check_title, check_desc in framework_checks:
            self.set_draw_color(*self.accent_teal)
            self.set_line_width(0.5)
            self.rect(12, self.get_y() + 1, 4, 4, 'D')
            
            self.set_x(20)
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(*self.primary_color)
            self.cell(0, 6, check_title, 0, 1, 'L')
            
            self.set_x(20)
            self.set_font('Helvetica', '', 9.5)
            self.set_text_color(*self.text_dark)
            self.multi_cell(170, 5, check_desc)
            self.ln(5)

        return bytes(self.output())