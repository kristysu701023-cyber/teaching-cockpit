import win32com.client
import pymupdf

w = win32com.client.Dispatch('Word.Application')
w.Visible = False
try:
    src = r"C:\2026AI_Agent\教學駕駛艙\情2-1至2-2_資訊安全知多少_兩頁版_學生版.docx"
    pdf = r"c:\2026AI_Agent\教學駕駛艙\cyber_student.pdf"
    doc = w.Documents.Open(src)
    pages = doc.ComputeStatistics(2)
    print("Cyber student pages:", pages)
    doc.SaveAs(pdf, 17)
    doc.Close(False)

    src_t = r"C:\2026AI_Agent\教學駕駛艙\情2-1至2-2_資訊安全知多少_兩頁版_教師解答版.docx"
    pdf_t = r"c:\2026AI_Agent\教學駕駛艙\cyber_teacher.pdf"
    doc_t = w.Documents.Open(src_t)
    pages_t = doc_t.ComputeStatistics(2)
    print("Cyber teacher pages:", pages_t)
    doc_t.SaveAs(pdf_t, 17)
    doc_t.Close(False)

    # Render pages
    pdf_doc = pymupdf.open(pdf)
    for i, p in enumerate(pdf_doc):
        pix = p.get_pixmap(dpi=150)
        pix.save(rf'c:\2026AI_Agent\教學駕駛艙\cyber_page_{i+1}.png')
    print("Rendered PNGs")
finally:
    w.Quit()
