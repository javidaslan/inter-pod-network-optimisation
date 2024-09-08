from kubernetes import client, config
from logger import setup_logger


class K8S:

    def __init__(self, kube_config_context=None):
        self.kube_config_context = kube_config_context
        if kube_config_context:
            config.load_kube_config(context=kube_config_context)
        else:
            config.load_kube_config()
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.logger = setup_logger('k8s')

    def list_nodes(self):
        try:
            self.logger.info(f"Getting all nodes from {self.kube_config_context}")
            nodes = self.core_v1.list_node()
            return nodes.items
        except client.exceptions.ApiException as e:
            self.logger.error(f"Exception when calling CoreV1Api->list_node: {e}")
            return []

    def extract_node_info(self, nodes):
        node_info_list = []
        try:
            self.logger.info(f"Extracting info from nodes")
            for node in nodes:
                name = node.metadata.name
                labels = node.metadata.labels
                az = labels.get('failure-domain.beta.kubernetes.io/zone', 'N/A')
                instance_type = labels.get('beta.kubernetes.io/instance-type', 'N/A')
                node_info_list.append({
                    'name': name,
                    'az': az,
                    'instance_type': instance_type
                })
            return node_info_list
        except Exception as e:
            self.logger.error(f"Exception while getting info from nodes: {e}")

    def get_nodes_for_deployment(self, namespace, deployment_name):
        deployment_info = {
            'name': deployment_name,
            'nodes': {}
        }
        try:
            self.logger.info(f"Getting nodes for deployment: {deployment_name}")
            deployment = self.apps_v1.read_namespaced_deployment(deployment_name, namespace)
            label_selector = deployment.spec.selector.match_labels
            label_selector_str = ','.join([f"{key}={value}" for key, value in label_selector.items()])
        except client.exceptions.ApiException as e:
            self.logger.error(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")
            return []
        try:
            pods = self.core_v1.list_namespaced_pod(namespace, label_selector=label_selector_str)
        except client.exceptions.ApiException as e:
            self.logger.error(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
            return []

        # Get the nodes where the pods are scheduled
        for pod in pods.items:
            node_name = pod.spec.node_name
            if node_name in deployment_info['nodes']:
                deployment_info['nodes'][node_name]['pods'] += 1
            else:
                deployment_info['nodes'][node_name] = {
                    'pods': 1
                }
        deployment_info['number_of_endpoints'] = len(pods.items)
        return deployment_info
