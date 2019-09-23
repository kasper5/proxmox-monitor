## Nagios plugin for monitoring Proxmox hypervisors.


Check if a Proxmox node is online:

``python3.7 proxmox-monitor.py check-node --node <node_name> --node-status``

Check memory usage on a Proxmox node:

``python3.7 proxmox-monitor.py check-node --node <node_name> --mem-usage``

Check if a service is running on a Proxmox node:

``python3.7 proxmox-monitor.py check-node --node <node_name> --service pveproxy``

Check subscription status on a Proxmox node:

``python3.7 proxmox-monitor.py check-node --node <node_name> --sub-status``
