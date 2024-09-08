import math
from helper import get_all_azs
from logger import setup_logger

logger = setup_logger('tar-availability-calculator')


def calculate_sum_of_vcpu(az, nodes):
    sum_az_vcpu = 0
    sum_all_vcpu = 0
    for node in nodes:
        if node['az'] == az:
            sum_az_vcpu += node['vcpu']
        sum_all_vcpu += node['vcpu']
    return sum_az_vcpu, sum_all_vcpu


def calculate_availability(nodes, distribution_config):
    # get all AZs
    azs = get_all_azs(nodes)
    overload_threshold = 0.2
    results_per_az = []
    number_of_endpoints = distribution_config['number_of_endpoints']
    for az in azs:
        logger.info(f"Calculating availability for {az}")
        sum_az_vcpu, sum_all_vcpu = calculate_sum_of_vcpu(az, nodes)
        expected_ratio = sum_az_vcpu/sum_all_vcpu
        minimum_endpoints = math.ceil((number_of_endpoints * expected_ratio)/(1+overload_threshold))

        # we are checking against all AZs, but it is possible that deployment has no pods in given AZ
        # following condition checks it
        if az in distribution_config:
            endpoints_per_az = distribution_config[az]
        else:
            endpoints_per_az = 0
        results_per_az.append({
            'AZ': az,
            'vCPUs': sum_az_vcpu,
            'all_vCPUs': sum_all_vcpu,
            'Minimum Endpoints': minimum_endpoints,
            'Endpoints': endpoints_per_az,
            'Sufficient Endpoints': endpoints_per_az >= minimum_endpoints,
            'Expected Ratio': expected_ratio
        })
    return results_per_az
