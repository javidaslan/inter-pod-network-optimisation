# Topology Aware Routing Availability (TAR) Calculator

This script calculate whether TAR can be enabled for given deployment with current distribution of pods across availability zones.

Script is based on AWS Article: [Exploring the effect of Topology Aware Hints on network traffic in Amazon Elastic Kubernetes Service](https://aws.amazon.com/blogs/containers/exploring-the-effect-of-topology-aware-hints-on-network-traffic-in-amazon-elastic-kubernetes-service/)

## how to use script

1. Install [requirements.txt](./requirements.txt)
2. Make sure you have access to necessary kubernetes cluster
3. Login to AWS (this is needed to get instance details from AWS API)
4. Run script:
    ```shell
    python main.py --ctx <cluster_name> --namespace <namespace> --deployment <deployment>
    ```

## Output

Example output can be as following:

```json

[{'AZ': 'eu-central-1a',
  'Endpoints': 3,
  'Expected Ratio': 0.4166666666666667,
  'Minimum Endpoints': 3,
  'Sufficient Endpoints': True,
  'all_vCPUs': 48,
  'vCPUs': 20},
 {'AZ': 'eu-central-1b',
  'Endpoints': 2,
  'Expected Ratio': 0.25,
  'Minimum Endpoints': 2,
  'Sufficient Endpoints': True,
  'all_vCPUs': 48,
  'vCPUs': 12},
 {'AZ': 'eu-central-1c',
  'Endpoints': 3,
  'Expected Ratio': 0.3333333333333333,
  'Minimum Endpoints': 3,
  'Sufficient Endpoints': True,
  'all_vCPUs': 48,
  'vCPUs': 16}]
```
