import pdfplumber
with pdfplumber.open('Data/PDF/TestStatement.pdf') as pdf:
    first_page = pdf.pages[0]
    print(first_page.find_tables(table_settings={
        
    })) 