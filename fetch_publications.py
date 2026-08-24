# import json
# import requests


print("THIS IS THE NEW FETCH_PUBLICATIONS.PY")
print("If you see this message, GitHub is running the correct file.")

# ORCID_ID = "0009-0008-4893-8029"

# url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

# response = requests.get(
#     url,
#     headers={
#         "Accept": "application/json"
#     }
# )

# print("HTTP status:", response.status_code)

# if not response.ok:
#     print("ORCID response:")
#     print(response.text)
#     response.raise_for_status()

# works = response.json()

# with open("publications.json", "w", encoding="utf-8") as f:
#     json.dump(works, f, indent=2, ensure_ascii=False)

# groups = works.get("group", [])

# print(f"Successfully retrieved {len(groups)} publication groups.")
