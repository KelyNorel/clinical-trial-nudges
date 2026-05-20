

"""
Download completed U.S. interventional clinical trials from ClinicalTrials.gov API v2.
Filters for trials with actual enrollment data.
"""

import requests
import pandas as pd
import time
import json
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

PARAMS = {
    "filter.overallStatus": "COMPLETED",
    "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
    "pageSize": 500,
}

NUDGE_KEYWORDS = [
    "reminder", "nudge", "notification", "outreach", "letter",
    "email", "text message", "sms", "phone call", "navigator",
    "incentive", "recruitment", "engagement", "motivational"
]

MAX_STUDIES = 20000

def fetch_all_studies():
    studies = []
    params = PARAMS.copy()
    page = 1

    print("Fetching studies from ClinicalTrials.gov API v2...")

    while True:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        batch = data.get("studies", [])
        studies.extend(batch)
        print(f"  Page {page}: {len(batch)} studies (total: {len(studies)})")

        if len(studies) >= MAX_STUDIES:
            print(f"  Reached {MAX_STUDIES} limit, stopping.")
            break

        next_token = data.get("nextPageToken")
        if not next_token:
            break

        params["pageToken"] = next_token
        page += 1
        time.sleep(0.3)

    return studies[:MAX_STUDIES]

def parse_studies(studies):
    rows = []
    for s in studies:
        proto = s.get("protocolSection", {})

        id_mod      = proto.get("identificationModule", {})
        status_mod  = proto.get("statusModule", {})
        design_mod  = proto.get("designModule", {})
        sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
        cond_mod    = proto.get("conditionsModule", {})
        arms_mod    = proto.get("armsInterventionsModule", {})

        # Only keep trials with ACTUAL enrollment
        enrollment = design_mod.get("enrollmentInfo", {})
        if enrollment.get("type") != "ACTUAL":
            continue

        # Detect nudge/recruitment intervention in arm text
        arms = arms_mod.get("armGroups", [])
        arm_text = " ".join([
            a.get("label", "") + " " + a.get("description", "")
            for a in arms
        ]).lower()

        has_nudge = int(any(kw in arm_text for kw in NUDGE_KEYWORDS))

        # Phase
        phases = design_mod.get("phases", [])
        phase_str = ", ".join(phases) if phases else "N/A"

        # Conditions (up to 3)
        conditions = cond_mod.get("conditions", [])
        condition_str = "; ".join(conditions[:3]) if conditions else "N/A"

        # Is oncology?
        oncology_keywords = ["cancer", "tumor", "carcinoma", "leukemia",
                             "lymphoma", "melanoma", "oncol", "neoplasm"]
        is_oncology = int(any(
            kw in condition_str.lower() for kw in oncology_keywords
        ))

        # Sponsor class
        sponsor_class = sponsor_mod.get("leadSponsor", {}).get("class", "N/A")

        # Dates
        start = status_mod.get("startDateStruct", {}).get("date", None)
        completion = status_mod.get("completionDateStruct", {}).get("date", None)

        # Allocation (RANDOMIZED vs not)
        design_info = design_mod.get("designInfo", {})
        allocation = design_info.get("allocation", "N/A")

        rows.append({
            "nct_id": id_mod.get("nctId"),
            "title": id_mod.get("briefTitle"),
            "condition": condition_str,
            "is_oncology": is_oncology,
            "phase": phase_str,
            "enrollment_actual": enrollment.get("count"),
            "sponsor_class": sponsor_class,
            "allocation": allocation,
            "start_date": start,
            "completion_date": completion,
            "has_nudge": has_nudge,
            "arm_text_snippet": arm_text[:400],
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    studies = fetch_all_studies()

    # Save raw JSON
    raw_path = RAW_DIR / "studies_raw.json"
    with open(raw_path, "w") as f:
        json.dump(studies, f)
    print(f"\nSaved {len(studies)} raw studies to {raw_path}")

    # Parse
    df = parse_studies(studies)
    print(f"\nParsed {len(df)} studies with actual enrollment")
    print(f"  Nudge trials : {df['has_nudge'].sum()}")
    print(f"  Control      : {(df['has_nudge'] == 0).sum()}")
    print(f"  Oncology     : {df['is_oncology'].sum()}")
    print(f"  Randomized   : {(df['allocation'] == 'RANDOMIZED').sum()}")

    out_path = PROCESSED_DIR / "trials_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")
    print(df.head(3).to_string())