import paramiko
import logging
import os
import datetime

class RemoteSystem:
    def __init__(self, software_repository: tuple, host_name: str, user_name: str, port_number: int, path: str, password: str, client_name: str) -> None:
        self.host_name = host_name
        self.user_name = user_name
        self.password = password
        self.port_number = port_number
        self.remote_path = path
        self.software_repo = software_repository
        self.client_name = client_name
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.host_name, port=self.port_number, username=self.user_name, password=self.password)
        self.setup_logging()

    def setup_logging(self):
        # Logging setup for remote_system.log in admin_logs directory
        log_directory_admin = '/home/kusuma/MSI/MSI_logs/admin_logs/'
        os.makedirs(log_directory_admin, exist_ok=True)
        logging.basicConfig(filename=os.path.join(log_directory_admin, 'remote_system.log'),
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger_admin = logging.getLogger('RemoteSystem')

        # Logging setup for software_conflicts.log in client_logs/client_name directory
        log_directory_client = f'/home/kusuma/MSI/MSI_logs/client_logs/{self.client_name}'
        os.makedirs(log_directory_client, exist_ok=True)
        self.logger_client = logging.getLogger('SoftwareConflicts')
        handler = logging.FileHandler(os.path.join(log_directory_client, 'software_conflicts.log'))
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger_client.addHandler(handler)
        self.logger_client.setLevel(logging.INFO)

    def file_transfer(self, file_name: str) -> None:
        username, host_name, host_path, password = self.software_repo

        self.logger_admin.info(f"sshpass -p {password} scp {username}@{host_name}:{host_path}/{file_name} {self.remote_path}")
        cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no {username}@{host_name}:{host_path}/{file_name} {self.remote_path}"

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            wait = stdout.read().decode("utf-8")
            self.logger_admin.info(f"File transfer successful: {file_name} @ Username: {self.user_name} IP: {self.host_name}")
        except Exception as e:
            self.logger_admin.error(f"Exception occurred during file transfer: {str(e)} @ Username: {self.user_name} IP: {self.host_name}")
            self.log_alert(f"Exception occurred during file transfer: {str(e)}")

    def install_software(self, file_name: str, os_type: str) -> str:
        if self.check_software_installed(file_name):
            self.logger_admin.warning(f"Software conflict detected: {file_name} is already installed @ Username: {self.user_name} IP: {self.host_name}")
            self.logger_client.warning(f"Software conflict detected: {file_name} is already installed")
            return "CONFLICT"

        self.file_transfer(file_name)
        cmd = f'echo {self.password} | sudo -S apt install ./{file_name} -y'
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)

        if stderr.channel.recv_exit_status() != 0:
            self.logger_admin.error(f"Failed to install {file_name} @ Username: {self.user_name} IP: {self.host_name}")
            return "FAILED"
        
        self.logger_admin.info(f"Successfully installed {file_name} @ Username: {self.user_name} IP: {self.host_name}")
        return "SUCCESS"

    def check_software_installed(self, file_name: str) -> bool:
        cmd = f'dpkg -l | grep {file_name.split(".")[0]}'
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        output = stdout.read().decode("utf-8")
        if output:
            self.logger_client.warning(f"Software {file_name} already installed @ Username: {self.user_name} IP: {self.host_name}")
            return True
        return False

    def log_alert(self, message: str):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger_client.error(f"{timestamp} - {message}")

    def close_connection(self) -> None:
        self.ssh_client.close()

if __name__ == '__main__':
    pass

