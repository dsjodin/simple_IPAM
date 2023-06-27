import requests

# API endpoint URL
api_url = "http://localhost:8000/ip_addresses/"

# Remove the reservation of an IP address by sending a PUT request to the API
def remove_reservation(ip_address):
    url = api_url + f"{ip_address}/release/"
    response = requests.put(url)
    if response.status_code == 200:
        print("Reservation removed successfully.")
    else:
        print("Failed to remove reservation.")

# Example usage: Remove the reservation of an IP address
ip_address = "192.168.0.100"

remove_reservation(ip_address)
