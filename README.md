# Palo-Alto-Expedition-Remote-Code

Critical Remote Code Execution Vulnerabilities in Palo Alto Expedition (Versions ≤ 1.2.91)

This project demonstrates the exploitation of two severe vulnerabilities identified in the Palo Alto Expedition platform:

    CVE-2024-5910: A weakness that allows unauthenticated attackers to reset the administrator password to a default value, enabling unauthorized access.
    CVE-2024-9464: A flaw enabling authenticated OS command injection, allowing arbitrary command execution in the context of the www-data user.

These vulnerabilities, when chained together, allow attackers to achieve complete remote code execution (RCE) on the target system, potentially leading to full system compromise. This exploit automates the attack process, providing options for password resets, authentication, and payload execution.

Steps to Run the Script
Step 1: Download the Script

Save the script to a file, e.g., exploit.py.
Step 2: Execute the Script

Run the script using Python:

python3 exploit.py

Step 3: Follow the Prompts

The script will prompt you for the following inputs:

    Target URL: Enter the full URL of the target (e.g., https://192.168.1.10).
    Username (Optional): Enter the username for authentication. Defaults to admin.
    Password (Optional): Enter the password for authentication. Defaults to paloalto.
    Reset Admin Password: If you do not have credentials, type yes to reset the admin password to the default.
    Writable Directory: Enter the path to a writable directory on the target. Defaults to /tmp/.
    Payload: Enter the command or payload you wish to execute on the target.

Step 4: Wait for Execution

The script will:

    Attempt to reset the admin password if no credentials are provided.
    Authenticate using the provided or reset credentials.
    Stage and execute the payload on the target.

Step 5: Check the Output

The script will display:

    Success messages for each step (e.g., password reset, authentication, command execution).
    Any errors encountered during execution.

Output Examples

Success Message:

[+] Admin password reset successfully to: paloalto
[+] Authentication successful. CSRF token retrieved.
[+] Command executed: id
[+] Payload executed successfully.

Error Message:

[-] Failed to reset admin password.
[-] Authentication failed.
[-] Command execution failed. HTTP code: 403



    
