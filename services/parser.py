import io
import pdfplumber
import docx


def extract_text(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()

    if name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text.strip()

    elif name.endswith(".docx"):
        document = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in document.paragraphs).strip()

    else:
        raise ValueError("Sirf PDF ya DOCX file allowed hai")