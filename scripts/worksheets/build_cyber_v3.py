import docx
import re
import copy
import win32com.client
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_cyber_worksheet(is_teacher=False):
    src_path = r"C:\Users\user\Desktop\情2-1至2-2_性別平等_兩頁版v3.docx"
    doc = Document(src_path)

    # 1. Modify XML for titles (WordArt / floating shapes)
    xml = doc.element.xml

    # Replace Title 1: 青春記事-性別平等 -> 資訊安全知多少
    xml = xml.replace("青春記事-性別平等", "資訊安全知多少")
    # Replace Title 2: 性別翹翹板 -> 個資保衛戰
    xml = xml.replace("性別翹翹板", "個資保衛戰")
    # Replace unit name in header
    xml = xml.replace("<w:t>性別平等</w:t>", "<w:t>資訊安全知多少</w:t>")

    # Save to a temporary docx and reload
    temp_mid = r"c:\2026AI_Agent\教學駕駛艙\temp_mid.docx"
    with open(temp_mid, "wb") as f:
        # We need to construct a docx with modified document.xml
        pass

    doc._element = parse_xml(xml.encode('utf-8'))
    
    # Check Table 0 (Page 1 Header) and Table 5 (Page 2 Header)
    # Ensure R0C3 has "資訊安全知多少"
    doc.tables[0].cell(0, 3).text = "資訊安全知多少"
    doc.tables[0].cell(0, 5).text = "情 2-1"
    doc.tables[5].cell(0, 3).text = "資訊安全知多少"
    doc.tables[5].cell(0, 5).text = "情 2-2"

    for t in [doc.tables[0], doc.tables[5]]:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    for r_run in p.runs:
                        r_run.font.name = "標楷體"
                        r_run.font.size = Pt(12)

    # ================= PAGE 1 =================
    # Table 2: Story Box
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
            run.font.bold = False

    # Paragraph: Prompt question
    # Find paragraph "★ 如果你是他的同學"
    for p in doc.paragraphs:
        if "★ 如果你是" in p.text:
            p.text = "★ 如果你是學校的資安小偵探，你平時會注意哪些資訊不被他人偷看或外洩？"
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(12)
                run.font.bold = True

    # Paragraph: Question 1
    for p in doc.paragraphs:
        if "1. 所謂「性別刻板印象」" in p.text:
            p.text = "1. 所謂「資訊」，就是將客觀原始的「資料」經過整理、統計與分析後，轉化為可用來判斷或行動的依據。解開 DIKW 知識金字塔的四個智慧階梯："
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(12)
                run.font.bold = False

    # Table 4: DIKW Pyramid Table (4 rows, 3 columns)
    t4 = doc.tables[4]
    t4_data = [
        ("階梯名稱與定義", "生活實例（健康中心）", "生活偵探推理（大隊接力）"),
        ("智慧 (Wisdom)\n最佳決策與行動", "啟動全校消毒、通報校安並宣導戴口罩", "【排定棒次奪冠】\n依數據排定最佳棒次與接棒策略" if is_teacher else "\n\n"),
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

    # Paragraph: Question 2
    for p in doc.paragraphs:
        if "2. 「性別」指的是生理上的差異" in p.text:
            p.text = (
                "2. 資訊安全的三大核心（CIA 三把安全鎖）：機密性（只有經授權的人能看到）、"
                "完整性（資料正確未被竄改）、可用性（需要時能隨時順暢使用）。"
                "在日常生活或學校中，你認為哪一把鎖最容易被大家忽略？為什麼？請說說你的看法。"
            )
            for run in p.runs:
                run.font.name = "標楷體"
                run.font.size = Pt(12)
                run.font.bold = False

    # ================= PAGE 2 =================
    # Paragraphs at the top of page 2
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

    # Table 7: Checkbox table (3 rows, 2 cols)
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

    for p in doc.paragraphs:
        if "我圈的這句話，限制了：" in p.text:
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

    # Table 8: 7 Rules Check Table (originally 6 rows, 5 cols)
    # In gender equality, headers were: 家事 | 男性家人 | 女性家人 | 我 | 我可以幫忙
    # We change headers to: 守則口訣 | 現代資安好習慣 | 我做到了 | 我可以做到
    t8 = doc.tables[8]
    # Header row
    t8.cell(0, 0).text = "守則口訣"
    t8.cell(0, 1).text = "現代資安具體做法"
    t8.cell(0, 2).text = "現代資安具體做法"
    t8.cell(0, 3).text = "我做到了"
    t8.cell(0, 4).text = "我可以做到"
    # Merge col 1 and col 2
    t8.cell(0, 1).merge(t8.cell(0, 2))

    t8_rules = [
        ("1. 密碼要長不重複", "改用 12~16 字以上「長密語」，不同帳號不共用", "□", "□"),
        ("2. 雙重驗證加道鎖", "開啟雙重驗證（2FA/MFA），密碼外洩也登不進", "□", "□"),
        ("3. 離開座位隨手鎖", "離開電腦隨手按【Win + L】鎖定，手機設螢幕鎖", "□", "□"),
        ("4. 公用設備必登出", "學校或公用電腦使用完畢，務必手動點「登出」", "□", "□"),
        ("5. 陌生要求先查證", "好友突傳借帳號或要驗證碼，先打電話向本人查證", "□", "□")
    ]
    for r_idx, (motto, action, c1, c2) in enumerate(t8_rules, start=1):
        t8.cell(r_idx, 0).text = motto
        t8.cell(r_idx, 1).text = action
        t8.cell(r_idx, 2).text = action
        t8.cell(r_idx, 1).merge(t8.cell(r_idx, 2))
        t8.cell(r_idx, 3).text = c1
        t8.cell(r_idx, 4).text = c2

    for row in t8.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "標楷體"
                    r.font.size = Pt(11.5)
                    if cell in [t8.cell(0, 0), t8.cell(0, 1), t8.cell(0, 3), t8.cell(0, 4)]:
                        r.font.bold = True

    for p in doc.paragraphs:
        if "我發現：　□ 大多是女性家人在做" in p.text:
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

    # Table 9: Detective Judgement Table (3 rows, 2 cols)
    t9 = doc.tables[9]
    if is_teacher:
        t9_data = [
            ("（○）離開學校電腦時，隨手按【Win + L】鎖定", "（✕）好友借帳號打遊戲，二話不說直接把帳密給他"),
            ("（○）拍照曬機票時，把機票條碼與護照個資塗黑遮蔽", "（✕）收到簡訊說包裹未取，立刻點連結輸入姓名電話"),
            ("（○）密碼使用由四個無關英文單字組成的 20 字元長密語", "（✕）網友說要送高級虛寶，約好放學後在公園單獨見面")
        ]
    else:
        t9_data = [
            ("（　）離開學校電腦時，隨手按【Win + L】鎖定", "（　）好友借帳號打遊戲，二話不說直接把帳密給他"),
            ("（　）拍照曬機票時，把機票條碼與護照個資塗黑遮蔽", "（　）收到簡訊說包裹未取，立刻點連結輸入姓名電話"),
            ("（　）密碼使用由四個無關英文單字組成的 20 字元長密語", "（　）網友說要送高級虛寶，約好放學後在公園單獨見面")
        ]

    for r_idx, row_vals in enumerate(t9_data):
        for c_idx, val in enumerate(row_vals):
            cell = t9.cell(r_idx, c_idx)
            cell.text = val
            for r in cell.paragraphs[0].runs:
                r.font.name = "標楷體"
                r.font.size = Pt(11.5)
                if is_teacher and ("○" in val or "✕" in val):
                    r.font.bold = True

    for p in doc.paragraphs:
        if "四、我的尊重宣言" in p.text:
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

    return doc

# Build student version and teacher version
doc_student = build_cyber_worksheet(is_teacher=False)
doc_student.save(r"C:\2026AI_Agent\教學駕駛艙\情2-1至2-2_資訊安全知多少_兩頁版_學生版.docx")
doc_student.save(r"C:\Users\user\Desktop\情2-1至2-2_資訊安全知多少_兩頁版v3.docx")

doc_teacher = build_cyber_worksheet(is_teacher=True)
doc_teacher.save(r"C:\2026AI_Agent\教學駕駛艙\情2-1至2-2_資訊安全知多少_兩頁版_教師解答版.docx")

print("Created both worksheets successfully!")
