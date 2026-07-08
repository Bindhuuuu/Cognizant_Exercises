"""
SkillGap AI - PDF Report Generator
Generates downloadable PDF analysis reports using ReportLab.
"""

import io
from datetime import datetime
from typing import Dict, List, Any, Optional
from utils.logger import setup_logger

logger = setup_logger("report_generator")


def generate_pdf_report(
    candidate_name: str,
    analysis_data: Dict[str, Any],
    output_path: Optional[str] = None
) -> bytes:
    """
    Generate a comprehensive PDF report for the resume analysis.
    
    Args:
        candidate_name: Name of the candidate
        analysis_data: Dictionary containing all analysis results
        output_path: Optional path to save the PDF file
    
    Returns:
        PDF content as bytes
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, KeepTogether
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # ------------------------------------------------------------------
        # Styles
        # ------------------------------------------------------------------
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=24,
            textColor=colors.HexColor("#667EEA"),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"
        )
        subtitle_style = ParagraphStyle(
            "CustomSubtitle",
            parent=styles["Normal"],
            fontSize=12,
            textColor=colors.HexColor("#888888"),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        section_header_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#667EEA"),
            spaceBefore=16,
            spaceAfter=8,
            fontName="Helvetica-Bold",
            borderPad=4
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#333333"),
            spaceAfter=4,
            leading=16
        )
        label_style = ParagraphStyle(
            "Label",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#666666"),
            fontName="Helvetica-Bold"
        )

        story = []

        # ------------------------------------------------------------------
        # Header / Title
        # ------------------------------------------------------------------
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("🎯 SkillGap AI", title_style))
        story.append(Paragraph("Resume Analysis & Career Intelligence Report", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#667EEA")))
        story.append(Spacer(1, 0.5*cm))

        # Report metadata
        meta_data = [
            ["Candidate:", candidate_name or "N/A"],
            ["Report Generated:", datetime.now().strftime("%d %B %Y, %I:%M %p")],
            ["Analysis Engine:", "SkillGap AI v1.0 (NLP + ML)"],
        ]
        meta_table = Table(meta_data, colWidths=[4*cm, 13*cm])
        meta_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#667EEA")),
            ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#333333")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.5*cm))

        # ------------------------------------------------------------------
        # Score Summary Cards
        # ------------------------------------------------------------------
        story.append(Paragraph("📊 Performance Summary", section_header_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#EEEEEE")))
        story.append(Spacer(1, 0.3*cm))

        ats_score = analysis_data.get("ats_score", 0)
        match_pct = analysis_data.get("match_percentage", 0)
        predicted_role = analysis_data.get("predicted_role", "N/A")
        confidence = analysis_data.get("confidence", 0)

        scores_data = [
            ["Metric", "Value", "Status"],
            ["ATS Resume Score", f"{ats_score}/100", _get_status(ats_score)],
            ["Skill Match %", f"{match_pct:.1f}%", _get_status(match_pct)],
            ["Predicted Role", predicted_role, ""],
            ["Confidence Score", f"{confidence:.1f}%", _get_status(confidence)],
        ]
        scores_table = Table(scores_data, colWidths=[6*cm, 5*cm, 6*cm])
        scores_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667EEA")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F9F9F9"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 0.5*cm))

        # ------------------------------------------------------------------
        # Extracted Information
        # ------------------------------------------------------------------
        extracted = analysis_data.get("extracted_info", {})
        if extracted:
            story.append(Paragraph("👤 Extracted Resume Information", section_header_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#EEEEEE")))
            story.append(Spacer(1, 0.3*cm))

            for key, value in extracted.items():
                if value and value != "Not found":
                    if isinstance(value, list):
                        display_val = ", ".join(value[:10])
                    else:
                        display_val = str(value)
                    story.append(Paragraph(f"<b>{key}:</b> {display_val}", body_style))

            story.append(Spacer(1, 0.3*cm))

        # ------------------------------------------------------------------
        # Skill Analysis
        # ------------------------------------------------------------------
        matching_skills = analysis_data.get("matching_skills", [])
        missing_skills = analysis_data.get("missing_skills", [])

        story.append(Paragraph("🔍 Skill Gap Analysis", section_header_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#EEEEEE")))
        story.append(Spacer(1, 0.3*cm))

        if matching_skills:
            story.append(Paragraph(
                f"<b>✅ Matching Skills ({len(matching_skills)}):</b>",
                label_style
            ))
            story.append(Paragraph(", ".join(matching_skills[:20]), body_style))
            story.append(Spacer(1, 0.2*cm))

        if missing_skills:
            story.append(Paragraph(
                f"<b>❌ Missing Skills ({len(missing_skills)}):</b>",
                label_style
            ))
            story.append(Paragraph(", ".join(missing_skills[:20]), body_style))
            story.append(Spacer(1, 0.3*cm))

        # ------------------------------------------------------------------
        # ATS Improvement Suggestions
        # ------------------------------------------------------------------
        suggestions = analysis_data.get("ats_suggestions", [])
        if suggestions:
            story.append(Paragraph("💡 ATS Improvement Suggestions", section_header_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#EEEEEE")))
            story.append(Spacer(1, 0.3*cm))
            for i, suggestion in enumerate(suggestions[:8], 1):
                story.append(Paragraph(f"{i}. {suggestion}", body_style))
            story.append(Spacer(1, 0.3*cm))

        # ------------------------------------------------------------------
        # Learning Recommendations
        # ------------------------------------------------------------------
        recommendations = analysis_data.get("recommendations", [])
        if recommendations:
            story.append(Paragraph("📚 Top Learning Recommendations", section_header_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#EEEEEE")))
            story.append(Spacer(1, 0.3*cm))

            rec_data = [["Course/Resource", "Platform", "Level"]]
            for rec in recommendations[:8]:
                rec_data.append([
                    rec.get("title", "")[:45],
                    rec.get("platform", ""),
                    rec.get("level", "")
                ])

            rec_table = Table(rec_data, colWidths=[9*cm, 4*cm, 4*cm])
            rec_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#764BA2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F9F9F9"), colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("WORDWRAP", (0, 0), (-1, -1), True),
            ]))
            story.append(rec_table)
            story.append(Spacer(1, 0.5*cm))

        # ------------------------------------------------------------------
        # Footer
        # ------------------------------------------------------------------
        story.append(Spacer(1, 1*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC")))
        story.append(Spacer(1, 0.2*cm))
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#AAAAAA"),
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            f"Generated by SkillGap AI | {datetime.now().strftime('%Y')} | AI-Powered Career Intelligence Platform",
            footer_style
        ))

        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Optionally save to file
        if output_path:
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)
            logger.info(f"PDF report saved to: {output_path}")

        logger.info(f"PDF report generated successfully for: {candidate_name}")
        return pdf_bytes

    except ImportError:
        logger.error("ReportLab not installed. Run: pip install reportlab")
        return b""
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        return b""


def _get_status(score: float) -> str:
    """Return a status label based on score value."""
    if score >= 80:
        return "✅ Excellent"
    elif score >= 60:
        return "🟡 Good"
    elif score >= 40:
        return "🟠 Average"
    else:
        return "🔴 Needs Work"
