# Palo-Alto-Expedition-Remote-Code

Critical Remote Code Execution Vulnerabilities in Palo Alto Expedition (Versions ≤ 1.2.91)

This project demonstrates the exploitation of two severe vulnerabilities identified in the Palo Alto Expedition platform:

    CVE-2024-5910: A weakness that allows unauthenticated attackers to reset the administrator password to a default value, enabling unauthorized access.
    CVE-2024-9464: A flaw enabling authenticated OS command injection, allowing arbitrary command execution in the context of the www-data user.

These vulnerabilities, when chained together, allow attackers to achieve complete remote code execution (RCE) on the target system, potentially leading to full system compromise. This exploit automates the attack process, providing options for password resets, authentication, and payload execution.
