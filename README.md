# CLI_edit_dataverse_metadata
Folder structure:

authenticate.py: server address and API token. This one should be stored locally AND NOT SHARED WITH ANYONE. 

download.py: this module downloads required metadata file(s) from Dataverse and saves locally in "JSON_metadata_downloads" folder. 

datablocks.py: this module defines functions to split downloaded .json file into metadatablocks for further editing. 

edit.py: main module that contains functions to edit metablocks in a single file. For testing purposes: adjust file name in main() function in the end of the code. 

edit_multiple.py: main module that contains code to edit all downloaded files (that are in "JSON_metadata_downloads" folder) one-by-one. Edited files are saved in "JSON_metadata_downloads_edited" folder. 

upload.py : this module uploads all files from "JSON_metadata_downloads_edited" back to Dataverse. 

utils.py: this module contains utility functions that are used across different modules. 

Steps to run:

download.py
edit_multiple.py 
upload.py

#later: these will be combined into main.py for main program flow. 
