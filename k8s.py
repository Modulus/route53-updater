from kubernetes import client, config
from pprint import pprint
# Configs can be set in Configuration class directly or using helper utility

def get_hosts():
    config.load_kube_config()

    k8s_client = client.ExtensionsV1beta1Api()

    result = k8s_client.list_ingress_for_all_namespaces()


    print("Listing result")

    hosts = []
    if result.items:
        for item in result.items:
            for rules in item.spec.rules:
                hosts.append(rules.host)

    pprint(hosts)
    return hosts
