import os
import logging
from dotenv import load_dotenv
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import AtlanConnectorType , APIQueryParamTypeEnum
from pyatlan.model.assets import Connection, APISpec, APIPath, APIObject, APIQuery, APIField #import typedefs you want to create

# Load credentials
load_dotenv()
ATLAN_BASE_URL =os.getenv('ATLAN_BASE_URL')
ATLAN_API_KEY =os.getenv('ATLAN_API_KEY')

client = AtlanClient(
    base_url= ATLAN_BASE_URL,
    api_key = ATLAN_API_KEY
)

#STEP 1: Specify Connection GUID
connection_qualified_name= 'example default/api/12344567' #connection_qualified_name

# Create Asset using the creator, change typedef based on asset type trying to create. 
apiObject = APIObject.creator(
    name="[example location]",
    connection_qualified_name = connection_qualified_name,
    api_field_count = 3
)
response = client.asset.save(apiObject)  
object_qualified_name = response.assets_created(asset_type=APIObject)[0].qualified_name 

# Step 4: Define child assets if typedef supports 
fields = [
     {"name": "Example Location Name"},
    {"name": "Example State"},
    {"name": "Example Zip"}

]
responses = []

# Step 5: Create child assets
for field in fields:
    apifield = APIField.creator(
        name=field["name"],
        parent_api_object_qualified_name=object_qualified_name,
        parent_api_query_qualified_name=None,
        connection_qualified_name=connection_qualified_name,
       # api_field_type=field["type"],
       # api_field_type_secondary=field["secondary"]
    )
    response = client.asset.save(apifield)
    responses.append(response)
