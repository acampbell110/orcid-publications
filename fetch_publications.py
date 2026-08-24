import os
import requests

CLIENT_ID = os.environ["ORCID_CLIENT_ID"]
CLIENT_SECRET = os.environ["ORCID_CLIENT_SECRET"]

response = requests.post(
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

print("HTTP status:", response.status_code)
print("ORCID response:", response.text)

if response.ok:
    print("SUCCESS: ORCID accepted the credentials.")
else:
    print("FAILED: ORCID rejected the credentials.")
