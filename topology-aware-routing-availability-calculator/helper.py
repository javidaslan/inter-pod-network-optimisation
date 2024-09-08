from logger import setup_logger

logger = setup_logger('helper')


def get_all_azs(nodes):
    azs = []
    logger.info("Getting list of AZs")
    for node in nodes:
        if node['az'] not in azs:
            azs.append(node['az'])
    return azs


def find_pod_az_distribution(nodes, deployment_info):
    nodes_for_deployment = deployment_info['nodes']
    logger.info("Creating pod-az distribution info")
    pod_az_distribution = {
        'name': deployment_info['name'],
        'number_of_endpoints': deployment_info['number_of_endpoints']
    }
    for nop in nodes_for_deployment:
        for node in nodes:
            if nop == node['name']:
                az = node['az']
                if az in pod_az_distribution:
                    pod_az_distribution[az] += deployment_info['nodes'][nop]['pods']
                else:
                    pod_az_distribution[az] = deployment_info['nodes'][nop]['pods']
    return pod_az_distribution
