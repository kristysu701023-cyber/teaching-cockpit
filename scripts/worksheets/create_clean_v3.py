import docx
import zipfile
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor

def create_cyber_docx(output_path, is_teacher=False):
    src_path = r"C:\Users\user\Desktop\情2-1至2-2_性別平等_兩頁版v3.docx"
    doc = Document(src_path)

    # 1. Update Table 0 & Table 5 (Headers)
    for t_idx in [0, 5]:
        t = doc.tables[t_idx]
        t.cell(0, 3).text = "資訊安全知多少"
        t.cell(0, 5).text = "情 2-1" if t_idx == 0 else "情 2-2"
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    for run in p.runs:
                        run.font.name = "標楷體"
                        run.font.size = Pt(12)

    # 2. Page 1: Story Box (Table 2)
    t2_cell = doc.tables[2].cell(0, 0)
    t2_cell.text = (
        "現代生活中，我們天天使用電腦、平板與手機，查資料、看影片、玩線上遊戲。"
        "但你知道嗎？分散零碎的「資料」經過有系統的記錄、整理與分析之後，就會轉化為巨大的「資訊力量」！"
        "如果這些重要資訊缺乏安全防護，遭人竊取、竄改或惡意破壞，就會引發嚴重的資安危機。"
        "為了發揮資訊的最大價值，保護資訊的安全就成了每個人必備的數位超能力。"
    )
    for p in t2_cell.paragraphs:
        for run in p.runs:
            run.font.name = "標楷體"
            run.font.size = Pt(12)

    # 3. Page 1: Prompt Question (Paragraph)
    for p in doc.paragraphs:
        if "★ 如果你是" in p.text:
            p.text = "★ 如果你是學校的資安小偵探，你平時會注意哪些資訊不被他人偷看或外洩？"
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(12)
                run.font.bold = True
        elif "1. 所謂「性別刻板印象」" in p.text:
            p.text = "1. 所謂「資訊」，就是將客觀原始的「資料」經過整理、統計與分析後，轉化為可用來判斷或行動的依據。解開 DIKW 知識金字塔的四個智慧階梯："
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(12)
        elif "2. 「性別」指的是生理上的差異" in p.text:
            p.text = (
                "2. 資訊安全的三大核心（CIA 三把安全鎖）：機密性（只有經授權的人能看到）、"
                "完整性（資料正確未被竄改）、可用性（需要時能隨時順暢使用）。"
                "在日常生活或學校中，你認為哪一把鎖最容易被大家忽略？為什麼？請說說你的看法。"
            )
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(12)

    # 4. Page 1: Table 4 (DIKW Table)
    t4 = doc.tables[4]
    t4_data = [
        ("階梯名稱與定義", "生活實例（健康中心）", "生活偵探推理（大隊接力）"),
        ("智慧 (Wisdom)\n最佳決策與行動", "啟動全校消毒、通報校安並宣導戴口罩", "【排定棒次奪冠】\n依選手優勢排定最佳棒次與策略" if is_teacher else "\n\n"),
        ("知識 (Knowledge)\n理解原因與規律", "理解流感流行期發燒伴隨咳嗽具傳染性", "【分析優勢規律】\n分析誰起跑快、誰過彎最強" if is_teacher else "\n\n"),
        ("資訊 (Information)\n加上情境與脈絡", "小華體溫連續兩天測得 38.5℃，開始發燒", "【測出選手秒數】\n測出全班每位選手 100m 跑步秒數" if is_teacher else "\n\n")
    ]
    for r_idx, row_vals in enumerate(t4_data):
        for c_idx, val in enumerate(row_vals):
            cell = t4.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(11 if r_idx > 0 else 12)
                if r_idx == 0:
                    run.font.bold = True
                elif is_teacher and c_idx == 2:
                    run.font.color.rgb = RGBColor(180, 40, 40)

    # 5. Page 2: Paragraphs
    for p in doc.paragraphs:
        if "生活中，我們常聽到「男生應該" in p.text:
            p.text = "生活中，我們天天在網路上傳訊息、玩遊戲、看限時動態……"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
        elif "這樣的話。這些話，會不會悄悄限制了我們？" in p.text:
            p.text = "但你知道嗎？有些看似平常的小動作，會不會悄悄把你的個資送給了陌生人？"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
        elif "一、這些話你聽過嗎？" in p.text:
            p.text = "一、這些情況你遇過嗎？"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
                r.font.bold = True
        elif "聽過的在 □ 裡打 ✓" in p.text:
            p.text = "遇過的在 □ 裡打 ✓；再把你覺得最危險的一項圈起來。"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(11)
        elif "我圈的這句話，限制了：" in p.text:
            p.text = "我圈的這項，最容易洩漏：　□ 帳號與密碼　　□ 私人住址與行程　　□ 個人隱私與錢財"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
        elif "二、家事小表" in p.text:
            p.text = "二、守護個資全新 7 大妙招（自我檢核表）"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
                r.font.bold = True
        elif "這些家事，現在家裡誰在做？" in p.text:
            p.text = "這些現代資安好習慣，你做到了嗎？做到的在「我做到了」打 ✓，還沒做到的在「我可以做到」打 ✓。"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(11)
        elif "我發現：　□ 大多是女性家人在做" in p.text:
            p.text = "我發現：　□ 我有良好的數位防護習慣　　□ 我還可以更加警覺小心"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
        elif "三、尊重小偵探" in p.text:
            p.text = "三、資安小偵探"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
                r.font.bold = True
        elif "尊重別人的做法打 ○，不尊重的打 ✕。" in p.text:
            p.text = "安全、正確的做法打 ○，有資安威脅或危險的打 ✕。"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(11)
        elif "四、我的尊重宣言" in p.text:
            p.text = "四、我的資安守護宣言"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)
                r.font.bold = True
        elif "我會＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿，讓每個人都能自在地做自己。" in p.text:
            p.text = "我會＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿，守護自己的個資與數位生活安全。"
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(13)

    # 6. Page 2: Table 7 (Checkboxes)
    t7 = doc.tables[7]
    t7_data = [
        ("□ 看到填問卷免費送遊戲造型或貼圖", "□ 好友傳訊說「差你一票，幫我衝人氣」"),
        ("□ 公用電腦用完只關視窗，沒按「登出」", "□ 在社群拍照打卡，連住家門牌都拍進去"),
        ("□ 所有遊戲和帳號都用同一組簡單密碼", "□ 看到不用密碼的免費公用 Wi-Fi 就連線")
    ]
    for r_idx, row_vals in enumerate(t7_data):
        for c_idx, val in enumerate(row_vals):
            cell = t7.cell(r_idx, c_idx)
            cell.text = val
            for r in cell.paragraphs[0].runs:
                r.font.name = "標楷體"
                r.font.size = Pt(12)

    # 7. Page 2: Table 8 (7 Rules Check Table)
    # Original Table 8 is 6 rows, 5 cols.
    # Col 0: 守則口訣
    # Col 1: 現代資安具體做法 (Merge Col 1 and 2)
    # Col 3: 我做到了
    # Col 4: 我可以做到
    t8 = doc.tables[8]
    
    # Row 0
    t8.cell(0, 0).text = "守則口訣"
    m0 = t8.cell(0, 1).merge(t8.cell(0, 2))
    m0.text = "現代資安具體做法"
    t8.cell(0, 3).text = "我做到了"
    t8.cell(0, 4).text = "我可以做到"

    t8_rules = [
        ("1. 密碼要長不重複", "改用 12~16 字以上長密語，不同帳號不共用"),
        ("2. 雙重驗證加道鎖", "開啟雙重驗證（2FA），即使密碼外洩也登不進"),
        ("3. 離開座位隨手鎖", "離開電腦隨手按【Win + L】，手機設螢幕鎖"),
        ("4. 公用設備必登出", "學校公用電腦用畢務必點「登出」關閉分頁"),
        ("5. 陌生要求先查證", "好友突傳借帳號或要驗證碼，先打電話問本人")
    ]
    for r_idx, (motto, action) in enumerate(t8_rules, start=1):
        t8.cell(r_idx, 0).text = motto
        m_row = t8.cell(r_idx, 1).merge(t8.cell(r_idx, 2))
        m_row.text = action
        t8.cell(r_idx, 3).text = "□"
        t8.cell(r_idx, 4).text = "□"

    for r_idx, row in enumerate(t8.rows):
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                for r in p.runs:
                    r.font.name = "標楷體"
                    r.font.size = Pt(11)
                    if r_idx == 0:
                        r.font.bold = True

    # 8. Page 2: Table 9 (Judgement Table)
    t9 = doc.tables[9]
    if is_teacher:
        t9_data = [
            ("（○）離開學校電腦時，隨手按【Win + L】鎖定", "（✕）好友借帳號打遊戲，直接把帳號密碼給他"),
            ("（○）拍照曬機票時，將條碼與護照個資塗黑遮蔽", "（✕）收到簡訊說包裹未取，立刻點連結輸入資料"),
            ("（○）密碼使用由四個無關英文單字組成的長密語", "（✕）網友說要送高級虛寶，約放學後在公園見面")
        ]
    else:
        t9_data = [
            ("（　）離開學校電腦時，隨手按【Win + L】鎖定", "（　）好友借帳號打遊戲，直接把帳號密碼給他"),
            ("（　）拍照曬機票時，將條碼與護照個資塗黑遮蔽", "（　）收到簡訊說包裹未取，立刻點連結輸入資料"),
            ("（　）密碼使用由四個無關英文單字組成的長密語", "（　）網友說要送高級虛寶，約放學後在公園見面")
        ]

    for r_idx, row_vals in enumerate(t9_data):
        for c_idx, val in enumerate(row_vals):
            cell = t9.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = "標楷體"
                r.font.size = Pt(11)
                if is_teacher and ("○" in val or "✕" in val):
                    r.font.bold = True

    # Fine tune paragraph spacings on page 2 to ensure it fits exactly 1 page
    for p in doc.paragraphs:
        p.paragraph_format.line_spacing = 1.05
        if p.paragraph_format.space_before and p.paragraph_format.space_before.pt > 4:
            p.paragraph_format.space_before = Pt(3)
        if p.paragraph_format.space_after and p.paragraph_format.space_after.pt > 4:
            p.paragraph_format.space_after = Pt(3)

    # Save to intermediate file
    temp_docx = output_path + ".temp.docx"
    doc.save(temp_docx)

    # Replace WordArt shape text and replace image3.png in zip
    shield_img_path = r"c:\2026AI_Agent\教學駕駛艙\cyber_shield.png"
    with open(shield_img_path, 'rb') as f_icon:
        shield_bytes = f_icon.read()

    with zipfile.ZipFile(temp_docx, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/media/image3.png':
                    zout.writestr(item, shield_bytes)
                    continue

                data = zin.read(item.filename)
                if item.filename == 'word/document.xml':
                    xml_str = data.decode('utf-8')
                    # Replace titles
                    xml_str = xml_str.replace("青春記事-性別平等", "資訊安全知多少")
                    xml_str = xml_str.replace("性別翹翹板", "個資保衛戰")
                    xml_str = xml_str.replace("<w:t>性別平等</w:t>", "<w:t>資訊安全知多少</w:t>")
                    data = xml_str.encode('utf-8')
                zout.writestr(item, data)

    if os.path.exists(temp_docx):
        os.remove(temp_docx)

print("Updated create_clean_v3.py ready")
