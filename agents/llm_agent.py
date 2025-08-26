import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load the env variables
load_dotenv()

class LLMAgent:
    """
    The agent responsible for interacting with the LLM (Gemini)
    to extract structured data from raw text.
    """

    def __init__(self):
        # Initialize the LLM model

        # Get the Gemini API key
        api_key = os.getenv("GEMINI_API_KEY")

        try:
            # Get the Gemini Api key
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            
            # Configure the Generative AI library with Api key
            genai.configure(api_key=api_key)

            # Initialize the AI model
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini Pro model initialized successfully.")
            
        except Exception as e:
            print(f"Error initializing LLMAgent: {e}")
            self.model = None

    def clean_json_response(self, raw_response_text):
        # Clean the markdown formatting done by LLM Agent

        start_index = raw_response_text.find('{')
        end_index = raw_response_text.rfind('}')

        if start_index != -1 and end_index != -1 and end_index > start_index:
            return raw_response_text[start_index : end_index + 1]
        else:
            print("Could not find a valid JSON object in the LLM response.")
            return "{}"
        
    def safe_json_parse(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            text = re.sub(r",\s*}", "}", text)
            text = re.sub(r",\s*]", "]", text)
            return json.loads(text)
    
    def extract_invoice_data(self, raw_text):
        # Send the raw text from an invoice and to LLM and get structured JSON format
        if not self.model:
            print("Model is not initialized. Cannot extract data.")
            return None
        
        prompt = f"""
        You are an expert AI assistant for invoice data extraction.
        Your task is to analyze the raw text and extract information into a valid JSON format.

        **CRITICAL RULES:**
        1.  The final output MUST be a single, valid JSON object. Do not include any text before or after the JSON.
        2.  Extract these fields: InvoiceNumber, InvoiceDate, VendorName, CustomerName, GSTIN, Subtotal, Tax, TotalAmount, Currency, PaymentTerms, ItemsList.
        3.  If a field is not found, you MUST use the value "N/A".
        4.  For numerical fields (Subtotal, Tax, TotalAmount, Quantity, UnitPrice, Amount), the value MUST be a number (e.g., 1250.00), NOT a string (e.g., "1250.00"). If not found, use "N/A".
        5.  The "ItemsList" field MUST be an array of objects. Each object must have "Description", "Quantity", "UnitPrice", and "Amount".
        6.  **VERY IMPORTANT**: When the "ItemsList" array has more than one item, you MUST place a comma (,) between the JSON objects.

        Here is an example of a perfect response:
        {{
            "InvoiceNumber": "INV-123",
            "ItemsList": [
                {{
                    "Description": "Item A",
                    "Quantity": 2,
                    "UnitPrice": 50.00,
                    "Amount": 100.00
                }},
                {{
                    "Description": "Item B",
                    "Quantity": 3,
                    "UnitPrice": 25.00,
                    "Amount": 75.00
                }}
            ],
            ...
        }}

        --- INVOICE TEXT TO ANALYZE ---
        {raw_text}
        --- END OF TEXT ---

        Now, provide the structured JSON output.
        """

        print("Sending text to Gemini for analysis")
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.candidates[0].content.parts[0].text if response.candidates else response.text
            cleaned_response = self.clean_json_response(raw_text)
            parsed_json = self.safe_json_parse(cleaned_response)
            print("Successfully extracted and parsed Invoice data")
            return parsed_json

        except json.JSONDecodeError as e:
            print(f"Error decodinng JSON from LLM response. Error: {e}")
            print(f"\nRaw response was {response.text}")
            return None
        except Exception as e:
            print(f"An error occured while communicating with the LLM. Error: {e}")
            return None
        

if __name__ == '__main__':
    sample_invoice_text = """
    MegaCorp Solutions
    123 Innovation Drive, Tech City
    Invoice #: INV-2025-001
    Date: 2025-08-26
    
    Bill To:
    John Doe
    Global Innovations Inc.
    456 Future Way, Metroburg
    
    Description        | Qty | Unit Price | Total
    -------------------------------------------------
    Cloud Service      | 10  | 50.00      | 500.00
    AI Consulting      | 5   | 150.00     | 750.00
    
    Subtotal: 1250.00
    GST (5%): 62.50
    TOTAL DUE: 1312.50 USD
    Payment Terms: Net 30 Days
    Vendor GSTIN: 22AABCU9567R1Z5
    """

    print("--- Initializing LLMAgent ---")
    llm_agent = LLMAgent()

    if llm_agent.model:
        print("\n--- Extracting data from sample text ---")
        extracted_data = llm_agent.extract_invoice_data(sample_invoice_text)

        if extracted_data:
            print("\nExtracted Invoice Data (JSON):")
            print(json.dumps(extracted_data, indent=4))
