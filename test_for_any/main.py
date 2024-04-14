from pdf2docx import parse
pdf_file = "d:\\test.pdf"
word_file = "test.docx"
parse(pdf_file, word_file, start=0, end=None)