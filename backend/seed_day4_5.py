"""
Day 4.5 — User Admin & File Management Practice
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

module = models.Module(
    title="Day 4.5 - User Admin & File Management Practice",
    description="Hands-on practice covering user/group management, permissions, ownership, special permissions, ACLs, and file operations.",
    sort_order=9,
    unlock_percent=0,
    is_published=False,
    time_limit=90,
)
db.add(module)
db.commit()
db.refresh(module)

questions = [
    # ── Practical Tasks ────────────────────────────────────────────────

    {
        "type": "practical",
        "text": "TASK 1 - Create Users for a Team\n\nCreate the following 3 users with home directories:\n- webadmin\n- dbadmin\n- netadmin\n\nAll three must exist with home directories under /home/.",
        "verify_command": "id webadmin >/dev/null 2>&1 && id dbadmin >/dev/null 2>&1 && id netadmin >/dev/null 2>&1 && test -d /home/webadmin && test -d /home/dbadmin && test -d /home/netadmin && echo 'all_created'",
        "verify_expected": "all_created",
        "verify_type": "contains",
        "points": 2.0,
        "order": 1,
    },
    {
        "type": "practical",
        "text": "TASK 2 - Create Groups and Assign Users\n\nCreate these groups:\n- sysops\n- database\n- network\n\nThen assign:\n- webadmin and netadmin to the 'sysops' group\n- dbadmin to the 'database' group\n- netadmin to the 'network' group\n\nNote: netadmin should be in BOTH sysops and network groups.",
        "verify_command": "groups webadmin 2>/dev/null | grep -q sysops && groups netadmin 2>/dev/null | grep -q sysops && groups netadmin 2>/dev/null | grep -q network && groups dbadmin 2>/dev/null | grep -q database && echo 'groups_ok'",
        "verify_expected": "groups_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 2,
    },
    {
        "type": "practical",
        "text": "TASK 3 - Set Password Expiry Policy\n\nSet password expiry for the user 'webadmin':\n- Maximum password age: 90 days\n- Minimum password age: 7 days\n- Warning before expiry: 14 days\n\nUse the chage command.",
        "verify_command": "chage -l webadmin 2>/dev/null | grep -q 'Maximum.*90' && chage -l webadmin 2>/dev/null | grep -q 'Minimum.*7' && chage -l webadmin 2>/dev/null | grep -q 'warning.*14' && echo 'expiry_set'",
        "verify_expected": "expiry_set",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
    },
    {
        "type": "practical",
        "text": "TASK 4 - Lock and Unlock Account\n\nLock the user account 'dbadmin' so they cannot login.\n\nVerify it is locked, then unlock it again.\n\nThe account must be UNLOCKED when you click verify.",
        "verify_command": "passwd -S dbadmin 2>/dev/null | grep -q ' P ' && echo 'unlocked'",
        "verify_expected": "unlocked",
        "verify_type": "contains",
        "points": 2.0,
        "order": 4,
    },
    {
        "type": "practical",
        "text": "TASK 5 - Create a Shared Project Directory\n\nCreate a directory /opt/project-alpha with the following:\n- Owner: root\n- Group: sysops\n- Permissions: rwxrwx--- (770)\n\nOnly root and members of sysops should have access.",
        "verify_command": "test -d /opt/project-alpha && stat -c '%a %G' /opt/project-alpha | grep -q '770 sysops' && echo 'dir_ok'",
        "verify_expected": "dir_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 5,
    },
    {
        "type": "practical",
        "text": "TASK 6 - Set the Sticky Bit\n\nSet the sticky bit on /opt/project-alpha so that users can only delete their own files inside it (not others' files).\n\nThe permission should become 1770.",
        "verify_command": "stat -c '%a' /opt/project-alpha | grep -q '1770' && echo 'sticky_set'",
        "verify_expected": "sticky_set",
        "verify_type": "contains",
        "points": 2.0,
        "order": 6,
    },
    {
        "type": "practical",
        "text": "TASK 7 - Set the SetGID Bit\n\nSet the SetGID bit on /opt/project-alpha so that any new files created inside it automatically inherit the 'sysops' group ownership.\n\nThe permission should become 3770 (sticky + setgid).",
        "verify_command": "stat -c '%a' /opt/project-alpha | grep -q '3770' && echo 'setgid_set'",
        "verify_expected": "setgid_set",
        "verify_type": "contains",
        "points": 2.0,
        "order": 7,
    },
    {
        "type": "practical",
        "text": "TASK 8 - Ownership and Permissions\n\nCreate the following file structure:\n/opt/project-alpha/config.conf  (owned by webadmin:sysops, permission 640)\n/opt/project-alpha/deploy.sh    (owned by webadmin:sysops, permission 750)\n/opt/project-alpha/README        (owned by webadmin:sysops, permission 644)\n\nThe files can contain any content.",
        "verify_command": "stat -c '%U:%G %a' /opt/project-alpha/config.conf 2>/dev/null | grep -q 'webadmin:sysops 640' && stat -c '%U:%G %a' /opt/project-alpha/deploy.sh 2>/dev/null | grep -q 'webadmin:sysops 750' && stat -c '%U:%G %a' /opt/project-alpha/README 2>/dev/null | grep -q 'webadmin:sysops 644' && echo 'files_ok'",
        "verify_expected": "files_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 8,
    },
    {
        "type": "practical",
        "text": "TASK 9 - Make a File Immutable\n\nUse the chattr command to make /opt/project-alpha/config.conf immutable (cannot be modified, deleted, or renamed even by root).\n\nVerify with lsattr.",
        "verify_command": "lsattr /opt/project-alpha/config.conf 2>/dev/null | grep -q 'i' && echo 'immutable'",
        "verify_expected": "immutable",
        "verify_type": "contains",
        "points": 2.0,
        "order": 9,
    },
    {
        "type": "practical",
        "text": "TASK 10 - Sudo Access\n\nGive the user 'webadmin' sudo access to run ONLY the following commands without a password:\n- /usr/bin/systemctl restart apache2\n- /usr/bin/systemctl status apache2\n\nCreate a file /etc/sudoers.d/webadmin with the correct entry.",
        "verify_command": "test -f /etc/sudoers.d/webadmin && grep -q 'systemctl restart apache2' /etc/sudoers.d/webadmin && grep -q 'NOPASSWD' /etc/sudoers.d/webadmin && echo 'sudo_ok'",
        "verify_expected": "sudo_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 10,
    },
    {
        "type": "practical",
        "text": "TASK 11 - Hard Link and Soft Link\n\nCreate a file /home/trainee/original.txt with the content 'This is the original file'\n\nThen create:\n- A hard link at /home/trainee/hardlink.txt\n- A symbolic link at /home/trainee/softlink.txt\n\nBoth should point to original.txt.",
        "verify_command": "test -f /home/trainee/original.txt && test -f /home/trainee/hardlink.txt && test -L /home/trainee/softlink.txt && INODE1=$(stat -c '%i' /home/trainee/original.txt) && INODE2=$(stat -c '%i' /home/trainee/hardlink.txt) && test \"$INODE1\" = \"$INODE2\" && echo 'links_ok'",
        "verify_expected": "links_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 11,
    },
    {
        "type": "practical",
        "text": "TASK 12 - Default Permissions with umask\n\nSet the umask for root to 0027 so that:\n- New files get 640 (rw-r-----)\n- New directories get 750 (rwxr-x---)\n\nAdd the umask setting to /root/.bashrc so it persists.\n\nThen create a test file /home/trainee/umask_test.txt to verify (it should have permission 640).",
        "verify_command": "grep -q 'umask 0027' /root/.bashrc 2>/dev/null && stat -c '%a' /home/trainee/umask_test.txt 2>/dev/null | grep -q '640' && echo 'umask_ok'",
        "verify_expected": "umask_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 12,
    },
    {
        "type": "practical",
        "text": "TASK 13 - Find Files by Permission\n\nFind all files under /opt/project-alpha/ with permission 640 and save the output to /home/trainee/perm640_files.txt",
        "verify_command": "test -f /home/trainee/perm640_files.txt && test -s /home/trainee/perm640_files.txt && grep -q 'config.conf' /home/trainee/perm640_files.txt && echo 'found'",
        "verify_expected": "found",
        "verify_type": "contains",
        "points": 2.0,
        "order": 13,
    },
    {
        "type": "practical",
        "text": "TASK 14 - User Skeleton Directory\n\nCustomize the skeleton directory so that every NEW user created gets a welcome file.\n\nCreate a file /etc/skel/welcome.txt with the content 'Welcome to SupportSages Training Server!'\n\nThen create a new user called 'testintern' (with home directory) and verify the welcome.txt was automatically copied to their home.",
        "verify_command": "test -f /etc/skel/welcome.txt && test -f /home/testintern/welcome.txt && grep -q 'SupportSages' /home/testintern/welcome.txt && echo 'skel_ok'",
        "verify_expected": "skel_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 14,
    },
    {
        "type": "practical",
        "text": "TASK 15 - Delete a User Completely\n\nDelete the user 'testintern' along with their home directory and mail spool.\n\nThe user should no longer exist on the system.",
        "verify_command": "! id testintern 2>/dev/null && ! test -d /home/testintern && echo 'deleted'",
        "verify_expected": "deleted",
        "verify_type": "contains",
        "points": 2.0,
        "order": 15,
    },

    # ── Theory / Short Answer ──────────────────────────────────────────

    {
        "type": "short_answer",
        "text": "Explain the difference between /etc/passwd and /etc/shadow. What information does each file store? Why is /etc/shadow more secure?",
        "correct_answer": "/etc/passwd stores user account info (username, UID, GID, home dir, shell) and is readable by all users. /etc/shadow stores encrypted passwords and password aging info (expiry, min/max age, warning) and is readable only by root. Separating passwords into shadow provides security because regular users cannot read the encrypted passwords.",
        "points": 2.0,
        "order": 16,
    },
    {
        "type": "short_answer",
        "text": "What is the difference between useradd and adduser in Ubuntu/Debian? When would you use each?",
        "correct_answer": "useradd is a low-level command that creates users with minimal defaults - you need to manually specify options like -m (home dir), -s (shell), etc. adduser is a higher-level interactive wrapper (Perl script on Debian/Ubuntu) that prompts for password, full name, and creates the home directory automatically. Use adduser for interactive user creation and useradd for scripting/automation.",
        "points": 2.0,
        "order": 17,
    },
    {
        "type": "short_answer",
        "text": "Explain setuid, setgid, and sticky bit. Give a real-world example of each.",
        "correct_answer": "SetUID (4xxx): When set on an executable, it runs with the file owner's permissions instead of the user running it. Example: /usr/bin/passwd has setuid so normal users can change their password (which requires writing to /etc/shadow owned by root). SetGID (2xxx): On files, runs with the group's permissions. On directories, new files inherit the directory's group. Example: shared project directories where all files should belong to the team group. Sticky bit (1xxx): On directories, only the file owner can delete their files. Example: /tmp has sticky bit so users can create files but can't delete each other's files.",
        "points": 3.0,
        "order": 18,
    },
    {
        "type": "short_answer",
        "text": "What is the difference between a hard link and a symbolic (soft) link? What happens when the original file is deleted in each case?",
        "correct_answer": "Hard link: Another name for the same inode/data on disk. Both names point to the same data blocks. If the original is deleted, the hard link still works because the data remains until all links are removed. Cannot cross filesystems, cannot link to directories. Soft link (symbolic): A pointer/shortcut to the original file path. If the original is deleted, the soft link becomes broken (dangling link). Can cross filesystems and link to directories. Has its own inode.",
        "points": 2.0,
        "order": 19,
    },
    {
        "type": "short_answer",
        "text": "What is umask? If the umask is set to 0027, what permissions will new files and directories get? Show the calculation.",
        "correct_answer": "umask is a mask that removes permissions from the default. Default for files is 666, for directories is 777. With umask 0027: Files: 666 - 027 = 640 (rw-r-----). Directories: 777 - 027 = 750 (rwxr-x---). The umask subtracts from the default permissions. 0=no mask, 2=remove write, 7=remove all. So owner gets full access, group gets read (files)/read+execute (dirs), others get nothing.",
        "points": 2.0,
        "order": 20,
    },

    # ── MCQ ─────────────────────────────────────────────────────────────

    {
        "type": "mcq",
        "text": "What does the command 'chmod 4755 script.sh' do?",
        "options": [
            "Sets sticky bit with rwxr-xr-x",
            "Sets setuid with rwxr-xr-x - the script runs as the file owner",
            "Sets setgid with rwxr-xr-x",
            "Makes the file immutable"
        ],
        "correct_answer": "1",
        "points": 1.0,
        "order": 21,
    },
    {
        "type": "mcq",
        "text": "Which command is used to change the ownership of a file to user 'john' and group 'developers'?",
        "options": [
            "chmod john:developers file.txt",
            "chown john:developers file.txt",
            "chgrp john:developers file.txt",
            "usermod john:developers file.txt"
        ],
        "correct_answer": "1",
        "points": 1.0,
        "order": 22,
    },
    {
        "type": "mcq",
        "text": "What does the 'passwd -l username' command do?",
        "options": [
            "Lists the user's password policy",
            "Locks the user account (prevents login)",
            "Changes the user's login shell",
            "Deletes the user's password"
        ],
        "correct_answer": "1",
        "points": 1.0,
        "order": 23,
    },
    {
        "type": "mcq",
        "text": "Which file is used as a template for new user home directories?",
        "options": [
            "/etc/default/useradd",
            "/etc/login.defs",
            "/etc/skel/",
            "/etc/profile"
        ],
        "correct_answer": "2",
        "points": 1.0,
        "order": 24,
    },
    {
        "type": "mcq",
        "text": "What does the command 'chattr +i file.txt' do?",
        "options": [
            "Makes the file invisible",
            "Makes the file immutable (cannot be modified or deleted even by root)",
            "Adds an index to the file for faster search",
            "Changes the inode number of the file"
        ],
        "correct_answer": "1",
        "points": 1.0,
        "order": 25,
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print(f"  - 15 Practical tasks")
print(f"  - 5 Theory questions")
print(f"  - 5 MCQ questions")
print(f"Module is DRAFT - publish from admin panel when ready")
db.close()
