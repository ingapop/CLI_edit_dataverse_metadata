#publishing metadata after it is changed and saved as a file in previous steps. 

import os
import logging
import json
import requests
import time 
import authenticate
from utils import get_file_names

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename='test.log', level=logging.DEBUG)



#define function to publish 

def publish_data(server_url, api_key, pers_id, FileToPublish):
    headers = {'X-Dataverse-key': api_key}
    url = f"{server_url}/api/datasets/:persistentId/?persistentId={pers_id}" 
    with open(FileToPublish, 'r', encoding='utf-8') as file:
        dataset_json = json.load(file)

    status = dataset_json['status']
    if status.lower() != 'ok':
        raise Exception(f"Get JSON status not ok: {status}, skipping.")
    
    data_json = dataset_json['data']
    json_identifier = data_json['identifier']
    
    tmp_pers_id = pers_id.split('/')[-1]
    if tmp_pers_id.lower() != json_identifier.lower():
        raise Exception(f"Requested and JSON identifiers do not match: {json_identifier} != {tmp_pers_id}. Skipping.")
    
    latest_version_json = data_json['latestVersion']
    metadata_blocks_json = latest_version_json['metadataBlocks']
    citation_block = metadata_blocks_json['citation']
    custom_lt_citation_block = metadata_blocks_json['customLtCitation']
    
    add_missing_contact_json(citation_block)
    add_missing_contact_json(custom_lt_citation_block)
    
    latest_version_json.pop('files', None)
    json_for_update = latest_version_json
    json_for_update_str = json.dumps(json_for_update)
    logging.info(f"Modified JSON: {json_for_update_str}")
    

    url = f"{server_url}/api/datasets/:persistentId/versions/:draft?persistentId={pers_id}"
    response = requests.put(url, headers=headers, data=json_for_update_str.encode('utf-8'))
    update_resp_str = response.text
    logging.info(f"Update http response: {update_resp_str}")
    

    while True:
        url = f"{server_url}/api/datasets/:persistentId/actions/:publish?persistentId={pers_id}&type=major&assureIsIndexed=true"
        response = requests.post(url, headers=headers)
        publish_resp_str = response.text
        logging.info(f"Publish https response: {publish_resp_str}")
        
        
        publish_resp_json = json.loads(publish_resp_str)
        status = publish_resp_json['status']
        print()
        if status.lower() == 'conflict':
            logging.info(f"Sleeping and retrying in 2 seconds: received publish status ={status}")
            time.sleep(2)
            continue
        
        if status.lower() != 'ok':
            raise Exception(f"Error publishing object {pers_id}: status not ok:{status}")
        else:
            logging.info(f"Object {pers_id} published.")
        
        break


# add missing parts to the file 

def add_missing_contact_json(block):
    fields = block['fields']
    for field in fields:
        type_name = field['typeName']
        if type_name.lower() == 'datasetcontact':
            dataset_contact_val_arr = field['value']
            for dataset_contact_val_arr_el in dataset_contact_val_arr:
                dataset_contact_email = {
                    "typeName": "datasetContactEmail",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": "data@ktu.lt"
                }
                dataset_contact_val_arr_el['datasetContactEmail'] = dataset_contact_email

        if type_name.lower() == 'customltdatasetcontact':
            dataset_contact_val_arr = field['value']
            for dataset_contact_val_arr_el in dataset_contact_val_arr:
                custom_lt_dataset_contact_email = {
                    "typeName": "customLtDatasetContactEmail",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": "data@ktu.lt"
                }
                dataset_contact_val_arr_el['customLtDatasetContactEmail'] = custom_lt_dataset_contact_email


def main():
    server_url = authenticate.SERVER_URL
    api_key = authenticate.API_KEY
    # Path to the folder containing JSON files
    filepath =  os.getcwd()
    metadataFileDirectoryPath = filepath + "/" + "JSON_metadata_downloads_edited"
    json_file_names = get_file_names(metadataFileDirectoryPath)



    # Iterate through the list of JSON file names
    for json_file_name in json_file_names:
        json_file_path = os.path.join(metadataFileDirectoryPath, json_file_name)
        pers_id = f"hdl:21.12137/{os.path.splitext(json_file_name)[0]}"
        print(pers_id)
        publish_data(server_url, api_key, pers_id, json_file_path)

if __name__ == "__main__":
    main() 



