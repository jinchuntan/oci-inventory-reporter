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
