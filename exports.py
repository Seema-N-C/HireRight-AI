# ============================================================
# exports.py — CSV export and PDF report generation
# ============================================================

import io
import datetime
import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak)


# ── CSV ───────────────────────────────────────────────────────

def build_csv(final_results: list) -> bytes:
    rows = []
    for rank, r in enumerate(final_results, 1):
        p     = r["parsed"]
        score = r["final_score"]
        if score >= 75:   status = "Shortlisted"
        elif score >= 50: status = "Under Review"
        else:             status = "Rejected"
        suggested = "; ".join([role for role, _ in r.get("role_suggestions", [])]) or "N/A"
        rows.append({
            "Rank":                        rank,
            "Name":                        p["Name"],
            "Email":                       p["Email"],
            "Phone":                       p["Phone"],
            "LinkedIn":                    p["LinkedIn"],
            "GitHub":                      p["GitHub"],
            "Similarity %":                round(r["similarity_score"] * 100, 2),
            "Prediction %":                round(r["prediction_prob"] * 100, 2),
            "Final Score %":               score,
            "Status":                      status,
            "Detected Skills":             ", ".join(p["Skills"]),
            "Possessed Skills (JD Match)": ", ".join(r.get("possessed_skills", [])) or "None",
            "Missing Skills":              ", ".join(r.get("missing_skills", []))   or "None",
            "Education":                   " | ".join(p["Education"]),
            "Experience":                  " | ".join(p["Experience"]),
            "Projects":                    " | ".join(p["Projects"]),
            "Certifications":              " | ".join(p["Certifications"]),
            "Achievements":                " | ".join(p["Achievements"]),
            "Suggested Roles (Rejected)":  suggested,
        })
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


# ── PDF ───────────────────────────────────────────────────────

