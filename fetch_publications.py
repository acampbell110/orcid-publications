import os
import json
import requests

ORCID_ID = "0009-0008-4893-8029"

CLIENT_ID = os.environ["ORCID_CLIENT_ID"]
CLIENT_SECRET = os.environ["ORCID_CLIENT_SECRET"]

# --------------------------------------------------
# Get ORCID public API access token
# --------------------------------------------------

token_response = requests.post(
    "https://orcid.org/oauth/token",
    headers={
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    },
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "/read-public",
    },
)

if not token_response.ok:
    print("ORCID token request failed:")
    print(token_response.text)
    token_response.raise_for_status()

access_token = token_response.json()["access_token"]

print("Successfully obtained ORCID access token.")

# --------------------------------------------------
# Retrieve public works
# --------------------------------------------------

works_response = requests.get(
    f"https://pub.orcid.org/v3.0/{ORCID_ID}/works",
    headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    },
)

if not works_response.ok:
    print("ORCID works request failed:")
    print(works_response.text)
    works_response.raise_for_status()

works = works_response.json()

# --------------------------------------------------
# Save the ORCID data
# --------------------------------------------------

with open("publications.json", "w", encoding="utf-8") as f:
    json.dump(works, f, indent=2, ensure_ascii=False)

groups = works.get("group", [])

print(f"Successfully retrieved {len(groups)} publication groups.")
