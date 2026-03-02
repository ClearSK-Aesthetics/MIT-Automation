import pandas as pd
from datetime import datetime


MIT_COLUMNS =[
  "Receipt Date Stamped",
  "Date of Input", 
  "Date of Document",
  "Due Date(IF Applicable)",
  "Sender Name",
  "Document Nature",
  "Description",
  "Invoice #",
  "Tracking Number",
  "Invoice amount",
  "GST( IF ANY)",
  "Amount($) Exc GST",
  "PIC",
  "URL LINK"]

def generate_mit_excel(data_dict):

    row_data = {
        "Receipt Date Stamped": data_dict.get("Receipt Date", ""),
        "Date of Input": data_dict.get("Date of Input", ""),
        "Date of Document": data_dict.get("Date of Document", ""),
        "Due Date (If Applicable)": data_dict.get("Due Date (If Applicable)", ""),
        "Sender Name": data_dict.get("Sender Name", ""),
        "Document Nature": "PV-Payment",
        "Document Category": "SUPPLIER INVOICE",
        "Description": data_dict.get("Description", ""),
        "Invoice #": data_dict.get("Invoice #", ""),
        "Tracking Number": "",
        "Invoice Amount": data_dict.get("Invoice Amount", ""),
        "GST (IF ANY)": "",
        "Amount ($) Exc GST": "",
        "PIC": data_dict.get("PIC", ""),
        "URL LINK": ""
    }

    df = pd.DataFrame([row_data], columns=MIT_COLUMNS)

    output_file = "MIT_Output.xlsx"
    df.to_excel(output_file, index=False)

    return output_file
