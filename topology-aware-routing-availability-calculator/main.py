import boto3
from pprint import pprint
import argparse
from k8s import K8S
from helper import find_pod_az_distribution
from aws import AWS
from tar_availability_calculator import calculate_availability


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate availability of Topology Aware Routing')
    parser.add_argument('--ctx', type=str, required=True, help='Kubernetes cluster context')
    parser.add_argument('--namespace', type=str, required=True, help='Kubernetes namespace')
    parser.add_argument('--deployment', type=str, required=True, help='Kubernetes deployment name')
    args = parser.parse_args()

    cluster_context = args.ctx
    namespace = args.namespace
    deployment = args.deployment

    instance_details = {}

    if cluster_context and namespace and deployment:
        print('\n', '-'*25, "TAR Calculation Logs", "-"*25, '\n')
        k8s = K8S(kube_config_context=cluster_context)
        all_nodes = k8s.extract_node_info(k8s.list_nodes())
        deployment_info = k8s.get_nodes_for_deployment(namespace, deployment)
        pod_az_distribution = find_pod_az_distribution(nodes=all_nodes, deployment_info=deployment_info)

        ec2_client = boto3.client('ec2', region_name="eu-central-1")
        aws = AWS(client=ec2_client)

        for node in all_nodes:
            instance_type = node['instance_type']
            if instance_type in instance_details:
                node['vcpu'] = instance_details[instance_type]['vcpu']
            else:
                details = aws.describe_instance_type(instance_type=instance_type)
                instance_details[instance_type] = details
                node['vcpu'] = details['vcpu']
        results = calculate_availability(all_nodes, pod_az_distribution)
        print('\n', '-'*25, "POD AZ Distribution", "-"*25, '\n')
        pprint(pod_az_distribution)
        print('\n', '-'*25, "TAR Availability Calculation Results", "-"*25, '\n')
        pprint(results)
