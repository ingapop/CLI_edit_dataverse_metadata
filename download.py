#This part includes code to interact with Dataverse API and download required metadata file(s).
#It takes user input of one or more file handles, which then are downloaded and saved locally in the directory called "JSON_metadata" (subdirectory of working directory)




#import required packages
import pyDataverse
from pyDataverse.api import NativeApi
import requests
import json
import os

#Import other required modules
import authenticate


#check if separate folder for downloaded json data  already exists. Create a new directory if it does not exist. 

filepath =  os.getcwd()
metadataFileDirectoryPath = filepath + "/" + "JSON_metadata_downloads"

try:
    os.mkdir(metadataFileDirectoryPath)
except FileExistsError:
    pass     

#set API connection

server_url = authenticate.SERVER_URL
token = authenticate.API_KEY
head = {'Authorization': 'token {}'.format(token)}
response = requests.get(server_url, headers=head)
api = NativeApi(server_url, token)

#get multiple pids from the user input 


file_pids = input("Please provide dataset PIDs separated by spaces: ").split()

# Iterate through the provided file PIDs
for file_pid in file_pids:
    # Get dataset metadata by file PID
    metadatafile = api.get_dataset(file_pid).json()
    # Remove everything before "/" from the file PID
    file_pid_cleaned = file_pid.split("/")[-1].replace(" ", "")

    # Get dataset metadata by file PID
    metadatafile = api.get_dataset(file_pid).json()

    # Save metadata JSON file with cleaned PID as filename
    with open(os.path.join(metadataFileDirectoryPath, f"{file_pid_cleaned}.json"), "w") as file:
        json.dump(metadatafile, file, indent=4)


    print(f"Metadata from dataset PID {file_pid} downloaded and saved successfully.")

