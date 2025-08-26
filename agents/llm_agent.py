import os
import json
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
        end_index = raw_response_text.find('}')

        if start_index != -1 and end_index != -1 and end_index > start_index:
            # Slicing the string to get only the required content
            return raw_response_text[start_index : end_index + 1]
        else:
            # If no JSON object is found, return an empty JSON object string
            print("Could not find a valid JSON object in the LLM response.")
            return "{}"
        
    
    def extract_invoice_data(self, raw_text):
        # Send the raw text from an invoice and to LLM and get structured JSON format
        if not self.model:
            print("Model is not initialized. Cannot extract data.")
            return None
        
        prompt = f"""
        You are an expert AI assistant specializing in invoice data extraction.
        Your task is to analyze the raw text provided below and extract the key information into a structured JSON format.

        Follow these rules strictly:
        1.  Extract the following fields: InvoiceNumber, InvoiceDate, VendorName, CustomerName, GSTIN, Subtotal, Tax, TotalAmount, Currency, PaymentTerms, ItemsList.
        2.  The "ItemsList" should be an array of objects, where each object has "Description", "Quantity", "UnitPrice", and "Amount".
        3.  If a field is not found in the text, you MUST use the value "N/A". Do not make up information.
        4.  The output MUST be a single, valid JSON object. Do not include any text or explanations before or after the JSON.
        5.  For dates, use the YYYY-MM-DD format if possible.
        6.  For numerical values (Subtotal, Tax, TotalAmount), extract only the numbers, without currency symbols.

        Here is the raw text from the invoice:
        --- INVOICE TEXT ---
        {raw_text}
        --- END OF TEXT ---

        Now, provide the structured JSON output.
        """

        print("Sending text to Gemini for analysis")
        try:
            # Calling the model to generate the content based on given prompt
            response = self.model.generate_content(prompt)

            # Clean the response to ensure its valid JSON
            cleaned_response = self.clean_json_response(response.text)

            # Parsing the cleaned text into a Python Dictionary
            parsed_json = json.loads(cleaned_response)
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
            # Using json.dumps for pretty printing the dictionary
            print(json.dumps(extracted_data, indent=4))
