#!/usr/bin/env python3

import os
import subprocess
import shutil

# Set the input directory (where your WAV files are located)
input_dir = "./input"
# Set the output directory (where you want the results to be saved)
output_dir = "./output"
output_dir_1 = "./ui/public/wav"
def copy_wav_files(source_dir, destination_dir):
    """Copies all .wav files from the source directory to the destination directory."""
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        return

    if not os.path.isdir(destination_dir):
        print(f"Destination directory '{destination_dir}' not found. Creating it.")
        try:
            os.makedirs(destination_dir, exist_ok=True)
        except OSError as e:
            print(f"Error: Failed to create destination directory '{destination_dir}': {e}")
            return

    copied_count = 0
    for filename in os.listdir(source_dir):
        if filename.endswith(".wav"):
            source_path = os.path.join(source_dir, filename)
            destination_path = os.path.join(destination_dir, filename)
            try:
                shutil.move(source_path, destination_path)
                print(f"Copied: {filename} to {destination_dir}")
                copied_count += 1
            except Exception as e:
                print(f"Error copying {filename} to {destination_dir}: {e}")

    print(f"Finished copying {copied_count} WAV files from '{source_dir}' to '{destination_dir}'.")


# Check if the input directory exists
if not os.path.isdir(input_dir):
    print(f"Error: Input directory '{input_dir}' not found.")
    exit(1)

# Check if the output directory exists, create it if it doesn't
if not os.path.isdir(output_dir):
    print(f"Output directory '{output_dir}' not found. Creating it.")
    try:
        os.makedirs(output_dir, exist_ok=True)  # exist_ok=True prevents error if dir exists
    except OSError as e:
        print(f"Error: Failed to create output directory '{output_dir}': {e}")
        exit(1)

# Run the birdnet_analyzer
command = [
    "python3",
    "-m",
    "birdnet_analyzer.analyze",
    f"{input_dir}/",
    "-o",
    f"{output_dir}/",
]

process = subprocess.run(command, capture_output=True, text=True)

# Check the exit code of the command
if process.returncode != 0:
    print(f"Error: birdnet_analyzer.analyze failed.")
    print(f"Stdout: {process.stdout}")
    print(f"Stderr: {process.stderr}")
    # In the bash script, there was a 'continue' statement which implies this was inside a loop.
    # If this script is meant to process all WAV files in the directory, you might need to add a loop here.
    # Assuming you want to process all WAV files at once, the 'continue' doesn't directly translate.
else:
    print("Finished processing all WAV files.")

copy_wav_files(input_dir, output_dir_1)

print("Finished copying WAV files to both destinations.")

