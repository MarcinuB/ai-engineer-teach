import json
import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional

load_dotenv()
client = anthropic.Anthropic()
class LineItem(BaseModel):
    description: str
    amount: float
# Define the Invoice data model
class Invoice(BaseModel):
    vendor: str
    amount: float
    date: Optional[str] = None
    description: Optional[str] = None
    line_items: list[LineItem] = []
    
def extract_invoice(raw_text: str) -> Invoice:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system="""You are a data extraction engine.
Extract invoice data from the user's text and return ONLY a JSON object.
No prose, no explanation, no markdown code fences — just the raw JSON.
Fields: vendor (string), amount (float), date (string or null), description (string or null),
line_items (array of objects with description (string) and amount (float)).""",
        messages=[
            {
                "role": "user",
                "content": raw_text
            }
        ]
    )
    print(f"Tokens used: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
    
    raw_json = response.content[0].text
    
    try:
        data = json.loads(raw_json)
        return Invoice(**data)
    except json.JSONDecodeError:
        raise ValueError(f"Model returned invalid JSON: {raw_json[:200]}")
    except ValidationError as e:
        raise ValueError(f"Model returned wrong shape: : {e}")
    
    
# ---- Test it ----
# sample_text = """
# Invoice received from Acme Software Ltd, dated March 15, 2024.
# Please process ayment of $3,750.00 for Q1 consulting services covering API integration and system architecture review.
# """

# invoice = extract_invoice(sample_text)    

# print (f"Vendor: {invoice.vendor}")
# print (f"Amount: {invoice.amount}")
# print (f"Date: {invoice.date}")
# print (f"Description: {invoice.description}")
# print()
# print("As dict: ", invoice.model_dump())


sample_text2 = """OVERDUE NOTICE — Invoice #INV-2024-089
From: DataFlow Solutions (UK)
Total: £12,400.00 GBP — PAYMENT 30 DAYS OVERDUE

Items:
- Cloud infrastructure audit: £4,500
- Security penetration testing: £5,200
- Remediation report and recommendations: £2,700
"""

invoice2 = extract_invoice(sample_text2)
print (f"Vendor: {invoice2.vendor}")
print (f"Amount: {invoice2.amount}")
print (f"Date: {invoice2.date}")
print (f"Description: {invoice2.description}")
for item in invoice2.line_items:
    print(f"  - {item.description}: {item.amount}")

print()
print("As dict: ", invoice2.model_dump())
