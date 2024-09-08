import boto3
from logger import setup_logger


class AWS:

    def __init__(self, client=None):
        self.logger = setup_logger('aws')
        self.client = client

    def describe_instance_type(self, instance_type):
        try:
            self.logger.info(f"Getting instance details for: {instance_type}")
            # Call the describe_instance_types method with specific instance type
            response = self.client.describe_instance_types(
                InstanceTypes=[instance_type]
            )
            # Check if we have any instance types returned
            if response['InstanceTypes']:
                # Extract the details of the instance type
                instance_type_details = response['InstanceTypes'][0]

                # Print out details of the specified instance type
                return {
                    "vcpu": instance_type_details['VCpuInfo']['DefaultVCpus']
                }
            else:
                self.logger.warn(f"No details found for instance type: {instance_type}")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
