import json
import requests

ORCID_ID = "0009-0008-4893-8029"

BASE_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}"

headers = {
    "Accept": "application/json"
}


# --------------------------------------------------
# Get all works
# --------------------------------------------------

response = requests.get(
    f"{BASE_URL}/works",
    headers=headers
)

print("Works HTTP status:", response.status_code)

if not response.ok:
    print(response.text)
    response.raise_for_status()

works = response.json()

groups = works.get("group", [])

print(f"Retrieved {len(groups)} publication groups.")


# --------------------------------------------------
# Extract full information for each publication
# --------------------------------------------------

publications = []

for group in groups:

    summaries = group.get("work-summary", [])

    if not summaries:
        continue

    summary = summaries[0]

    put_code = summary.get("put-code")

    if not put_code:
        continue

    # Get full work record
    work_response = requests.get(
        f"{BASE_URL}/work/{put_code}",
        headers=headers
    )

    print(
        f"Fetching work {put_code}: "
        f"HTTP {work_response.status_code}"
    )

    if not work_response.ok:
        print(work_response.text)
        continue

    work = work_response.json()


    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    title = (
        work.get("title", {})
        .get("title", {})
        .get("value", "")
    )


    # --------------------------------------------------
    # Journal
    # --------------------------------------------------

    journal = (
        work.get("journal-title", {})
        .get("value", "")
    )


    # --------------------------------------------------
    # Publication date
    # --------------------------------------------------

    publication_date = work.get(
        "publication-date",
        {}
    )

    year = (
        publication_date
        .get("year", {})
        .get("value")
    )


    # --------------------------------------------------
    # DOI
    # --------------------------------------------------

    doi = None

    external_ids = (
        work.get("external-ids", {})
        .get("external-id", [])
    )

    for external_id in external_ids:

        if external_id.get(
            "external-id-type"
        ) == "doi":

            doi = external_id.get(
                "external-id-value"
            )

            break


    # --------------------------------------------------
    # Authors
    # --------------------------------------------------

    authors = []

    contributors = (
        work.get("contributors", {})
        .get("contributor", [])
    )

    for contributor in contributors:

        credit_name = (
            contributor
            .get("credit-name", {})
            .get("value")
        )

        if credit_name:
            authors.append(credit_name)


    # --------------------------------------------------
    # Save publication
    # --------------------------------------------------

    publications.append({
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "doi": doi
    })


# --------------------------------------------------
# Sort newest first
# --------------------------------------------------

publications.sort(
    key=lambda x: int(x["year"])
    if x["year"] else 0,
    reverse=True
)


# --------------------------------------------------
# Write simplified JSON
# --------------------------------------------------

with open(
    "publications.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        publications,
        f,
        indent=2,
        ensure_ascii=False
    )


print(
    f"Saved {len(publications)} publications."
)
