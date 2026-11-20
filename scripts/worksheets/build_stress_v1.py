"""《做壓力的主人》學習單 情3-1～3-3（學生版＋教師解答版）

用法：python build_stress_v1.py
- 以 Kristy 原學習單（D 槽 .doc）為底：保留表頭、華康鏤空標題、背包圖、花邊。
- 內文依網站 units/g5-stress-master 重寫；圓餅圖與流程圖用 PIL 重畫（教師版紅字填答）。
"""
import copy
import os
import re
import tempfile

import win32com.client
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont

SRC_DOC = r"D:\新化國小資優班\114新化國小資優班\五資\五年級情意\114.01情意\做壓力的主人\做壓力的主人.doc"
PROJECT = r"C:\2026AI_Agent\教學駕駛艙"
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
NAME = "情3-1至3-3_做壓力的主人"
FONT = "標楷體"
KAIU = r"C:\Windows\Fonts\kaiu.ttf"
RED = RGBColor(0xC0, 0x00, 0x00)
RED_PIL = (192, 0, 0)
TMP = tempfile.mkdtemp(prefix="stress_ws_")


# ───────────────────────── 原檔轉 docx ─────────────────────────
CACHE_TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache", "做壓力的主人_template.docx")


def convert_template():
    # D 槽（原始 .doc）不在時，改用本機快取的轉檔結果（_cache 不進 git）
    if not os.path.exists(SRC_DOC) and os.path.exists(CACHE_TPL):
        return CACHE_TPL
    out = os.path.join(TMP, "template.docx")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    try:
        d = word.Documents.Open(SRC_DOC, False, True)
        d.SaveAs2(out, 16)  # 保持 .doc 相容模式（改新版會讓花邊、換行全部跑掉）
        d.Close(False)
    finally:
        word.Quit()
    return out


# ───────────────────────── 圖：標題鏤空字 ─────────────────────────
TITLE_FONT = os.path.join(os.path.expanduser("~"), r"AppData\Local\Microsoft\Windows\Fonts\DFTTHBC.TTC")  # 華康海報體W12


def make_title_png(text):
    path = os.path.join(TMP, f"title_{text}.png")
    ft = ImageFont.truetype(TITLE_FONT, 300, index=1)
    im = Image.new("RGBA", (300 * len(text) + 100, 420), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    d.text((40, 40), text, font=ft, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))
    im.crop(im.getbbox()).save(path)
    return path


# ───────────────────────── 圖：壓力的警訊圓餅 ─────────────────────────
def kfont(size):
    return ImageFont.truetype(KAIU, size)


def make_pie(path, teacher):
    W = H = 1000
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    cx, cy, r = 500, 500, 470
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline="black", width=5)
    import math
    for ang in (-90, 30, 150):  # 上、右下、左下三條分隔線
        a = math.radians(ang)
        d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)], fill="black", width=5)
    lab, ans = kfont(52), kfont(44)
    # 三個區塊：標題位置、寫字線、答案
    zones = [
        ("情緒反應", (120, 250), [(110, 400, 470), (110, 490, 470), (110, 580, 470)],
         ["緊張、灰心", "恐懼、煩躁"]),
        ("生理反應", (560, 250), [(530, 400, 890), (530, 490, 890), (530, 580, 890)],
         ["手腳冰冷、冒冷汗", "肩頸痠痛、胃痛"]),
        ("疾病", (440, 690), [(260, 810, 740), (290, 900, 710)],
         ["偏頭痛、腸道發炎", "感冒、高血壓"]),
    ]
    for title, (tx, ty), lines, answers in zones:
        d.text((tx, ty), title, font=lab, fill="black")
        # 不畫書寫線（Kristy：不要線條），學生直接寫在格子裡
        if teacher:
            for (x1, y, x2), a in zip(lines, answers):
                w = d.textlength(a, font=ans)
                d.text(((x1 + x2 - w) / 2, y - 54), a, font=ans, fill=RED_PIL)
    im.save(path)


# ───────────────────────── 圖：壓力分析流程圖 ─────────────────────────
def arrow(d, p1, p2, width=6, head=26):
    import math
    d.line([p1, p2], fill="black", width=width)
    a = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    left = (p2[0] - head * math.cos(a - 0.45), p2[1] - head * math.sin(a - 0.45))
    right = (p2[0] - head * math.cos(a + 0.45), p2[1] - head * math.sin(a + 0.45))
    d.polygon([p2, left, right], fill="black")


