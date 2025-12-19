import base64
import json
from googleapiclient import discovery

def kill_billing(event, context):
    data = json.loads(
        base64.b64decode(event["data"]).decode("utf-8")
    )

    project_id = data["budgetDisplayName"].split("/")[-1]

    billing = discovery.build("cloudbilling", "v1")
    billing.projects().updateBillingInfo(
        name=f"projects/{project_id}",
        body={"billingAccountName": ""}
    ).execute()