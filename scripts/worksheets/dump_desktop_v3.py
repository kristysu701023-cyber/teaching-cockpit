import docx

doc = docx.Document(r'C:\Users\user\Desktop\情2-1至2-2_性別平等_兩頁版v3.docx')

lines = []
lines.append("=== SECTIONS ===")
for i, s in enumerate(doc.sections):
    lines.append(f"Section {i}: Top={s.top_margin.pt}pt, Bottom={s.bottom_margin.pt}pt, Left={s.left_margin.pt}pt, Right={s.right_margin.pt}pt")

lines.append("\n=== PARAGRAPHS & TABLES IN ORDER ===")
for elem in doc.element.body:
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(elem, doc)
        txt = p.text.strip()
        if txt:
            runs_info = []
            for r in p.runs:
                runs_info.append(f"[{r.text}|{r.font.name}|{r.font.size.pt if r.font.size else 'None'}pt|b={r.bold}]")
            lines.append(f"P: {''.join(runs_info)}")
    elif tag == 'tbl':
        tbl = docx.table.Table(elem, doc)
        lines.append(f"\n--- TABLE ({len(tbl.rows)}x{len(tbl.columns)}) ---")
        for r_idx, r in enumerate(tbl.rows):
            row_cells = []
            for c_idx, c in enumerate(r.cells):
                cell_txt = []
                for p in c.paragraphs:
                    p_txt = []
                    for run in p.runs:
                        p_txt.append(f"{run.text}({run.font.name},{run.font.size.pt if run.font.size else 'def'}pt,b={run.bold})")
                    cell_txt.append("".join(p_txt))
                row_cells.append("\n".join(cell_txt))
            lines.append(f"  R{r_idx}: " + " | ".join(row_cells))

with open(r'c:\2026AI_Agent\教學駕駛艙\desktop_v3_structure.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print("Dumped structure successfully")
