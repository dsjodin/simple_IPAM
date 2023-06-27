import requests

# API endpoint URL
api_url = "http://localhost:4000/ip_addresses/"

# Reserve an IP address by sending a POST request to the API
def reserve_ip_address(ip_address, hostname, vlan_id):
    payload = {
        "ip_address": ip_address,
        "hostname": hostname,
        "vlan_id": vlan_id
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        print("IP address reserved successfully.")
    else:
        print("Failed to reserve IP address.")

# Example usage: Reserve an IP address
ip_address = "192.168.0.100"
hostname = "example-hostname"
vlan_id = 10

reserve_ip_address(ip_address, hostname, vlan_id)
