import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner margins (padding) for a table cell in dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """Set background color of a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Set subtle gray borders for a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_header_table(doc, sheet_id="情 3-1"):
    """Create the standard 4-row 6-column header table exactly matching Kristy's spec."""
    table = doc.add_table(rows=4, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="555555", sz="6", val="single")
    
    col_widths = [Inches(1.0), Inches(1.5), Inches(1.0), Inches(1.8), Inches(1.0), Inches(1.2)]
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # Row 0
    table.cell(0, 0).text = "學習領域"
    table.cell(0, 1).text = "情意發展"
    table.cell(0, 2).text = "單元名稱"
    table.cell(0, 3).text = "資訊安全知多少"
    table.cell(0, 4).text = "教材編號"
    table.cell(0, 5).text = sheet_id

    # Row 1
    table.cell(1, 0).text = "資優班"
    table.cell(1, 1).text = "五年　 班"
    table.cell(1, 2).text = "學生姓名"
    table.cell(1, 3).text = ""
    table.cell(1, 4).text = "指導老師"
    table.cell(1, 5).text = "蘇佳柔"

    # Row 2
    table.cell(2, 0).text = "教學日期"
    table.cell(2, 1).text = "　年　月　日"
    table.cell(2, 2).text = "學習成績"
    table.cell(2, 3).text = ""
    table.cell(2, 4).text = "家長簽章"
    table.cell(2, 5).text = ""

    # Row 3 (merge 5 cells for criteria)
    table.cell(3, 0).text = "學習表現"
    merged = table.cell(3, 1)
    for c in range(2, 6):
        merged = merged.merge(table.cell(3, c))
    merged.text = "□準時上課　□專心認真　□踴躍發表　□創意構想　□課堂練習佳"

    # Style all cells
    label_bg = "F4F4F4"
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            
            # Label columns styling
            if c_idx in [0, 2, 4] and r_idx < 3:
                set_cell_shading(cell, label_bg)
            if r_idx == 3 and c_idx == 0:
                set_cell_shading(cell, label_bg)
                
            for run in p.runs:
                run.font.name = "標楷體"
                run._r.get_or_add_rPr().set(qn('w:rFonts'), parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="DFKai-SB" w:eastAsia="標楷體" w:hAnsi="DFKai-SB"/>'))
                run.font.size = Pt(10)
                if (c_idx in [0, 2, 4] and r_idx < 3) or (r_idx == 3 and c_idx == 0):
                    run.font.bold = True
                if r_idx == 3 and c_idx != 0:
                    run.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_outline_title(doc, title_text):
    """Add a cute large title with outline/hollow style using DFP Girl font."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    
    # Diamond / star bullet
    r_bullet = p.add_run("✦ ")
    r_bullet.font.size = Pt(22)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = RGBColor(220, 100, 50)
    
    # Outline title run
    r_title = p.add_run(title_text)
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    
    # Set font to 華康少女文字 and enable outline (鏤空)
    rPr = r_title._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="華康少女文字" w:hAnsi="華康少女文字" w:eastAsia="華康少女文字" w:cs="華康少女文字"/>')
    outline = parse_xml(f'<w:outline {nsdecls("w")}/>')
    rPr.append(rFonts)
    rPr.append(outline)

print("Helper functions ready")
