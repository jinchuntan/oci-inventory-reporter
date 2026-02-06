import oci


def list_instances(config: dict, signer, compartment_id: str):
    compute = oci.core.ComputeClient(config=config, signer=signer)
    instances = compute.list_instances(compartment_id=compartment_id).data
    out = []
    for i in instances:
        out.append({
            "type": "compute_instance",
            "name": i.display_name,
            "state": i.lifecycle_state,
            "ocid": i.id,
            "availability_domain": getattr(i, "availability_domain", ""),
        })
    return out


def list_vcns_and_subnets(config: dict, signer, compartment_id: str):
    vcn_client = oci.core.VirtualNetworkClient(config=config, signer=signer)

    vcns = vcn_client.list_vcns(compartment_id=compartment_id).data
    out = []

    for v in vcns:
        out.append({
            "type": "vcn",
            "name": v.display_name,
            "state": v.lifecycle_state,
            "ocid": v.id,
            "cidr": v.cidr_block,
        })

        subnets = vcn_client.list_subnets(compartment_id=compartment_id, vcn_id=v.id).data
        for s in subnets:
            out.append({
                "type": "subnet",
                "name": s.display_name,
                "state": s.lifecycle_state,
                "ocid": s.id,
                "cidr": s.cidr_block,
                "vcn_name": v.display_name,
            })

    return out
