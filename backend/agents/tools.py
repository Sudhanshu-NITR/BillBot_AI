import os
import json
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from pydantic import BaseModel, ValidationError

load_dotenv()

class CurrencyInput(BaseModel):
    amount: float
    from_currency: str

@tool("convert_currency")
def convert_currency(tool_input: str) -> str:
    """
    Convert a given amount from a source currency to INR (Indian Rupees).
    The input to this tool MUST be a single-line JSON string with keys "amount" and "from_currency".
    """

    # Parsing
    try:
        input_data = json.loads(tool_input)
        validated_input = CurrencyInput(**input_data)
        amount = validated_input.amount
        from_currency = validated_input.from_currency
    except (json.JSONDecodeError, ValidationError) as e:
        return f"Error: Invalid input format. Provide JSON like '{{\"amount\": 123.45, \"from_currency\": \"USD\"}}'. Details: {e}"

    to_currency = "INR"
    if from_currency.upper() == to_currency:
        return json.dumps({
            "converted_amount": amount,
            "currency": to_currency
        })

    api_key = os.getenv("CURRENCY_API_KEY")
    if not api_key:
        return "Error: Currency API key not found."

    print(f"Using CurrencyConverterTool: Converting {amount} {from_currency} to {to_currency}...")

    try:
        response = requests.get(
            f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency={from_currency}&currencies={to_currency}"
        )
        response.raise_for_status()
        data = response.json()

        if "data" in data and to_currency in data["data"]:
            rate = data["data"][to_currency]["value"]
            converted_amount = round(amount * rate, 2)
            return json.dumps({
                "converted_amount": converted_amount,
                "currency": to_currency,
                "rate": rate
            })

        return f"Error: Could not find conversion rate in response. Response: {data}"

    except Exception as e:
        return f"Error during currency conversion: {e}"
