import pandas as pd

# Load the Excel file
df = pd.read_excel(r"C:\Users\JyothirKakara\Documents\Practise\servicenow_dummy_data.xlsx")

# Convert to JSON and save
df.to_json("servicenow_data.json", orient="records", indent=4)
