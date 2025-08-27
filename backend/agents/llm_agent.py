import os
import json
import re
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from agents.tools import convert_currency

# Load the env variables
load_dotenv()

class LLMAgent:
    """
    The agent responsible for interacting with the LLM (Gemini)
    to extract structured data from raw text using LangChain.
    """

    def __init__(self):
        # Initializing the LLM model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Defining the tools the agent can use
        self.tools = [convert_currency]
        
        # Creating the prompt template
        prompt_template = self._create_prompt_template()
        
        # Creating the agent itself
        agent = create_react_agent(self.llm, self.tools, prompt_template)
        
        # Creating the agent executor, which runs the agent
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True,                   # Setting to True to see the agent's thought process
            handle_parsing_errors=True      # Gracefully handles any output errors
        )
        print("LangChain Agent initialized successfully with CurrencyConverterTool.")

    def _create_prompt_template(self):
        template = """
        You are an expert AI assistant for invoice data extraction.
        Your goal is to extract key information from the provided invoice text and
        convert the total amount to INR if necessary.

        You have access to the following tools:
        {tools}

        To complete your task, you must use the following format:

        Thought: Do I need to use a tool? Yes or No.
        Action: The tool to use, chosen from [{tool_names}].
        Action Input: A single-line JSON string with no newlines that matches the tool's input schema exactly.
                    For example: {{"amount": 1312.50, "from_currency": "USD"}}
        Observation: The result of the tool call.
        ... (this Thought/Action/Action Input/Observation can repeat N times) ...

        Thought: I now have all the information required.
        Final Answer: A single, valid JSON object containing the extracted data.

        **JSON Output Rules:**
        1. Extract these fields from the text: 
        InvoiceNumber, InvoiceDate, VendorName, CustomerName, GSTIN, Subtotal, Tax, TotalAmount, Currency, PaymentTerms, ItemsList.
        2. If a field is not found, use the value "N/A".
        3. After using the currency tool, add this new field to the JSON:
        - "TotalAmountINR": The final converted amount in INR. If the currency is already INR, just use the original TotalAmount.
        4. All numerical values in the JSON must be numbers (not strings).
        5. The "ItemsList" field must be an array of objects. Each object must have "Description", "Quantity", "UnitPrice", and "Amount".
        6. If there are multiple items in "ItemsList", separate them with a comma.
        7. The final answer must be a single JSON object — no extra text or explanation.

        Begin!

        Invoice Text:
        {input}

        {agent_scratchpad}
        """
        return PromptTemplate.from_template(template)

    def run_agentic_extraction(self, raw_text: str) -> dict:
        # Runs the LangChain agent to perform the full extraction and tool-use workflow.
        print("Starting LangChain agent execution...")
        try:
            response = self.agent_executor.invoke({"input": raw_text})
            
            # The final answer is in the 'output' key. It's a string that needs to be parsed.
            final_answer_str = response.get("output", "{}")
            
            # Cleaning up any markdown formatting before parsing
            match = re.search(r"\{.*\}", final_answer_str, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                print("\nAgent did not return a valid JSON object.")
                return {"error": "Failed to parse agent's final answer."}

        except Exception as e:
            print(f"\nAn error occurred during agent execution: {e}")
            return {"error": str(e)}
        

if __name__ == '__main__':
    # Testing locally
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

    print("Initializing LLMAgent for a direct test")
    try:
        llm_agent = LLMAgent()
        print("\nRunning agentic extraction from sample text")
        extracted_data = llm_agent.run_agentic_extraction(sample_invoice_text)

        if extracted_data and "error" not in extracted_data:
            print("\nFinal Extracted Data (JSON):")
            print(json.dumps(extracted_data, indent=4))
        else:
            print("\nAgentic extraction failed or returned an error.")
            print(f"   Result: {extracted_data}")
            
    except Exception as e:
        print(f"\nA fatal error occurred during the test run: {e}")