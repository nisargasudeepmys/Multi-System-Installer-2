from datetime import datetime
from remote_system import RemoteSystem
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from database import DatabaseManager
from mail_sender import MailSender
import logging
import os

class JobScheduler:
    def __init__(self):
        self.db = DatabaseManager('database.db')
        self.software_repository = self.db.get_software_repo_machine()
        self.pool = ThreadPoolExecutor(10)
        self.setup_logging()

    def setup_logging(self):
        log_directory = '/home/kusuma/MSI/MSI_logs/admin_logs/'
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(filename=os.path.join(log_directory, 'job_scheduler.log'),
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')

    def executor(self, job_id: int, machine_id: int, software_id: int):
        try:
            db = DatabaseManager('database.db')
            email = MailSender()
            # Fetch machine details, including client_name (same as username)
            host_name, user_name, port_number, path, os_type, password = db.get_machine(machine_id=machine_id)
            client_name = user_name  # Assuming client_name is the same as username

            remote_system = RemoteSystem(self.software_repository, host_name, user_name, port_number, path, password, client_name)
            
            name, extension = db.get_software(software_id=software_id)
            filename = name + extension
            start_time = datetime.now()
            status = remote_system.install_software(file_name=filename, os_type=os_type)
            end_time = datetime.now()

            if status == "CONFLICT":
                logging.warning(f"Machine ID: {machine_id} Software ID: {software_id} Status:Software Conflict detected")
                print(f"Machine ID: {machine_id}\nSoftware ID: {software_id}\nStatus:Software Conflict detected")
                db.create_completed_job(job_id=job_id, machine_id=machine_id, software_id=software_id, status="CONFLICT", completion_time=end_time, error_message="Software already installed")
            elif status == "FAILED":
                logging.error(f"Machine ID: {machine_id} Software ID: {software_id} Status: Failed")
                print(f"Machine ID: {machine_id}\nSoftware ID: {software_id}\nStatus: Failed")
                db.create_completed_job(job_id=job_id, machine_id=machine_id, software_id=software_id, status="FAILED", completion_time=end_time, error_message="Installation failed")
            else:
                logging.info(f"Machine ID: {machine_id} Software ID: {software_id} Status: Completed")
                print(f"Machine ID: {machine_id}\nSoftware ID: {software_id}\nStatus: Completed")
                email.send_mail(start_time=start_time, end_time=end_time, machine_id=machine_id, package_name=filename, status_report="success", receiver_mail="kcs0903mys@gmail.com")
                db.create_completed_job(job_id=job_id, machine_id=machine_id, software_id=software_id, status="SUCCESS", completion_time=end_time, error_message="N/A")
            
            db.delete_scheduled_job(job_id=job_id)
            remote_system.close_connection()
            db.close_connection()  # Close the database connection
        except Exception as e:
            logging.error(f"An error occurred during execution: {str(e)}")
            try:
                db.create_completed_job(job_id=job_id, machine_id=machine_id, software_id=software_id, status="FAILED", completion_time=datetime.now(), error_message=str(e))
            except Exception as db_error:
                logging.error(f"Failed to log job failure: {str(db_error)}")

    def run(self):
        terminate_flag = True
        while terminate_flag:
            scheduled_jobs = self.db.read_all_scheduled_jobs()
            print("Scheduled Jobs:", scheduled_jobs)
            futures = []
            for job in scheduled_jobs:
                job_id, machine_id, software_id, scheduled_time = job
                format_string = '%Y-%m-%d %H:%M:%S'
                datetime_object = datetime.strptime(scheduled_time, format_string)
                if datetime_object <= datetime.now():
                    future = self.pool.submit(self.executor, job_id, machine_id, software_id)
                    futures.append(future)
            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    logging.error(f"Job execution failed: {str(e)}")
            print("Waiting for 5 minutes before checking for new jobs")
            time.sleep(5 * 60)

if __name__ == "__main__":
    JobScheduler().run()

