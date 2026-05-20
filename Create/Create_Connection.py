#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectionCategory, AtlanConnectorType

# Load credentials
load_dotenv()
ATLAN_BASE_URL =os.getenv('ATLAN_BASE_URL')
ATLAN_API_KEY =os.getenv('ATLAN_API_KEY')

client = AtlanClient(
    base_url= ATLAN_BASE_URL,
    api_key = ATLAN_API_KEY
)

admin_role_guid = client.role_cache.get_id_for_name("$admin")
    
# Create a connection, change the connector type 
connection = Connection.creator(
        client=client,
        name="MSSQL_API_Test",
        connector_type=AtlanConnectorType.MSSQL,  # change the connector type
        admin_roles=[admin_role_guid],
    )
        
print("💾 Saving connection...")
    
# Save the connection to Atlan
response = client.asset.save(connection)
