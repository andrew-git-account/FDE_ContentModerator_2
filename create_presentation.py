"""
Generate PDF presentation for MiniBase Content Moderation Agent.

Creates a 5-slide presentation summarizing the agent design and value proposition.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import io


def create_volume_risk_chart():
    """Create volume vs risk matrix chart for Slide 2."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Data points: (volume, risk, label)
    points = [
        (1080, 2, "Routine Spam\n1,080/day\n9 hrs/day", 'green'),
        (360, 8, "Grey-zone Cases\n360/day\n30 hrs/day", 'red'),
        (60, 6, "User Appeals\n60/day\n8 hrs/day", 'orange'),
        (5, 9, "IP Claims\n3-5/week", 'darkred')
    ]

    for volume, risk, label, color in points:
        ax.scatter(volume, risk, s=3000, alpha=0.6, c=color, edgecolors='black', linewidth=2)
        ax.annotate(label, (volume, risk), ha='center', va='center', fontsize=10, weight='bold')

    ax.set_xlabel('Volume (posts/day)', fontsize=14, weight='bold')
    ax.set_ylabel('Risk of Error (1-10)', fontsize=14, weight='bold')
    ax.set_title('Volume × Risk Analysis: Where to Automate?', fontsize=16, weight='bold', pad=20)
    ax.set_xlim(-50, 1200)
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)

    # Add "Automation Target" annotation
    ax.annotate('PRIMARY AUTOMATION TARGET', xy=(1080, 2), xytext=(800, 4),
                arrowprops=dict(arrowstyle='->', lw=2, color='darkgreen'),
                fontsize=12, weight='bold', color='darkgreen')

    plt.tight_layout()

    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def create_delegation_chart():
    """Create delegation architecture chart for Slide 3."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Data
    archetypes = ['Fully\nAgentic\n🤖', 'Agent-Led\n🤝', 'Human-Led\n👤', 'Human-Only\n⛔']
    volumes = [800, 280, 360, 31]
    colors_list = ['#2ecc71', '#f39c12', '#3498db', '#e74c3c']

    bars = ax.barh(archetypes, volumes, color=colors_list, edgecolor='black', linewidth=2)

    # Add volume labels
    for i, (bar, vol) in enumerate(zip(bars, volumes)):
        ax.text(vol + 30, i, f'{vol} posts/day', va='center', fontsize=12, weight='bold')

    ax.set_xlabel('Volume (posts/day)', fontsize=14, weight='bold')
    ax.set_title('Four Delegation Archetypes', fontsize=16, weight='bold', pad=20)
    ax.set_xlim(0, 900)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def create_value_chart():
    """Create value metrics chart for Slide 4."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Time savings
    categories = ['Spam\nHandling', 'Context\nGathering', 'Total\nSavings']
    hours = [7, 2, 9]
    colors_list = ['#2ecc71', '#3498db', '#f39c12']

    bars = ax1.bar(categories, hours, color=colors_list, edgecolor='black', linewidth=2)
    ax1.set_ylabel('Hours/Day Saved', fontsize=12, weight='bold')
    ax1.set_title('Time Savings (Daily)', fontsize=14, weight='bold')
    ax1.set_ylim(0, 10)

    for bar, h in zip(bars, hours):
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.3, f'{h} hrs',
                ha='center', va='bottom', fontsize=12, weight='bold')

    # Right: ROI
    categories = ['Investment', 'Year 1\nValue', 'ROI']
    values = [14, 137, 10.7]
    colors_list = ['#e74c3c', '#2ecc71', '#f39c12']

    bars = ax2.bar(categories, values, color=colors_list, edgecolor='black', linewidth=2)
    ax2.set_ylabel('Value (£K)', fontsize=12, weight='bold')
    ax2.set_title('First-Year ROI', fontsize=14, weight='bold')
    ax2.set_ylim(0, 150)

    labels = ['£14K', '£137K', '10.7:1']
    for bar, val, label in zip(bars, values, labels):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 5, label,
                ha='center', va='bottom', fontsize=12, weight='bold')

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf


