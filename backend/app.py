import os
import threading
import time
import requests
from flask import Flask, request, jsonify, send_file, send_from_directory
from agents.orchestrator import Orchestrator
from flask_cors import CORS

KEEP_ALIVE_URL = "https://billbot-ai.onrender.com"
PING_INTERVAL = 30 # in seconds

def ping_website():
    """Sends a GET request to the keep-alive URL."""
    try:
        response = requests.get(KEEP_ALIVE_URL)
        print(f"Keep-alive ping sent to {KEEP_ALIVE_URL}, Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Keep-alive ping failed: {e}")

def keep_alive():
    """Runs the ping function in an infinite loop with a delay."""
    while True:
        ping_website()
        time.sleep(PING_INTERVAL)


# Initializing Flask, pointing static to React build
app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# Orchestrator Initialization
try:
    print("Initializing the master Orchestrator... This may take a moment.")
    orchestrator = Orchestrator()
    print("Orchestrator is ready and waiting for requests.")
except Exception as e:
    print(f"FATAL: Could not initialize the orchestrator. Error: {e}")
    orchestrator = None


# API Endpoints
@app.route('/process-invoices', methods=['POST'])
def process_invoices():
    """
    Main API endpoint. Expects JSON with 'drive_link'.
    """
    if not orchestrator:
        return jsonify({"error": "Orchestrator unavailable due to initialization error."}), 500
    
    data = request.get_json()
    if not data or 'drive_link' not in data:
        return jsonify({"error": "Missing 'drive_link' in request body"}), 400
    
    drive_link = data['drive_link']
    print(f"\nReceived new request. Starting workflow for: {drive_link}")

    try:
        result_path = orchestrator.process_invoices_from_drive(drive_link)

        if result_path and os.path.exists(result_path):
            print(f"Workflow successful. Sending file: {result_path}")
            return send_file(
                result_path,
                as_attachment=True,
                download_name=os.path.basename(result_path)
            )
        else:
            print("Workflow finished but no file was generated.")
            return jsonify({"error": "Failed to process invoices or no data was extracted."}), 500
    except Exception as e:
        print(f"Unexpected error during workflow: {e}")
        return jsonify({"error": "Internal server error occurred."}), 500


# React Frontend Routes
@app.route("/")
def index():
    """Serve React index.html"""
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(_):
    """Redirect unknown routes to React (for React Router)"""
    return send_from_directory(app.static_folder, "index.html")


# Main Entrypoint
if __name__ == '__main__':
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
