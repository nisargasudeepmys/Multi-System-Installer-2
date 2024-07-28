import xml.etree.ElementTree as ET
import re
import subprocess
import sqlite3
import logging

from database import DatabaseManager

class MachineStatus:
    def __init__(self, input_file,output_file,db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.db_manager = DatabaseManager(db_name)
        self.input_file = input_file
        self.output_file = output_file
        self.host_details = []
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename='job_scheduler.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')
	
    def fetch_status_info(self):
        ip_addresses = self.db_manager.get_ip_addresses()
        with open(self.input_file, 'w') as file:
             for ip_address in ip_addresses:
                  file.write(ip_address[0] + "\n")
        logging.info("Fetched machine details from database")

    def scan_nmap(self):
    	cmd = f"nmap -v -iL {self.input_file} -oX {self.output_file}"
    	
    	try:
    		result = subprocess.run(cmd , shell=True , capture_output=True , text=True)
    		logging.info("Nmap scan completed successfully")
    		
    	except subprocess.CalledProcessError as e:
    		logging.error(f"Error occured while running Nmap scan : {e}")
   
    def check_uptime(self,username , password , ip_address):
        cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{ip_address} 'uptime -s'"
        try:
            result = subprocess.run(cmd , shell=True , capture_output=True , text=True ,check=True)
            if result.returncode == 0:
               uptime_info = result.stdout.strip()
               pattern = r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"

               match = re.search(pattern , uptime_info)
               if match:
                  uptime = match.group(1)
                  return uptime	
        except subprocess.CalledProcessError as e:
            logging.error(f"Error: {e}")
            return None       
            
		
    
    def parse_scan_xml(self):
        tree = ET.parse(self.output_file)
        root = tree.getroot()

        for host in root.findall('.//host'):  # . is current node and // selects host at all depths
            status = host.find('status')
            address = host.find('address')
            ports = host.find('ports')

            machine_state = status.get('state')
            ip_address = address.get('addr')
            self.host_details.append((ip_address, machine_state))


    def get_status_uptime(self):
        self.fetch_status_info()
        self.scan_nmap()
        self.parse_scan_xml()
   
        machine_status_details = []

        for ip_address, machine_state in self.host_details:
            machine_id , username , machine_type ,password= self.db_manager.get_machine_details(ip_address)
            if machine_state == 'up':
               uptime= self.check_uptime(username , password , ip_address)
               machine_status_details.append((machine_id ,username , machine_type, ip_address, machine_state, uptime))
            else:
                  machine_status_details.append((machine_id ,username , machine_type, ip_address, machine_state,'-'))
        return machine_status_details
