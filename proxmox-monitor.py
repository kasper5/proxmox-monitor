__author__ = "Kasper Fast"

import click
import sys
from proxmoxer import ProxmoxAPI

api_host = ""
api_username = ""
api_password = ""

mem_warn_threshold = "85"
mem_crit_threshold = "95"


proxmox = ProxmoxAPI(api_host, user=api_username,
                     password=api_password, verify_ssl=False)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--node', type=str, help="Proxmox node name.")
@click.option('--service', type=str, help="Proxmox service name.")
def check_service(node, service):
    for s in proxmox.nodes(node).services.get():
        if s['name'] == service:
            if s['state'] == "running":
                out = "OK: ({0}) => {1}".format(s['name'], s['state'])
                print(out)
                sys.exit(0)
            else:
                out = "CRITICAL: ({0}) => {1}".format(s['name'], s['state'])
                print(out)
                sys.exit(2)


@cli.command()
@click.option('--node', type=str, help="Proxmox node name.")
@click.option('--node-status', is_flag=True, help="Check Proxmox node status.")
@click.option('--mem-usage', is_flag=True, help="Check Proxmox node memory usage.")
@click.option('--sub-status', is_flag=True, help="Check Proxmox subscription status.")
def check_node(node, node_status, mem_usage, sub_status):

    if sub_status:
        sub_status = proxmox.nodes(node).subscription.get()['status']
        if sub_status != "Active":
            print("CRITICAL: subscription status on node ({0}) is {1}.".format(node, sub_status))
            sys.exit(2)
        else:
            print("OK: subscription status on node ({0}) is {1}.".format(node, sub_status))
            sys.exit(0)

    if mem_usage:
        for i in proxmox.cluster.resources.get():
            if i['type'] == "node":
                if i['node'] == node:
                    pct = '{0:.2f}'.format((i['mem'] / i['maxmem'] * 100))
                    if pct >= mem_crit_threshold:
                        print("CRITICAL: memory usage on node (" + node + ") is " + pct+"%")
                    elif pct >= mem_warn_threshold:
                        print("WARNING: memory usage on node (" + node + ") is " + pct+"%")
                    else:
                        print("OK: memory usage on node (" + node + ") is " + pct+"%")

    if node_status:
        for s in proxmox.cluster.status.get():
            if s['name'] == node:
                if s['online'] == 1:
                    out = "OK: node ({0}) is online.".format(s['name'])
                    print(out)
                    sys.exit(0)
                else:
                    out = "CRITICAL: node ({0}) is not online! Please investigate!".format(s['name'])
                    print(out)
                    sys.exit(2)


if __name__ == "__main__":
    cli()
