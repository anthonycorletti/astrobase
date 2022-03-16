from typing import List

import typer
import yaml

from astrobasecloud.providers.main import AstrobaseAWSClient
from astrobasecloud.utils.str_to_dict import str_to_dict

app = typer.Typer(help="""Manage Amazon Elastic Kubernetes Engine Clusters.""")


@app.command("create")
def _create(
    kubernetes_control_plane_arn: str = typer.Option(...),
    cluster_subnet_id: List[str] = typer.Option(...),
    cluster_security_group_id: List[str] = typer.Option(...),
    nodegroup_noderole_mapping: str = typer.Option(
        ...,
        help="A mapping of nodegroup name to the nodegroup role arn."
        " Format: nodegroupname=fullArn,nodegroupname2=fullArn2",
    ),
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    ),
) -> None:
    """Create one or many Kubernetes clusters."""
    ab_client = AstrobaseAWSClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            cluster_spec = spec["cluster"]
            cluster_spec["roleArn"] = kubernetes_control_plane_arn
            cluster_spec["resourcesVpcConfig"] = {}
            cluster_spec["resourcesVpcConfig"]["subnetIds"] = cluster_subnet_id
            cluster_spec["resourcesVpcConfig"][
                "securityGroupIds"
            ] = cluster_security_group_id
            nodegroup_noderole_map = str_to_dict(input_str=nodegroup_noderole_mapping)
            for ng in cluster_spec["nodegroups"]:
                ng["nodeRole"] = nodegroup_noderole_map[ng["nodegroupName"]]
            ab_client.create_cluster(cluster_spec=cluster_spec)


@app.command("delete")
def _delete(
    kubernetes_control_plane_arn: str = typer.Option(...),
    cluster_subnet_id: List[str] = typer.Option(...),
    cluster_security_group_id: List[str] = typer.Option(...),
    nodegroup_noderole_mapping: str = typer.Option(
        ...,
        help="A mapping of nodegroup name to the nodegroup role arn."
        " Format: nodegroupname=fullArn,nodegroupname2=fullArn2",
    ),
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    ),
) -> None:
    """Delete one or many Kubernetes clusters."""
    ab_client = AstrobaseAWSClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            cluster_spec = spec["cluster"]
            cluster_spec["roleArn"] = kubernetes_control_plane_arn
            cluster_spec["resourcesVpcConfig"] = {}
            cluster_spec["resourcesVpcConfig"]["subnetIds"] = cluster_subnet_id
            cluster_spec["resourcesVpcConfig"][
                "securityGroupIds"
            ] = cluster_security_group_id
            nodegroup_noderole_map = str_to_dict(input_str=nodegroup_noderole_mapping)
            for ng in cluster_spec["nodegroups"]:
                ng["nodeRole"] = nodegroup_noderole_map[ng["nodegroupName"]]
            ab_client.delete_cluster(cluster_spec=cluster_spec)
