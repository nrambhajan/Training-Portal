"""
Day 2.5 — Linux Practical Tasks (Intermediate)
Run once on server: python3 seed_day2_5.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

module = models.Module(
    title="Day 2.5 - Linux Practical Tasks (Intermediate)",
    description="15 intermediate practical tasks covering networking, services, disk management, text processing, and shell scripting.",
    sort_order=3,
    unlock_percent=0,
    is_published=False,
    time_limit=90,
)
db.add(module)
db.commit()
db.refresh(module)

questions = [
    {
        "type": "practical",
        "text": "TASK 1 - Check Open Ports\n\nFind all listening TCP ports on your server and save the output to /home/trainee/open_ports.txt\n\nUse the 'ss' command with appropriate flags.",
        "verify_command": "test -s /home/trainee/open_ports.txt && grep -q 'LISTEN' /home/trainee/open_ports.txt && echo 'done'",
        "verify_expected": "done",
        "verify_type": "contains",
        "points": 2.0,
        "order": 1,
        "hint": "Use: ss -tlnp > /home/trainee/open_ports.txt",
    },
    {
        "type": "practical",
        "text": "TASK 2 - Install and Start a Service\n\nInstall the 'nginx' web server and make sure it is running and enabled to start on boot.",
        "verify_command": "systemctl is-active nginx && systemctl is-enabled nginx",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 2.0,
        "order": 2,
        "hint": "Use: sudo apt install nginx -y && sudo systemctl enable --now nginx",
    },
    {
        "type": "practical",
        "text": "TASK 3 - Configure a Custom Nginx Page\n\nReplace the default Nginx welcome page with your own.\n\nCreate /var/www/html/index.html with the content:\n<h1>SupportSages Training Server</h1>\n<p>Configured by trainee</p>",
        "verify_command": "curl -s http://localhost 2>/dev/null | grep -q 'SupportSages Training Server' && echo 'page_ok'",
        "verify_expected": "page_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
        "hint": "Use: echo '<h1>SupportSages Training Server</h1><p>Configured by trainee</p>' | sudo tee /var/www/html/index.html",
    },
    {
        "type": "practical",
        "text": "TASK 4 - Disk Usage Report\n\nFind the top 5 largest directories under / (root) and save the output to /home/trainee/largest_dirs.txt\n\nThe file should show directory sizes.",
        "verify_command": "test -s /home/trainee/largest_dirs.txt && wc -l < /home/trainee/largest_dirs.txt | awk '{print ($1 >= 5) ? \"done\" : \"fail\"}'",
        "verify_expected": "done",
        "verify_type": "contains",
        "points": 2.0,
        "order": 4,
        "hint": "Use: du -h --max-depth=1 / 2>/dev/null | sort -hr | head -5 > /home/trainee/largest_dirs.txt",
    },
    {
        "type": "practical",
        "text": "TASK 5 - Create a Swap File\n\nCreate a 512MB swap file at /swapfile and activate it.\n\nSteps:\n1. Create the file: sudo fallocate -l 512M /swapfile\n2. Set permissions: sudo chmod 600 /swapfile\n3. Set up swap: sudo mkswap /swapfile\n4. Enable it: sudo swapon /swapfile\n5. Verify with: swapon --show",
        "verify_command": "swapon --show | grep -c '/swapfile'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 5,
        "hint": "Follow the steps: fallocate, chmod 600, mkswap, swapon",
    },
    {
        "type": "practical",
        "text": "TASK 6 - Text Processing with awk\n\nThe file /etc/passwd has fields separated by ':'.\n\nExtract only the username (field 1) and home directory (field 6) from /etc/passwd and save to /home/trainee/users_homes.txt\n\nFormat: username:/home/directory (one per line)",
        "verify_command": "test -s /home/trainee/users_homes.txt && head -1 /home/trainee/users_homes.txt | grep -q ':/' && echo 'formatted'",
        "verify_expected": "formatted",
        "verify_type": "contains",
        "points": 2.0,
        "order": 6,
        "hint": "Use: awk -F: '{print $1 \":\" $6}' /etc/passwd > /home/trainee/users_homes.txt",
    },
    {
        "type": "practical",
        "text": "TASK 7 - Set Up UFW Firewall\n\nInstall and configure the UFW firewall:\n1. Allow SSH (port 22)\n2. Allow HTTP (port 80)\n3. Allow HTTPS (port 443)\n4. Enable the firewall\n\nMake sure UFW is active after configuration.",
        "verify_command": "ufw status | grep -q 'Status: active' && ufw status | grep -q '22' && ufw status | grep -q '80' && echo 'firewall_ok'",
        "verify_expected": "firewall_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 7,
        "hint": "Use: sudo ufw allow 22 && sudo ufw allow 80 && sudo ufw allow 443 && sudo ufw --force enable",
    },
    {
        "type": "practical",
        "text": "TASK 8 - Schedule a Log Rotation\n\nCreate a bash script at /home/trainee/log_rotate.sh that:\n1. Copies /var/log/syslog to /home/trainee/logs/syslog_$(date +%Y%m%d).log\n2. Creates the /home/trainee/logs/ directory if it doesn't exist\n\nMake the script executable and run it once to test.",
        "verify_command": "test -x /home/trainee/log_rotate.sh && test -d /home/trainee/logs && ls /home/trainee/logs/syslog_*.log 2>/dev/null | wc -l | awk '{print ($1 >= 1) ? \"done\" : \"fail\"}'",
        "verify_expected": "done",
        "verify_type": "contains",
        "points": 3.0,
        "order": 8,
        "hint": "Script should have: #!/bin/bash, mkdir -p /home/trainee/logs, cp /var/log/syslog /home/trainee/logs/syslog_$(date +%Y%m%d).log",
    },
    {
        "type": "practical",
        "text": "TASK 9 - Monitor System Resources\n\nInstall the 'htop' tool and save a snapshot of running processes to /home/trainee/processes.txt\n\nUse the 'ps' command to list all running processes sorted by CPU usage (top 20).",
        "verify_command": "which htop >/dev/null 2>&1 && test -s /home/trainee/processes.txt && echo 'done'",
        "verify_expected": "done",
        "verify_type": "contains",
        "points": 2.0,
        "order": 9,
        "hint": "Use: sudo apt install htop -y && ps aux --sort=-%cpu | head -20 > /home/trainee/processes.txt",
    },
    {
        "type": "practical",
        "text": "TASK 10 - Create Multiple Users with a Script\n\nCreate a bash script at /home/trainee/create_users.sh that creates 3 users:\n- user1, user2, user3\n\nEach should have a home directory. Run the script to create them.",
        "verify_command": "test -x /home/trainee/create_users.sh && id user1 >/dev/null 2>&1 && id user2 >/dev/null 2>&1 && id user3 >/dev/null 2>&1 && echo 'all_users_created'",
        "verify_expected": "all_users_created",
        "verify_type": "contains",
        "points": 2.0,
        "order": 10,
        "hint": "Script: #!/bin/bash then use 'useradd -m user1' for each user. chmod +x and run with sudo.",
    },
    {
        "type": "practical",
        "text": "TASK 11 - SSH Key Generation\n\nGenerate an SSH key pair for the trainee user:\n- Save it at /home/trainee/.ssh/id_rsa\n- No passphrase (empty)\n- Type: RSA, 4096 bits\n\nBoth id_rsa and id_rsa.pub should exist.",
        "verify_command": "test -f /home/trainee/.ssh/id_rsa && test -f /home/trainee/.ssh/id_rsa.pub && echo 'keypair_exists'",
        "verify_expected": "keypair_exists",
        "verify_type": "contains",
        "points": 2.0,
        "order": 11,
        "hint": "Use: ssh-keygen -t rsa -b 4096 -f /home/trainee/.ssh/id_rsa -N '' (empty passphrase)",
    },
    {
        "type": "practical",
        "text": "TASK 12 - Set Up a Static IP Address\n\nCreate a netplan configuration file at /etc/netplan/99-static.yaml with the following:\n- A comment line: # Training static config\n\nDon't apply it (just create the file). The file should be valid YAML.",
        "verify_command": "test -f /etc/netplan/99-static.yaml && grep -q 'Training static config' /etc/netplan/99-static.yaml && echo 'config_exists'",
        "verify_expected": "config_exists",
        "verify_type": "contains",
        "points": 2.0,
        "order": 12,
        "hint": "Use sudo nano /etc/netplan/99-static.yaml and add the comment. Be careful with YAML indentation.",
    },
    {
        "type": "practical",
        "text": "TASK 13 - Secure a Directory\n\nCreate a directory /home/trainee/secret/ and:\n1. Set permissions to 700 (only owner can access)\n2. Create a file called /home/trainee/secret/passwords.txt with content 'TopSecret123'\n3. Set file permissions to 600",
        "verify_command": "test -d /home/trainee/secret && stat -c '%a' /home/trainee/secret | grep -q '700' && stat -c '%a' /home/trainee/secret/passwords.txt | grep -q '600' && grep -q 'TopSecret123' /home/trainee/secret/passwords.txt && echo 'secured'",
        "verify_expected": "secured",
        "verify_type": "contains",
        "points": 2.0,
        "order": 13,
        "hint": "mkdir, chmod 700 for dir, create file, chmod 600 for file",
    },
    {
        "type": "practical",
        "text": "TASK 14 - System Log Analysis\n\nSearch /var/log/syslog for the word 'error' (case insensitive) and save:\n1. The count to /home/trainee/error_count.txt\n2. The last 10 error lines to /home/trainee/recent_errors.txt",
        "verify_command": "test -s /home/trainee/error_count.txt && test -f /home/trainee/recent_errors.txt && echo 'logs_analyzed'",
        "verify_expected": "logs_analyzed",
        "verify_type": "contains",
        "points": 2.0,
        "order": 14,
        "hint": "Use: grep -ic 'error' /var/log/syslog > error_count.txt && grep -i 'error' /var/log/syslog | tail -10 > recent_errors.txt",
    },
    {
        "type": "practical",
        "text": "TASK 15 - Health Check Script\n\nCreate a comprehensive server health check script at /home/trainee/healthcheck.sh that outputs:\n1. Current date/time\n2. Server uptime\n3. CPU load average (from /proc/loadavg)\n4. Memory usage (free -h)\n5. Disk usage of / (df -h /)\n6. Number of running processes\n7. Number of logged-in users\n\nMake the script executable and run it. Save the output to /home/trainee/health_report.txt",
        "verify_command": "test -x /home/trainee/healthcheck.sh && test -s /home/trainee/health_report.txt && grep -q 'Mem' /home/trainee/health_report.txt && echo 'health_ok'",
        "verify_expected": "health_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 15,
        "hint": "Script with #!/bin/bash, then date, uptime, cat /proc/loadavg, free -h, df -h /, ps aux | wc -l, who | wc -l. Run: bash healthcheck.sh > health_report.txt",
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print("All 15 practical tasks!")
print("Module is DRAFT - publish from admin panel when ready")
db.close()
