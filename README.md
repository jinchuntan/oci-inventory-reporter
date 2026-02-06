# OCI Inventory Reporter (Markdown + CSV + Object Storage Upload)

This repo generates an OCI resource inventory report for a target compartment and uploads it to OCI Object Storage.

## What it does

- Lists Compute instances
- Lists VCNs and their Subnets
- Generates Markdown + CSV reports
- Uploads the reports to an Object Storage bucket

## Prerequisites

- Python 3.9+
- OCI config file at `~/.oci/config` (API key auth)

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

## Output
<img width="940" height="184" alt="image" src="https://github.com/user-attachments/assets/4205c8c1-4992-48ae-835e-2192b88de511" />
<img width="940" height="449" alt="image" src="https://github.com/user-attachments/assets/b573497f-cacf-4119-a340-faea9fba8b8c" />
