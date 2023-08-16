#This file contains common utils used across different modules, such as directory to keep 


import os

COMMON_DIRECTORY_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads")
DOWNLOADED_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads")
EDITED_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads_edited")

def create_metadata_directory(directory_path):
    try:
        os.mkdir(directory_path)
    except FileExistsError:
        pass

def get_file_names(folder_path):
    """
    Get a list of file names from a folder.
    
    Args:
        folder_path (str): Path to the folder.
        
    Returns:
        List[str]: List of file names in the folder.
    """
    file_names = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_names.append(filename)
    return file_names

SAVEANDEXIT = False 

