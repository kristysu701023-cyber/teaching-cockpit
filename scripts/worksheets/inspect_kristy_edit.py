import docx
import os

desktop = r"C:\Users\user\Desktop"
target = None
for f in os.listdir(desktop):
    if "無愛心" in f and f.endswith(".docx"):
        target = os.path.join(desktop, f)
        break

if target:
    doc = docx.Document(target)
    print(f"File: {target}")
    print(f"Paragraphs: {len(doc.paragraphs)}, Tables: {len(doc.tables)}")
    
    with open(r"c:\2026AI_Agent\教學駕駛艙\kristy_edited_text.txt", "w", encoding="utf-8") as out:
        out.write("=== PARAGRAPHS ===\n")
        for i, p in enumerate(doc.paragraphs):
            if p.text.strip():
                out.write(f"P{i}: {p.text.strip()}\n")
                
        out.write("\n=== TABLES ===\n")
        for t_idx, t in enumerate(doc.tables):
            out.write(f"\n--- TABLE {t_idx} ({len(t.rows)}x{len(t.columns)}) ---\n")
            for r_idx, r in enumerate(t.rows):
                row_str = " | ".join([c.text.strip().replace('\n', ' ') for c in r.cells])
                out.write(f"R{r_idx}: {row_str}\n")
    print("Exported kristy_edited_text.txt")
