import pdfplumber
import pandas as pd
import re

PDF_PATH = "../data/result.pdf"
CSV_PATH = "../data/result.csv"

rows = []

pattern = re.compile(
    r"(\d{9})\s+([A-Z\s\-]+?)\s+Q-[A-Z0-9]+/(\d{2,3})"
)

with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        for line in text.split("\n"):
            match = pattern.search(line)
            if match:
                roll = match.group(1)
                name = match.group(2).strip()
                marks = match.group(3)

                rows.append([roll, name, marks])

df = pd.DataFrame(rows, columns=["roll_number", "name", "marks"])
df.to_csv(CSV_PATH, index=False)

print(f"✅ CSV created successfully with {len(df)} records")
