import docx
import shutil
import win32com.client
from docx import Document
from docx.shared import Pt, RGBColor

import os
desktop = r"C:\Users\user\Desktop"
src = None
for f in os.listdir(desktop):
    if "無愛心" in f and f.endswith(".docx") and not f.startswith("~$"):
        src = os.path.join(desktop, f)
        break

dst_teacher = r"C:\2026AI_Agent\教學駕駛艙\情2-1至2-2_資訊安全知多少_兩頁版_教師解答版.docx"
shutil.copyfile(src, dst_teacher)

doc = Document(dst_teacher)

# Page 1: Table 4 (DIKW)
t4 = doc.tables[4]
t4_answers = [
    "【排定棒次奪冠】\n依選手優勢排定最佳棒次與接棒策略",
    "【分析優勢規律】\n分析誰起跑快、誰過彎最強",
    "【測出選手秒數】\n測出全班每位選手 100m 跑步秒數"
]
for r_idx, ans in enumerate(t4_answers, start=1):
    cell = t4.cell(r_idx, 2)
    cell.text = ans
    p = cell.paragraphs[0]
    for r in p.runs:
        r.font.name = "標楷體"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(180, 40, 40)

# Page 2: Table 8 (5 Rules)
t8 = doc.tables[8]
t8_answers = [
    "改用 12~16 字以上長密語，不同帳號不共用密碼",
    "開啟雙重驗證（2FA/MFA），結合密碼與手機驗證碼",
    "離開電腦隨手按【Win + L】鎖定，手機設螢幕鎖",
    "公用電腦用畢務必點「登出」並關閉無痕瀏覽",
    "好友借帳號或要驗證碼，先打電話問本人（撥 165）"
]
for r_idx, ans in enumerate(t8_answers, start=1):
    cell = t8.cell(r_idx, 1)
    cell.text = "【參考做法】" + ans
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    for r in p.runs:
        r.font.name = "標楷體"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(180, 40, 40)

# Page 2: Table 9 (Judgement)
t9 = doc.tables[9]
t9_answers = [
    ("（○）離開學校電腦時，隨手按【Win + L】鎖定", "（✕）好友借帳號打遊戲，直接把帳號密碼給他"),
    ("（○）拍照曬機票時，將條碼與護照個資塗黑遮蔽", "（✕）收到簡訊說包裹未取，立刻點連結輸入資料"),
    ("（○）密碼用四個無關英文單字組成的長密語", "（✕）網友說要送高級虛寶，約放學後在公園見面")
]
for r_idx, (c0_txt, c1_txt) in enumerate(t9_answers):
    cell0 = t9.cell(r_idx, 0)
    cell1 = t9.cell(r_idx, 1)
    cell0.text = c0_txt
    cell1.text = c1_txt
    for cell in [cell0, cell1]:
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        for r in p.runs:
            r.font.name = "標楷體"
            r.font.size = Pt(11)
            if "○" in r.text or "✕" in r.text:
                r.font.bold = True
                r.font.color.rgb = RGBColor(180, 40, 40)

# Page 2: Prompt answers
for p in doc.paragraphs:
    if "我圈的這項可能洩漏" in p.text:
        p.text = "我圈的這項可能洩漏【帳號密碼與住家隱私】；如果遇到，我會【不點擊連結、不交出資料，立刻查證】。"
        for r in p.runs:
            r.font.name = "標楷體"
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(180, 40, 40)
    elif "我最想加強的是第" in p.text:
        p.text = "我最想加強的是第【2】招，因為【開啟雙重驗證就算密碼被猜到，別人也登不進去，防護最安全】。"
        for r in p.runs:
            r.font.name = "標楷體"
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(180, 40, 40)
    elif "我選的情況：" in p.text:
        p.text = "我選的情況：【好友借帳號打遊戲】；正確做法：【帳密絕不借人，保護帳號安全與自身權益】。"
        for r in p.runs:
            r.font.name = "標楷體"
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(180, 40, 40)
    elif "我會＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿，守護自己的個資與數位生活安全。" in p.text:
        p.text = "我會【落實長密語與雙重驗證、不隨意點擊可疑連結】，守護自己的個資與數位生活安全。"
        for r in p.runs:
            r.font.name = "標楷體"
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(180, 40, 40)

doc.save(dst_teacher)
print("Saved teacher docx successfully!")
