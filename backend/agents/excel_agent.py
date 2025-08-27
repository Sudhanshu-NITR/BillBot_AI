import os
import json
import pandas as pd

class ExcelAgent:
    """
    An agent responsible for creating an Excel file from a list of
    structured invoice data.
    """
    def create_excel_from_data(self, invoices_list, output_folder='Processed', filename='Invoices_Processed.xlsx'):
        # Takes a list of invoices as dictionaries and saves them to a Excel file
        
        if not invoices_list:
            print("No invoice data provided, Skipping Excel file creation")
            return None
        
        print(f"creating Excel file from {len(invoices_list)} invoice(s)...")
        try:
            # Converting the list of dictionaries into a Pandas dataframe
            df = pd.DataFrame(invoices_list)

            # ItemsList is a list of dictionaries so to make it readable in a single excel cell, we convert it into a json string
            if 'ItemsList' in df.columns:
                df['ItemsList'] = df['ItemsList'].apply(
                    lambda item: json.dumps(item, indent=2) if isinstance(item, list) else item
                )

            # Create the output directory and exists_ok=True prevents error if it not exists already
            os.makedirs(output_folder, exist_ok=True)

            # Create full path of the output file
            output_path = os.path.join(output_folder, filename)

            # Saving the Dataframe to excel file
            df.to_excel(output_path, index=False)

            print(f"Excel file created successfully at: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"An error occurred while creating the Excel file: {e}")
            return None
        

if __name__ == '__main__':
    excel_agent = ExcelAgent()

    sample_data = [
        {
            "InvoiceNumber": "INV-2025-001",
            "InvoiceDate": "2025-08-26",
            "VendorName": "MegaCorp Solutions",
            "CustomerName": "Global Innovations Inc.",
            "GSTIN": "22AABCU9567R1Z5",
            "Subtotal": 1250.00,
            "Tax": 62.50,
            "TotalAmount": 1312.50,
            "Currency": "USD",
            "PaymentTerms": "Net 30 Days",
            "ItemsList": [
                {"Description": "Cloud Service", "Quantity": 10, "UnitPrice": 50.00, "Amount": 500.00},
                {"Description": "AI Consulting", "Quantity": 5, "UnitPrice": 150.00, "Amount": 750.00}
            ]
        },
        {
            "InvoiceNumber": "INV-2025-002",
            "InvoiceDate": "2025-08-27",
            "VendorName": "Quantum Systems",
            "CustomerName": "Future Enterprises",
            "GSTIN": "N/A",
            "Subtotal": 2000.00,
            "Tax": 100.00,
            "TotalAmount": 2100.00,
            "Currency": "USD",
            "PaymentTerms": "Due on receipt",
            "ItemsList": [
                {"Description": "Hardware Rental", "Quantity": 2, "UnitPrice": 1000.00, "Amount": 2000.00}
            ]
        }
    ]

    file_path = excel_agent.create_excel_from_data(sample_data)

    if file_path:
        print(f"\nTest completed. Check the generated file at: {file_path}")

