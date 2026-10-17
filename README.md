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

## Setup and Run

Run these commands from the repository root with Python 3.11 or newer.
Configure OCI API-key authentication in `~/.oci/config` first
(`%USERPROFILE%\.oci\config` on Windows).

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
.\.venv\Scripts\python.exe src/main.py
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env with your compartment OCID and destination bucket before running.
.venv/bin/python src/main.py
```

Copy the template only on first setup; keep an existing `.env` when updating.
If your Windows installation uses `python` instead of `py -3.11`, substitute
that command when creating the environment. No environment activation is needed.

### Configuration and Permissions

| Setting | Meaning |
| --- | --- |
| `OCI_COMPARTMENT_OCID` | Required: the compartment to inspect. |
| `OCI_BUCKET_NAME` | Required: the destination bucket for reports. |
| `OCI_OBJECT_PREFIX` | Report object prefix; defaults to `inventory`. |
| `OCI_PROFILE` | OCI SDK profile name; defaults to `DEFAULT`. |

The configured identity must be allowed to read Compute instances, VCNs and subnets,
resolve the Object Storage namespace, and upload objects to the selected bucket.
The script checks the bucket and creates a private bucket if it is missing,
so it also needs permission to read the bucket and create it when necessary.
Reports are saved under `reports/` before upload. Resource collection is read-only,
but uploading reports writes to Object Storage.

Local `.env` files, signing keys, environments and generated reports are ignored by Git.

## Output
<img width="940" height="184" alt="image" src="https://github.com/user-attachments/assets/4205c8c1-4992-48ae-835e-2192b88de511" />
<img width="940" height="449" alt="image" src="https://github.com/user-attachments/assets/b573497f-cacf-4119-a340-faea9fba8b8c" />
