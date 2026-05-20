import json
import os
import uuid
import urllib.request
from copy import deepcopy
from dotenv import load_dotenv

# Load credentials
load_dotenv()
ATLAN_BASE_URL =os.getenv('ATLAN_BASE_URL')
ATLAN_API_KEY =os.getenv('ATLAN_API_KEY')

# This must be your Generic OpenLineage connection name in Atlan
JOB_NAMESPACE = "atlan-ol" # Name of Generic OpenLineage Connection

ORACLE_NAMESPACE = "oracle"
ORACLE_TABLE = "FinanceDB.Gold.Instruments"
ORACLE_COLUMN = "Instrument_Name"

BQ_NAMESPACE = "bigquery"
BQ_TABLE = "wide-world-importers-387612.analytics.d_workcenter"
BQ_COLUMN = "object_id"

ENDPOINT = f"{ATLAN_BASE_URL}/events/openlineage/generic-openlineage/api/v1/lineage"
RUN_ID = str(uuid.uuid4())
PRODUCER = "https://atlan-demo.local/manual-openlineage"

base_event = {
    "eventTime": "2026-05-20T14:30:00.000Z",
    "eventType": "START",
    "producer": PRODUCER,
    "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent",
    "run": {
        "runId": RUN_ID
    },
    "job": {
        "namespace": JOB_NAMESPACE,
        "name": "oracle_to_bigquery_finance_instruments",
        "facets": {
            "jobType": {
                "_producer": PRODUCER,
                "_schemaURL": "https://openlineage.io/spec/facets/1-0-0/JobTypeJobFacet.json#/$defs/JobTypeJobFacet",
                "integration": "custom",
                "jobType": "JOB",
                "processingType": "BATCH"
            }
        }
    },
    "inputs": [
        {
            "namespace": ORACLE_NAMESPACE,
            "name": ORACLE_TABLE,
            "facets": {
                "schema": {
                    "_producer": PRODUCER,
                    "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
                    "fields": [
                        {"name": ORACLE_COLUMN, "type": "VARCHAR2"}
                    ]
                }
            }
        }
    ],
    "outputs": [
        {
            "namespace": BQ_NAMESPACE,
            "name": BQ_TABLE,
            "facets": {
                "schema": {
                    "_producer": PRODUCER,
                    "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
                    "fields": [
                        {"name": BQ_COLUMN, "type": "STRING"}
                    ]
                },
                "columnLineage": {
                    "_producer": PRODUCER,
                    "_schemaURL": "https://openlineage.io/spec/facets/1-2-0/ColumnLineageDatasetFacet.json#/$defs/ColumnLineageDatasetFacet",
                    "fields": {
                        BQ_COLUMN: {
                            "inputFields": [
                                {
                                    "namespace": ORACLE_NAMESPACE,
                                    "name": ORACLE_TABLE,
                                    "field": ORACLE_COLUMN,
                                    "transformations": [
                                        {
                                            "type": "DIRECT",
                                            "subtype": "IDENTITY",
                                            "description": "Mapped from Oracle Instrument_Name to BigQuery object_id"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }
    ]
}

complete_event = deepcopy(base_event)
complete_event["eventType"] = "COMPLETE"
complete_event["eventTime"] = "2026-05-20T14:31:00.000Z"

def send_event(event):
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(event).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {ATLAN_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Atlan-PythonSDK/9.7.2",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"{event['eventType']} -> {resp.status}")
            print(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} {e.reason}")
        print("Response body:", e.read().decode("utf-8", errors="ignore"))
        print("Endpoint:", ENDPOINT)

send_event(base_event)
send_event(complete_event)

