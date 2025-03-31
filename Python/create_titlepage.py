from docx import Document
from docx.shared import Pt
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime
import comtypes.client
import locale

# Load template
doc = Document(fr"C:\Users\danny\Documents\GitHub\Statistiek\Python\FMW_titelblad.docx")
locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

vaknaam = "Statistiek (deel 1)"
vakcode = "STA"
datum = "20250523"
examinator = "Dr. ir. D.A.M.P. Blom"
peer_review = ""
aantal_opgaven = "4"
aantal_paginas = "4"
tentamentijd = "13:30-16:30"

formatted_date = datetime.strptime(datum, "%Y%m%d").strftime("%d %B %Y")
print(formatted_date)

doc_path = fr"C:\Users\danny\Documents\GitHub\Statistiek\Python\FMW_titelblad_{datum}.docx"
pdf_path = fr"C:\Users\danny\Documents\GitHub\Statistiek\Python\FMW_titelblad_{datum}.pdf"

# Replace placeholders
replacements = {
    "{{vaknaam}}": vaknaam,
    "{{datum}}": str(formatted_date),
    "{{examinator_naam}}": examinator,
    "{{peer_review}}": peer_review,
    "{{num_opgaves}}": aantal_opgaven,
    "{{vakcode}}": vakcode,
    "{{tentamentijd}}": tentamentijd,
    "{{num_paginas}}": aantal_paginas
}

def replace_text(paragraphs):
    for para in paragraphs:
        for key, value in replacements.items():
            if key in para.text:
                para.text = para.text.replace(key, value)
                para.alignment = WD_ALIGN_VERTICAL.CENTER # Align text to center

                for run in para.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(12)

replace_text(doc.paragraphs)

# Replace text inside table cells and center-align
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            replace_text(cell.paragraphs)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

# Save the filled document
doc.save(doc_path)

def convert_docx_to_pdf(input_path, output_path):
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(input_path)
    doc.SaveAs(output_path, FileFormat=17)  # 17 = wdFormatPDF
    doc.Close()
    word.Quit()

convert_docx_to_pdf(doc_path, pdf_path)
