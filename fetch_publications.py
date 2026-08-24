import os
import json
import requests

ORCID_ID = "0009-0008-4893-8029"

CLIENT_ID = os.environ["ORCID_CLIENT_ID"]
CLIENT_SECRET = os.environ["ORCID_CLIENT_SECRET"]

# Get an access token
token_response = requests.post(
    "https://orcid.org/oauth/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "/read-public",
    },
    headers={
        "Accept": "application/json"
    },
)

token_response.raise_for_status()
access_token = token_response.json()["access_token"]

# Retrieve the ORCID works
works_response = requests.get(
    f"https://pub.orcid.org/v3.0/{ORCID_ID}/works",
    headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    },
)

works_response.raise_for_status()
works = works_response.json()

# Save the raw public works data
with open("publications.json", "w", encoding="utf-8") as f:
    json.dump(works, f, indent=2)

print(f"Retrieved {len(works.get('group', []))} publication groups.")
