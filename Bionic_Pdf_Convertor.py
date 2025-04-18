import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfWriter, PdfReader
from typing import List
import io
import os

def convert_text_to_bionic(text: str, bold_chars: int = 3) -> str:
    words = text.split()
    bionic_words = []
    for word in words:
        if len(word) > bold_chars:
            bionic_word = f"<b>{word[:bold_chars]}</b>{word[bold_chars:]}"
        else:
            bionic_word = f"<b>{word}</b>"
        bionic_words.append(bionic_word)
    return " ".join(bionic_words)

def process_pdf_page(input_pdf_path: str, output_pdf_path: str):
    doc = fitz.open(input_pdf_path)
    writer = PdfWriter()
    styles = getSampleStyleSheet()
    style = styles['Normal']; style.fontName = "Helvetica"; style.fontSize = 12

    for pno in range(doc.page_count):
        page = doc.load_page(pno)
        text_dict = page.get_text("dict")
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        pw, ph = letter

        # 1) Draw text in Bionic style
        for block in text_dict["blocks"]:
            if block["type"] == 0 and "lines" in block:
                txt = " ".join(span["text"] for line in block["lines"] for span in line["spans"])
                btxt = convert_text_to_bionic(txt.strip())
                p = Paragraph(btxt, style)
                w, h = p.wrap(pw, ph)
                x0, y0, x1, y1 = block["bbox"]
                p.drawOn(c, x0, ph - y1 - h)

        # 2) Draw images by locating their rectangles on the page
        for img_idx, img_info in enumerate(page.get_images(full=True)):
            xref = img_info[0]
            # extract pixmap
            pix = fitz.Pixmap(doc, xref)
            if pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            tmp = f"img_p{pno}_x{xref}.png"
            pix.save(tmp)
            pix = None

            # find all places this image appears
            for rect in page.get_image_rects(xref):
                x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
                w_pts = x1 - x0
                h_pts = y1 - y0
                img = Image(tmp, width=w_pts, height=h_pts)
                # ReportLab origin at lower-left; PyMuPDF bbox origin at top-left
                img.drawOn(c, x0, ph - y1)
            os.remove(tmp)

        c.showPage()
        c.save()
        packet.seek(0)

        reader = PdfReader(packet)
        writer.add_page(reader.pages[0])

    with open(output_pdf_path, "wb") as out_f:
        writer.write(out_f)
    doc.close()
    print(f"✅ Wrote bionic PDF with images: {output_pdf_path}")

if __name__ == "__main__":
    pdf_name = input("Please provide pdf path:")
    process_pdf_page(fr"{pdf_name}", "converted_bionic.pdf")