def wrap(d, text, font, maxw):
    out, line = [], ""
    for ch in text:
        if d.textlength(line + ch, font=font) > maxw and ch not in "，。、）」；：":
            out.append(line)
            line = ch
        else:
            line += ch
    if line:
        out.append(line)
    return out


def make_flow(path, teacher):
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    lab, ans = kfont(46), kfont(42)
    boxes = {
        "role": ((10, 10, 1590, 170), "主要角色簡介：",
                 "韓信，漢朝的大將軍，很會帶兵打仗。"),
        "time": ((10, 220, 770, 330), "事件時間：", "西元前 204 年"),
        "place": ((830, 220, 1590, 330), "發生地點：", "趙國的井陘口（今河北省）"),
        "prob": ((10, 390, 690, 620), "①面臨的問題：", "趙國有 20 萬大軍，韓信只有 3 萬人"),
        "press": ((910, 390, 1590, 620), "②壓力：", "背後是河，沒有退路，只能往前"),
        "react": ((910, 670, 1590, 890), "③反應：", "士兵知道不能後退，只好拚命作戰"),
        "result": ((10, 670, 690, 890), "④結果：", "以少勝多，打敗趙國"),
    }
    for (x1, y1, x2, y2), title, a in boxes.values():
        d.rounded_rectangle([x1, y1, x2, y2], radius=36, outline="black", width=5)
        d.text((x1 + 30, y1 + 22), title, font=lab, fill="black")
        if teacher:
            tw = d.textlength(title, font=lab)
            if y2 - y1 < 150:  # 矮框：答案接在標題後面
                d.text((x1 + 30 + tw, y1 + 26), a, font=ans, fill=RED_PIL)
            else:
                for i, ln in enumerate(wrap(d, a, ans, x2 - x1 - 70)):
                    d.text((x1 + 40, y1 + 84 + i * 54), ln, font=ans, fill=RED_PIL)
    arrow(d, (390, 170), (390, 218))
    arrow(d, (1210, 170), (1210, 218))
    arrow(d, (390, 330), (350, 388))
    arrow(d, (1210, 330), (440, 388))
    arrow(d, (692, 505), (906, 505))
    arrow(d, (1250, 620), (1250, 668))
    arrow(d, (908, 780), (694, 780))
    im.save(path)


# ───────────────────────── docx 小工具 ─────────────────────────
def style_run(run, size=12, bold=False, color=None):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = parse_xml('<w:rFonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        rpr.insert(0, rfonts)
    for k in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(k), FONT)
    if color is not None:
        run.font.color.rgb = color


def fmt_par(p, before=0, after=2, line=1.15, indent=None, hanging=None, align=None):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if indent is not None:
        pf.first_line_indent = Cm(indent)
    if hanging is not None:
        pf.left_indent = Cm(hanging)
        pf.first_line_indent = Cm(-hanging)
    if align is not None:
        p.alignment = align
    # 不對齊格線，避免標楷體行距被撐大
    ppr = p._element.get_or_add_pPr()
    ppr.append(parse_xml('<w:snapToGrid xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="0"/>'))


def add_runs(p, parts, size=12):
    """parts: [(text, {'b':bool, 'red':bool})] 或字串"""
    if isinstance(parts, str):
        parts = [(parts, {})]
    for text, opt in parts:
        style_run(p.add_run(text), size=size, bold=opt.get("b", False), color=RED if opt.get("red") else None)


def para(doc, parts, size=12, **kw):
    p = doc.add_paragraph()
    fmt_par(p, **kw)
    add_runs(p, parts, size)
    return p


def heading(doc, text, size=13):
    return para(doc, [(text, {"b": True})], size=size, before=5, after=2)


def set_borders(table, show=True):
    v = "single" if show else "nil"
    xml = ('<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           + "".join(f'<w:{e} w:val="{v}" w:sz="8" w:space="0" w:color="000000"/>'
                     for e in ("top", "left", "bottom", "right", "insideH", "insideV"))
           + "</w:tblBorders>")
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    tblPr.append(parse_xml(xml))


