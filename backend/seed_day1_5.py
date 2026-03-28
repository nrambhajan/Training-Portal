"""
Day 1.5 — Linux Hands-On Practice
Run once on server: python3 seed_day1_5.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

module = models.Module(
    title="Day 1.5 - Linux Hands-On Practice",
    description="15 practical tasks to build your Linux confidence. Practice file operations, permissions, users, processes, scripting, and more on your training server.",
    sort_order=2,
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
        "text": "TASK 1 - Create Directory Structure\n\nCreate the following directory structure:\n/home/trainee/company/hr\n/home/trainee/company/finance\n/home/trainee/company/engineering\n\nAll three directories must exist.",
        "verify_command": "test -d /home/trainee/company/hr && test -d /home/trainee/company/finance && test -d /home/trainee/company/engineering && echo 'all_exist'",
        "verify_expected": "all_exist",
        "verify_type": "contains",
        "points": 2.0,
        "order": 1,
        "hint": "Use mkdir -p to create nested directories. You can create all three in one command.",
    },
    {
        "type": "practical",
        "text": "TASK 2 - Create Files with Content\n\nCreate these files:\n- /home/trainee/company/hr/employees.txt (containing 'Employee List')\n- /home/trainee/company/finance/budget.txt (containing 'Annual Budget')\n- /home/trainee/company/engineering/servers.txt (containing 'Server List')",
        "verify_command": "grep -q 'Employee List' /home/trainee/company/hr/employees.txt 2>/dev/null && grep -q 'Annual Budget' /home/trainee/company/finance/budget.txt 2>/dev/null && grep -q 'Server List' /home/trainee/company/engineering/servers.txt 2>/dev/null && echo 'all_good'",
        "verify_expected": "all_good",
        "verify_type": "contains",
        "points": 2.0,
        "order": 2,
        "hint": "Use echo 'text' > filename to create files with content.",
    },
    {
        "type": "practical",
        "text": "TASK 3 - Copy and Move Files\n\nCopy /home/trainee/company/engineering/servers.txt to /home/trainee/company/hr/servers_backup.txt\n\nThen move /home/trainee/company/finance/budget.txt to /home/trainee/company/finance/budget_2025.txt",
        "verify_command": "test -f /home/trainee/company/hr/servers_backup.txt && test -f /home/trainee/company/finance/budget_2025.txt && echo 'done'",
        "verify_expected": "done",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
        "hint": "Use cp for copying and mv for moving/renaming files.",
    },
    {
        "type": "practical",
        "text": "TASK 4 - File Permissions\n\nChange the permissions of /home/trainee/company/hr/employees.txt so that:\n- Owner can read and write (6)\n- Group can read only (4)\n- Others have no access (0)\n\nFinal permission should be 640.",
        "verify_command": "stat -c '%a' /home/trainee/company/hr/employees.txt",
        "verify_expected": "640",
        "verify_type": "contains",
        "points": 2.0,
        "order": 4,
        "hint": "Use chmod 640 filename. Remember: 6=rw, 4=r, 0=none.",
    },
    {
        "type": "practical",
        "text": "TASK 5 - Create a User\n\nCreate a new user called 'developer' on your server with a home directory.",
        "verify_command": "id developer 2>/dev/null && echo 'user_exists'",
        "verify_expected": "user_exists",
        "verify_type": "contains",
        "points": 2.0,
        "order": 5,
        "hint": "Use: sudo useradd -m developer (the -m flag creates the home directory)",
    },
    {
        "type": "practical",
        "text": "TASK 6 - Create a Group and Add User\n\nCreate a group called 'devteam' and add the user 'developer' to this group.",
        "verify_command": "groups developer 2>/dev/null | grep -c devteam",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 6,
        "hint": "Use: sudo groupadd devteam && sudo usermod -aG devteam developer",
    },
    {
        "type": "practical",
        "text": "TASK 7 - Find Files\n\nFind all .txt files inside /home/trainee/company/ and save the list to /home/trainee/found_files.txt\n\nThe output file should contain the full paths of all .txt files found.",
        "verify_command": "test -f /home/trainee/found_files.txt && grep -c '.txt' /home/trainee/found_files.txt",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 7,
        "hint": "Use: find /home/trainee/company/ -name '*.txt' > /home/trainee/found_files.txt",
    },
    {
        "type": "practical",
        "text": "TASK 8 - Redirect & Append Output\n\nRun 'df -h' and save its output to /home/trainee/disk_usage.txt\nThen run 'free -h' and APPEND its output to the SAME file.\n\nThe file should contain both disk and memory info.",
        "verify_command": "grep -q 'Filesystem' /home/trainee/disk_usage.txt 2>/dev/null && grep -q 'Mem:' /home/trainee/disk_usage.txt 2>/dev/null && echo 'both_present'",
        "verify_expected": "both_present",
        "verify_type": "contains",
        "points": 2.0,
        "order": 8,
        "hint": "Use > for redirect (overwrite) and >> for append. Example: df -h > file.txt && free -h >> file.txt",
    },
    {
        "type": "practical",
        "text": "TASK 9 - Symbolic Link\n\nCreate a symbolic link (shortcut) at /home/trainee/engineering_link that points to /home/trainee/company/engineering/",
        "verify_command": "test -L /home/trainee/engineering_link && readlink /home/trainee/engineering_link | grep -c engineering",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 9,
        "hint": "Use: ln -s /home/trainee/company/engineering/ /home/trainee/engineering_link",
    },
    {
        "type": "practical",
        "text": "TASK 10 - Process Management\n\nStart a background process using: sleep 9999 &\n\nThen find its PID and save it to /home/trainee/sleep_pid.txt\n\nThe file should contain only the process ID number.",
        "verify_command": "PID=$(cat /home/trainee/sleep_pid.txt 2>/dev/null | tr -d '[:space:]') && test -n \"$PID\" && ps -p $PID > /dev/null 2>&1 && echo 'running'",
        "verify_expected": "running",
        "verify_type": "contains",
        "points": 2.0,
        "order": 10,
        "hint": "Run 'sleep 9999 &' then use 'echo $!' to get the PID, or use 'pgrep sleep'",
    },
    {
        "type": "practical",
        "text": "TASK 11 - Grep and Count\n\nThe file /etc/passwd contains all user accounts.\n\nCount how many accounts use '/bin/bash' as their shell and save JUST the count number to /home/trainee/bash_users_count.txt",
        "verify_command": "EXPECTED=$(grep -c '/bin/bash' /etc/passwd) && ACTUAL=$(cat /home/trainee/bash_users_count.txt 2>/dev/null | tr -d '[:space:]') && test \"$EXPECTED\" = \"$ACTUAL\" && echo 'correct'",
        "verify_expected": "correct",
        "verify_type": "contains",
        "points": 2.0,
        "order": 11,
        "hint": "Use: grep -c '/bin/bash' /etc/passwd > /home/trainee/bash_users_count.txt",
    },
    {
        "type": "practical",
        "text": "TASK 12 - Set Up a Cron Job\n\nSet up a cron job for root that runs every day at 2:00 AM and saves the date to a log file.\n\nThe cron entry should be:\n0 2 * * * /usr/bin/date >> /var/log/daily_date.log",
        "verify_command": "crontab -l 2>/dev/null | grep -c 'daily_date.log'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 12,
        "hint": "Use 'crontab -e' to edit. Format: minute hour day month weekday command",
    },
    {
        "type": "practical",
        "text": "TASK 13 - Archive and Compress\n\nCreate a tar.gz archive of the /home/trainee/company/ directory.\nSave it as /home/trainee/company_backup.tar.gz",
        "verify_command": "test -f /home/trainee/company_backup.tar.gz && tar -tzf /home/trainee/company_backup.tar.gz 2>/dev/null | head -1 && echo 'valid_archive'",
        "verify_expected": "valid_archive",
        "verify_type": "contains",
        "points": 2.0,
        "order": 13,
        "hint": "Use: tar -czf /home/trainee/company_backup.tar.gz -C /home/trainee company",
    },
    {
        "type": "practical",
        "text": "TASK 14 - Change Hostname\n\nChange the server hostname to 'trainee-server'.\nThe change should persist after reboot.",
        "verify_command": "hostnamectl --static 2>/dev/null",
        "verify_expected": "trainee-server",
        "verify_type": "contains",
        "points": 2.0,
        "order": 14,
        "hint": "Use: sudo hostnamectl set-hostname trainee-server",
    },
    {
        "type": "practical",
        "text": "TASK 15 - Write a Bash Script\n\nCreate a bash script at /home/trainee/sysinfo.sh that outputs:\n- The hostname\n- Current date and time\n- System uptime\n- Disk usage (df -h)\n- Memory usage (free -h)\n\nMake the script executable (chmod +x).",
        "verify_command": "test -x /home/trainee/sysinfo.sh && bash /home/trainee/sysinfo.sh 2>/dev/null | grep -c 'Mem'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 15,
        "hint": "Create file with #!/bin/bash at top, then hostname, date, uptime, df -h, free -h. Use chmod +x to make executable.",
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print("All 15 practical hands-on tasks!")
print("Module is DRAFT - publish from admin panel when ready")
db.close()
