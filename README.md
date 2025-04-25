# bird_watch

This application analyzes `.wav` audio files to identify bird sounds and stores the analysis results in a database. It integrates with the BirdNET-Analyzer to perform the audio analysis.

## Setup

Follow these steps to set up and run the `bird_watch` application:

1.  **Install BirdNET-Analyzer:**
    Follow the official installation instructions for BirdNET-Analyzer. Ensure that it is installed directly in your environment (without using a virtual environment). You can find the instructions here: [https://github.com/birdnet-team/BirdNET-Analyzer](https://github.com/birdnet-team/BirdNET-Analyzer)

2.  **Install Dependencies:**
    Navigate to the root folder of the `bird_watch` repository and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database Parameters:**
    Edit the database connection parameters in the following Python files:
    * `createDB.py`: Modify the variables containing database credentials (e.g., host, username, password, database name) to match your database setup.
    * `insertDb.py`: Similarly, update the database connection details in this file.

4.  **Create the Database:**
    Run the `createDB.py` script to create the necessary database schema:
    ```bash
    python createDB.py
    ```

5.  **Set up birdwatch\_service.py as a Service:**
    Configure `birdwatch_service.py` to run as a system service. The specific steps for this will depend on your operating system (e.g., using `systemd` on Linux). You will need to create a service definition file that specifies how the service should be started, stopped, and managed.

6.  **Run the UI Service (Node.js):**
    The user interface component of `bird_watch` is likely a Node.js application. Navigate to the UI directory (assuming it's named `ui`) and start the Node.js service. You might need to install Node.js dependencies first:
    ```bash
    cd ui # If you are not already in the ui folder
    npm install 
    npm start 
    ```