def table(doc, rows, cols, widths, borders=True):
    t = doc.add_table(rows=rows, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_borders(t, borders)
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = Cm(widths[i])
    return t


def cell_text(cell, parts, size=12, align=None, line=1.15, after=0):
    p = cell.paragraphs[0]
    fmt_par(p, after=after, line=line, align=align)
    add_runs(p, parts, size)
    return p


def cell_par(cell, parts, size=12, align=None, line=1.15, after=0):
    p = cell.add_paragraph()
    fmt_par(p, after=after, line=line, align=align)
    add_runs(p, parts, size)
    return p


def row_height(row, cm):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(
        f'<w:trHeight xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="{int(cm * 567)}" w:hRule="atLeast"/>'))


def vcenter(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml('<w:vAlign xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="center"/>'))


def page_break(doc):
    """獨立的 1pt 段落放分頁符號，避免下一頁表頭被多擠下一行"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)
    r = p.add_run()
    r.font.size = Pt(1)
    r.add_break(WD_BREAK.PAGE)


def ans(teacher, text, blank="　"):
    """教師版紅字答案；學生版留空白"""
    return (text, {"red": True}) if teacher else (blank, {})


# ───────────────────────── 組裝 ─────────────────────────
def build(template, teacher):
    doc = Document(template)
    body = doc.element.body
    els = list(body.iterchildren())
    sect = els[-1]
    keep = {  # 原檔：表頭表格＋標題段落（含背包圖、鏤空字）＋留白段落
        1: [0, 2, 3, 4],
        2: [20, 21, 22, 24],
        3: [48, 49, 50, 51],
    }
    flower = copy.deepcopy(els[77])
    blocks = {k: [copy.deepcopy(els[i]) for i in v] for k, v in keep.items()}
    for el in els[:-1]:
        body.remove(el)

    def put_block(n):
        for el in blocks[n]:
            sect.addprevious(el)
        # 教材編號：第 3 單元（原檔是情4）
        from docx.table import Table
        code_cell = Table(blocks[n][0], doc).cell(0, 5)
        runs = [r for p in code_cell.paragraphs for r in p.runs]
        runs[0].text = f"情3-{n}"
        for r in runs[1:]:
            r.text = ""
        # 花邊：改成固定在頁面底部，掛在標題段落上
        fl = copy.deepcopy(flower)
        x = fl.xml if hasattr(fl, "xml") else None
        grp_run = fl.find(qn("w:r"))
        title_p = blocks[n][1]
        title_p.append(grp_run)
        # 標題字體：Kristy 選華康海報體W12（2026-11-19）
        # 舊式文字藝術師抓不到個人資料夾的華康字型 → 改成「文字方塊＋鏤空字效果」，字可以直接改
        TF = "華康海報體W12(P)"
        for tp in list(title_p.iter("{urn:schemas-microsoft-com:vml}textpath")):
            text = (tp.get("string") or "").strip()
            if not text:
                continue
            if text == "抗壓妙方":  # Kristy 2026-11-20 手動調整：情3-3 標題也用「做壓力的主人」
                text = "做壓力的主人"
            shp = tp.getparent()
            st = shp.get("style")
            st = re.sub(r"width:[\d.]+pt", "width:%.1fpt" % (46 * len(text) + 20), st)
            st = re.sub(r"height:[\d.]+pt", "height:62pt", st)
            st = re.sub(r"margin-top:([\d.]+)pt", lambda m: "margin-top:%.2fpt" % (float(m.group(1)) + 51 - 10), st)
            st = st.replace("mso-position-vertical-relative:text", "mso-position-vertical-relative:page")
            W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            new = parse_xml(
                f'<v:rect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="{W}" '
                f'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
                f'id="{shp.get("id")}_tb" style="{st}" filled="f" stroked="f">'
                f'<v:textbox inset="0,0,0,0"><w:txbxContent><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
                f'<w:snapToGrid w:val="0"/></w:pPr><w:r><w:rPr>'
                f'<w:rFonts w:ascii="{TF}" w:eastAsia="{TF}" w:hAnsi="{TF}"/><w:outline/><w:spacing w:val="-10"/><w:sz w:val="88"/><w:szCs w:val="88"/>'
                
                f'</w:rPr><w:t>{text}</w:t></w:r></w:p></w:txbxContent></v:textbox></v:rect>')
            shp.addprevious(new)
            shp.getparent().remove(shp)
        # 情3-3 抗壓妙方：背包男孩換成「克服壓力」圖（Gemini 依原圖畫風生成，2026-11-19）
        if n == 3:
            img = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stress_overcome.jpg")
            rid, _ = doc.part.get_or_add_image(img)
            iw, ih = Image.open(img).size
            for idata in list(title_p.iter("{urn:schemas-microsoft-com:vml}imagedata")):
                if idata.get(qn("r:id")) != "rId7":  # 只換背包男孩（rId7），不動底部花邊
                    continue
                idata.set(qn("r:id"), rid)
                shp = idata.getparent()
                hpt = 86.0
                st = re.sub(r"width:[\d.]+pt", "width:%.1fpt" % (hpt * iw / ih), shp.get("style"))
                st = re.sub(r"height:[\d.]+pt", "height:%.1fpt" % hpt, st)
                st = re.sub(r"margin-top:([\d.]+)pt", lambda m: "margin-top:%.2fpt" % (float(m.group(1)) + 2), st)
                shp.set("style", st)
        # 標題鏤空字與背包圖：改成相對頁面定位（原本相對段落，換頁後會跑掉）
        for shp in title_p.iter("{urn:schemas-microsoft-com:vml}shape"):
            st = shp.get("style") or ""
            m = re.search(r"margin-top:([\d.]+)pt", st)
            if m and "vertical-relative:text" in st:
                st = st.replace(m.group(0), "margin-top:%.2fpt" % (float(m.group(1)) + 51))
                shp.set("style", st.replace("mso-position-vertical-relative:text", "mso-position-vertical-relative:page"))
        # Kristy 2026-11-20 在 Word 裡手動微調的位置（pt），照抄進來，重新產生時才不會蓋掉
        OVR = {2: {"img": (314.2, 144.15)},
               3: {"title": (-11.05, 152.75, 264.0), "img": (280.5, 154.85)}}
        def _place(el, left, top, width=None):
            st = el.get("style")
            st = re.sub(r"margin-left:[-\d.]+pt", "margin-left:%.2fpt" % left, st)
            st = re.sub(r"margin-top:[-\d.]+pt", "margin-top:%.2fpt" % top, st)
            if width is not None:
                st = re.sub(r"width:[\d.]+pt", "width:%.1fpt" % width, st)
            el.set("style", st)
        V = "{urn:schemas-microsoft-com:vml}"
        for key, val in OVR.get(n, {}).items():
            if key == "title":
                for r in title_p.iter(V + "rect"):
                    _place(r, *val)
            else:
                for idata in title_p.iter(V + "imagedata"):
                    shp = idata.getparent()
                    if "margin-top:7" not in shp.get("style"):  # 跳過底部花邊
                        _place(shp, *val)
        # 底部花邊：原本的花朵換成紙膠帶花邊（Kristy 選 H，2026-11-20）
        washi = os.path.join(os.path.dirname(os.path.abspath(__file__)), "border_washi.jpg")
        wrid, _ = doc.part.get_or_add_image(washi)
        ww, wh = Image.open(washi).size
        # Kristy 2026-11-20 第二次手動調整：花邊對齊左邊界（各頁 left, top，單位 pt）
        WASHI_POS = {1: (0, 776.5), 2: (0, 775.5), 3: (-5.5, 775.5)}
        for g in list(title_p.iter("{urn:schemas-microsoft-com:vml}group")):
            wpt = 445.0
            new = parse_xml(
                f'<v:shape xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" '
                f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                f'id="washi_p{n}" type="#_x0000_t75" style="position:absolute;margin-left:{WASHI_POS[n][0]}pt;margin-top:{WASHI_POS[n][1]}pt;'
                f'width:{wpt:.1f}pt;height:{wpt * wh / ww:.1f}pt;z-index:-251654656;'
                f'mso-position-vertical-relative:page;mso-position-horizontal-relative:margin">'
                f'<v:imagedata r:id="{wrid}" o:title=""/></v:shape>')
            g.addprevious(new)
            g.getparent().remove(g)
        if teacher:  # 表頭「家長簽章」旁的空格標示教師版
            tbl = blocks[n][0]
            from docx.table import Table
            c = Table(tbl, doc).cell(2, 5)
            p0 = c.paragraphs[0]
            add_runs(p0, [("教師解答版", {"b": True, "red": True})], 12)
            p0.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ===================== 情4-1 認識壓力 =====================
    put_block(1)
    p = para(doc, "壓力是我們遇到挑戰時，身體和心裡進入的「備戰狀態」。先有讓你覺得有壓力的事情（壓力源），"
                  "心裡感受到壓力（壓力感），身體、心情和行為才跟著起變化（壓力反應）。壓力感的大小，取決於"
                  "「覺得自己能不能處理」和「對自己的期望有多高」。壓力太少會提不起勁，太多會慌亂出錯，"
                  "剛剛好的時候表現最好。", size=12.5, indent=0.88, line=1.2, after=0)

    heading(doc, "一、壓力三步驟：把下面三句話的代號，寫進對的格子裡")
    para(doc, "Ⓐ 我覺得好緊張，怕考不好　　Ⓑ 晚上睡不著，肚子痛　　Ⓒ 下週要段考", after=3)
    t = table(doc, 2, 5, [3.9, 1.0, 3.9, 1.0, 3.9], borders=False)
    heads = ["壓力源", "→", "壓力感", "→", "壓力反應"]
    answers = ["Ⓒ 下週要段考", "", "Ⓐ 我覺得好緊張，怕考不好", "", "Ⓑ 晚上睡不著，肚子痛"]
    for i, h in enumerate(heads):
        c0, c1 = t.cell(0, i), t.cell(1, i)
        cell_text(c0, [(h, {"b": True})], 13, align=WD_ALIGN_PARAGRAPH.CENTER)
        if h == "→":
            t.cell(0, i).merge(t.cell(1, i))
            vcenter(t.cell(0, i))
            continue
        cell_text(c1, [ans(teacher, answers[i])], 11, align=WD_ALIGN_PARAGRAPH.CENTER)
        vcenter(c1)
        for c in (c0, c1):
            tcPr = c._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(
                '<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                + "".join(f'<w:{e} w:val="single" w:sz="8" w:space="0" w:color="000000"/>' for e in ("top", "left", "bottom", "right"))
                + "</w:tcBorders>"))
    row_height(t.rows[1], 1.05)

    heading(doc, "二、壓力的警訊：把詞語庫裡的詞，寫進圓圈裡對的地方").paragraph_format.space_before = Pt(12)
    t = table(doc, 1, 2, [10.8, 4.4], borders=False)
    pie = os.path.join(TMP, f"pie_{int(teacher)}.png")
    make_pie(pie, teacher)
    cp = t.cell(0, 0).paragraphs[0]
    fmt_par(cp, after=0, line=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    cp.add_run().add_picture(pie, width=Cm(10.2))
    bank = t.cell(0, 1)
    vcenter(bank)
    inner = bank.add_table(rows=1, cols=1)
    set_borders(inner, True)
    ic = inner.cell(0, 0)
    ic.width = Cm(4.2)
    cell_text(ic, [("詞語庫", {"b": True})], 13, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)
    for words in ["緊張　　灰心", "恐懼　　煩躁", "手腳冰冷　冒冷汗", "肩頸痠痛　胃痛", "偏頭痛　腸道發炎", "感冒　　高血壓"]:
        cell_par(ic, words, 13, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.5)
    bank.paragraphs[0].paragraph_format.space_after = Pt(0)
    page_break(doc)

    # ===================== 情4-2 壓力也能是助力 =====================
    put_block(2)
    para(doc, "世界上許多知名人物都是在壓力中成長。古代的韓信、曹操、伍子胥，現代的麟洋配、薩利機長，"
              "都在壓力下發揮出能力。", size=12.5, indent=0.88, line=1.2)
    heading(doc, "一、連連看：他們在壓力下發揮了哪一種能力？")
    # 連連看：說明縮短，左右兩排圓點中間留約 4 公分好畫線（Kristy：原本太擠很難連）
    people = [("韓信", "背水列陣，沒有退路", "勇往直前"),
              ("曹操", "被發現，立刻改口獻刀", "急中生智"),
              ("伍子胥", "逃亡怕被發現，特別警覺", "風吹草動也察覺"),
              ("麟洋配", "衛冕壓力下拚到最後一球", "勇往直前"),
              ("薩利機長", "引擎熄火，迫降河上", "急中生智")]
    t = table(doc, 5, 4, [7.0, 0.8, 3.1, 4.3], borders=False)
    for i, (who, what, a) in enumerate(people):
        cell_text(t.cell(i, 0), [(f"{who}：", {"b": True}), (what, {})], 12, line=1.2)
        cell_text(t.cell(i, 1), [("●", {})], 12, align=WD_ALIGN_PARAGRAPH.CENTER)
        if teacher:
            cell_text(t.cell(i, 2), [(a, {"red": True})], 10, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(3):
            vcenter(t.cell(i, c))
        row_height(t.rows[i], 0.95)
    for i, a in [(0, "勇往直前"), (2, "急中生智"), (4, "風吹草動也察覺")]:
        cell_text(t.cell(i, 3), [("● " + a, {"b": True})], 12)
        vcenter(t.cell(i, 3))

    # （壓力分析流程圖已依 Kristy 要求拿掉，make_flow 保留備用）
    heading(doc, "二、壓力也讓我變厲害：照著提示，寫下你的經驗", 13).paragraph_format.space_before = Pt(16)
    para(doc, "想一想：有沒有一次，你因為有壓力，反而讓自己進步了？", size=12, after=6)
    R = lambda t: (t, {"red": True})
    box = lambda on: "■" if (teacher and on) else "□"
    L = 1.9
    para(doc, [("1. 那時候我遇到：", {"b": True}),
               (f"{box(False)}考試　{box(True)}比賽　{box(False)}上台報告　{box(False)}其他＿＿＿＿＿＿", {})],
         after=0, line=L)
    para(doc, [("　 事情是：", {})] + ([R("三年級第一次參加朗讀比賽")] if teacher else [("＿" * 27, {})]), after=0, line=L)
    para(doc, [("2. 我當時的感覺：", {"b": True}),
               (f"{box(True)}緊張　{box(False)}害怕　{box(True)}擔心　{box(False)}其他＿＿＿＿＿＿", {})],
         after=0, line=L)
    para(doc, [("3. 我做了什麼：", {"b": True})] + ([R("每天對著鏡子練習，請家人當聽眾")] if teacher else [("＿" * 26, {})]),
         after=0, line=L)
    if not teacher:
        para(doc, "　 " + "＿" * 33, after=0, line=L)
    para(doc, [("4. 後來我學會了／變厲害的地方：", {"b": True})] + ([R("上台說話比較不怕了")] if teacher else [("＿" * 18, {})]),
         after=0, line=L)
    if not teacher:
        para(doc, "　 " + "＿" * 33, after=0, line=L)
    para(doc, [("5. 這件事讓我知道，壓力可以：", {"b": True}),
               (f"{box(True)}更努力 {box(False)}更專心 {box(False)}想出好辦法 {box(False)}其他＿＿＿", {})],
         after=0, line=L, size=12)
    if teacher:
        para(doc, [R("（說出遇到的壓力、用的方法、學到的能力即可；勾選題可以多選）")], after=0, line=1.6)
    page_break(doc)

    # ===================== 情4-3 抗壓妙方 =====================
    put_block(3)
    heading(doc, "一、抗壓妙方五招", 13).paragraph_format.space_before = Pt(0)
    tips = [("1.找出原因，解決問題：", "換個想法，例如「即使我拒絕，我們依然能做朋友」。"),
            ("2.建立合理期望：", "量力而行，不必事事完美；拒絕超載，不答應太多事。"),
            ("3.提升處事能力：", "用輕重緩急排次序；把複雜的任務分解成小步驟。"),
            ("4.建立支援網：", "找人說出來，壓力會變小；接受別人的幫忙。"),
            ("5.健康的生活習慣：", "運動、均衡飲食、睡飽，留時間休息和做喜歡的事。")]
    for h, txt in tips:
        para(doc, [(h, {"b": True}), (txt, {})], hanging=0.55, after=0, line=1.15)

    heading(doc, "二、輕重緩急：把這週待辦事項的代號，寫進對的格子")
    para(doc, "Ⓐ 明天要交的數學作業　Ⓑ 下週五的專題報告　Ⓒ 下個月的科展", after=0, line=1.2)
    para(doc, "Ⓓ 今天要還圖書館的書　Ⓔ 同學傳訊息問要不要上線玩遊戲　Ⓕ 整理書桌抽屜", after=3, line=1.2)
    t = table(doc, 2, 2, [7.6, 7.6])
    quad = [("重要又緊急（第 1 個做）", "Ⓐ"), ("重要但不急（排時間做）", "Ⓑ Ⓒ"),
            ("緊急但不太重要（快速處理）", "Ⓓ Ⓔ"), ("不急也不太重要（最後做）", "Ⓕ")]
    for k, (h, a) in enumerate(quad):
        c = t.cell(k // 2, k % 2)
        cell_text(c, [(h, {"b": True})], 12)
        cell_par(c, [ans(teacher, a)], 13, align=WD_ALIGN_PARAGRAPH.CENTER)
    for r in t.rows:
        row_height(r, 1.1)

    heading(doc, "三、用哪一招？在（　）裡寫上招式的編號 1～5")
    cases = [("阿凱的科展報告好複雜，不知道從哪裡開始。", "3"),
             ("小恩被同學排擠，不敢跟任何人說。", "4"),
             ("小琪覺得「一定要答應朋友，才不會被討厭」，常常勉強自己。", "1"),
             ("大宇每天滑手機到半夜，白天沒精神、心情很差。", "5"),
             ("小芸參加 4 個社團、2 個比賽，每天寫作業到 11 點。", "2")]
    for txt, a in cases:
        para(doc, [("（", {}), ans(teacher, a.center(2, " "), "　 "), ("）", {}), (txt, {})], after=0, line=1.25)

    heading(doc, "四、我的抗壓計畫")
    if teacher:
        plan = [("我的壓力：", "專題報告快來不及了"), ("屬於：", "■課業　□人際　□家庭　□自己　□3C 與社群"),
                ("我要用第（ 3 ）招：", "分解步驟，每天做一小段"), ("我可以求助的人：", "導師")]
        para(doc, [(plan[0][0], {}), (plan[0][1], {"red": True}), ("　（", {}), ("課業", {"red": True}),
                   ("）", {})], after=0, line=1.35)
        para(doc, [("我要用第（", {}), (" 3 ", {"red": True}), ("）招：", {}), (plan[2][1], {"red": True}),
                   ("（招式對得上壓力即可）", {"red": True})], after=0, line=1.35)
    else:
        para(doc, "我的壓力：＿＿＿＿＿＿＿＿＿＿（□課業 □人際 □家庭 □自己 □3C與社群）", after=0, line=1.35)
        para(doc, "我要用第（　）招：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", after=0, line=1.35)

    # 結語（呼應網站開場「壓力像風，也能讓風箏飛得更高」）
    sp = doc.add_paragraph()
    fmt_par(sp, after=0, line=1.0)
    sp.paragraph_format.space_before = Pt(6)
    t = table(doc, 1, 1, [15.2])
    c = t.cell(0, 0)
    cell_text(c, [("結語：", {"b": True}),
                  ("壓力就像風，風剛剛好，風箏才能飛得又高又穩。遇到壓力時，找出原因、量力而行、"
                   "排好次序、找人說說話、照顧好身體，你就是壓力的主人！", {})], 12.5, line=1.4, after=0)
    return doc


def to_pdf(docx_path):
    pdf = os.path.splitext(docx_path)[0] + ".pdf"
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    try:
        d = word.Documents.Open(docx_path, False, True)
        pages = d.ComputeStatistics(2)
        d.ExportAsFixedFormat(pdf, 17)
        d.Close(False)
    finally:
        word.Quit()
    return pdf, pages


if __name__ == "__main__":
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else PROJECT
    tpl = convert_template()
    for teacher, suffix in [(False, "學生版"), (True, "教師解答版")]:
        path = os.path.join(out_dir, f"{NAME}_{suffix}.docx")
        build(tpl, teacher).save(path)
        pdf, pages = to_pdf(path)
        print(suffix, "pages =", pages, path)
