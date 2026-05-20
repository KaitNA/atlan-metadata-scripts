import os
import logging
from dotenv import load_dotenv
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import AtlanConnectorType , APIQueryParamTypeEnum
from pyatlan.model.assets import Connection, APISpec, APIPath, APIObject, APIQuery, APIField 

# Load environment variables from .env file
load_dotenv()
BASE_URL = str(os.getenv('ATLAN_BASE_URL'))
API_KEY = str(os.getenv('ATLAN_API_KEY'))

### Intialize Client
client = AtlanClient(
    base_url= BASE_URL,
    api_key = API_KEY
)
# STEP 1: 
# #Get the admin role GUID (required for connection creation)
admin_role_guid = client.role_cache.get_id_for_name("$admin")

# Create a connection with the desired connector type. Uncomment this section to create a connection
#connection = Connection.creator(
#    name="Banking APP",  # Provide a human-readable name for your connection
#    connector_type=AtlanConnectorType.APP,  # Set the connector type you want
#    admin_roles=[admin_role_guid],  # Specify who can administer this connection
    # Optional: You can also specify admin groups or users
    # admin_groups=["group-name"],
    # admin_users=["username"],

# Save the connection to Atlan
#response = client.asset.save(connection)

# Get the qualified name of the created connection
#connection_qualified_name = response.assets_created(asset_type=Connection)[0].qualified_name
#print(f"Connection created successfully with qualified name: {connection_qualified_name}")

#STEP 2: Create API spec and object first
connection_qualified_name= 'default/api/1779216981' #connection_qualified_name -use this if you created a connection
spec_qualified_name = 'default/api/1779216981/Example_API'

# Create API object
apiObject = APIObject.creator(
    name="release",
    connection_qualified_name = connection_qualified_name,
    api_field_count = 3
)
response = client.asset.save(apiObject) # 
object_qualified_name = response.assets_created(asset_type=APIObject)[0].qualified_name 

# Step 4: Define field metadata
fields = [
     {"name": "INDUSTRY_LOAN"},
    {"name": "RATE"},
    {"name": "TYPE"}

]

responses = []

# Step 5: Create API fields
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
