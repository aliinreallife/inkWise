import os
import subprocess
import sys

def main():
    # If running as a standalone executable, use the current working directory
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS  # Temporary directory where PyInstaller bundles files
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to InkWise.py
    script_path = os.path.join(base_dir, 'main.py')

    # Check if the file exists
    if not os.path.exists(script_path):
        print(f"Error: File does not exist: {script_path}")
        sys.exit(1)

    # Command to run the Streamlit app
    command = f'streamlit run "{script_path}"'
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
