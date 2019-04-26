# What is this
Simple command line tool to update route53 entries with ingress names on triggering


# How to use
pip install -r requirements.txt
python main.py --profile "aws-cli profile name" --zone-id "route53 zone id" --target "elb-dns-name" --target-zone-id "target zone of elb"

# Verify all ingresses have route53 aliases
python verify.py --profile "aws-cli profile nmae" --zone-id "route 53 zone id"


# NB! 
You can leave out the quotes from all parameters