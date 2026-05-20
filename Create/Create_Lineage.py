from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import APIObject, Process, CustomEntity, Column, Table, Application, ApplicationField #import typedeffs
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
ATLAN_BASE_URL =os.getenv('ATLAN_BASE_URL')
ATLAN_API_KEY =os.getenv('ATLAN_API_KEY')

client = AtlanClient(
    base_url= ATLAN_BASE_URL,
    api_key = ATLAN_API_KEY
)


process = Process.creator(
    name=" API -> Oracle", # Give process a name
    connection_qualified_name="oracle/1234567", #Specify connection where process assets will be created under. 
    inputs=[APIObject.ref_by_qualified_name("default/api/1234567/APIName")], #change asset typedef and quali name
    outputs=[Table.ref_by_qualified_name("default/oracle/1234567/Database/Schema/Table")], #change asset typedef and quali name
)

resp = client.asset.save(process)

procs = resp.assets_created(Process) or resp.assets_updated(Process)
print("✓ Process saved:", procs[0].guid if procs else "no process returned")
