import boto3
import logging
# Initializing loggers and requisites
FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger("Main")


def add_dns(ingress=None, zone_id=None, elb_zone_id=None, elb_dns=None, region=None, profile=None):
    boto3.setup_default_session(profile_name=profile)
    route53 = boto3.client("route53")

    logger.info("Creating dns entry for ingress")

    logger.info(f"name: {ingress}")
    logger.info(f"zone_id: {zone_id}")
    logger.info(f"region: {region}")

    response = route53.change_resource_record_sets(
        HostedZoneId=f'{zone_id}',
        ChangeBatch={
            'Comment': f"DNS Entry for nginx ingress on kubernetes with name {ingress}",
            'Changes': [
                {
                    'Action': 'UPSERT', #'CREATE', #|'DELETE'|'UPSERT',
                    'ResourceRecordSet': {
                        'Name': f"{ingress}",
                        'Region' : f'{region}',
                        'SetIdentifier': f'{ingress}',
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': f'{elb_zone_id}',
                            'DNSName': f'{elb_dns}',
                            'EvaluateTargetHealth': False
                        },

                    }
                },
            ]
        }
    )

    logger.info(f"Response: {response}")