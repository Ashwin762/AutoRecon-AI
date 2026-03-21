from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
import os

# Color palette
BLACK = HexColor('#000000')
GREEN = HexColor('#00ff41')
CYAN = HexColor('#00d4ff')
RED = HexColor('#ff0040')
YELLOW = HexColor('#ffd700')
DARK_GRAY = HexColor('#0a0a0a')
MID_GRAY = HexColor('#1a1a1a')
LIGHT_GRAY = HexColor('#2a2a2a')
DIM_GREEN = HexColor('#003310')

def get_risk_color(score):
    if score >= 70:
        return RED
    elif score >= 40:
        return YELLOW
    return GREEN

def get_risk_label(score):
    if score >= 70:
        return "CRITICAL"
    elif score >= 40:
        return "MEDIUM"
    return "LOW"

def generate_pdf_report(scan_data: dict, output_path: str) -> str:
    domain = scan_data["domain"]
    subdomains = scan_data.get("subdomains", [])
    dns_info = scan_data.get("dns_info", {})
    port_scan = scan_data.get("port_scan", {})
    breach_results = scan_data.get("breach_results", [])
    ai_report = scan_data.get("ai_report", {})
    risk_score = ai_report.get("risk_score", 0)
    risk_color = get_risk_color(risk_score)
    risk_label = get_risk_label(risk_score)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )

    styles = getSampleStyleSheet()
    elements = []

    # ── HEADER ──
    header_data = [[
        Paragraph(f'<font color="#00ff41" size="22"><b>AUTORECON AI</b></font>', styles['Normal']),
        Paragraph(f'<font color="#555555" size="8">THREAT INTELLIGENCE REPORT<br/>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</font>', styles['Normal'])
    ]]
    header_table = Table(header_data, colWidths=[100*mm, 80*mm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLACK),
        ('TEXTCOLOR', (0, 0), (-1, -1), GREEN),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 1, GREEN),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8*mm))

    # ── TARGET ──
    target_data = [[
        Paragraph('<font color="#555555" size="8">TARGET</font>', styles['Normal']),
        Paragraph('<font color="#555555" size="8">RISK SCORE</font>', styles['Normal']),
        Paragraph('<font color="#555555" size="8">RISK LEVEL</font>', styles['Normal']),
        Paragraph('<font color="#555555" size="8">SCAN DATE</font>', styles['Normal']),
    ], [
        Paragraph(f'<font color="#00d4ff" size="16"><b>{domain.upper()}</b></font>', styles['Normal']),
        Paragraph(f'<font color="{risk_color.hexval()}" size="16"><b>{risk_score}/100</b></font>', styles['Normal']),
        Paragraph(f'<font color="{risk_color.hexval()}" size="16"><b>{risk_label}</b></font>', styles['Normal']),
        Paragraph(f'<font color="#00ff41" size="10">{datetime.now().strftime("%Y-%m-%d")}</font>', styles['Normal']),
    ]]
    target_table = Table(target_data, colWidths=[45*mm, 35*mm, 35*mm, 65*mm])
    target_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, HexColor('#00ff4133')),
        ('LINEBEFORE', (1, 0), (1, -1), 1, HexColor('#1a1a1a')),
        ('LINEBEFORE', (2, 0), (2, -1), 1, HexColor('#1a1a1a')),
        ('LINEBEFORE', (3, 0), (3, -1), 1, HexColor('#1a1a1a')),
    ]))
    elements.append(target_table)
    elements.append(Spacer(1, 6*mm))

    # ── STATS ──
    stats = [
        ("SUBDOMAINS", str(len(subdomains)), "#00ff41"),
        ("IP ADDRESSES", str(len(dns_info.get("ip_addresses", []))), "#00d4ff"),
        ("OPEN PORTS", str(port_scan.get("total_open_ports", 0)), "#ffd700"),
        ("BREACHES", str(len(breach_results)), "#ff0040"),
        ("VULNERABILITIES", str(len(port_scan.get("vulnerabilities", []))), "#ff0040"),
    ]
    stats_data = [
        [Paragraph(f'<font color="{c}" size="18"><b>{v}</b></font>', styles['Normal']) for _, v, c in stats],
        [Paragraph(f'<font color="#555555" size="7">{l}</font>', styles['Normal']) for l, _, _ in stats],
    ]
    stats_table = Table(stats_data, colWidths=[36*mm]*5)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
        ('BOX', (0, 0), (-1, -1), 1, HexColor('#00ff4122')),
        ('LINEBEFORE', (1, 0), (4, -1), 1, HexColor('#1a1a1a')),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 6*mm))

    # ── DNS INTELLIGENCE ──
    elements.append(Paragraph('<font color="#555555" size="8">── DNS INTELLIGENCE</font>', styles['Normal']))
    elements.append(Spacer(1, 3*mm))

    dns_rows = [
        [Paragraph('<font color="#00d4ff" size="8">IP ADDRESSES</font>', styles['Normal']),
         Paragraph(f'<font color="#00ff41" size="8">{", ".join(dns_info.get("ip_addresses", [])[:5])}</font>', styles['Normal'])],
        [Paragraph('<font color="#00d4ff" size="8">MAIL SERVERS</font>', styles['Normal']),
         Paragraph(f'<font color="#00ff41" size="8">{", ".join(dns_info.get("mail_servers", [])[:3])}</font>', styles['Normal'])],
        [Paragraph('<font color="#00d4ff" size="8">NAMESERVERS</font>', styles['Normal']),
         Paragraph(f'<font color="#00ff41" size="8">{", ".join(dns_info.get("nameservers", [])[:3])}</font>', styles['Normal'])],
    ]
    dns_table = Table(dns_rows, colWidths=[35*mm, 145*mm])
    dns_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, HexColor('#00ff4122')),
        ('LINEBELOW', (0, 0), (-1, -2), 1, HexColor('#1a1a1a')),
    ]))
    elements.append(dns_table)
    elements.append(Spacer(1, 6*mm))

    # ── SUBDOMAINS ──
    elements.append(Paragraph('<font color="#555555" size="8">── SUBDOMAIN ENUMERATION</font>', styles['Normal']))
    elements.append(Spacer(1, 3*mm))

    # Split subdomains into 3 columns
    sub_sample = subdomains[:60]
    chunk = max(1, len(sub_sample) // 3)
    col1 = sub_sample[:chunk]
    col2 = sub_sample[chunk:chunk*2]
    col3 = sub_sample[chunk*2:]

    max_rows = max(len(col1), len(col2), len(col3))
    sub_rows = []
    for i in range(max_rows):
        row = []
        for col in [col1, col2, col3]:
            if i < len(col):
                sub = col[i]
                is_sensitive = any(k in sub for k in ["dev", "stage", "test", "admin"])
                color = "#ffd700" if is_sensitive else "#00ff4166"
                prefix = "⚠ " if is_sensitive else "◈ "
                row.append(Paragraph(f'<font color="{color}" size="7">{prefix}{sub[:45]}</font>', styles['Normal']))
            else:
                row.append(Paragraph('', styles['Normal']))
        sub_rows.append(row)

    if sub_rows:
        sub_table = Table(sub_rows, colWidths=[60*mm, 60*mm, 60*mm])
        sub_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#00ff4122')),
        ]))
        elements.append(sub_table)

    if len(subdomains) > 60:
        elements.append(Spacer(1, 2*mm))
        elements.append(Paragraph(
            f'<font color="#555555" size="7">... and {len(subdomains) - 60} more subdomains</font>',
            styles['Normal']
        ))
    elements.append(Spacer(1, 6*mm))

    # ── AI REPORT ──
    elements.append(Paragraph('<font color="#555555" size="8">── AI THREAT ANALYSIS · LLAMA3 70B</font>', styles['Normal']))
    elements.append(Spacer(1, 3*mm))

    report_text = ai_report.get("report", "No report generated")
    report_style = ParagraphStyle(
        'ReportStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#00ff41'),
        backColor=DARK_GRAY,
        leading=14,
        leftIndent=8,
        rightIndent=8,
        spaceBefore=2,
        spaceAfter=2,
    )
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#00d4ff'),
        backColor=DARK_GRAY,
        leading=16,
        leftIndent=8,
        spaceBefore=8,
        spaceAfter=4,
    )

    report_container = []
    for line in report_text.split('\n'):
        if line.startswith('##'):
            report_container.append(Paragraph(
                f'<b>{line.replace("##", "").strip()}</b>',
                header_style
            ))
        elif line.startswith('*'):
            report_container.append(Paragraph(
                f'◈ {line.replace("*", "").strip()}',
                report_style
            ))
        elif line.strip():
            report_container.append(Paragraph(line, report_style))

    ai_data = [[p] for p in report_container]
    if ai_data:
        ai_table = Table(ai_data, colWidths=[180*mm])
        ai_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#00d4ff33')),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(ai_table)

    elements.append(Spacer(1, 6*mm))

    # ── FOOTER ──
    footer_data = [[
        Paragraph('<font color="#333333" size="7">Generated by AutoRecon AI · For authorized security assessment only</font>', styles['Normal']),
        Paragraph('<font color="#333333" size="7">CONFIDENTIAL</font>', styles['Normal'])
    ]]
    footer_table = Table(footer_data, colWidths=[130*mm, 50*mm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLACK),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('LINEABOVE', (0, 0), (-1, -1), 1, HexColor('#1a1a1a')),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    return output_path