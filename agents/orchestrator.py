from agents.drive_agent import DriveAgent
from agents.parser_agent import ParserAgent
from agents.llm_agent import LLMAgent
from agents.excel_agent import ExcelAgent

class Orchestrator:
    """
    The orchestrator agent that manages the entire workflow,
    coordinating all other specialist agents.
    """

    def __init__(self):
        # Initializing the orchestrator and all the specialist agents it needs.

        print("Orchestrator initializing all specialist agents...")
        try:
            self.drive_agent = DriveAgent()
            self.parser_agent = ParserAgent()
            self.llm_agent = LLMAgent()
            self.excel_agent = ExcelAgent()

            print("All Agents initialized successfully")
        except Exception as e:
            print(f"Critical Error during agent initialization. Error: {e}")
            raise
        

    def process_invoices_from_drive(self, folder_link):
        # Executes the end-to-end invoice processing workflow.

        print(f"\nStarting Invoice processing workflow for folder: {folder_link}")

        # Using DriveAgent to get the list of files
        drive_files = self.drive_agent.list_files_in_folder(folder_link=folder_link)
        if not drive_files:
            print("No files in the Drive folder.")
            return None
        
        # Looping through files, download, parse, and extract data
        all_extracted_data = []
        total_files = len(drive_files)

        for i, file_obj in enumerate(drive_files):
            file_title = file_obj['title']
            print(f"\nProcessing file {i+1}/{total_files}: {file_title}")

            # Download file
            downloaded_path = self.drive_agent.download_file(file_obj=file_obj)
            if not downloaded_path:
                print(f"Skipping file {file_title} due to download failure")
                continue

            # Parsing the file to extract raw text
            raw_text = self.parser_agent.parse_file(downloaded_path)
            if not raw_text:
                print(f"Skipping file {file_title} as no text could be extracted.")
                continue

            # Using LLM to extract structured data from the raw text
            invoice_data = self.llm_agent.extract_invoice_data(raw_text=raw_text)
            if not invoice_data:
                print(f"Skipping file {file_title} as data extraction failed.")
                continue
            
            # Add the Source filename for traceability
            invoice_data['SourceFile'] = file_title
            all_extracted_data.append(invoice_data)

            print(f"Successfully processed and extracted data from {file_title}.")


        if not all_extracted_data:
            print("\nNo data was successfully extracted from any file. No Excel report was generated")
            return None
        
        # Using excel agent to create the final report
        print(f"\nFinalizing Process...")
        final_excel_path = self.excel_agent.create_excel_from_data(all_extracted_data)

        if final_excel_path:
            print(f"\n🎉 Workflow complete! Final report is available at: {final_excel_path}")
        else:
            print("\nWorkflow finished, but failed to generate the final Excel report.")

        return final_excel_path
    
    
if __name__ == '__main__':
    test_folder_link = "https://drive.google.com/drive/u/1/folders/1VdiwsTvc-ctYfTpp9yQdpndoNsjXUuOn"

    try:
        orchestrator = Orchestrator()
        orchestrator.process_invoices_from_drive(test_folder_link)
    except Exception as e:
        print(f"\n🚨 A fatal error occurred in the main orchestrator block: {e}")

        
