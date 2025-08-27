import os
from flask import Flask, request, jsonify, send_file
from agents.orchestrator import Orchestrator
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


# Globally Initialize the orchestrator once 
try:
    print("Initializing the master Orchestrator... This may take a moment.")
    orchestrator = Orchestrator()
    print("Orchestrator is ready and waiting for requests.")
except Exception as e:
    print(f"FATAL: Could not initialize the orchestrator. The app cannot start. Error: {e}")
    orchestrator = None


@app.route('/process-invoices', methods=['POST'])
def process_invoices():
    """
    This is the main API endpoint. It expects a POST request with a JSON body
    containing the 'drive_link'.
    """
    if not orchestrator:
        return jsonify({"error": "Orchestrator is not available due to an initialization error."}), 500
    
    # Extracting the JSON data from the incoming request
    data = request.get_json()
    if not data or 'drive_link' not in data:
        return jsonify({"error": "Missing 'drive_link' in request body"}), 400
    
    # Extracting the drive link
    drive_link = data['drive_link']
    print(f"\nReceived new request. Starting workflow for: {drive_link}")


    try:
        # Calling the main workflow from the Orchestrator
        result_path = orchestrator.process_invoices_from_drive(drive_link)

        if result_path and os.path.exists(result_path):
            # Workflow ran successfully 
            print(f"Workflow successfull. Sending file: {result_path}")
            return send_file(
                result_path,
                as_attachment=True,
                download_name=os.path.basename(result_path)
            )
        else:
            # Workflow failed
            print("Workflow finished but no file was generated.")
            return jsonify({"error" : "Failed to process invoices or no data was extracted."}), 500
    except Exception as e:
        print(f"An unexpected error occurred during the workflow: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)