import sqlite3
import subprocess

def get_clients():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT  ip_address, username, password FROM machines WHERE machine_type = 'user'")
    clients = [{"ip": row[0], "username": row[1], "password": row[2]} for row in c.fetchall()]
    conn.close()
    return clients

def get_software_repo():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM software_repository")
    software_repo = [row[0] for row in c.fetchall()]
    conn.close()
    return software_repo

def create_database(client_list):
    conn = sqlite3.connect('software_inventory.db')
    c = conn.cursor()
    # Create a table for each client
    for client in client_list:
        table_name = f"{client['username']}"  
        c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                      id INTEGER PRIMARY KEY, 
                      name TEXT, 
                      version TEXT)''')
    conn.commit()
    conn.close()
    
def update_database(client, software_repo):
    conn = sqlite3.connect('software_inventory.db')
    c = conn.cursor()
    table_name = f"{client['username']}"  

    installed_software = {}
    for software in software_repo:
        version = check_software_installed(client, software)
        if version:
            installed_software[software] = version

    c.execute(f"SELECT name, version FROM {table_name}")
    recorded_software = {name: version for name, version in c.fetchall()}

    new_software = set(installed_software.keys()) - set(recorded_software.keys())
    for software in new_software:
        c.execute(f"INSERT INTO {table_name} (name, version) VALUES (?, ?)", (software, installed_software[software]))
        print(f"New software installed on {client['username']}: {software} (Version: {installed_software.get(software, 'Version not available')}")

    removed_software = set(recorded_software.keys()) - set(installed_software.keys())
    for software in removed_software:
        c.execute(f"DELETE FROM {table_name} WHERE name=?", (software,))
        print(f"Software removed from {client['username']}: {software}")

    for software, version in installed_software.items():
        if software in recorded_software and recorded_software[software] != version:
            c.execute(f"UPDATE {table_name} SET version=? WHERE name=?", (version, software))
            print(f"Software updated on {client['username']}: {software} (New Version: {version})")

    conn.commit()
    conn.close()
    
def check_software_installed(client, software):
    try:
        ssh_command = ['sshpass', '-p', client['password'], 'ssh', f"{client['username']}@{client['ip']}", f"which {software}"]
        result = subprocess.check_output(ssh_command).decode().strip()
        if result:
            version_command = ['sshpass', '-p', client['password'], 'ssh', f"{client['username']}@{client['ip']}", f"{software} --version"]
            version = subprocess.check_output(version_command).decode().strip()
            return version if version else None
        else:
            return None
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    clients = get_clients()
    
    software_repo = get_software_repo()
    
    create_database(clients)
    
    for client in clients:
        update_database(client, software_repo)


