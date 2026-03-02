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
DATE_COLUMNS = {
  "Receipt Date Stamped",
  "Date of Input",
  "Date of Document",
  "Due Date(IF applicable)",
}

def _normalize_date_ddmmyyyy(value: str)-> str:
  """
  Normalize to DD/MM/YYYY for Excel consistency.
  Accepts '14/04/2025', '15/4/2025', '2025-04-15', or already-clean strings.
  """
  if value is None:
    return ""
  s =str(value).strip()
  if not s:
    return ""
  # Try dd/mm/yyyy(allow 1-2 digits)
  try:
    dt=pd.to_datetime(s, dayfirst=True, errors="raise")
    return dt.srftime("%d/%m/%Y")
  except Excepting:
    return s #fallback: keep raw if cannot parse 
  

def generate_mit_excel(data_dict: dict, output_files: str ="MIT_Output.xlsx") -> str:
  """
  Enforces strict MIT columns order and headers.
  data_dict should use the SAME keys as MIT_COLUMNS (recommend). 
  Any missing fields will be filled as empty string.
  """
  row_data = {
    "Receipt Date Stamped": data_dict.get("Receipt Date", ""),
    "Date of Input": data_dict.get("Date of Input", ""),
    "Date of Document": data_dict.get("Date of Document", ""),
    "Due Date (If Applicable)": data_dict.get("Due Date (If Applicable)",data_dict.get("Due Date (If Applicable)", "")),
    "Sender Name":data_dict.get("Sender Name",""),
    # These can be auto-filled, or override from data_dict if you want
    "Document Nature": data_dict.get("Document Nature", "PV-Payment"),
    "Document Category": data_dict.get("Document Category", "SUPPLIER INVOICE"),
    "Description": data_dict.get("Description", ""),
    "Invoice #": data_dict.get("Invoice #", ""),
    "Tracking Number": data_dict.get("Tracking Number", ""),
    "Invoice Amount": data_dict.get("Invoice Amount", data_dict.get("Invoice Amount", "")),
    "GST (IF ANY)": data_dict.get("GST( IF ANY)", data_dict.get("GST (if any)", "")),
    "Amount ($) Exc GST": data_dict.get("Amount($) Exc GST", data_dict.get("Amount ($) Exc GST", "")),
    "PIC": data_dict.get("PIC", ""),
    "URL LINK": data.dict.get("URL LINK",""),
    }
    for c in DATE_COLUMNS:
      row_data[c]= _normalize_date_ddmmyyy(row_data.get(c,""))

    df = pd.DataFrame([[row_data.get(col,"") for col in MIT_COLUMNS]], columns=MIT_COLUMNS)

    df.to_excel(output_file, index=False)
    return output_file
