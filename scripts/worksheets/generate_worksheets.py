import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client

def create_worksheet(output_path, is_teacher=False):
    doc = Document()
    
    # Page setup: A4, tight margins (0.45 in / 1.15 cm top/bottom, 0.55 in left/right)
    for s in doc.sections:
        s.top_margin = Inches(0.42)
        s.bottom_margin = Inches(0.42)
        s.left_margin = Inches(0.55)
        s.right_margin = Inches(0.55)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        
    def set_font(run, font_name="標楷體", size_pt=9.5, bold=False, color_rgb=None, outline=False):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        if color_rgb:
            run.font.color.rgb = color_rgb
        rPr = run._r.get_or_add_rPr()
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:eastAsia="{font_name}" w:hAnsi="{font_name}"/>')
        rPr.append(rFonts)
        if outline:
            rPr.append(parse_xml(f'<w:outline {nsdecls("w")}/>'))

    def set_cell_margins(cell, top=35, bottom=35, left=65, right=65):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_shd(cell, color_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        tcPr.append(shd)

    def set_table_borders(table, color="666666", sz="4", val="single"):
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

    def add_header(sheet_id):
        table = doc.add_table(rows=4, cols=6)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="333333", sz="5", val="single")
        
        col_w = [Inches(0.95), Inches(1.35), Inches(0.95), Inches(1.8), Inches(0.95), Inches(1.17)]
        for row in table.rows:
            for idx, w in enumerate(col_w):
                row.cells[idx].width = w

        data = [
            [("學習領域", True), ("情意發展", False), ("單元名稱", True), ("資訊安全知多少", False), ("教材編號", True), (sheet_id, True)],
            [("資優班", True), ("五年　 班", False), ("學生姓名", True), ("", False), ("指導老師", True), ("蘇佳柔", False)],
            [("教學日期", True), ("　年　月　日", False), ("學習成績", True), ("", False), ("家長簽章", True), ("", False)],
            [("學習表現", True), ("□準時上課　□專心認真　□踴躍發表　□創意構想　□課堂練習佳", False)]
        ]

        for r_idx in range(3):
            for c_idx in range(6):
                txt, is_lbl = data[r_idx][c_idx]
                cell = table.cell(r_idx, c_idx)
                cell.text = txt
                if is_lbl:
                    set_cell_shd(cell, "F2F2F2")

        # Row 3 merge
        table.cell(3, 0).text = data[3][0][0]
        set_cell_shd(table.cell(3, 0), "F2F2F2")
        merged = table.cell(3, 1)
        for c in range(2, 6):
            merged = merged.merge(table.cell(3, c))
        merged.text = data[3][1][0]

        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                set_cell_margins(cell, top=40, bottom=40, left=70, right=70)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                for run in p.runs:
                    is_b = (c_idx in [0, 2, 4] and r_idx < 3) or (r_idx == 3 and c_idx == 0) or (r_idx == 0 and c_idx == 5)
                    set_font(run, "標楷體", size_pt=9 if r_idx == 3 and c_idx != 0 else 9.5, bold=is_b)

    def add_outline_title(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        
        r_ico = p.add_run("✦ ")
        set_font(r_ico, "微軟正黑體", size_pt=18, bold=True, color_rgb=RGBColor(230, 100, 30))
        
        r_t = p.add_run(title_text)
        set_font(r_t, "華康少女文字", size_pt=20, bold=True, outline=True)

    def add_concept_box(text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(7.17)
        set_cell_shd(cell, "F7F9FA")
        set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
        
        tblPr = tbl._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="20" w:space="0" w:color="2B6CB0"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run("❖ 核心概念： " + text)
        set_font(r, "微軟正黑體", size_pt=9, bold=False, color_rgb=RGBColor(40, 60, 80))

    def add_section_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        
        r1 = p.add_run(f"【{num_str}】")
        set_font(r1, "微軟正黑體", size_pt=10.5, bold=True, color_rgb=RGBColor(43, 108, 176))
        r2 = p.add_run(f" {title_str}")
        set_font(r2, "微軟正黑體", size_pt=10.5, bold=True, color_rgb=RGBColor(30, 30, 30))

    # ================= PAGE 1: 情 3-1 =================
    add_header("情 3-1")
    add_outline_title("資訊安全知多少：資料變寶藏")
    add_concept_box("所謂「資訊」，就是將分散零碎的「資料」經過有系統的記錄、整理、統計與分析之後，從中獲得可以用來作為判斷或行動依據的寶藏！")

    add_section_heading("任務一", "解開 DIKW 知識金字塔（由下而上四個智慧階梯）")
    
    pyr_table = doc.add_table(rows=5, cols=4)
    pyr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(pyr_table, color="A0AEC0", sz="4", val="single")
    
    col_w_pyr = [Inches(1.0), Inches(1.25), Inches(2.7), Inches(2.22)]
    for row in pyr_table.rows:
        for idx, w in enumerate(col_w_pyr):
            row.cells[idx].width = w

    headers = ["階層位置", "要素名稱", "意義與定義", "生活實例（以健康中心為例）"]
    for c_idx, h in enumerate(headers):
        cell = pyr_table.cell(0, c_idx)
        cell.text = h
        set_cell_shd(cell, "E2E8F0")

    pyr_data = [
        ("最頂層", "智慧 (Wisdom)", "做出最佳的決策、前瞻判斷與具體行動", "例：健康中心啟動全班消毒、通報校安並宣導戴口罩"),
        ("第三層", "知識 (Knowledge)", "歸納理解背後的原因、模式與因果關聯", "例：理解流感高發期伴隨發燒咳嗽，具群聚傳染風險"),
        ("第二層", "資訊 (Information)", "加上脈絡、時間與情境，產生明確意義", "例：小華在校體溫連續兩天測得 38.5℃，開始發燒"),
        ("最底層", "資料 (Data)", "客觀未經處理的原始數字、文字或符號", "例：38.5、小華、09:00（單純的數字與代號）")
    ]

    for r_idx, (pos, name, desc, ex) in enumerate(pyr_data, start=1):
        c0 = pyr_table.cell(r_idx, 0)
        c1 = pyr_table.cell(r_idx, 1)
        c2 = pyr_table.cell(r_idx, 2)
        c3 = pyr_table.cell(r_idx, 3)

        c0.text = pos
        set_cell_shd(c0, "F8FAFC")
        
        if is_teacher:
            c1.text = name
            c2.text = desc
            c3.text = ex
        else:
            if r_idx in [1, 3]: # Wisdom & Information blanked for student
                c1.text = "（　　　　）\n" + ("(Wisdom)" if r_idx == 1 else "(Information)")
            else:
                c1.text = name
            c2.text = desc
            c3.text = ex

    for row in pyr_table.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=30, bottom=30, left=55, right=55)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            for run in p.runs:
                set_font(run, "微軟正黑體", size_pt=8.5, bold=False)

    for cell in pyr_table.rows[0].cells:
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(20, 50, 80)

    # Detective Creative Challenge
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("★ 資優思考題：換你當偵探！學校舉辦「運動會大隊接力」，請寫出一個從資料轉變為智慧的例子：")
    set_font(r_sub, "微軟正黑體", size_pt=9, bold=True, color_rgb=RGBColor(180, 70, 20))

    tbl_ex = doc.add_table(rows=2, cols=4)
    tbl_ex.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ex, color="CBD5E0", sz="4", val="single")
    for row in tbl_ex.rows:
        for idx, w in enumerate([Inches(1.79), Inches(1.79), Inches(1.79), Inches(1.79)]):
            row.cells[idx].width = w
    
    ex_headers = ["1. 資料 (Data)", "2. 資訊 (Information)", "3. 知識 (Knowledge)", "4. 智慧 (Wisdom)"]
    for i, h in enumerate(ex_headers):
        tbl_ex.cell(0, i).text = h
        set_cell_shd(tbl_ex.cell(0, i), "EDF2F7")
        for run in tbl_ex.cell(0, i).paragraphs[0].runs:
            set_font(run, "微軟正黑體", size_pt=8.5, bold=True)
            
    if is_teacher:
        teacher_answers = [
            "【參考答案】\n全班 100m 測驗秒數（如：14.2s, 15.1s）",
            "【參考答案】\n分析出誰跑得快、誰在彎道跑得最好",
            "【參考答案】\n發現前四棒領先能提升士氣、排棒順序影響總秒數",
            "【參考答案】\n排定最佳棒次名單與接棒策略，在決賽奪冠！"
        ]
        for i, ans in enumerate(teacher_answers):
            tbl_ex.cell(1, i).text = ans
            for run in tbl_ex.cell(1, i).paragraphs[0].runs:
                set_font(run, "微軟正黑體", size_pt=8, bold=False, color_rgb=RGBColor(160, 40, 40))
    else:
        for i in range(4):
            tbl_ex.cell(1, i).text = "\n\n"

    for row in tbl_ex.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=30, bottom=30, left=50, right=50)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    add_section_heading("任務二", "賈資安偵探事務所（影片觀後心得與思考）")
    
    tbl_v = doc.add_table(rows=2, cols=1)
    tbl_v.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_v, color="CBD5E0", sz="4", val="single")
    tbl_v.cell(0, 0).width = Inches(7.17)
    tbl_v.cell(1, 0).width = Inches(7.17)

    p_v1 = tbl_v.cell(0, 0).paragraphs[0]
    p_v1.paragraph_format.line_spacing = 1.05
    p_v1.add_run("1. 在《資安偵探》影片中，偵探遇到了什麼資安危機？他是如何冷靜解決問題的？\n")
    if is_teacher:
        r_ans = p_v1.add_run("【參考答案】例如面對可疑釣魚郵件或勒索危機，不慌張隨意點擊連結，而是先切斷網路、查驗寄件者真實網址，並利用備份檔案與多重驗證化解危機。")
        set_font(r_ans, "微軟正黑體", size_pt=8.5, color_rgb=RGBColor(160, 40, 40))
    else:
        p_v1.add_run("\n")

    p_v2 = tbl_v.cell(1, 0).paragraphs[0]
    p_v2.paragraph_format.line_spacing = 1.05
    p_v2.add_run("2. 看完影片後，請寫下一句你最想提醒家人或同學的「資安金句」：\n")
    if is_teacher:
        r_ans2 = p_v2.add_run("【參考答案】「密碼要長不重複，雙重驗證加道鎖；不明連結莫點開，先停先問多查證！」")
        set_font(r_ans2, "微軟正黑體", size_pt=8.5, color_rgb=RGBColor(160, 40, 40))
    else:
        p_v2.add_run("\n")

    for row in tbl_v.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=35, bottom=35, left=65, right=65)
            for run in cell.paragraphs[0].runs:
                if not run.font.color.rgb:
                    set_font(run, "微軟正黑體", size_pt=8.5, bold=False)

    # ================= PAGE 2: 情 3-2 =================
    doc.add_page_break()
    add_header("情 3-2")
    add_outline_title("資訊安全知多少：個資保衛戰")
    add_concept_box("資訊安全的核心，在於守護資訊的三把安全鎖（CIA 三要素），並建立良好的個人數位防護習慣！")

    add_section_heading("任務一", "守護資訊的三把安全鎖（CIA 三要素情境配對）")

    tbl_cia = doc.add_table(rows=4, cols=3)
    tbl_cia.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cia, color="A0AEC0", sz="4", val="single")
    for row in tbl_cia.rows:
        row.cells[0].width = Inches(1.5)
        row.cells[1].width = Inches(2.6)
        row.cells[2].width = Inches(3.07)

    for i, h in enumerate(["安全鎖 (CIA 要素)", "核心意義與守護目標", "生活真實威脅案例（請配對）"]):
        tbl_cia.cell(0, i).text = h
        set_cell_shd(tbl_cia.cell(0, i), "E2E8F0")

    cia_rows = [
        ("1. 機密性\n(Confidentiality)", "只有經授權的人才能看到資料，防止外洩與偷窺。", "【情境甲】同學偷拍他人私密日記或成績單，並上傳到未設限的公開社群。"),
        ("2. 完整性\n(Integrity)", "確保資料在傳輸與保存中正確無誤，未被竄改或造假。", "【情境乙】惡作劇同學偷偷駭入學校運動會報名表，把別人的參賽項目亂改。"),
        ("3. 可用性\n(Availability)", "合法使用者在需要時，系統能隨時順暢運作與存取。", "【情境丙】駭客用海量封包癱瘓學校線上選課伺服器（DDoS），導致所有人無法登入。")
    ]

    for r_idx, (lock, mean, situ) in enumerate(cia_rows, start=1):
        c0 = tbl_cia.cell(r_idx, 0)
        c1 = tbl_cia.cell(r_idx, 1)
        c2 = tbl_cia.cell(r_idx, 2)
        c0.text = lock
        set_cell_shd(c0, "F8FAFC")
        c1.text = mean
        if is_teacher:
            match_letter = ["甲", "乙", "丙"][r_idx-1]
            c2.text = f"✔ 正確配對：【情境{match_letter}】\n" + situ
        else:
            c2.text = "對應情境：【　　】\n" + situ

    for row in tbl_cia.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=18, bottom=18, left=50, right=50)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            for run in p.runs:
                set_font(run, "微軟正黑體", size_pt=8, bold=False)

    for cell in tbl_cia.rows[0].cells:
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(20, 50, 80)

    add_section_heading("任務二", "保護個資全新升級「現代 7 大妙招」（寫出具體防護行動）")

    tbl_7 = doc.add_table(rows=8, cols=3)
    tbl_7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_7, color="CBD5E0", sz="4", val="single")
    for row in tbl_7.rows:
        row.cells[0].width = Inches(0.75)
        row.cells[1].width = Inches(1.7)
        row.cells[2].width = Inches(4.72)

    tbl_7.cell(0, 0).text = "編號"
    tbl_7.cell(0, 1).text = "現代守則口訣"
    tbl_7.cell(0, 2).text = "現代資安具體做法與重要觀念（請簡要填答）"
    for i in range(3):
        set_cell_shd(tbl_7.cell(0, i), "EDF2F7")

    rules_7 = [
        ("第 1 招", "密碼要長不重複", 
         "改用 12~16 字以上「長密語」（隨機多詞組合）；不同網站絕不共用密碼！",
         "改用 12~16 字以上長密語；每個帳號使用不同密碼。"),
        ("第 2 招", "雙重驗證加道鎖", 
         "開啟雙重驗證（2FA/MFA，密碼＋手機驗證碼），即使密碼外洩也登不進！",
         "開啟雙重驗證（2FA/MFA），結合密碼與手機驗證碼。"),
        ("第 3 招", "螢幕鎖定隨手鎖", 
         "離開座位養成按【Win+L】鎖定習慣；手機平板設定螢幕自動鎖定與密碼。",
         "離開座位隨手按【Win+L】鎖定螢幕；手機設密碼。"),
        ("第 4 招", "公用設備必登出", 
         "公用電腦用畢務必手動點「登出」並關閉無痕；不使用不明公用充電孔。",
         "公用電腦使用完畢一律手動「登出」；不亂插充電孔。"),
        ("第 5 招", "公共網路莫亂連", 
         "不任意連線未設密碼的免費公用 Wi-Fi，防範帳密封包遭基地台側錄。",
         "不連線無加密的免費公用 Wi-Fi，改用行動網路。"),
        ("第 6 招", "好康換獎全多詐", 
         "免費送遊戲點數、造型虛寶或轉傳抽獎，絕不提供姓名電話與帳密！",
         "免費虛寶與抽獎多為詐騙個資陷阱，絕不隨便填寫。"),
        ("第 7 招", "陌生要求先查證", 
         "好友突然借帳號、要驗證碼或怪連結，先以電話當面查證；防詐撥 165！",
         "好友借帳號或要驗證碼，先打電話向本人確認；撥 165。")
    ]

    for idx, (no, motto, full_desc, short_ans) in enumerate(rules_7, start=1):
        c0 = tbl_7.cell(idx, 0)
        c1 = tbl_7.cell(idx, 1)
        c2 = tbl_7.cell(idx, 2)
        c0.text = no
        set_cell_shd(c0, "F8FAFC")
        c1.text = motto
        set_cell_shd(c1, "F0F4F8")
        
        if is_teacher:
            c2.text = "【參考解答】" + full_desc
            for r in c2.paragraphs[0].runs:
                set_font(r, "微軟正黑體", size_pt=7.5, color_rgb=RGBColor(160, 40, 40))
        else:
            c2.text = "做法重點：" + short_ans + "\n請寫下具體行動："

    for row in tbl_7.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=14, bottom=14, left=45, right=45)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            for run in p.runs:
                if not run.font.color.rgb:
                    set_font(run, "微軟正黑體", size_pt=7.5, bold=False)

    for cell in tbl_7.rows[0].cells:
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(20, 50, 80)

    # Detective Challenge Case
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(2)
    p_ch.paragraph_format.space_after = Pt(1)
    r_ch = p_ch.add_run("★ 資安偵探出任務（個資漏洞抓錯）：")
    set_font(r_ch, "微軟正黑體", size_pt=8.5, bold=True, color_rgb=RGBColor(180, 70, 20))

    tbl_ch = doc.add_table(rows=1, cols=1)
    tbl_ch.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ch, color="CBD5E0", sz="4", val="single")
    tbl_ch.cell(0, 0).width = Inches(7.17)
    set_cell_margins(tbl_ch.cell(0, 0), top=25, bottom=25, left=55, right=55)
    
    p_case = tbl_ch.cell(0, 0).paragraphs[0]
    p_case.paragraph_format.line_spacing = 1.0
    p_case.add_run("【情境】小美發文：「拿到日本機票囉！（附清楚機票條碼與護照照片，打卡『我家』，寫著全家出國七天！）」\n")
    if is_teacher:
        r_ans3 = p_case.add_run("【參考解答】1. 機票條碼與護照：可掃出旅客個資與訂位代碼恐被退改票。對策：票券條碼務必遮蔽。\n"
                               "2. 打卡住家：暴露精確住址。對策：不即時打卡。 3. 宣告全家出國七天：唱空城計引竊賊。對策：回國後再分享。")
        set_font(r_ans3, "微軟正黑體", size_pt=7.5, color_rgb=RGBColor(160, 40, 40))
    else:
        p_case.add_run("請圈出貼文中的 3 個個資威脅，並寫出對策：\n1. 機票條碼：\n2. 打卡住家：\n3. 宣告出國：")

    for run in tbl_ch.cell(0, 0).paragraphs[0].runs:
        if not run.font.color.rgb:
            set_font(run, "微軟正黑體", size_pt=8, bold=False)

    doc.save(output_path)
    print(f"Saved: {output_path}")

out_dir = r"c:\2026AI_Agent\教學駕駛艙"
create_worksheet(os.path.join(out_dir, "資安偵探任務學習單_情3-1情3-2_學生版.docx"), is_teacher=False)
create_worksheet(os.path.join(out_dir, "資安偵探任務學習單_情3-1情3-2_教師解答版.docx"), is_teacher=True)
