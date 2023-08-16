import json

def load_metadata(filename, encoding='utf-8'):
    # Opening JSON file and automatically closing it using a context manager
    with open(filename) as f:
        metadata = json.load(f)

    return metadata

# Main Metadata variables to edit.
def get_metadata_blocks(metadata):
    CITATIONMETADATA = metadata['data']['latestVersion']['metadataBlocks']['citation']['fields']
    GEOMETADATA = metadata['data']['latestVersion']['metadataBlocks']['geospatial']['fields']
    SCIENCEMETADATA = metadata['data']['latestVersion']['metadataBlocks']['socialscience']['fields']
    LT_CITATIONMETADATA = metadata['data']['latestVersion']['metadataBlocks']['customLtCitation']['fields']
    LT_GEOMETADATA = metadata['data']['latestVersion']['metadataBlocks']['customLtGeospatial']['fields']
    LT_SCIENCEMETADATA = metadata['data']['latestVersion']['metadataBlocks']['customLtSocialScience']['fields']
    OTHERBLOCKS = metadata['data']['latestVersion']
    OTHERBLOCKS_VARS = ['distributionDate', 'productionDate', "termsOfUse", "confidentialityDeclaration", "restrictions", "citationRequirements",
                        "conditions", "disclaimer", "termsOfAccess", "originalArchive", "availabilityStatus", "sizeOfCollection"]

    return CITATIONMETADATA, GEOMETADATA, SCIENCEMETADATA, LT_CITATIONMETADATA, LT_GEOMETADATA, LT_SCIENCEMETADATA, OTHERBLOCKS, OTHERBLOCKS_VARS

