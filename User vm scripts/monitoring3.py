import psutil
import time
import subprocess
import datetime
import paramiko
import os
from dotenv import load_dotenv

class SystemMonitor:
    # Threshold values
    CPU_THRESHOLD = 90  # 90% CPU usage threshold
    DISK_THRESHOLD = 20 * 1024**3  # 20 GB disk space threshold (in bytes)

    def __init__(self):
        load_dotenv()
        self.admin_hostname = os.getenv('SYSTEM_MONITOR_ADMIN_HOSTNAME')
        self.admin_username = os.getenv('SYSTEM_MONITOR_ADMIN_USERNAME')
        self.key_filename = os.getenv('SYSTEM_MONITOR_KEY_FILENAME')
        self.client_machine_name = self.get_username()
        self.admin_log_dir = os.getenv('SYSTEM_MONITOR_ADMIN_LOG_DIR').format(client_machine_name=self.client_machine_name)

    def get_username(self):
        return subprocess.check_output(['whoami']).strip().decode('utf-8')

    def check_cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=2)
        if cpu_percent > self.CPU_THRESHOLD:
            alert_message = f"High CPU usage on {self.client_machine_name}'s machine: {cpu_percent}%"
            self.log_alert(alert_message)
            self.send_alert_to_admin(alert_message)
            return f"High CPU usage: {cpu_percent}%"
        return None

    def check_disk_space(self):
        disk_usage = psutil.disk_usage('/')
        if disk_usage.free < self.DISK_THRESHOLD:
            alert_message = f"Low disk space on {self.client_machine_name}'s machine: {disk_usage.free / 1024**3:.2f} GB remaining"
            self.log_alert(alert_message)
            self.send_alert_to_admin(alert_message)
            return f"Low disk space: {disk_usage.free / 1024**3:.2f} GB remaining"
        return None

    def get_log_file_name(self):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        if current_month <= 4:
            period = "jan-apr"
        elif current_month <= 8:
            period = "may-aug"
        else:
            period = "sep-dec"
        return f"{period}_{current_year}_logs.log"

    def log_alert(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file_name = self.get_log_file_name()
        with open(log_file_name, 'a') as file:
            file.write(f"{timestamp} - {message}\n")
        self.transfer_log_to_admin(log_file_name)

    def transfer_log_to_admin(self, log_file_name):
        admin_folder = self.admin_log_dir
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=self.admin_hostname, username=self.admin_username, key_filename=self.key_filename)
            sftp = ssh_client.open_sftp()

            try:
                sftp.chdir(admin_folder)
            except IOError:
                try:
                    sftp.mkdir(admin_folder)
                    sftp.chdir(admin_folder)
                except Exception as e:
                    print(f"Failed to create directory {admin_folder}. Error: {e}")
                    raise e

            sftp.put(log_file_name, os.path.join(admin_folder, log_file_name))
            print(f"Successfully transferred {log_file_name} to {admin_folder}")
            sftp.close()
        except Exception as e:
            self.log_error(log_file_name, f"Error transferring log to admin: {e}")
        finally:
            ssh_client.close()

    def log_error(self, log_file_name, error_message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(log_file_name, 'a') as file:
                file.write(f"{timestamp} - {error_message}\n")
        except IOError as e:
            print(f"Failed to write to log file {log_file_name}. Error: {e}")

    def send_alert_to_admin(self, message):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=self.admin_hostname, username=self.admin_username, key_filename=self.key_filename)
            command = f"DISPLAY=:0 notify-send 'Alert from {self.client_machine_name}' '{message}'"
            stdin, stdout, stderr = ssh_client.exec_command(command)
            stdout_text = stdout.read().decode()
            stderr_text = stderr.read().decode()
            if stdout_text:
                print(stdout_text)
            if stderr_text:
                print(stderr_text)
        except Exception as e:
            log_file_name = self.get_log_file_name()
            self.log_error(log_file_name, f"Error sending alert to admin: {e}")
        finally:
            ssh_client.close()

    def monitor(self):
        while True:
            cpu_alert = self.check_cpu_usage()
            disk_alert = self.check_disk_space()

            if cpu_alert:
                print(cpu_alert)
            if disk_alert:
                print(disk_alert)

            time.sleep(24*60*60)  # Check every day

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.monitor()

