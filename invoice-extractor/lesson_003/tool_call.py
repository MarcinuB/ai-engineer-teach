import json
import os
from openai import OpenAI
from pydantic import BaseModel, Field

from pathlib import Path
from dotenv import load_dotenv

# __file__ is this script; .parent is lesson_003/; .parent again is invoice-extractor/
load_dotenv(Path(__file__).parent.parent / ".env")

# Ollama
BASE_URL = "http://localhost:11434/v1"
API_KEY="ollama"
MODEL = 'llama3.2'

# Open AI
# BASE_URL = "https://api.openai.com/v1"
# API_KEY = os.getenv("OPENAI_API_KEY")
# MODEL = "gpt-4o"

# Anthropic
# BASE_URL = "http://localhost:11434/v1"
# API_KEY = os.getenv("ANTHROPIC_API_KEY")
# MODEL = "claude-3-5-haiku-20241022"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


### Tool: vat_rates
VAT_RATES = {"PL": 0.23, "DE": 0.19, "FR": 0.20, "GB": 0.20, "US": 0.0}

def get_vat_rate(country_code: str) -> dict:
    rate = VAT_RATES.get(country_code.upper())
    if rate is None:
        return {"error", f"Unknown country: {country_code}"}
    return {"country_code": country_code.upper(), "vat_rate": rate}

class GetVatRateInput(BaseModel): 
    country_code: str = Field(description="ISO 3166-1 alpha-2 code, e.g. 'PL'")


### Tool: Currency conversion
class ConvertCurrencyInput(BaseModel):
    amount: float = Field(description="Amount to convert")
    from_currency: str = Field(description="Source currency, e.g. 'EUR'")
    to_currency: str = Field(description="Target currency, e.g. 'PLN'")

RATES_FROM_EUR = { "EUR": 1.0, "PLN": 4.25, "USD": 1.08, "GBP": 0.85 }

def convert_currency(amount: float, from_currency: str, to_currency: str):
    amount = float(amount)
    if not from_currency or not to_currency:
        return {"error": "from_currency and to_currency are required"}
    
    result = amount * RATES_FROM_EUR[to_currency] / RATES_FROM_EUR[from_currency]
    
    return {"result": result, "from": from_currency, "to": to_currency}

def pydantic_to_tool(name: str, description: str, model: type[BaseModel]) -> dict:
    schema = model.model_json_schema()
    schema.pop("title", None) #Pydantic adds a title field the model doesn't need
    return {
        "type": "function",
        "function": {"name": name, "description": description, "parameters": schema}
    }
    
tools = [
    pydantic_to_tool("get_vat_rate", "Returns VAT rate for a country.", GetVatRateInput),
    pydantic_to_tool("convert_currency", "Converts an amount between currencies. Both from_currency and to_currency must be ISO 4217 codes e.g. 'EUR', 'PLN', 'USD'. Never leave either field empty.", ConvertCurrencyInput)
]

TOOL_MAP = {
    "get_vat_rate": get_vat_rate,
    "convert_currency": convert_currency
}

INPUT_MODELS = {
    "get_vat_rate": GetVatRateInput,
    "convert_currency": ConvertCurrencyInput,
}   

def run_tool(name: str, arguments: dict):
    fn = TOOL_MAP.get(name)
    if not fn:
        return {"error": f"Unknown tool: {name}"}
    
    fn = TOOL_MAP.get(name)
    model = INPUT_MODELS.get(name)
    if model:
        arguments = model(**arguments).model_dump()
    return fn(**arguments)
    

def run_with_tools(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "Always use tools to look up VAT rates. Never use your training data for tax rates.",
        },
        {"role": "user", "content": user_message}
    ]
    
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools
        )
        
        choice = response.choices[0]
        
        if choice.finish_reason == "stop":
            return choice.message.content
        if choice.finish_reason == "tool_calls":
            messages.append(choice.message) #assistant's request goes into history
            
            for tc in choice.message.tool_calls:
                args = json.loads(tc.function.arguments)
                result =  run_tool(tc.function.name, args)
                print(f".  [tool] {tc.function.name}({args}) -> {result}")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result)
                })
            #loop: model now sees the tool results and continues
            
if __name__ == "__main__":
    question = (
        """I'm invoicing a client in Poland for €1,200 net.
        What's the VAT amount and the gross total?
        Show all amounts in PLN."""
    )
    print(f"User: {question}\n")
    answer = run_with_tools(question)
    print(f"\nAssistant: {answer}")