def generate_pdf_report(final_results: list, metrics: dict) -> bytes:
    PUR   = rl_colors.HexColor("#667eea")
    LPINK = rl_colors.HexColor("#f093fb")
    GRN   = rl_colors.HexColor("#4ade80")
    ORN   = rl_colors.HexColor("#fbbf24")
    RD    = rl_colors.HexColor("#f87171")
    WHITE = rl_colors.white
    DARK  = rl_colors.HexColor("#0f0c29")
    LGRAY = rl_colors.HexColor("#1a1040")
    TEAL  = rl_colors.HexColor("#22d3ee")

    shortlisted = sum(1 for r in final_results if r["final_score"] >= 75)

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=letter,
                               leftMargin=0.65*inch, rightMargin=0.65*inch,
                               topMargin=0.65*inch,  bottomMargin=0.6*inch)

    def S(name, **kw): return ParagraphStyle(name, **kw)
    def sp(h=8):       return Spacer(1, h)

    def page_border(canvas, doc):
        canvas.saveState()
        w, h = letter
        canvas.setStrokeColor(PUR);   canvas.setLineWidth(3); canvas.rect(18, 18, w-36, h-36)
        canvas.setStrokeColor(LPINK); canvas.setLineWidth(1); canvas.rect(24, 24, w-48, h-48)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(rl_colors.HexColor("#555555"))
        canvas.drawCentredString(w/2, 30, "HireRight AI — Intelligence That Hires Right.")
        canvas.drawRightString(w-30, 30, f"Page {doc.page}")
        canvas.restoreState()

    story = []

    # ── Cover ──
    cover = Table([[Paragraph("🤖  HireRight AI",
                              S("cv", fontName="Helvetica-Bold", fontSize=28,
                                textColor=LPINK, alignment=TA_CENTER))]],
                  colWidths=[doc.width])
    cover.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), DARK),
                               ("TOPPADDING", (0,0), (-1,-1), 35),
                               ("BOTTOMPADDING", (0,0), (-1,-1), 35)]))
    story.append(cover)

    bar = Table([[""]], colWidths=[doc.width])
    bar.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PUR),
                              ("TOPPADDING", (0,0), (-1,-1), 4),
                              ("BOTTOMPADDING", (0,0), (-1,-1), 4)]))
    story.append(bar); story.append(sp(20))

    story.append(Paragraph("AI-Powered Intelligent Recruitment",
                            S("t1", fontName="Helvetica-Bold", fontSize=18, textColor=PUR, alignment=TA_CENTER)))
    story.append(Paragraph("& Candidate Analytics System",
                            S("t2", fontName="Helvetica-Bold", fontSize=16, textColor=PUR, alignment=TA_CENTER)))
    story.append(sp(6))
    story.append(Paragraph("Intelligence That Hires Right.",
                            S("t3", fontName="Helvetica-Oblique", fontSize=12, textColor=LPINK, alignment=TA_CENTER)))
    story.append(Paragraph("Powered by RoBERTa-based Sentence Transformer",
                            S("t3b", fontName="Helvetica-Oblique", fontSize=10,
                              textColor=rl_colors.HexColor("#667eea"), alignment=TA_CENTER)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PUR, spaceAfter=16, spaceBefore=10))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%B %d, %Y — %I:%M %p')}",
                            S("t4", fontName="Helvetica", fontSize=10,
                              textColor=rl_colors.HexColor("#555555"), alignment=TA_CENTER)))
    story.append(sp(20))

    stats_t = Table([[
        Paragraph(f"<b>{len(final_results)}</b><br/>Candidates",
                  S("s1", fontName="Helvetica", fontSize=12, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f"<b>{shortlisted}</b><br/>Shortlisted",
                  S("s2", fontName="Helvetica", fontSize=12, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f"<b>{metrics['accuracy']}%</b><br/>Accuracy",
                  S("s3", fontName="Helvetica", fontSize=12, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f"<b>{metrics['roc_auc']}</b><br/>ROC AUC",
                  S("s4", fontName="Helvetica", fontSize=12, textColor=WHITE, alignment=TA_CENTER)),
    ]], colWidths=[doc.width/4]*4)
    stats_t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), PUR),
        ("BACKGROUND", (1,0), (1,-1), GRN),
        ("BACKGROUND", (2,0), (2,-1), LPINK),
        ("BACKGROUND", (3,0), (3,-1), rl_colors.HexColor("#a855f7")),
        ("TOPPADDING", (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LINEAFTER", (0,0), (2,-1), 1, WHITE),
    ]))
    story.append(stats_t); story.append(PageBreak())

    # ── Rankings Table ──
    story.append(Paragraph("Candidate Rankings",
                            S("h1", fontName="Helvetica-Bold", fontSize=14, textColor=PUR, spaceAfter=8)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PUR, spaceAfter=10))

    tdata = [[Paragraph(f"<b>{h}</b>",
                        S(f"th{i}", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER))
              for i, h in enumerate(["Rank", "Name", "Sim %", "Pred %", "Final", "Status"])]]

    for rank, r in enumerate(final_results, 1):
        sc = r["final_score"]
        if sc >= 75:   sc_col = GRN;  sc_txt = "Shortlisted"
        elif sc >= 50: sc_col = ORN;  sc_txt = "Under Review"
        else:          sc_col = RD;   sc_txt = "Rejected"
        tdata.append([
            Paragraph(str(rank), S(f"ra{rank}", fontName="Helvetica-Bold", fontSize=9, alignment=TA_CENTER)),
            Paragraph(r["parsed"]["Name"], S(f"rb{rank}", fontName="Helvetica", fontSize=9)),
            Paragraph(f"{round(r['similarity_score']*100,1)}%", S(f"rc{rank}", fontName="Helvetica", fontSize=9, alignment=TA_CENTER)),
            Paragraph(f"{round(r['prediction_prob']*100,1)}%", S(f"rd{rank}", fontName="Helvetica", fontSize=9, alignment=TA_CENTER)),
            Paragraph(f"{sc}%", S(f"re{rank}", fontName="Helvetica-Bold", fontSize=10, alignment=TA_CENTER)),
            Paragraph(sc_txt, S(f"rf{rank}", fontName="Helvetica-Bold", fontSize=9, textColor=sc_col, alignment=TA_CENTER)),
        ])

    rt = Table(tdata, colWidths=[0.5*inch, 1.8*inch, 1*inch, 1*inch, 1*inch, 1.2*inch])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PUR),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID", (0,0), (-1,-1), 0.5, rl_colors.HexColor("#333")),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("BOX", (0,0), (-1,-1), 1.5, PUR),
    ]))
    story.append(rt); story.append(sp(20))

    # ── Per-Candidate Skill Detail ──
    story.append(HRFlowable(width="100%", thickness=1, color=PUR, spaceAfter=10, spaceBefore=6))
    story.append(Paragraph("Skill Analysis per Candidate",
                            S("h2", fontName="Helvetica-Bold", fontSize=13, textColor=PUR, spaceAfter=6)))

    for rank, r in enumerate(final_results, 1):
        p  = r["parsed"]; sc = r["final_score"]
        if sc >= 75:   status_str = "Shortlisted"; sc_col = GRN
        elif sc >= 50: status_str = "Under Review"; sc_col = ORN
        else:          status_str = "Rejected";     sc_col = RD

        story.append(sp(6))
        name_row = Table([[
            Paragraph(f"<b>#{rank} — {p['Name']}</b>",
                      S(f"nr{rank}", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE)),
            Paragraph(f"<b>{status_str} | {sc}%</b>",
                      S(f"ns{rank}", fontName="Helvetica-Bold", fontSize=11, textColor=sc_col, alignment=TA_CENTER)),
        ]], colWidths=[doc.width*0.65, doc.width*0.35])
        name_row.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), DARK),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (0,-1), 10),
        ]))
        story.append(name_row)

        possessed_str = ", ".join(r.get("possessed_skills", [])[:6]) or "None"
        missing_str   = ", ".join(r.get("missing_skills",   [])[:6]) or "None"
        skill_rows    = [
            [Paragraph("<b>Possessed Skills (JD Match):</b>",
                       S(f"pk{rank}", fontName="Helvetica-Bold", fontSize=8, textColor=GRN)),
             Paragraph(possessed_str,
                       S(f"pv{rank}", fontName="Helvetica", fontSize=8, textColor=rl_colors.HexColor("#aaaaaa")))],
            [Paragraph("<b>Missing Skills:</b>",
                       S(f"mk{rank}", fontName="Helvetica-Bold", fontSize=8, textColor=RD)),
             Paragraph(missing_str,
                       S(f"mv{rank}", fontName="Helvetica", fontSize=8, textColor=rl_colors.HexColor("#aaaaaa")))],
        ]
        if sc < 50 and r.get("role_suggestions"):
            roles_str = " | ".join([f"{role} ({info['match_pct']}%)" for role, info in r["role_suggestions"]])
            skill_rows.append([
                Paragraph("<b>Suggested Roles:</b>",
                          S(f"rk{rank}", fontName="Helvetica-Bold", fontSize=8, textColor=TEAL)),
                Paragraph(roles_str,
                          S(f"rv{rank}", fontName="Helvetica", fontSize=8, textColor=rl_colors.HexColor("#aaaaaa"))),
            ])

        sd_table = Table(skill_rows, colWidths=[1.6*inch, doc.width-1.6*inch])
        sd_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), LGRAY),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,-2), 0.3, rl_colors.HexColor("#333")),
        ]))
        story.append(sd_table)

    doc.build(story, onFirstPage=page_border, onLaterPages=page_border)
    buffer.seek(0)
    return buffer.read()
