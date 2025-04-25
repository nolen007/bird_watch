import subprocess
import time
import schedule
import logging
import os
import shutil # For moving files
from datetime import datetime

# Configure logging
logging.basicConfig(filename='./logs/service.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_bird_analysis():
    logging.info("Starting bird analysis...")

    # Execute analyze.py
    analyze_process = subprocess.run(['/usr/bin/python3', 'analyze.py'], capture_output=True, text=True)
    with open('./logs/birdwatch.log', 'a') as log_file:
        log_file.write(analyze_process.stdout)
        if analyze_process.stderr:
            log_file.write(f"Error (analyze.py): {analyze_process.stderr}\n")

    if analyze_process.returncode != 0:
        logging.error(f"analyze.py failed with exit code {analyze_process.returncode}. Output: {analyze_process.stderr}")
        return

    logging.info("analyze.py executed successfully.")

       # Execute insertBird.py
    insert_process = subprocess.run(['/usr/bin/python3', 'insertDb.py'], capture_output=True, text=True)
    with open('./logs/mysql.log', 'a') as log_file:
        log_file.write(insert_process.stdout)
        if insert_process.stderr:
            log_file.write(f"Error (insertDb.py): {insert_process.stderr}\n")

    if insert_process.returncode != 0:
        logging.error(f"insertBird.py failed with exit code {insert_process.returncode}. Output: {insert_process.stderr}")
        return

    logging.info("insertDb.py executed successfully.")
    logging.info("Bird analysis cycle completed.")

def job():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Running scheduled job at {timestamp}")
    run_bird_analysis()
    logging.info(f"Scheduled job finished at {timestamp}")

job()
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    logging.info("Bird watching service started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
