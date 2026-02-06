import os
import sys
from pathlib import Path

import oci
from dotenv import load_dotenv

from inventory import list_instances, list_vcns_and_subnets
from report import timestamp_utc, write_markdown, write_csv


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        print(f"ERROR: Missing env var: {name}")
        sys.exit(1)
    return v


def get_config_and_signer():
    profile = os.getenv("OCI_PROFILE", "DEFAULT")
    config_file = os.path.expanduser("~/.oci/config")

    if not os.path.exists(config_file):
        print("ERROR: OCI config file not found at ~/.oci/config")
        sys.exit(1)

    config = oci.config.from_file(config_file, profile_name=profile)
    signer = oci.signer.Signer(
        tenancy=config["tenancy"],
        user=config["user"],
        fingerprint=config["fingerprint"],
        private_key_file_location=config["key_file"],
        pass_phrase=config.get("pass_phrase"),
    )
    return config, signer


def ensure_bucket(os_client, namespace: str, compartment_id: str, bucket_name: str):
    try:
        os_client.get_bucket(namespace_name=namespace, bucket_name=bucket_name)
        print(f"Bucket exists: {bucket_name}")
        return
    except oci.exceptions.ServiceError as e:
        if e.status != 404:
            raise

    details = oci.object_storage.models.CreateBucketDetails(
        name=bucket_name,
        compartment_id=compartment_id,
        public_access_type="NoPublicAccess",
        storage_tier="Standard",
        versioning="Disabled",
    )
    os_client.create_bucket(namespace_name=namespace, create_bucket_details=details)
    print(f"Bucket created: {bucket_name}")


def upload_file(os_client, namespace: str, bucket_name: str, object_name: str, file_path: Path):
    print(f"Uploading: {object_name}")
    with file_path.open("rb") as f:
        os_client.put_object(
            namespace_name=namespace,
            bucket_name=bucket_name,
            object_name=object_name,
            put_object_body=f
        )
    print("Upload complete.")


def main():
    load_dotenv()

    compartment_id = require_env("OCI_COMPARTMENT_OCID")
    bucket_name = require_env("OCI_BUCKET_NAME")
    prefix = os.getenv("OCI_OBJECT_PREFIX", "inventory")

    config, signer = get_config_and_signer()
    region = config.get("region", "")
    print(f"Using region: {region}")

    os_client = oci.object_storage.ObjectStorageClient(config=config, signer=signer)
    namespace = os_client.get_namespace().data
    print(f"Object Storage Namespace: {namespace}")

    # Gather inventory
    records = []
    records += list_instances(config, signer, compartment_id)
    records += list_vcns_and_subnets(config, signer, compartment_id)

    ts = timestamp_utc()
    reports_dir = Path("reports")
    md_path = reports_dir / f"inventory_{ts}.md"
    csv_path = reports_dir / f"inventory_{ts}.csv"

    write_markdown(records, md_path, header="OCI Resource Inventory Report")
    write_csv(records, csv_path)

    print(f"Generated: {md_path}")
    print(f"Generated: {csv_path}")

    # Upload to Object Storage
    ensure_bucket(os_client, namespace, compartment_id, bucket_name)
    upload_file(os_client, namespace, bucket_name, f"{prefix}/{md_path.name}", md_path)
    upload_file(os_client, namespace, bucket_name, f"{prefix}/{csv_path.name}", csv_path)

    print("Done.")


if __name__ == "__main__":
    main()
