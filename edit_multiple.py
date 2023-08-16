#import packages

import json
import os
from tabulate import tabulate
import textwrap

#other modules:

from edit import edit_metadata, save_exit
from datablocks import load_metadata, get_metadata_blocks
from utils import get_file_names, SAVEANDEXIT

def save_file(metadata:dict, filename:str,output_path):  
    global SAVEANDEXIT
    user_input = input(
        "Select Y to exit and save changes in your hard drive. Select N to continue editing: y/n").lower()
    print(f"User input: {user_input}")  # Add this line for debugging
    if user_input == 'y':
        filepath = os.path.join(output_path, filename)
        with open(filepath, "w") as f: 
            json.dump(metadata, f)
        print(f"Changes saved for {filepath}")
        SAVEANDEXIT = True
        
    else:
        SAVEANDEXIT = False



def main():

    DOWNLOADED_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads")
    EDITED_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads_edited")

    if not os.path.exists(EDITED_PATH):
        os.makedirs(EDITED_PATH)

    json_files = get_file_names(DOWNLOADED_PATH)
    print ("Files to edit:", json_files)
    for json_file in json_files:
        json_path = os.path.join(DOWNLOADED_PATH, json_file)
        metadata = load_metadata(json_path)
        filename = os.path.basename(json_path)

        # Reset SAVEANDEXIT for each file
        SAVEANDEXIT = False

        while not SAVEANDEXIT:
            edit_metadata(metadata, filename, EDITED_PATH)

            user_input = input("Do you want to continue editing this file? Y for keep editing this file, N for moving to next file (if there are more files left)" )
            if user_input.lower() == 'n':
                print("Saving this file and moving to next...")
                filepath = os.path.join(EDITED_PATH, filename)
                with open(filepath, "w") as f: 
                    json.dump(metadata, f)
                    print(f"Changes saved for {filepath}")

                break
    print ("Finished editing, no more files in the folder.")        

if __name__ == "__main__":
    main()
