import os
import re
import json
from dotenv import load_dotenv
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

class DriveAgent:
    """
        An agent Responsible for connecting the Google Drive and handling files
    """

    def __init__(self):
        # Loading the Service account Credentials as JSON from env variables
        credentials_json_string = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")

        if not credentials_json_string:
            raise ValueError("Service Account Credentials missing")
        
        # Converting the JSON credentials into Python dict
        credentials_dict = json.loads(credentials_json_string)


        # passing the credentials
        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_dict": credentials_dict
            }
        }

        # Creating an instance of GoogleAuth
        gauth = GoogleAuth(settings=settings)

        # Performing the Authentication
        gauth.ServiceAuth() 

        # Creating a drive instance and assigning to self
        self.drive = GoogleDrive(gauth)
        
        print("Google Authentication done successfully!!")


    def extract_folderid_from_link(self, folder_link):
        # Using Regex to find a match for /folders/
        match_folders = re.search(r'/folders/([a-zA-Z0-9-_]+)', folder_link)
        if match_folders:
            return match_folders.group(1)

        # If not found, use regex to find 'id=' pattern
        match_id = re.search(r'id=([a-zA-Z0-9-_]+)', folder_link)

        if match_id:
            return match_id.group(1)
        
        # If not found, return None
        return None
    

    @retry(
        stop = stop_after_attempt(3), # Maximum no. of attempts
        wait = wait_exponential(multiplier=1, min=2, max=10) # waits for 2s, 4s,..
    )
    def list_files_in_folder(self, folder_link):
        folder_id = self.extract_folderid_from_link(folder_link)

        if not folder_id:
            # No folder id found, print a error and return empty list
            print("Invalid Folder Link")
            return []
        
        try:
            # Finding all the files inside the folder and returning
            query = f"'{folder_id}' in parents and trashed=false"
            file_list = self.drive.ListFile({'q': query}).GetList()
            return file_list
        except Exception as e:
            # Retrying if failed
            print(f"API error, retrying... ({e})")
            raise e
        

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def download_file(self, file_obj, download_path='downloads'):
        # Download the file locally using the file_obj into the download_path 
        try:
            # Check if the downloads directory exists, if not, create one
            if not os.path.exists(download_path):
                print(f"Creating Download Directory at {download_path}")
                os.makedirs(download_path)

            # Extract the files title and create the full local path
            file_title = file_obj['title']
            local_file_path = os.path.join(download_path, file_title)

            print(f"Attempting to download {file_title}")

            # Downloading the file's content
            file_obj.GetContentFile(local_file_path)

            print(f"Download successful! File saved to: {local_file_path}")

            return local_file_path
        except Exception as e:
            print(f"Download failed for '{file_obj['title']}'. Retrying... Error: {e}")
            raise e
        

if __name__ == '__main__':
    test_folder_link = "https://drive.google.com/drive/folders/1VdiwsTvc-ctYfTpp9yQdpndoNsjXUuOn?usp=sharing"
    
    try:
        # Create an instance of the agent
        drive_agent = DriveAgent()
        
        # List the files in the folder
        files_in_drive = drive_agent.list_files_in_folder(test_folder_link)
        
        # If any files are found, download the first one as a test
        if files_in_drive:
            print("\n--- Files found in Drive folder ---")
            first_file = files_in_drive[0]
            downloaded_path = drive_agent.download_file(first_file)
            if downloaded_path:
                print(f"\nTest file downloaded to: {downloaded_path}")
        elif not files_in_drive and test_folder_link != "https://drive.google.com/drive/folders/YOUR_FOLDER_ID_HERE":
             print("\nNo files found. Check if the folder is empty or shared correctly.")

    except ValueError as ve:
        print(f"\nConfiguration Error: {ve}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")