def create_presentation():
    """Create the full PDF presentation."""

    output_path = Path(__file__).parent / "Deliverables" / "MiniBase_Agent_Presentation.pdf"
    output_path.parent.mkdir(exist_ok=True)

    # Page setup
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#2c3e50')
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        leftIndent=20,
        textColor=colors.HexColor('#2c3e50')
    )

    # Story (content)
    story = []

    # ===== SLIDE 1: The Problem =====
    story.append(Paragraph("MiniBase Content Moderation Agent", title_style))
    story.append(Paragraph("Week 2 FDE Program Deliverable - Scenario 4", body_style))
    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph("The Problem: Moderation at Capacity", heading_style))
    story.append(Paragraph("MiniBase's hybrid moderation team is drowning in routine spam, leaving no capacity for nuanced judgment cases.", body_style))
    story.append(Spacer(1, 0.2*inch))

    problem_data = [
        ['Metric', 'Current State', 'Impact'],
        ['Daily posts flagged', '1,500/day', '12.5% of all posts'],
        ['Team capacity', '47 hrs/day', '8 volunteers + 2 staff'],
        ['Routine spam', '1,080/day (72%)', '9 hrs/day consumed'],
        ['Grey-zone cases', '360/day (24%)', '30 hrs/day needed'],
        ['Burnout risk', 'HIGH', 'Volunteers quitting'],
    ]

    problem_table = Table(problem_data, colWidths=[2*inch, 1.8*inch, 2*inch])
    problem_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    story.append(problem_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>The Stakes:</b> \"False positives are survivable; one viral false negative is existential.\"", body_style))

    story.append(PageBreak())

    # ===== SLIDE 2: Why NOT Full Automation =====
    story.append(Paragraph("Why NOT \"Just Automate Everything\"?", heading_style))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>The Trap:</b> Assuming all moderation work is the same ignores asymmetric risk.", body_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("• <b>Routine spam (72% of queue):</b> High volume, low risk, clear patterns → Automate", bullet_style))
    story.append(Paragraph("• <b>Grey-zone cases (24% of queue):</b> Lower volume, existential risk → Requires human judgment", bullet_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("<b>Grey-zone examples requiring cultural context:</b>", body_style))
    story.append(Paragraph("• Harsh critique vs. harassment (tone, subforum norms, invitation)", bullet_style))
    story.append(Paragraph("• Community member vs. commercial spam (established vs. new user)", bullet_style))
    story.append(Paragraph("• Sponsor sensitivities (the \"2024 incident\" precedent)", bullet_style))
    story.append(Spacer(1, 0.2*inch))

    # Add volume-risk chart
    chart_buf = create_volume_risk_chart()
    chart_img = Image(chart_buf, width=5.5*inch, height=4.1*inch)
    story.append(chart_img)

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>The Insight:</b> Automate 9 hrs/day of low-risk spam to create capacity for 30 hrs/day of high-risk judgment.", body_style))

    story.append(PageBreak())

    # ===== SLIDE 3: Delegation Architecture =====
    story.append(Paragraph("The Solution: Four Delegation Archetypes", heading_style))
    story.append(Paragraph("Not one-size-fits-all automation — right delegation for each task type.", body_style))
    story.append(Spacer(1, 0.2*inch))

    delegation_data = [
        ['Archetype', 'Volume/Day', 'Use Case', 'Value'],
        ['🤖 Fully Agentic', '800 posts', 'Clear spam (link farms, gibberish)', '7 hrs saved'],
        ['🤝 Agent-Led', '280 posts', 'Edge cases → propose, human approves', '3 hrs saved'],
        ['👤 Human-Led', '360 posts', 'Grey-zone → agent gathers context', '2 hrs saved'],
        ['⛔ Human-Only', '31 posts', 'IP claims, bans → no agent role', '0 hrs saved'],
    ]

    delegation_table = Table(delegation_data, colWidths=[1.5*inch, 1.2*inch, 2.3*inch, 1.2*inch])
    delegation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgreen, colors.lightyellow, colors.lightblue, colors.pink]),
    ]))
    story.append(delegation_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Safety Bar (Always Escalate):</b>", body_style))
    story.append(Paragraph("• Sponsor accounts (2024 incident precedent) → Tom reviews personally", bullet_style))
    story.append(Paragraph("• High community engagement (>12 reactions) → risky to auto-remove", bullet_style))
    story.append(Paragraph("• Low confidence (<0.7) → requires human judgment", bullet_style))
    story.append(Paragraph("• Subforum-specific norms (e.g., painters \"no critique without invitation\")", bullet_style))
    story.append(Spacer(1, 0.2*inch))

    # Add delegation chart
    delegation_chart_buf = create_delegation_chart()
    delegation_chart_img = Image(delegation_chart_buf, width=5.5*inch, height=3.3*inch)
    story.append(delegation_chart_img)

    story.append(PageBreak())

    # ===== SLIDE 4: Value & Safety =====
    story.append(Paragraph("The Value & Safety Case", heading_style))
    story.append(Spacer(1, 0.15*inch))

    # Add value chart
    value_chart_buf = create_value_chart()
    value_chart_img = Image(value_chart_buf, width=6.5*inch, height=2.7*inch)
    story.append(value_chart_img)
    story.append(Spacer(1, 0.2*inch))

    value_data = [
        ['Value Metrics', 'Target', 'Safety Metrics (Non-Negotiable)', 'Target'],
        ['Time saved on spam', '77% reduction\n(9→2 hrs/day)', 'Moderation accuracy', '≥95% precision'],
        ['Capacity freed', '7 hrs/day for\ngrey-zone cases', 'False negative rate', '<0.1%\n(zero viral)'],
        ['Growth headroom', '33% increase\n(1,500→2,000/day)', 'Sponsor safety', '100% escalation'],
        ['First-year ROI', '10.7:1\n(£137K / £14K)', 'Audit trail', '100% logged'],
    ]

    value_table = Table(value_data, colWidths=[1.8*inch, 1.5*inch, 1.9*inch, 1.3*inch])
    value_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#27ae60')),
        ('BACKGROUND', (2, 0), (3, 0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (1, -1), [colors.lightgreen, colors.Color(0.9, 0.95, 0.9)]),
        ('ROWBACKGROUNDS', (2, 1), (3, -1), [colors.Color(1, 0.9, 0.9), colors.Color(1, 0.95, 0.95)]),
    ]))
    story.append(value_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Key Message:</b> This isn't about replacing moderators — it's about freeing them from brain-dead spam work so they can focus on nuanced cases that build community trust.", body_style))

    story.append(PageBreak())

    # ===== SLIDE 5: Validation & Next Steps =====
    story.append(Paragraph("Validation: Proven Buildable", heading_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("<b>What We Built (Week 2 FDE Deliverables):</b>", body_style))
    story.append(Paragraph("• <b>Agent Purpose Document:</b> 18 micro-tasks mapped to delegation archetypes, confidence thresholds, escalation triggers", bullet_style))
    story.append(Paragraph("• <b>System Integration Plan:</b> 8 systems analyzed, 212 hrs effort with specific technical constraints addressed (no hand-waving)", bullet_style))
    story.append(Paragraph("• <b>Discovery Questions:</b> 18 design-changing questions for Tom (6 critical, 9 high priority)", bullet_style))
    story.append(Paragraph("• <b>Live Demo:</b> StreamLit app validating delegation logic on 4 test cases (link farm spam, harsh critique, user appeal, IP claim)", bullet_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Demo Validation Results:</b>", body_style))
    story.append(Paragraph("✅ Link farm spam → Auto-remove (Fully Agentic, confidence 0.98)", bullet_style))
    story.append(Paragraph("✅ Harsh critique → Escalate (Human-Led, confidence 0.65, subforum norm conflict)", bullet_style))
    story.append(Paragraph("✅ User appeal → Context gathered (Human-Led, 5 minutes saved)", bullet_style))
    story.append(Paragraph("✅ IP claim → Human-only (No agent role, legal sensitivity)", bullet_style))
    story.append(Spacer(1, 0.3*inch))

    roadmap_data = [
        ['Phase', 'Timeline', 'Key Activities', 'Success Criteria'],
        ['Discovery', 'Week 3', 'Answer 18 critical questions with Tom', 'All design-changing questions resolved'],
        ['Phase 1: Build', 'Weeks 4-19\n(16 weeks)', 'Build spam automation + escalation logic\nIntegrate 8 systems (Discourse, Gallery, etc.)', 'System tests pass\n≥95% accuracy on test fixtures'],
        ['Shadow Mode', 'Weeks 20-23\n(4 weeks)', 'Run parallel with humans\nCalibrate confidence thresholds', 'Zero false negatives\nModerator trust established'],
        ['Go-Live', 'Week 24', 'Phase 1 production deployment', '7 hrs/day savings achieved\n<10% override rate'],
    ]

    roadmap_table = Table(roadmap_data, colWidths=[1.2*inch, 1.2*inch, 2.6*inch, 1.5*inch])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.Color(0.95, 0.95, 1), colors.Color(1, 1, 0.95)]),
    ]))
    story.append(roadmap_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Closed Build Loop Outcome:</b> Specification is complete and buildable. Ready to proceed to discovery and implementation.", body_style))

    # Build PDF
    doc.build(story)

    return output_path


if __name__ == "__main__":
    output_path = create_presentation()
    print(f"Presentation created: {output_path}")
    print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"   5 slides covering: Problem, Anti-Pattern, Solution, Value/Safety, Validation")
