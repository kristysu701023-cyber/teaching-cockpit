import win32com.client
import os

w = win32com.client.Dispatch('Word.Application')
w.Visible = False
try:
    src = r"C:\Users\user\Desktop\情2-1至2-2_性別平等_兩頁版v3.docx"
    dst = r"c:\2026AI_Agent\教學駕駛艙\desktop_v3.pdf"
    doc = w.Documents.Open(src)
    print("Desktop v3 pages:", doc.ComputeStatistics(2))
    doc.SaveAs(dst, 17)
    doc.Close(False)
    print("Exported desktop_v3.pdf")
finally:
    w.Quit()
