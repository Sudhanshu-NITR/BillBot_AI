import os
import io
import pdfplumber
from google.cloud import vision


class ParserAgent:
    """
    An agent that extracts text from files using pdfplumber for PDFs
    and Google Cloud Vision API for images.
    """

    def __init__(self):
        # Initiatlizing the Google Cloud Vision Client
        try:
            self.vision_client = vision.ImageAnnotatorClient()
            print("Google Cloud Vision Client initialized successfully!!")
        except Exception as e:
            print(f"Failed to initialize Google Cloud Vision client. Error: {e}")
            print("   Please ensure your service account credentials are set correctly.")
            self.vision_client = None

    
    def extract_text_from_pdf(self, pdf_path):
        # Extracts text from pdf stored locally        
        print(f"Parsing pdf {pdf_path}")
        try:
            # To safely open the pdf
            with pdfplumber.open(pdf_path) as pdf:
                # Full pdf text is stored in full_text
                full_text = []
                # Iterate through every page
                for page in pdf.pages:
                    # Extract text present in each page
                    text = page.extract_text()
                    if text:
                        full_text.append(text)
                return "\n".join(full_text)
            
        except Exception as e:
            print(f"Error parsing the pdf at {pdf_path}, Error: {e}")
            return None
        

    def extract_text_from_image(self, image_path):
        # Extracting text from Images
        if not self.vision_client:
            print("Vision client is not available. Cannot parse image.")
            return None
        
        try:
            # Reading the imgae in binary mode
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            # Create a google vision image object from the content
            image = vision.Image(content=content)

            response = self.vision_client.text_detection(image=image)

            if response.error.message:
                raise Exception(
                    f"Cloud Vision API error: {response.error.message}"
                )
            
            if response.full_text_annotation:
                return response.full_text_annotation # Return the text in the form of a string
            else:
                print(f"No text found in image: {image_path}")
                return ""
            
        except Exception as e:
            print(f"Error parsing image {image_path}: {e}")
            return None

    def parse_file(self, file_path):
        # identify the file type and extract the text out of it accordingly

        try:
            # Split the file path into root, file_extension
            _, file_extension = os.path.splitext(file_path)
            file_extension = file_extension.lower()

            supported_image_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']

            if file_extension == '.pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_extension in supported_image_formats:
                return self.extract_text_from_image(file_path)
            else:
                print(f"Unsupported file type: {file_extension}. Skipping file: {file_path}")
                return None
        except Exception as e:
            print(f"An unexpected error occured during parsing, Error: {e}")
            return None
        

if __name__ == '__main__':
    print("--- Initializing ParserAgent ---")
    parser_agent = ParserAgent()

    # Define paths to your test files
    test_pdf_path = os.path.join('downloads', 'sample_invoice.pdf')
    test_image_path = os.path.join('downloads', 'sample_invoice.png')

    print("\n--- Testing PDF Parsing ---")
    if os.path.exists(test_pdf_path):
        pdf_text = parser_agent.parse_file(test_pdf_path)
        if pdf_text:
            print("\nExtracted Text from PDF:")
            print("---------------------------------")
            print(pdf_text[:500] + "...") # Print first 500 characters
            print("---------------------------------")
    else:
        print(f"Test file not found: {test_pdf_path}")

    print("\n--- Testing Image Parsing (OCR) ---")
    if os.path.exists(test_image_path):
        image_text = parser_agent.parse_file(test_image_path)
        if image_text:
            print("\nExtracted Text from Image:")
            print("---------------------------------")
            print(image_text)
            print("---------------------------------")
    else:
        print(f"Test file not found: {test_image_path}")
