import boto3
import logging
import argparse
from k8s import get_hosts

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger("Main")


def get_entries(profile=None, hosted_zone_id=None):
    names = []
    boto3.setup_default_session(profile_name=profile)
    route53 = boto3.client("route53")

    result = route53.list_resource_record_sets(HostedZoneId=hosted_zone_id )

    logger.info(f"Found: {result['ResourceRecordSets']}")

    for entries in result["ResourceRecordSets"]:
        logger.info(f"Adding name: {entries['Name']} to list")
        names.append(entries["Name"])

    logger.info(f"returning: {names}")

    return names


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create iam user for eks clusters on aws")
    parser.add_argument("--profile", type=str,  dest="profile", help="name of the aws profile in ~/.aws/credentials",
                        required=True)
    parser.add_argument("--zone-id", type=str, dest="zone_id", help="route 53 zone id", default=None)

    args = parser.parse_args()

    hosts = get_hosts()
    entries = get_entries(profile=args.profile, hosted_zone_id=args.zone_id)


    for host in hosts:
        try:
            logging.info(f"Checkinf if {host} is present in route53")
            assert f"{host}." in entries
        except AssertionError as error:
            logger.error(f"Record {host} does not exist on route53!!! On noes :O")


