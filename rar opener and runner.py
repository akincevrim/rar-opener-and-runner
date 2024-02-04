import rarfile
import os
import shutil
import logging
import concurrent.futures
from tqdm import tqdm

logging.basicConfig(filename='rar_runner.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_border(message):
    border = '=' * 50
    return f"\n{border}\n{message}\n{border}\n"

def extract_all(rar_path, output_folder, password=None):
    try:
        with rarfile.RarFile(rar_path, 'r', password=password) as rar:
            logging.info(add_border(f"Extracting all files from {rar_path} to {output_folder}..."))
            total_files = len(rar.namelist())
            extracted_files = 0
            for file in rar.infolist():
                rar.extract(file, output_folder)
                extracted_files += 1
                logging.info(f"Extracted {file.filename} ({extracted_files}/{total_files})")
            logging.info(add_border("Extraction completed successfully."))
    except rarfile.RarCannotExec:
        logging.error(add_border("Error: rarfile module cannot execute the rar command. Make sure 'unrar' is installed."))
    except rarfile.BadRarFile:
        logging.error(add_border("Error: Not a valid RAR file."))
    except rarfile.RarCRCError:
        logging.error(add_border("Error: CRC error in RAR file."))
    except rarfile.RarExecError:
        logging.error(add_border("Error: Incorrect password provided."))
    except Exception as e:
        logging.error(add_border(f"An error occurred: {str(e)}"))

def extract_selected(rar_path, output_folder, selected_files, password=None):
    try:
        with rarfile.RarFile(rar_path, 'r', password=password) as rar:
            logging.info(add_border(f"Extracting selected files from {rar_path} to {output_folder}..."))
            total_files = len(selected_files)
            extracted_files = 0
            for file in selected_files:
                rar.extract(file, output_folder)
                extracted_files += 1
                logging.info(f"Extracted {file} ({extracted_files}/{total_files})")
            logging.info(add_border("Extraction completed successfully."))
    except rarfile.RarCannotExec:
        logging.error(add_border("Error: rarfile module cannot execute the rar command. Make sure 'unrar' is installed."))
    except rarfile.BadRarFile:
        logging.error(add_border("Error: Not a valid RAR file."))
    except rarfile.RarCRCError:
        logging.error(add_border("Error: CRC error in RAR file."))
    except rarfile.RarExecError:
        logging.error(add_border("Error: Incorrect password provided."))
    except Exception as e:
        logging.error(add_border(f"An error occurred: {str(e)}"))

def view_contents(rar_path, password=None):
    try:
        with rarfile.RarFile(rar_path, 'r', password=password) as rar:
            logging.info(add_border(f"Contents of {rar_path}:"))
            for file in rar.infolist():
                logging.info(file.filename)
            logging.info(add_border("Viewing completed."))
    except rarfile.RarCannotExec:
        logging.error(add_border("Error: rarfile module cannot execute the rar command. Make sure 'unrar' is installed."))
    except rarfile.BadRarFile:
        logging.error(add_border("Error: Not a valid RAR file."))
    except rarfile.RarCRCError:
        logging.error(add_border("Error: CRC error in RAR file."))
    except rarfile.RarExecError:
        logging.error(add_border("Error: Incorrect password provided."))
    except Exception as e:
        logging.error(add_border(f"An error occurred: {str(e)}"))

def autorun(rar_path, output_folder, action, selected_files=None, password=None):
    if action == 'extract_all':
        extract_all(rar_path, output_folder, password=password)
    elif action == 'extract_selected':
        extract_selected(rar_path, output_folder, selected_files, password=password)
    elif action == 'view_contents':
        view_contents(rar_path, password=password)

def interactive_mode():
    print("Welcome to RAR Runner interactive mode.")
    rar_path = input("Enter the path to the RAR archive: ").strip()
    password = input("Enter the password for the RAR archive (press Enter if none): ").strip() or None
    action = input("Choose an action (extract_all/extract_selected/view_contents): ").strip()

    if action == 'extract_selected':
        selected_files = input("Enter the list of files to extract (comma-separated): ").strip().split(',')
        selected_files = [file.strip() for file in selected_files]
        output_folder = input("Enter the path to the output folder for extraction: ").strip()
        autorun(rar_path, output_folder, action, selected_files, password=password)
    else:
        output_folder = input("Enter the path to the output folder: ").strip()
        autorun(rar_path, output_folder, action, password=password)

if __name__ == "__main__":
    interactive_mode()
