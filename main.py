#QnD Simple IPAM for test purpose

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'ipam'
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the IPAM table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ipam (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ip_address VARCHAR(15) UNIQUE,
        hostname VARCHAR(50),
        vlan_id INT,
        reserved BOOLEAN DEFAULT 0
    )
''')

class IPAddress(BaseModel):
    ip_address: str
    hostname: str
    vlan_id: int

class IPAddressResponse(BaseModel):
    id: int
    ip_address: str
    hostname: str
    vlan_id: int
    reserved: bool

@app.post("/ip_addresses/", response_model=IPAddressResponse)
def add_ip_address(ip_address: IPAddress):
    try:
        cursor.execute('INSERT INTO ipam (ip_address, hostname, vlan_id) VALUES (%s, %s, %s)',
                       (ip_address.ip_address, ip_address.hostname, ip_address.vlan_id))
        conn.commit()
        return {
            "id": cursor.lastrowid,
            "ip_address": ip_address.ip_address,
            "hostname": ip_address.hostname,
            "vlan_id": ip_address.vlan_id,
            "reserved": False
        }
    except mysql.connector.IntegrityError:
        return {"detail": "IP address already exists"}

@app.put("/ip_addresses/{ip_address}/reserve/")
def reserve_ip_address(ip_address: str, hostname: str):
    cursor.execute('UPDATE ipam SET reserved = 1, hostname = %s WHERE ip_address = %s', (hostname, ip_address))
    conn.commit()
    return {"detail": "IP address reserved successfully"}

@app.put("/ip_addresses/{ip_address}/release/")
def release_ip_address(ip_address: str):
    cursor.execute('UPDATE ipam SET reserved = 0, hostname = NULL WHERE ip_address = %s', (ip_address,))
    conn.commit()
    return {"detail": "IP address released successfully"}

@app.get("/ip_addresses/", response_model=List[IPAddressResponse])
def get_all_ip_addresses():
    cursor.execute('SELECT * FROM ipam')
    rows = cursor.fetchall()
    ip_addresses = []
    for row in rows:
        ip_address = {
            "id": row[0],
            "ip_address": row[1],
            "hostname": row[2],
            "vlan_id": row[3],
            "reserved": row[4]
        }
        ip_addresses.append(ip_address)
    return ip_addresses

@app.get("/", response_class=HTMLResponse)
def read_ip_addresses(request: Request):
    cursor.execute('SELECT * FROM ipam')
    rows = cursor.fetchall()
    ip_addresses = []
    for row in rows:
        ip_address = {
            "id": row[0],
            "ip_address": row[1],
            "hostname": row[2],
            "vlan_id": row[3],
            "reserved": row[4]
        }
        ip_addresses.append(ip_address)

    return templates
