from services.parser import extract_text

with open("resume1.docx", "rb") as f:
    data = f.read()

print(extract_text(data, "resume1.docx"))

from services.parser import extract_text

with open("resume2.pdf", "rb") as f:
    data = f.read()

print(extract_text(data, "resume2.pdf"))