import json
import re
import time
import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional

from lesson_002.json_utils import strip_json_fence
from lesson_002.retry_utils import create_with_retry

load_dotenv()
client = anthropic.Anthropic(timeout=30.0)

# ── Models ──────────────────────────────────────────────────────────────────

class LineItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    vendor: str
    amount: float
    date: Optional[str] = None
    description: Optional[str] = None
    line_items: list[LineItem] = []

# ── Helpers ──────────────────────────────────────────────────────────────────

SYSTEM = """You are a data extraction engine.
Extract invoice data and return ONLY a JSON object — no prose, no fences.
Fields: vendor (str), amount (float), date (str|null), description (str|null),
line_items (array of {description: str, amount: float})."""

# ── Main extractor ───────────────────────────────────────────────────────────

def extract_invoice(raw_text: str, max_corrections: int = 2) -> Invoice:
    conversation = [{"role": "user", "content": raw_text}]
    
    for attempt in range(max_corrections + 1):
        response = create_with_retry(
            client,
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM,
            messages=conversation
        )
        raw = strip_json_fence(response.content[0].text)
        
        try:
            return Invoice(**json.loads(raw))
        
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == max_corrections:
                raise ValueError(f"Failed after {max_corrections} corrections {e}")
            conversation += [
                {"role": "assistant", "content": response.content[0].text},
                {"role": "user", "content": f"Invalid response - {e}. return only valid JSON."}
            ]
            print(f"[correction {attempt+1}] {type(e).__name__}")


# ── Test ──────────────────────────────────────────────────────────────────────

sample = """OVERDUE NOTICE — Invoice #INV-2024-089
From: DataFlow Solutions (UK)
Total: £12,400.00 GBP — PAYMENT 30 DAYS OVERDUE

Items:
- Cloud infrastructure audit: £4,500
- Security penetration testing: £5,200
- Remediation report and recommendations: £2,700
"""

invoice = extract_invoice(sample)
print(f"Vendor:     {invoice.vendor}")
print(f"Amount:     {invoice.amount}")
print(f"Date:       {invoice.date}")
print(f"Line items: {len(invoice.line_items)}")
for item in invoice.line_items:
    print(f"  - {item.description}: {item.amount}")