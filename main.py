from k8s import get_hosts
from route53 import add_dns, remove_dns
import logging
import argparse

from botocore.errorfactory import ClientError
# Initializing loggers and requisites
FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger("Main")

if __name__ == "__main__":

    logger.info("Creating route53 entry for kubernetes nginx ingress")

    parser = argparse.ArgumentParser(description="Create iam user for eks clusters on aws")
    parser.add_argument("--profile", type=str,  dest="profile", help="name of the aws profile in ~/.aws/credentials",
                        required=True)
    parser.add_argument("--zone-id", type=str, dest="zone_id", help="route 53 zone id", default=None)
    parser.add_argument("--target", type=str, dest="target", help="target dns name entry (elb dns name or similar)", default=None)
    parser.add_argument("--target-zone-id", type=str, dest="target_zone_id", help="target dns zone id", default=None)
    parser.add_argument("--region", type=str, dest="region", help="region of target (ie eu-west-1)", default="eu-west-1")
    parser.add_argument("--delete", type=str, dest="delete", help="to delete entries (yes/no)", default="no")

    args = parser.parse_args()

    logger.info(f"Using profile {args.profile}")
    logger.info(f"Target: {args.target}")
    logger.info(f"Zone id: {args.zone_id}")
    logger.info(f"Target zoner id: {args.target_zone_id}")
    logger.info(f"Region of target: {args.region}")

    hosts = get_hosts()
    print(f"Found these hosts: {hosts}")

    for host in hosts:
        try:
            if args.delete == "no" or not args.delete:
                add_dns(ingress=host,
                        zone_id=args.zone_id,
                        elb_zone_id=args.target_zone_id,
                        elb_dns=args.target,
                        region=args.region,
                        profile=args.profile)
            elif args.delete == "yes":
                remove_dns(ingress=host,
                           zone_id=args.zone_id,
                           elb_zone_id=args.target_zone_id,
                           elb_dns=args.target,
                           region=args.region,
                           profile=args.profile)
            else:
                logger.error("What are you trying to do? I cannot understand your command. \
                Either remote the --delete flag og write --delete yes/no")
        except ClientError as error:
            logger.error(f"Failed to add dns entry for {host}, because of {error}")
