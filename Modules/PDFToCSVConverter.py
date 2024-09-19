
import PyPDF2
import pandas as pd
import tabula
reader = PyPDF2.PdfReader("Data/TestStatement.pdf")

text = ""
print(len(reader.pages))
for page in reader.pages:
    text += page.extract_text();

print(text)
df = pd.DataFrame(text)
df.to_csv("test.csv")