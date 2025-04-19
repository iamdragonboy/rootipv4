import random
import string

user_vps_data = {}

default_ports = [80, 443, 22, 2022, 8080, 5080, 3001]
random_domains = [
    "node1.example.com",
    "vpshost.net",
    "cloud-zone.io",
    "ipv4hub.org",
    "edge-node.xyz"
]

def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def deploy_vps(user_id):
    user_id = str(user_id)
    ssh_pass = generate_password()
    vps_ip = f"192.168.{random.randint(1, 254)}.{random.randint(2, 254)}"
    user_vps_data[user_id] = {
        "ports": [],
        "ssh_pass": ssh_pass,
        "ip": vps_ip
    }
    return vps_ip, ssh_pass

def start_vps(user_id):
    return f"VPS started for user {user_id}."

def restart_vps(user_id):
    return f"VPS restarted for user {user_id}."

def list_vps(user_id):
    user_id = str(user_id)
    data = user_vps_data.get(user_id, {})
    ports = data.get("ports", [])
    ip = data.get("ip", "N/A")
    return f"VPS IP: {ip} | Ports: {', '.join(map(str, ports)) or 'None'}"

def show_all_node_users():
    if not user_vps_data:
        return "No active VPS users."
    return "Active VPS users:\n" + "\n".join([f"- User {uid}" for uid in user_vps_data])

def delete_vps(user_id):
    user_id = str(user_id)
    if user_id in user_vps_data:
        del user_vps_data[user_id]
        return f"VPS deleted for user {user_id}."
    return "No VPS to delete."

def node_admin():
    return "Node status: online. All systems normal."

def add_ports(user_id):
    user_id = str(user_id)
    if user_id not in user_vps_data:
        return "Please deploy your VPS first using `./deployipv4`"
    user_vps_data[user_id]["ports"] = default_ports.copy()
    return f"Ports added: {', '.join(map(str, default_ports))}"

def get_port_urls(user_id):
    user_id = str(user_id)
    ports = user_vps_data.get(user_id, {}).get("ports", [])
    if not ports:
        return "No ports assigned. Use `./port add` first."
    domain = random.choice(random_domains)
    urls = [f"http://{domain}:{port}" for port in ports]
    return "Port URLs:\n" + "\n".join(urls)
